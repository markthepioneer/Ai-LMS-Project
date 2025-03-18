# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base

# Enums for database use
class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DELEGATED = "delegated"
    COMPLETED = "completed"
    CANCELED = "canceled"

class AssetClass(enum.Enum):
    STOCK = "stock"
    BOND = "bond"
    ETF = "etf"
    MUTUAL_FUND = "mutual_fund"
    CRYPTO = "cryptocurrency"
    CASH = "cash"
    REAL_ESTATE = "real_estate"
    COMMODITY = "commodity"

# User model (for authentication)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    finance_preferences = relationship("FinancePreference", back_populates="user", uselist=False)
    health_preferences = relationship("HealthPreference", back_populates="user", uselist=False)

# Finance Models
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.now)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True)
    description = Column(String)
    
    # Relationships
    budget_id = Column(Integer, ForeignKey("budgets.id"))
    budget = relationship("Budget", back_populates="transactions")

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String, index=True)
    amount = Column(Float, nullable=False)
    period = Column(String)  # 'monthly', 'weekly', etc.
    
    # Relationships
    transactions = relationship("Transaction", back_populates="budget")

class FinancePreference(Base):
    __tablename__ = "finance_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    risk_tolerance = Column(String)  # 'conservative', 'moderate', 'aggressive'
    savings_goal_percentage = Column(Float, default=20.0)  # Default 20% of income
    investment_goal_percentage = Column(Float, default=15.0)  # Default 15% of income
    expense_categories = Column(JSON)  # Custom expense categories
    
    # Relationships
    user = relationship("User", back_populates="finance_preferences")

# Health Models
class SleepRecord(Base):
    __tablename__ = "sleep_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.now)
    duration_hours = Column(Float)
    quality = Column(Integer)  # 1-10 scale
    notes = Column(String)

class ExerciseRecord(Base):
    __tablename__ = "exercise_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.now)
    activity_type = Column(String)
    duration_minutes = Column(Integer)
    intensity = Column(Integer)  # 1-10 scale
    calories_burned = Column(Integer)
    notes = Column(String)

class HealthPreference(Base):
    __tablename__ = "health_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    sleep_goal_hours = Column(Float, default=8.0)
    exercise_goal_minutes = Column(Integer, default=150)  # Weekly goal
    daily_calorie_goal = Column(Integer)
    daily_water_goal = Column(Float)  # In liters
    favorite_activities = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="health_preferences")

# Task Management Models
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    estimated_duration_minutes = Column(Integer)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED)
    category = Column(String)
    delegatable = Column(Boolean, default=False)
    completion_date = Column(DateTime)

# Portfolio Management Models
class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, index=True)
    name = Column(String)
    asset_class = Column(Enum(AssetClass))
    quantity = Column(Float)
    purchase_price = Column(Float)
    purchase_date = Column(DateTime)
    account = Column(String)
    notes = Column(String)

# This is a simplified version of the models.
# More detailed models would include:
# - Memory Assistant (reminders, contacts, events)
# - Email and Call Handler (emails, drafts, templates, phone calls)
# - Life Balancer (life areas, goals, rewards, metrics)
