# portfolio_module.py
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
    prefix="/portfolio",
    tags=["portfolio"],
    responses={404: {"description": "Not found"}},
)

# Pydantic enum models
class AssetClassEnum(str, enum.Enum):
    STOCK = "stock"
    BOND = "bond"
    ETF = "etf"
    MUTUAL_FUND = "mutual_fund"
    CRYPTO = "cryptocurrency"
    CASH = "cash"
    REAL_ESTATE = "real_estate"
    COMMODITY = "commodity"

# Pydantic models for request/response
class InvestmentBase(BaseModel):
    symbol: str
    name: str
    asset_class: AssetClassEnum
    quantity: float
    purchase_price: float
    purchase_date: datetime
    account: Optional[str] = None
    notes: Optional[str] = None

class InvestmentCreate(InvestmentBase):
    pass

class Investment(InvestmentBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class InvestmentUpdate(BaseModel):
    symbol: Optional[str] = None
    name: Optional[str] = None
    asset_class: Optional[AssetClassEnum] = None
    quantity: Optional[float] = None
    purchase_price: Optional[float] = None
    purchase_date: Optional[datetime] = None
    account: Optional[str] = None
    notes: Optional[str] = None

class InvestmentTransactionBase(BaseModel):
    transaction_type: str  # "buy", "sell", "dividend", "split"
    quantity: float
    price: float
    date: Optional[datetime] = None
    fees: Optional[float] = 0.0
    notes: Optional[str] = None

class InvestmentTransactionCreate(InvestmentTransactionBase):
    pass

class InvestmentTransaction(InvestmentTransactionBase):
    id: int
    investment_id: int
    
    class Config:
        orm_mode = True

# Endpoints
@router.post("/investments/", response_model=Investment)
def create_investment(investment: InvestmentCreate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_investment = models.Investment(
        user_id=user_id,
        symbol=investment.symbol,
        name=investment.name,
        asset_class=investment.asset_class.value,
        quantity=investment.quantity,
        purchase_price=investment.purchase_price,
        purchase_date=investment.purchase_date,
        account=investment.account,
        notes=investment.notes
    )
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    return db_investment

@router.get("/investments/", response_model=List[Investment])
def read_investments(
    skip: int = 0, 
    limit: int = 100, 
    asset_class: Optional[AssetClassEnum] = None,
    account: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    query = db.query(models.Investment).filter(models.Investment.user_id == user_id)
    
    if asset_class:
        query = query.filter(models.Investment.asset_class == asset_class.value)
    if account:
        query = query.filter(models.Investment.account == account)
    
    return query.offset(skip).limit(limit).all()

@router.get("/investments/{investment_id}", response_model=Investment)
def read_investment(investment_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    investment = db.query(models.Investment).filter(
        models.Investment.id == investment_id, 
        models.Investment.user_id == user_id
    ).first()
    
    if investment is None:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    return investment

@router.put("/investments/{investment_id}", response_model=Investment)
def update_investment(investment_id: int, investment_update: InvestmentUpdate, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_investment = db.query(models.Investment).filter(
        models.Investment.id == investment_id, 
        models.Investment.user_id == user_id
    ).first()
    
    if db_investment is None:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    # Update provided fields
    update_data = investment_update.dict(exclude_unset=True)
    
    # Convert enum values to their string representations
    if "asset_class" in update_data and update_data["asset_class"] is not None:
        update_data["asset_class"] = update_data["asset_class"].value
    
    for key, value in update_data.items():
        setattr(db_investment, key, value)
    
    db.commit()
    db.refresh(db_investment)
    return db_investment

@router.delete("/investments/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investment(investment_id: int, db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    db_investment = db.query(models.Investment).filter(
        models.Investment.id == investment_id, 
        models.Investment.user_id == user_id
    ).first()
    
    if db_investment is None:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    db.delete(db_investment)
    db.commit()
    return {"status": "success"}

@router.get("/analysis/portfolio-allocation")
def analyze_portfolio_allocation(db: Session = Depends(get_db)):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Get all investments
    investments = db.query(models.Investment).filter(models.Investment.user_id == user_id).all()
    
    if not investments:
        return {
            "total_value": 0,
            "allocation": [],
            "message": "No investments found in portfolio."
        }
    
    # Calculate total portfolio value and allocation by asset class
    asset_classes = {}
    total_value = 0
    
    for inv in investments:
        # Calculate current value (in a real app, this would use current market prices)
        current_value = inv.quantity * inv.purchase_price
        total_value += current_value
        
        # Add to asset class
        if inv.asset_class in asset_classes:
            asset_classes[inv.asset_class] += current_value
        else:
            asset_classes[inv.asset_class] = current_value
    
    # Calculate percentages and create response
    allocation = []
    for asset_class, value in asset_classes.items():
        percentage = (value / total_value * 100) if total_value > 0 else 0
        allocation.append({
            "asset_class": asset_class,
            "value": value,
            "percentage": round(percentage, 2)
        })
    
    # Sort by percentage (descending)
    allocation.sort(key=lambda x: x["percentage"], reverse=True)
    
    return {
        "total_value": total_value,
        "allocation": allocation
    }

@router.get("/analysis/investment-performance")
def analyze_investment_performance(
    period: str = "year",
    db: Session = Depends(get_db)
):
    # In a real implementation, get user_id from the token
    user_id = 1  # For demo purposes
    
    # Get all investments
    investments = db.query(models.Investment).filter(models.Investment.user_id == user_id).all()
    
    if not investments:
        return {
            "message": "No investments found in portfolio."
        }
    
    # In a real app, this would calculate actual performance based on market data
    # For now, we'll use dummy data
    return {
        "period": period,
        "total_return_percentage": 8.7,
        "total_return_value": 12500,
        "benchmark_comparison": {
            "sp500": 7.2,
            "difference": 1.5
        },
        "top_performers": [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "return_percentage": 15.3
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft Corporation",
                "return_percentage": 12.8
            }
        ],
        "worst_performers": [
            {
                "symbol": "GE",
                "name": "General Electric Company",
                "return_percentage": -3.2
            }
        ],
        "note": "This is example data. In a real app, this would use actual market data and transaction history."
    }
