# finance_module.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from .database import get_db
from . import models
from pydantic import BaseModel

# Define router
router = APIRouter(
    prefix="/finance",
    tags=["finance"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    date: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class BudgetBase(BaseModel):
    category: str
    amount: float
    period: str

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

# Endpoints
@router.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_transaction = models.Transaction(
        user_id=user_id,
        amount=transaction.amount,
        category=transaction.category,
        description=transaction.description,
        date=transaction.date or datetime.now()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/transactions/", response_model=List[Transaction])
def read_transactions(
    skip: int = 0, 
    limit: int = 100, 
    start_date: Optional[datetime] = None, 
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.Transaction).filter(models.Transaction.user_id == user_id)
    
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    if category:
        query = query.filter(models.Transaction.category == category)
    
    return query.order_by(models.Transaction.date.desc()).offset(skip).limit(limit).all()

@router.post("/budgets/", response_model=Budget)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_budget = models.Budget(
        user_id=user_id,
        category=budget.category,
        amount=budget.amount,
        period=budget.period
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.get("/budgets/", response_model=List[Budget])
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).offset(skip).limit(limit).all()

@router.get("/analysis/spending")
def analyze_spending(
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
    
    # Get transactions for the period
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.date >= start_date,
        models.Transaction.date <= end_date
    ).all()
    
    # Analyze spending by category
    categories = {}
    total_spending = 0
    
    for tx in transactions:
        if tx.amount < 0:  # Only count expenses (negative amounts)
            amount = abs(tx.amount)
            total_spending += amount
            
            if tx.category in categories:
                categories[tx.category] += amount
            else:
                categories[tx.category] = amount
    
    # Calculate percentages
    category_analysis = []
    for category, amount in categories.items():
        category_analysis.append({
            "category": category,
            "amount": amount,
            "percentage": round((amount / total_spending * 100), 2) if total_spending > 0 else 0
        })
    
    # Sort by amount (descending)
    category_analysis.sort(key=lambda x: x["amount"], reverse=True)
    
    return {
        "period": period,
        "start_date": start_date,
        "end_date": end_date,
        "total_spending": total_spending,
        "categories": category_analysis
    }
