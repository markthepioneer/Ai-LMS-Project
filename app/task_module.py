# task_module.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import enum

from .database import get_db
from . import models
from pydantic import BaseModel

# Define router
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

# Pydantic enum models
class TaskPriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatusEnum(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DELEGATED = "delegated"
    COMPLETED = "completed"
    CANCELED = "canceled"

# Pydantic models for request/response
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_duration_minutes: Optional[int] = None
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    category: Optional[str] = None
    delegatable: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    status: TaskStatusEnum = TaskStatusEnum.NOT_STARTED
    completion_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_duration_minutes: Optional[int] = None
    priority: Optional[TaskPriorityEnum] = None
    category: Optional[str] = None
    delegatable: Optional[bool] = None
    status: Optional[TaskStatusEnum] = None

# Endpoints
@router.post("/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_task = models.Task(
        user_id=user_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        estimated_duration_minutes=task.estimated_duration_minutes,
        priority=task.priority.value,  # Use the enum value
        category=task.category,
        delegatable=task.delegatable
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[Task])
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[TaskStatusEnum] = None,
    priority: Optional[TaskPriorityEnum] = None,
    category: Optional[str] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.Task).filter(models.Task.user_id == user_id)
    
    if status:
        query = query.filter(models.Task.status == status.value)
    if priority:
        query = query.filter(models.Task.priority == priority.value)
    if category:
        query = query.filter(models.Task.category == category)
    if due_before:
        query = query.filter(models.Task.due_date <= due_before)
    if due_after:
        query = query.filter(models.Task.due_date >= due_after)
    
    return query.order_by(models.Task.due_date.asc(), models.Task.priority.desc()).offset(skip).limit(limit).all()

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.user_id == user_id
    ).first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.user_id == user_id
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update provided fields
    update_data = task_update.dict(exclude_unset=True)
    
    # Convert enum values to their string representations
    if "priority" in update_data and update_data["priority"] is not None:
        update_data["priority"] = update_data["priority"].value
    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = update_data["status"].value
        
        # If task is being marked as completed, set completion date
        if update_data["status"] == "completed" and db_task.status != "completed":
            update_data["completion_date"] = datetime.now()
        # If task is being unmarked as completed, remove completion date
        elif update_data["status"] != "completed" and db_task.status == "completed":
            update_data["completion_date"] = None
    
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.user_id == user_id
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"status": "success"}

@router.post("/{task_id}/complete", response_model=Task)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.user_id == user_id
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task status and completion date
    db_task.status = "completed"
    db_task.completion_date = datetime.now()
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/today", response_model=List[Task])
def get_today_tasks(db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Get today's date
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Get tasks due today or overdue that aren't completed
    tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.status.not_in_(["completed", "canceled"]),
        (models.Task.due_date < tomorrow) | (models.Task.due_date == None)
    ).order_by(models.Task.priority.desc()).all()
    
    return tasks

@router.get("/analysis/completion")
def analyze_task_completion(
    period: str = "month",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now()
    if not start_date:
        if period == "month":
            start_date = end_date - timedelta(days=30)
        elif period == "year":
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=7)  # Default to week
    
    # Get all tasks created in the period
    all_tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.created_at >= start_date,
        models.Task.created_at <= end_date
    ).all()
    
    # Get completed tasks in the period
    completed_tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.status == "completed",
        models.Task.completion_date >= start_date,
        models.Task.completion_date <= end_date
    ).all()
    
    # Calculate statistics
    total_created = len(all_tasks)
    total_completed = len(completed_tasks)
    
    if total_created == 0:
        completion_rate = 0
    else:
        completion_rate = (total_completed / total_created) * 100
    
    # Analyze by category
    categories = {}
    for task in completed_tasks:
        category = task.category or "uncategorized"
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
    
    # Calculate average completion time
    completion_times = []
    for task in completed_tasks:
        if task.created_at and task.completion_date:
            delta = task.completion_date - task.created_at
            completion_times.append(delta.total_seconds() / 3600)  # Hours
    
    avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
    
    return {
        "period": period,
        "start_date": start_date,
        "end_date": end_date,
        "total_tasks_created": total_created,
        "total_tasks_completed": total_completed,
        "completion_rate_percentage": round(completion_rate, 1),
        "average_completion_time_hours": round(avg_completion_time, 1),
        "completed_by_category": categories
    }
