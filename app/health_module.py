# health_module.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from .database import get_db
from . import models
from pydantic import BaseModel

# Define router
router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response
class SleepRecordBase(BaseModel):
    date: Optional[datetime] = None
    duration_hours: float
    quality: int  # 1-10 scale
    notes: Optional[str] = None

class SleepRecordCreate(SleepRecordBase):
    pass

class SleepRecord(SleepRecordBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class ExerciseRecordBase(BaseModel):
    date: Optional[datetime] = None
    activity_type: str
    duration_minutes: int
    intensity: int  # 1-10 scale
    calories_burned: Optional[int] = None
    notes: Optional[str] = None

class ExerciseRecordCreate(ExerciseRecordBase):
    pass

class ExerciseRecord(ExerciseRecordBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class HealthPreferenceUpdate(BaseModel):
    sleep_goal_hours: Optional[float] = None
    exercise_goal_minutes: Optional[int] = None
    daily_calorie_goal: Optional[int] = None
    daily_water_goal: Optional[float] = None
    favorite_activities: Optional[List[str]] = None

# Endpoints
@router.post("/sleep/", response_model=SleepRecord)
def record_sleep(sleep: SleepRecordCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_sleep = models.SleepRecord(
        user_id=user_id,
        date=sleep.date or datetime.now(),
        duration_hours=sleep.duration_hours,
        quality=sleep.quality,
        notes=sleep.notes
    )
    db.add(db_sleep)
    db.commit()
    db.refresh(db_sleep)
    return db_sleep

@router.get("/sleep/", response_model=List[SleepRecord])
def get_sleep_records(
    skip: int = 0, 
    limit: int = 100, 
    start_date: Optional[datetime] = None, 
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.SleepRecord).filter(models.SleepRecord.user_id == user_id)
    
    if start_date:
        query = query.filter(models.SleepRecord.date >= start_date)
    if end_date:
        query = query.filter(models.SleepRecord.date <= end_date)
    
    return query.order_by(models.SleepRecord.date.desc()).offset(skip).limit(limit).all()

@router.post("/exercise/", response_model=ExerciseRecord)
def record_exercise(exercise: ExerciseRecordCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_exercise = models.ExerciseRecord(
        user_id=user_id,
        date=exercise.date or datetime.now(),
        activity_type=exercise.activity_type,
        duration_minutes=exercise.duration_minutes,
        intensity=exercise.intensity,
        calories_burned=exercise.calories_burned,
        notes=exercise.notes
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.get("/exercise/", response_model=List[ExerciseRecord])
def get_exercise_records(
    skip: int = 0, 
    limit: int = 100, 
    start_date: Optional[datetime] = None, 
    end_date: Optional[datetime] = None,
    activity_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.ExerciseRecord).filter(models.ExerciseRecord.user_id == user_id)
    
    if start_date:
        query = query.filter(models.ExerciseRecord.date >= start_date)
    if end_date:
        query = query.filter(models.ExerciseRecord.date <= end_date)
    if activity_type:
        query = query.filter(models.ExerciseRecord.activity_type == activity_type)
    
    return query.order_by(models.ExerciseRecord.date.desc()).offset(skip).limit(limit).all()

@router.get("/preferences/")
def get_health_preferences(db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    prefs = db.query(models.HealthPreference).filter(models.HealthPreference.user_id == user_id).first()
    
    if not prefs:
        # Create default preferences if none exist
        prefs = models.HealthPreference(
            user_id=user_id,
            sleep_goal_hours=8.0,
            exercise_goal_minutes=150,
            daily_calorie_goal=2000,
            daily_water_goal=2.5,
            favorite_activities=["Walking", "Running", "Yoga"]
        )
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
    
    return prefs

@router.put("/preferences/")
def update_health_preferences(preferences: HealthPreferenceUpdate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    prefs = db.query(models.HealthPreference).filter(models.HealthPreference.user_id == user_id).first()
    
    if not prefs:
        # Create new preferences
        prefs = models.HealthPreference(user_id=user_id)
        db.add(prefs)
    
    # Update provided fields
    if preferences.sleep_goal_hours is not None:
        prefs.sleep_goal_hours = preferences.sleep_goal_hours
    if preferences.exercise_goal_minutes is not None:
        prefs.exercise_goal_minutes = preferences.exercise_goal_minutes
    if preferences.daily_calorie_goal is not None:
        prefs.daily_calorie_goal = preferences.daily_calorie_goal
    if preferences.daily_water_goal is not None:
        prefs.daily_water_goal = preferences.daily_water_goal
    if preferences.favorite_activities is not None:
        prefs.favorite_activities = preferences.favorite_activities
    
    db.commit()
    db.refresh(prefs)
    return prefs

@router.get("/analysis/sleep")
def analyze_sleep(
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
    
    # Get sleep records for the period
    sleep_records = db.query(models.SleepRecord).filter(
        models.SleepRecord.user_id == user_id,
        models.SleepRecord.date >= start_date,
        models.SleepRecord.date <= end_date
    ).all()
    
    # Get user's sleep goal
    prefs = db.query(models.HealthPreference).filter(models.HealthPreference.user_id == user_id).first()
    sleep_goal = prefs.sleep_goal_hours if prefs else 8.0
    
    # Calculate statistics
    total_records = len(sleep_records)
    
    if total_records == 0:
        return {
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "records_count": 0,
            "message": "No sleep data available for the selected period."
        }
    
    total_sleep = sum(record.duration_hours for record in sleep_records)
    avg_sleep = total_sleep / total_records
    avg_quality = sum(record.quality for record in sleep_records) / total_records
    
    # Calculate goal achievement
    goal_achievement = (avg_sleep / sleep_goal) * 100 if sleep_goal > 0 else 0
    
    # Find best and worst days
    best_sleep = max(sleep_records, key=lambda x: x.quality)
    worst_sleep = min(sleep_records, key=lambda x: x.quality)
    
    return {
        "period": period,
        "start_date": start_date,
        "end_date": end_date,
        "records_count": total_records,
        "average_sleep_hours": round(avg_sleep, 1),
        "average_quality": round(avg_quality, 1),
        "goal_hours": sleep_goal,
        "goal_achievement_percentage": round(goal_achievement, 1),
        "best_sleep": {
            "date": best_sleep.date,
            "duration_hours": best_sleep.duration_hours,
            "quality": best_sleep.quality,
            "notes": best_sleep.notes
        },
        "worst_sleep": {
            "date": worst_sleep.date,
            "duration_hours": worst_sleep.duration_hours,
            "quality": worst_sleep.quality,
            "notes": worst_sleep.notes
        }
    }
