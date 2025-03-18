# memory_module.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import enum

from .database import get_db
from . import models
from pydantic import BaseModel

# Define router
router = APIRouter(
    prefix="/memory",
    tags=["memory"],
    responses={404: {"description": "Not found"}},
)

# Pydantic enum models
class ReminderPriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ReminderTypeEnum(str, enum.Enum):
    TASK = "task"
    EVENT = "event"
    BIRTHDAY = "birthday"
    HOLIDAY = "holiday"
    ROUTINE = "routine"
    CUSTOM = "custom"

class RelationshipTypeEnum(str, enum.Enum):
    FAMILY = "family"
    FRIEND = "friend"
    COLLEAGUE = "colleague"
    ACQUAINTANCE = "acquaintance"
    CLIENT = "client"
    OTHER = "other"

# Pydantic models for request/response
class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    priority: ReminderPriorityEnum = ReminderPriorityEnum.MEDIUM
    type: ReminderTypeEnum
    recurrence: Optional[str] = None
    recurrence_pattern: Optional[str] = None
    related_contact_id: Optional[int] = None

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class ContactBase(BaseModel):
    name: str
    relationship: RelationshipTypeEnum
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[datetime] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    gift_preferences: Optional[List[str]] = None
    important_dates: Optional[Dict[str, datetime]] = None

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    participants: Optional[List[str]] = None
    is_all_day: bool = False
    recurrence: Optional[str] = None
    external_id: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class GiftIdeaBase(BaseModel):
    contact_id: int
    idea: str
    estimated_price: Optional[float] = None
    occasion: Optional[str] = None
    notes: Optional[str] = None
    url: Optional[str] = None

class GiftIdeaCreate(GiftIdeaBase):
    pass

class GiftIdea(GiftIdeaBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

# Endpoints for Reminders
@router.post("/reminders/", response_model=Reminder)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Convert enum values to strings for database
    db_reminder = models.Reminder(
        user_id=user_id,
        title=reminder.title,
        description=reminder.description,
        due_date=reminder.due_date,
        priority=reminder.priority,
        type=reminder.type,
        recurrence=reminder.recurrence,
        recurrence_pattern=reminder.recurrence_pattern,
        related_contact_id=reminder.related_contact_id
    )
    
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.get("/reminders/", response_model=List[Reminder])
def read_reminders(
    skip: int = 0, 
    limit: int = 100, 
    priority: Optional[ReminderPriorityEnum] = None,
    reminder_type: Optional[ReminderTypeEnum] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.Reminder).filter(models.Reminder.user_id == user_id)
    
    if priority:
        query = query.filter(models.Reminder.priority == priority)
    if reminder_type:
        query = query.filter(models.Reminder.type == reminder_type)
    if due_before:
        query = query.filter(models.Reminder.due_date <= due_before)
    if due_after:
        query = query.filter(models.Reminder.due_date >= due_after)
    
    return query.order_by(models.Reminder.due_date).offset(skip).limit(limit).all()

@router.get("/reminders/upcoming", response_model=List[Reminder])
def get_upcoming_reminders(days: int = 7, db: Session = Depends(get_db)):
    """Get reminders due in the next X days"""
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    now = datetime.now()
    end_date = now + timedelta(days=days)
    
    return db.query(models.Reminder).filter(
        models.Reminder.user_id == user_id,
        models.Reminder.due_date >= now,
        models.Reminder.due_date <= end_date
    ).order_by(models.Reminder.due_date).all()

@router.get("/reminders/{reminder_id}", response_model=Reminder)
def read_reminder(reminder_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id,
        models.Reminder.user_id == user_id
    ).first()
    
    if reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    return reminder

# Endpoints for Contacts
@router.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_contact = models.Contact(
        user_id=user_id,
        name=contact.name,
        relationship=contact.relationship,
        email=contact.email,
        phone=contact.phone,
        birthday=contact.birthday,
        address=contact.address,
        notes=contact.notes,
        gift_preferences=contact.gift_preferences,
        important_dates=contact.important_dates
    )
    
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/contacts/", response_model=List[Contact])
def read_contacts(
    skip: int = 0, 
    limit: int = 100, 
    relationship: Optional[RelationshipTypeEnum] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.Contact).filter(models.Contact.user_id == user_id)
    
    if relationship:
        query = query.filter(models.Contact.relationship == relationship)
    if search:
        query = query.filter(models.Contact.name.ilike(f"%{search}%"))
    
    return query.order_by(models.Contact.name).offset(skip).limit(limit).all()

@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    contact = db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.user_id == user_id
    ).first()
    
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return contact

@router.get("/contacts/birthdays/upcoming", response_model=List[Contact])
def get_upcoming_birthdays(days: int = 30, db: Session = Depends(get_db)):
    """Get contacts with birthdays in the next X days"""
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # This is a simplified implementation that doesn't account for year
    today = datetime.now().date()
    
    # Get all contacts with birthdays
    contacts = db.query(models.Contact).filter(
        models.Contact.user_id == user_id,
        models.Contact.birthday.isnot(None)
    ).all()
    
    # Filter contacts with upcoming birthdays
    upcoming = []
    for contact in contacts:
        # Set birth date to current year for comparison
        birth_date = contact.birthday.date()
        birthday_this_year = datetime(today.year, birth_date.month, birth_date.day).date()
        
        # If birthday already passed this year, look at next year
        if birthday_this_year < today:
            birthday_this_year = datetime(today.year + 1, birth_date.month, birth_date.day).date()
        
        # Check if birthday is within the specified range
        days_until = (birthday_this_year - today).days
        if 0 <= days_until <= days:
            upcoming.append(contact)
    
    # Sort by days until birthday
    upcoming.sort(key=lambda c: (
        datetime(today.year, c.birthday.month, c.birthday.day) 
        if datetime(today.year, c.birthday.month, c.birthday.day).date() >= today 
        else datetime(today.year + 1, c.birthday.month, c.birthday.day)
    ))
    
    return upcoming

# Endpoints for Gift Ideas
@router.post("/gift-ideas/", response_model=GiftIdea)
def create_gift_idea(gift_idea: GiftIdeaCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Verify contact exists and belongs to user
    contact = db.query(models.Contact).filter(
        models.Contact.id == gift_idea.contact_id,
        models.Contact.user_id == user_id
    ).first()
    
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db_gift_idea = models.GiftIdea(
        user_id=user_id,
        contact_id=gift_idea.contact_id,
        idea=gift_idea.idea,
        estimated_price=gift_idea.estimated_price,
        occasion=gift_idea.occasion,
        notes=gift_idea.notes,
        url=gift_idea.url
    )
    
    db.add(db_gift_idea)
    db.commit()
    db.refresh(db_gift_idea)
    return db_gift_idea

@router.get("/gift-ideas/", response_model=List[GiftIdea])
def read_gift_ideas(
    skip: int = 0, 
    limit: int = 100, 
    contact_id: Optional[int] = None,
    occasion: Optional[str] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.GiftIdea).filter(models.GiftIdea.user_id == user_id)
    
    if contact_id:
        query = query.filter(models.GiftIdea.contact_id == contact_id)
    if occasion:
        query = query.filter(models.GiftIdea.occasion == occasion)
    if max_price:
        query = query.filter(models.GiftIdea.estimated_price <= max_price)
    
    return query.offset(skip).limit(limit).all()

# Add more endpoints as needed for Events and other memory-related features
