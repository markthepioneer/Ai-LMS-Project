# life_balancer_module.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import enum

from .database import get_db
from . import models
from pydantic import BaseModel
from .ai_engine.common import analyze_text, generate_response

# Define router
router = APIRouter(
    prefix="/life-balance",
    tags=["life-balance"],
    responses={404: {"description": "Not found"}},
)

# Pydantic enum models
class LifeAreaTypeEnum(str, enum.Enum):
    WORK = "work"
    HEALTH = "health"
    RELATIONSHIPS = "relationships"
    PERSONAL_GROWTH = "personal_growth"
    RECREATION = "recreation"
    SPIRITUALITY = "spirituality"
    COMMUNITY = "community"
    FINANCE = "finance"

class GoalStatusEnum(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    ABANDONED = "abandoned"

class GoalPriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RewardTypeEnum(str, enum.Enum):
    ACTIVITY = "activity"
    PURCHASE = "purchase"
    EXPERIENCE = "experience"
    ACHIEVEMENT = "achievement"
    CUSTOM = "custom"

# Pydantic models for request/response
class LifeAreaBase(BaseModel):
    type: LifeAreaTypeEnum
    importance: int  # 1-10 scale
    satisfaction: int  # 1-10 scale
    target_hours_per_week: Optional[float] = None
    notes: Optional[str] = None

class LifeAreaCreate(LifeAreaBase):
    pass

class LifeArea(LifeAreaBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    life_area: LifeAreaTypeEnum
    due_date: Optional[datetime] = None
    priority: GoalPriorityEnum = GoalPriorityEnum.MEDIUM
    expected_time_investment: Optional[float] = None  # In hours
    milestones: Optional[List[Dict[str, Any]]] = None
    reward_id: Optional[int] = None

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    user_id: int
    created_at: datetime
    status: GoalStatusEnum = GoalStatusEnum.NOT_STARTED
    progress_percent: int = 0
    
    class Config:
        orm_mode = True

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    life_area: Optional[LifeAreaTypeEnum] = None
    due_date: Optional[datetime] = None
    priority: Optional[GoalPriorityEnum] = None
    status: Optional[GoalStatusEnum] = None
    progress_percent: Optional[int] = None
    milestones: Optional[List[Dict[str, Any]]] = None
    reward_id: Optional[int] = None
    expected_time_investment: Optional[float] = None

class RewardBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: RewardTypeEnum
    cost: Optional[float] = None
    location: Optional[str] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None

class RewardCreate(RewardBase):
    pass

class Reward(RewardBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class MeTimeBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    preferred_days: Optional[List[int]] = None  # 0-6 (Monday-Sunday)
    preferred_time_ranges: Optional[List[Dict[str, str]]] = None  # [{"start": "09:00", "end": "12:00"}]
    activity_type: Optional[str] = None
    location: Optional[str] = None
    required_items: Optional[List[str]] = None
    priority: int = 5  # 1-10 scale

class MeTimeCreate(MeTimeBase):
    pass

class MeTime(MeTimeBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class LifeMetricBase(BaseModel):
    name: str
    category: LifeAreaTypeEnum
    current_value: float
    target_value: float
    initial_value: Optional[float] = None
    units: Optional[str] = None
    measurement_frequency: Optional[str] = None  # 'daily', 'weekly', 'monthly'
    higher_is_better: bool = True
    notes: Optional[str] = None

class LifeMetricCreate(LifeMetricBase):
    pass

class LifeMetric(LifeMetricBase):
    id: int
    user_id: int
    progress_percent: Optional[int] = None
    
    class Config:
        orm_mode = True

# Endpoints for Life Areas
@router.post("/areas/", response_model=LifeArea)
def create_life_area(life_area: LifeAreaCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Validate rating scales
    if not (1 <= life_area.importance <= 10):
        raise HTTPException(status_code=400, detail="Importance must be between 1 and 10")
    
    if not (1 <= life_area.satisfaction <= 10):
        raise HTTPException(status_code=400, detail="Satisfaction must be between 1 and 10")
    
    # Check if area already exists for user
    existing_area = db.query(models.LifeArea).filter(
        models.LifeArea.user_id == user_id,
        models.LifeArea.type == life_area.type
    ).first()
    
    if existing_area:
        raise HTTPException(
            status_code=400,
            detail=f"Life area '{life_area.type}' already exists for this user"
        )
    
    db_life_area = models.LifeArea(
        user_id=user_id,
        type=life_area.type,
        importance=life_area.importance,
        satisfaction=life_area.satisfaction,
        target_hours_per_week=life_area.target_hours_per_week,
        notes=life_area.notes
    )
    
    db.add(db_life_area)
    db.commit()
    db.refresh(db_life_area)
    return db_life_area

@router.get("/areas/", response_model=List[LifeArea])
def read_life_areas(db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    return db.query(models.LifeArea).filter(models.LifeArea.user_id == user_id).all()

@router.put("/areas/{area_id}", response_model=LifeArea)
def update_life_area(
    area_id: int, 
    life_area: LifeAreaCreate, 
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Validate rating scales
    if not (1 <= life_area.importance <= 10):
        raise HTTPException(status_code=400, detail="Importance must be between 1 and 10")
    
    if not (1 <= life_area.satisfaction <= 10):
        raise HTTPException(status_code=400, detail="Satisfaction must be between 1 and 10")
    
    db_life_area = db.query(models.LifeArea).filter(
        models.LifeArea.id == area_id,
        models.LifeArea.user_id == user_id
    ).first()
    
    if db_life_area is None:
        raise HTTPException(status_code=404, detail="Life area not found")
    
    # Update fields
    db_life_area.importance = life_area.importance
    db_life_area.satisfaction = life_area.satisfaction
    db_life_area.target_hours_per_week = life_area.target_hours_per_week
    db_life_area.notes = life_area.notes
    
    db.commit()
    db.refresh(db_life_area)
    return db_life_area

# Endpoints for Goals
@router.post("/goals/", response_model=Goal)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Verify life area exists
    life_area = db.query(models.LifeArea).filter(
        models.LifeArea.user_id == user_id,
        models.LifeArea.type == goal.life_area
    ).first()
    
    if life_area is None:
        raise HTTPException(
            status_code=400,
            detail=f"Life area '{goal.life_area}' does not exist for this user"
        )
    
    # Verify reward exists if provided
    if goal.reward_id:
        reward = db.query(models.Reward).filter(
            models.Reward.id == goal.reward_id,
            models.Reward.user_id == user_id
        ).first()
        
        if reward is None:
            raise HTTPException(status_code=404, detail="Reward not found")
    
    # Convert milestones to JSON
    milestones_json = goal.milestones if goal.milestones else []
    
    db_goal = models.Goal(
        user_id=user_id,
        title=goal.title,
        description=goal.description,
        life_area=goal.life_area,
        due_date=goal.due_date,
        created_at=datetime.now(),
        priority=goal.priority,
        status=GoalStatusEnum.NOT_STARTED,
        progress_percent=0,
        milestones_json=milestones_json,
        reward_id=goal.reward_id,
        expected_time_investment=goal.expected_time_investment
    )
    
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/goals/", response_model=List[Goal])
def read_goals(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[GoalStatusEnum] = None,
    life_area: Optional[LifeAreaTypeEnum] = None,
    priority: Optional[GoalPriorityEnum] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.Goal).filter(models.Goal.user_id == user_id)
    
    if status:
        query = query.filter(models.Goal.status == status)
    if life_area:
        query = query.filter(models.Goal.life_area == life_area)
    if priority:
        query = query.filter(models.Goal.priority == priority)
    
    return query.order_by(models.Goal.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/goals/{goal_id}", response_model=Goal)
def read_goal(goal_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == user_id
    ).first()
    
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return goal

@router.put("/goals/{goal_id}", response_model=Goal)
def update_goal(
    goal_id: int, 
    goal_update: GoalUpdate, 
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == user_id
    ).first()
    
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Update fields if provided
    update_data = goal_update.dict(exclude_unset=True)
    
    # Check if life area exists if being updated
    if "life_area" in update_data:
        life_area = db.query(models.LifeArea).filter(
            models.LifeArea.user_id == user_id,
            models.LifeArea.type == update_data["life_area"]
        ).first()
        
        if life_area is None:
            raise HTTPException(
                status_code=400,
                detail=f"Life area '{update_data['life_area']}' does not exist for this user"
            )
    
    # Check if reward exists if being updated
    if "reward_id" in update_data and update_data["reward_id"] is not None:
        reward = db.query(models.Reward).filter(
            models.Reward.id == update_data["reward_id"],
            models.Reward.user_id == user_id
        ).first()
        
        if reward is None:
            raise HTTPException(status_code=404, detail="Reward not found")
    
    # Update milestones
    if "milestones" in update_data:
        db_goal.milestones_json = update_data.pop("milestones")
    
    for key, value in update_data.items():
        setattr(db_goal, key, value)
    
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.post("/goals/{goal_id}/progress", response_model=Goal)
def update_goal_progress(
    goal_id: int, 
    progress: int,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Validate progress
    if not (0 <= progress <= 100):
        raise HTTPException(status_code=400, detail="Progress must be between 0 and 100")
    
    db_goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == user_id
    ).first()
    
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Update progress
    db_goal.progress_percent = progress
    
    # Update status based on progress
    if progress == 0:
        db_goal.status = GoalStatusEnum.NOT_STARTED
    elif progress == 100:
        db_goal.status = GoalStatusEnum.COMPLETED
    elif db_goal.status not in [GoalStatusEnum.DEFERRED, GoalStatusEnum.ABANDONED]:
        db_goal.status = GoalStatusEnum.IN_PROGRESS
    
    db.commit()
    db.refresh(db_goal)
    return db_goal

# Endpoints for Rewards
@router.post("/rewards/", response_model=Reward)
def create_reward(reward: RewardCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_reward = models.Reward(
        user_id=user_id,
        name=reward.name,
        description=reward.description,
        type=reward.type,
        cost=reward.cost,
        location=reward.location,
        duration_minutes=reward.duration_minutes,
        notes=reward.notes
    )
    
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward

@router.get("/rewards/", response_model=List[Reward])
def read_rewards(
    skip: int = 0, 
    limit: int = 100, 
    reward_type: Optional[RewardTypeEnum] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.Reward).filter(models.Reward.user_id == user_id)
    
    if reward_type:
        query = query.filter(models.Reward.type == reward_type)
    
    return query.offset(skip).limit(limit).all()

# Endpoints for Me Time
@router.post("/me-time/", response_model=MeTime)
def create_me_time(me_time: MeTimeCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Validate priority
    if not (1 <= me_time.priority <= 10):
        raise HTTPException(status_code=400, detail="Priority must be between 1 and 10")
    
    db_me_time = models.MeTime(
        user_id=user_id,
        title=me_time.title,
        description=me_time.description,
        duration_minutes=me_time.duration_minutes,
        preferred_days=me_time.preferred_days,
        preferred_time_ranges=me_time.preferred_time_ranges,
        activity_type=me_time.activity_type,
        location=me_time.location,
        required_items=me_time.required_items,
        priority=me_time.priority
    )
    
    db.add(db_me_time)
    db.commit()
    db.refresh(db_me_time)
    return db_me_time

@router.get("/me-time/", response_model=List[MeTime])
def read_me_time(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    return db.query(models.MeTime).filter(models.MeTime.user_id == user_id).offset(skip).limit(limit).all()

@router.get("/me-time/schedule/", response_model=List[Dict[str, Any]])
def generate_me_time_schedule(
    days_ahead: int = 7,
    db: Session = Depends(get_db)
):
    """Generate a schedule for Me Time activities for the next X days"""
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Get all Me Time activities
    me_time_activities = db.query(models.MeTime).filter(models.MeTime.user_id == user_id).all()
    
    if not me_time_activities:
        return []
    
    # In a real implementation, this would use scheduling algorithms
    # and consider calendar availability, energy levels, etc.
    # For now, create a simple schedule
    
    schedule = []
    today = datetime.now().date()
    
    for day in range(days_ahead):
        current_date = today + timedelta(days=day)
        weekday = current_date.weekday()  # 0-6 (Monday to Sunday)
        
        # Find activities suitable for this day
        suitable_activities = [
            activity for activity in me_time_activities
            if not activity.preferred_days or weekday in activity.preferred_days
        ]
        
        if suitable_activities:
            # Sort by priority
            suitable_activities.sort(key=lambda x: x.priority, reverse=True)
            activity = suitable_activities[0]
            
            # Find a suitable time
            if activity.preferred_time_ranges and activity.preferred_time_ranges[0]:
                time_range = activity.preferred_time_ranges[0]
                start_time = time_range.get("start", "18:00")
            else:
                start_time = "18:00"  # Default to 6 PM
            
            schedule.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "weekday": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][weekday],
                "activity_id": activity.id,
                "title": activity.title,
                "start_time": start_time,
                "duration_minutes": activity.duration_minutes,
                "location": activity.location
            })
    
    return schedule

# Life Balance Analysis Endpoints
@router.get("/wheel-of-life", response_model=Dict[str, Any])
def get_wheel_of_life(db: Session = Depends(get_db)):
    """Get data for a Wheel of Life visualization"""
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Get all life areas
    areas = db.query(models.LifeArea).filter(models.LifeArea.user_id == user_id).all()
    
    # If no areas exist, create default ones
    if not areas:
        default_areas = [
            {"type": LifeAreaTypeEnum.WORK, "importance": 8, "satisfaction": 6},
            {"type": LifeAreaTypeEnum.HEALTH, "importance": 9, "satisfaction": 5},
            {"type": LifeAreaTypeEnum.RELATIONSHIPS, "importance": 8, "satisfaction": 7},
            {"type": LifeAreaTypeEnum.PERSONAL_GROWTH, "importance": 7, "satisfaction": 6},
            {"type": LifeAreaTypeEnum.RECREATION, "importance": 6, "satisfaction": 4},
            {"type": LifeAreaTypeEnum.SPIRITUALITY, "importance": 5, "satisfaction": 5},
            {"type": LifeAreaTypeEnum.COMMUNITY, "importance": 6, "satisfaction": 4},
            {"type": LifeAreaTypeEnum.FINANCE, "importance": 7, "satisfaction": 6}
        ]
        
        for area_data in default_areas:
            db_area = models.LifeArea(
                user_id=user_id,
                type=area_data["type"],
                importance=area_data["importance"],
                satisfaction=area_data["satisfaction"]
            )
            db.add(db_area)
        
        db.commit()
        areas = db.query(models.LifeArea).filter(models.LifeArea.user_id == user_id).all()
    
    # Calculate overall life balance score
    total_importance = sum(area.importance for area in areas)
    weighted_satisfaction = sum(area.importance * area.satisfaction for area in areas)
    overall_score = weighted_satisfaction / total_importance if total_importance > 0 else 0
    
    # Create area data for visualization
    area_data = []
    for area in areas:
        area_data.append({
            "id": area.id,
            "name": area.type.replace("_", " ").title(),
            "importance": area.importance,
            "satisfaction": area.satisfaction,
            "gap": area.importance - area.satisfaction if area.importance > area.satisfaction else 0
        })
    
    # Sort by importance
    area_data.sort(key=lambda x: x["importance"], reverse=True)
    
    return {
        "overall_score": round(overall_score, 1),
        "max_score": 10,
        "areas": area_data
    }

@router.get("/burnout-risk", response_model=Dict[str, Any])
def analyze_burnout_risk(db: Session = Depends(get_db)):
    """Analyze the risk of burnout based on life balance"""
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Get life areas
    areas = db.query(models.LifeArea).filter(models.LifeArea.user_id == user_id).all()
    
    if not areas:
        return {
            "risk_level": "unknown",
            "risk_score": 0,
            "factors": [],
            "recommendations": ["Please set up your life areas to enable burnout analysis"]
        }
    
    # Calculate risk factors
    risk_factors = []
    risk_score = 0
    
    # Check work-life balance
    work_area = next((a for a in areas if a.type == LifeAreaTypeEnum.WORK), None)
    if work_area and work_area.satisfaction <= 4:
        risk_factors.append("Low work satisfaction")
        risk_score += 2
    
    # Check health
    health_area = next((a for a in areas if a.type == LifeAreaTypeEnum.HEALTH), None)
    if health_area and health_area.satisfaction <= 5:
        risk_factors.append("Health concerns")
        risk_score += 3
    
    # Check overall satisfaction gaps
    for area in areas:
        if area.importance - area.satisfaction >= 4:
            risk_factors.append(f"Large gap in {area.type.replace('_', ' ').title()}")
            risk_score += 2
    
    # Get recent goals
    goals = db.query(models.Goal).filter(
        models.Goal.user_id == user_id,
        models.Goal.created_at >= datetime.now() - timedelta(days=30)
    ).all()
    
    # Check goal overload
    if len(goals) > 5:
        risk_factors.append("Too many active goals (goal overload)")
        risk_score += 2
    
    # Determine risk level
    risk_level = "low"
    if risk_score >= 8:
        risk_level = "high"
    elif risk_score >= 4:
        risk_level = "medium"
    
    # Generate recommendations
    recommendations = []
    if "Low work satisfaction" in risk_factors:
        recommendations.append("Consider discussing workload or work environment with your manager")
    
    if "Health concerns" in risk_factors:
        recommendations.append("Prioritize sleep, exercise, and healthy eating habits")
    
    if "Too many active goals" in risk_factors:
        recommendations.append("Consider reducing the number of active goals and prioritizing the most important ones")
    
    if any("Large gap" in factor for factor in risk_factors):
        recommendations.append("Focus on areas with the largest satisfaction gaps")
    
    # Always add these
    recommendations.append("Schedule regular 'me time' for recovery and enjoyment")
    recommendations.append("Practice mindfulness or relaxation techniques")
    
    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "max_score": 10,
        "factors": risk_factors,
        "recommendations": recommendations
    }
