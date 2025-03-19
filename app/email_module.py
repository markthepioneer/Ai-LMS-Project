# email_module.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import enum

from .database import get_db
from . import models
from pydantic import BaseModel, EmailStr
from .ai_engine.common import analyze_text, generate_response

# Define router
router = APIRouter(
    prefix="/email",
    tags=["email"],
    responses={404: {"description": "Not found"}},
)

# Pydantic enum models
class EmailPriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class EmailCategoryEnum(str, enum.Enum):
    PERSONAL = "personal"
    WORK = "work"
    FINANCE = "finance"
    SHOPPING = "shopping"
    TRAVEL = "travel"
    SOCIAL = "social"
    PROMOTIONS = "promotions"
    UPDATES = "updates"
    FORUMS = "forums"
    OTHER = "other"

class CallTypeEnum(str, enum.Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"
    MISSED = "missed"
    VOICEMAIL = "voicemail"

# Pydantic models for request/response
class EmailBase(BaseModel):
    subject: str
    body: str
    sender: Optional[EmailStr] = None
    recipients: List[EmailStr]
    cc: Optional[List[EmailStr]] = []
    bcc: Optional[List[EmailStr]] = []
    has_attachments: Optional[bool] = False
    is_read: Optional[bool] = False
    starred: Optional[bool] = False
    priority: Optional[EmailPriorityEnum] = EmailPriorityEnum.MEDIUM
    category: Optional[EmailCategoryEnum] = EmailCategoryEnum.OTHER
    labels: Optional[List[str]] = []
    external_id: Optional[str] = None

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    user_id: int
    date: datetime
    
    class Config:
        orm_mode = True

class EmailDraftBase(BaseModel):
    subject: str
    body: str
    recipients: List[EmailStr]
    cc: Optional[List[EmailStr]] = []
    bcc: Optional[List[EmailStr]] = []
    in_reply_to: Optional[int] = None

class EmailDraftCreate(EmailDraftBase):
    pass

class EmailDraft(EmailDraftBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    sent: bool = False
    sent_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    body: str
    category: Optional[str] = None
    variables: Optional[List[str]] = []

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplate(EmailTemplateBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class PhoneCallBase(BaseModel):
    contact_name: Optional[str] = None
    phone_number: str
    call_type: CallTypeEnum
    duration_seconds: Optional[int] = 0
    date: Optional[datetime] = None
    notes: Optional[str] = None
    recording_url: Optional[str] = None
    transcription: Optional[str] = None

class PhoneCallCreate(PhoneCallBase):
    pass

class PhoneCall(PhoneCallBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class EmailAnalysisRequest(BaseModel):
    email_id: int

class EmailDraftGenerationRequest(BaseModel):
    email_id: Optional[int] = None  # For reply generation
    template_id: Optional[int] = None
    template_variables: Optional[Dict[str, Any]] = None
    subject: Optional[str] = None  # For new email generation
    recipients: Optional[List[EmailStr]] = None
    context: Optional[str] = None  # Additional context for generation

# Endpoints for Emails
@router.post("/", response_model=Email)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_email = models.Email(
        user_id=user_id,
        subject=email.subject,
        body=email.body,
        sender=email.sender,
        recipients=email.recipients,
        cc=email.cc,
        bcc=email.bcc,
        date=datetime.now(),
        has_attachments=email.has_attachments,
        is_read=email.is_read,
        starred=email.starred,
        priority=email.priority,
        category=email.category,
        labels=email.labels,
        external_id=email.external_id
    )
    
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

@router.get("/", response_model=List[Email])
def read_emails(
    skip: int = 0, 
    limit: int = 100, 
    is_read: Optional[bool] = None,
    starred: Optional[bool] = None,
    category: Optional[EmailCategoryEnum] = None,
    label: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.Email).filter(models.Email.user_id == user_id)
    
    if is_read is not None:
        query = query.filter(models.Email.is_read == is_read)
    if starred is not None:
        query = query.filter(models.Email.starred == starred)
    if category:
        query = query.filter(models.Email.category == category)
    if label:
        query = query.filter(models.Email.labels.contains([label]))
    
    return query.order_by(models.Email.date.desc()).offset(skip).limit(limit).all()

@router.get("/{email_id}", response_model=Email)
def read_email(email_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    email = db.query(models.Email).filter(
        models.Email.id == email_id,
        models.Email.user_id == user_id
    ).first()
    
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    return email

@router.post("/{email_id}/mark-read", response_model=Email)
def mark_email_as_read(email_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    email = db.query(models.Email).filter(
        models.Email.id == email_id,
        models.Email.user_id == user_id
    ).first()
    
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    email.is_read = True
    db.commit()
    db.refresh(email)
    return email

@router.post("/{email_id}/toggle-star", response_model=Email)
def toggle_email_star(email_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    email = db.query(models.Email).filter(
        models.Email.id == email_id,
        models.Email.user_id == user_id
    ).first()
    
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    email.starred = not email.starred
    db.commit()
    db.refresh(email)
    return email

# Endpoints for Email Drafts
@router.post("/drafts/", response_model=EmailDraft)
def create_draft(draft: EmailDraftCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_draft = models.EmailDraft(
        user_id=user_id,
        subject=draft.subject,
        body=draft.body,
        recipients=draft.recipients,
        cc=draft.cc,
        bcc=draft.bcc,
        in_reply_to=draft.in_reply_to,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(db_draft)
    db.commit()
    db.refresh(db_draft)
    return db_draft

@router.get("/drafts/", response_model=List[EmailDraft])
def read_drafts(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    return db.query(models.EmailDraft).filter(
        models.EmailDraft.user_id == user_id,
        models.EmailDraft.sent == False
    ).order_by(models.EmailDraft.updated_at.desc()).offset(skip).limit(limit).all()

@router.put("/drafts/{draft_id}", response_model=EmailDraft)
def update_draft(
    draft_id: int, 
    draft_update: EmailDraftCreate, 
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_draft = db.query(models.EmailDraft).filter(
        models.EmailDraft.id == draft_id,
        models.EmailDraft.user_id == user_id,
        models.EmailDraft.sent == False
    ).first()
    
    if db_draft is None:
        raise HTTPException(status_code=404, detail="Draft not found or already sent")
    
    for key, value in draft_update.dict().items():
        setattr(db_draft, key, value)
    
    db_draft.updated_at = datetime.now()
    db.commit()
    db.refresh(db_draft)
    return db_draft

@router.post("/drafts/{draft_id}/send", response_model=EmailDraft)
def send_draft(draft_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_draft = db.query(models.EmailDraft).filter(
        models.EmailDraft.id == draft_id,
        models.EmailDraft.user_id == user_id,
        models.EmailDraft.sent == False
    ).first()
    
    if db_draft is None:
        raise HTTPException(status_code=404, detail="Draft not found or already sent")
    
    # Mark as sent
    db_draft.sent = True
    db_draft.sent_at = datetime.now()
    
    # In a real implementation, this would actually send the email
    # Create sent email record
    sent_email = models.Email(
        user_id=user_id,
        subject=db_draft.subject,
        body=db_draft.body,
        sender="user@example.com",  # In real implementation, get from user profile
        recipients=db_draft.recipients,
        cc=db_draft.cc,
        bcc=db_draft.bcc,
        date=datetime.now(),
        is_read=True,
        category=EmailCategoryEnum.PERSONAL.value  # Default category
    )
    
    db.add(sent_email)
    db.commit()
    db.refresh(db_draft)
    return db_draft

# Endpoints for Email Templates
@router.post("/templates/", response_model=EmailTemplate)
def create_template(template: EmailTemplateCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_template = models.EmailTemplate(
        user_id=user_id,
        name=template.name,
        subject=template.subject,
        body=template.body,
        category=template.category,
        variables=template.variables,
        created_at=datetime.now()
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.get("/templates/", response_model=List[EmailTemplate])
def read_templates(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.EmailTemplate).filter(models.EmailTemplate.user_id == user_id)
    
    if category:
        query = query.filter(models.EmailTemplate.category == category)
    
    return query.order_by(models.EmailTemplate.name).offset(skip).limit(limit).all()

# AI-Enhanced Email Features
@router.post("/analyze", response_model=Dict[str, Any])
def analyze_email_content(analysis_req: EmailAnalysisRequest, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    email = db.query(models.Email).filter(
        models.Email.id == analysis_req.email_id,
        models.Email.user_id == user_id
    ).first()
    
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Use AI to analyze email content
    analysis = {}
    
    # Sentiment analysis
    sentiment = analyze_text(email.body, "sentiment")
    analysis["sentiment"] = sentiment
    
    # Keywords extraction
    keywords = analyze_text(email.body, "keywords")
    analysis["keywords"] = keywords
    
    # Auto-categorization
    # In a real implementation, this would use ML to categorize
    if "invoice" in email.body.lower() or "payment" in email.body.lower():
        suggested_category = EmailCategoryEnum.FINANCE
    elif "meeting" in email.body.lower() or "project" in email.body.lower():
        suggested_category = EmailCategoryEnum.WORK
    elif "sale" in email.body.lower() or "discount" in email.body.lower():
        suggested_category = EmailCategoryEnum.PROMOTIONS
    else:
        suggested_category = email.category or EmailCategoryEnum.OTHER
    
    analysis["suggested_category"] = suggested_category
    
    # Check for action items or urgent content
    if "urgent" in email.body.lower() or "asap" in email.body.lower():
        analysis["urgency"] = "high"
        analysis["suggested_priority"] = EmailPriorityEnum.URGENT
    elif "please" in email.body.lower() and ("review" in email.body.lower() or "respond" in email.body.lower()):
        analysis["urgency"] = "medium"
        analysis["suggested_priority"] = EmailPriorityEnum.HIGH
    else:
        analysis["urgency"] = "normal"
        analysis["suggested_priority"] = email.priority or EmailPriorityEnum.MEDIUM
    
    return {
        "email_id": email.id,
        "subject": email.subject,
        "analysis": analysis
    }

@router.post("/generate-draft", response_model=EmailDraft)
def generate_email_draft(draft_req: EmailDraftGenerationRequest, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    subject = ""
    body = ""
    recipients = []
    
    # Generate a reply
    if draft_req.email_id:
        email = db.query(models.Email).filter(
            models.Email.id == draft_req.email_id,
            models.Email.user_id == user_id
        ).first()
        
        if email is None:
            raise HTTPException(status_code=404, detail="Email not found")
        
        # Create a reply
        subject = f"Re: {email.subject}" if not email.subject.startswith("Re: ") else email.subject
        recipients = [email.sender] if email.sender else []
        
        # Generate content using AI
        context = {
            "original_email": email.body,
            "original_subject": email.subject,
            "sender": email.sender,
            "additional_context": draft_req.context or ""
        }
        
        body = generate_response(context, "email_reply")
    
    # Use a template
    elif draft_req.template_id:
        template = db.query(models.EmailTemplate).filter(
            models.EmailTemplate.id == draft_req.template_id,
            models.EmailTemplate.user_id == user_id
        ).first()
        
        if template is None:
            raise HTTPException(status_code=404, detail="Template not found")
        
        subject = template.subject
        body = template.body
        
        # Replace variables if provided
        if draft_req.template_variables:
            for var, value in draft_req.template_variables.items():
                placeholder = f"{{{var}}}"
                subject = subject.replace(placeholder, str(value))
                body = body.replace(placeholder, str(value))
        
        recipients = draft_req.recipients or []
    
    # Generate from scratch
    elif draft_req.subject and draft_req.context:
        subject = draft_req.subject
        
        # Generate content using AI
        context = {
            "subject": subject,
            "topic": draft_req.context
        }
        
        body = generate_response(context, "email_generation")
        recipients = draft_req.recipients or []
    
    else:
        raise HTTPException(
            status_code=400, 
            detail="Must provide either email_id, template_id, or subject and context"
        )
    
    # Create the draft
    draft = models.EmailDraft(
        user_id=user_id,
        subject=subject,
        body=body,
        recipients=recipients,
        cc=[],
        bcc=[],
        in_reply_to=draft_req.email_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft

# Phone Call Endpoints
@router.post("/calls/", response_model=PhoneCall)
def record_phone_call(call: PhoneCallCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_call = models.PhoneCall(
        user_id=user_id,
        contact_name=call.contact_name,
        phone_number=call.phone_number,
        call_type=call.call_type,
        duration_seconds=call.duration_seconds,
        date=call.date or datetime.now(),
        notes=call.notes,
        recording_url=call.recording_url,
        transcription=call.transcription
    )
    
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

@router.get("/calls/", response_model=List[PhoneCall])
def read_phone_calls(
    skip: int = 0, 
    limit: int = 100, 
    call_type: Optional[CallTypeEnum] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.PhoneCall).filter(models.PhoneCall.user_id == user_id)
    
    if call_type:
        query = query.filter(models.PhoneCall.call_type == call_type)
    
    return query.order_by(models.PhoneCall.date.desc()).offset(skip).limit(limit).all()

@router.post("/calls/{call_id}/transcribe", response_model=PhoneCall)
def transcribe_call(
    call_id: int,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    call = db.query(models.PhoneCall).filter(
        models.PhoneCall.id == call_id,
        models.PhoneCall.user_id == user_id
    ).first()
    
    if call is None:
        raise HTTPException(status_code=404, detail="Call not found")
    
    # In a real implementation, this would process the recording and generate a transcription
    # For demo purposes, generate a dummy transcription
    call.transcription = "This is an automatically generated transcription of the call."
    
    db.commit()
    db.refresh(call)
    return call

# Email Statistics and Analytics
@router.get("/statistics", response_model=Dict[str, Any])
def get_email_statistics(
    period: str = "month", 
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Calculate date range based on period
    now = datetime.now()
    if period == "week":
        start_date = now - timedelta(days=7)
    elif period == "month":
        start_date = now - timedelta(days=30)
    elif period == "year":
        start_date = now - timedelta(days=365)
    else:
        start_date = now - timedelta(days=30)  # Default to month
    
    # Get emails in the period
    emails = db.query(models.Email).filter(
        models.Email.user_id == user_id,
        models.Email.date >= start_date
    ).all()
    
    # Calculate statistics
    total_count = len(emails)
    unread_count = sum(1 for e in emails if not e.is_read)
    starred_count = sum(1 for e in emails if e.starred)
    
    # Count by category
    categories = {}
    for email in emails:
        category = email.category or "uncategorized"
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
    
    # Calculate response times for received emails
    # In a real implementation, this would track when emails were responded to
    avg_response_time = 8.7  # Dummy value in hours
    
    return {
        "period": period,
        "start_date": start_date,
        "end_date": now,
        "total_emails": total_count,
        "unread_emails": unread_count,
        "starred_emails": starred_count,
        "categories": categories,
        "avg_response_time_hours": avg_response_time
    }
