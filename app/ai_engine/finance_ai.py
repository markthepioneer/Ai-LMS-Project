# ai_engine/finance_ai.py
import logging
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from .common import get_completion, analyze_text, AIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_spending_patterns(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze spending patterns from a list of transactions
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Dictionary with spending pattern insights
    """
    try:
        # Convert to pandas DataFrame for analysis
        df = pd.DataFrame(transactions)
        
        # Basic validation
        if df.empty or 'amount' not in df.columns:
            return {
                "error": "No valid transaction data provided"
            }
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Focus on spending (negative amounts)
        spending_df = df[df['amount'] < 0].copy()
        spending_df['amount'] = spending_df['amount'].abs()  # Convert to positive for analysis
        
        # Group by category
        if 'category' in df.columns:
            category_spending = spending_df.groupby('category')['amount'].agg(['sum', 'count', 'mean'])
            category_spending = category_spending.reset_index()
            category_spending = category_spending.sort_values('sum', ascending=False)
            
            # Calculate percentages
            total_spending = category_spending['sum'].sum()
            category_spending['percentage'] = (category_spending['sum'] / total_spending * 100).round(2)
            
            categories = category_spending.to_dict('records')
        else:
            categories = []
            total_spending = spending_df['amount'].sum() if not spending_df.empty else 0
        
        # Time-based analysis
        if 'date' in df.columns:
            # Monthly spending
            spending_df['month'] = spending_df['date'].dt.to_period('M')
            monthly_spending = spending_df.groupby('month')['amount'].sum()
            monthly_spending = monthly_spending.reset_index()
            monthly_spending['month'] = monthly_spending['month'].astype(str)
            
            # Day of week analysis
            spending_df['day_of_week'] = spending_df['date'].dt.day_name()
            dow_spending = spending_df.groupby('day_of_week')['amount'].sum()
            
            temporal_analysis = {
                "monthly": monthly_spending.to_dict('records'),
                "day_of_week": dow_spending.to_dict()
            }
        else:
            temporal_analysis = {}
        
        # Find anomalies (transactions significantly above average)
        if not spending_df.empty:
            mean_amount = spending_df['amount'].mean()
            std_amount = spending_df['amount'].std()
            threshold = mean_amount + (2 * std_amount)  # 2 standard deviations
            
            anomalies = spending_df[spending_df['amount'] > threshold]
            anomaly_transactions = anomalies.to_dict('records')
        else:
            anomaly_transactions = []
        
        return {
            "total_spending": float(total_spending),
            "category_analysis": categories,
            "temporal_analysis": temporal_analysis,
            "anomalies": anomaly_transactions,
            "transaction_count": len(spending_df)
        }
    
    except Exception as e:
        logger.error(f"Error analyzing spending patterns: {str(e)}")
        return {
            "error": f"Failed to analyze spending patterns: {str(e)}"
        }

def generate_budget_recommendations(
    income: float,
    expenses: List[Dict[str, Any]],
    savings_goal_percentage: float = 20.0
) -> Dict[str, Any]:
    """
    Generate budget recommendations based on income and expense history
    
    Args:
        income: Monthly income amount
        expenses: List of expense dictionaries with category and amount
        savings_goal_percentage: Target percentage of income to save
        
    Returns:
        Dictionary with budget recommendations
    """
    try:
        # Convert expenses to DataFrame
        expense_df = pd.DataFrame(expenses)
        
        # Group expenses by category
        category_expenses = expense_df.groupby('category')['amount'].sum()
        
        # Calculate total expenses and current savings
        total_expenses = category_expenses.sum()
        current_savings = income - total_expenses
        current_savings_percentage = (current_savings / income * 100) if income > 0 else 0
        
        # Calculate target savings
        target_savings = income * (savings_goal_percentage / 100)
        savings_gap = target_savings - current_savings
        
        # Generate category-specific recommendations
        recommendations = []
        
        # If we're not meeting savings goal, suggest reductions
        if savings_gap > 0:
            # Calculate what percentage of expenses needs to be reduced
            reduction_factor = savings_gap / total_expenses
            
            for category, amount in category_expenses.items():
                recommended_amount = amount * (1 - reduction_factor)
                reduction = amount - recommended_amount
                
                recommendations.append({
                    "category": category,
                    "current_amount": float(amount),
                    "recommended_amount": float(recommended_amount),
                    "reduction": float(reduction),
                    "reduction_percentage": float(reduction / amount * 100) if amount > 0 else 0
                })
        else:
            # We're exceeding our savings goal, provide balanced recommendations
            for category, amount in category_expenses.items():
                recommendations.append({
                    "category": category,
                    "current_amount": float(amount),
                    "recommended_amount": float(amount),  # Keep the same
                    "reduction": 0.0,
                    "reduction_percentage": 0.0
                })
        
        # Sort recommendations by reduction amount (highest first)
        recommendations.sort(key=lambda x: x["reduction"], reverse=True)
        
        return {
            "monthly_income": float(income),
            "total_expenses": float(total_expenses),
            "current_savings": float(current_savings),
            "current_savings_percentage": float(current_savings_percentage),
            "target_savings": float(target_savings),
            "target_savings_percentage": float(savings_goal_percentage),
            "savings_gap": float(savings_gap),
            "category_recommendations": recommendations
        }
    
    except Exception as e:
        logger.error(f"Error generating budget recommendations: {str(e)}")
        return {
            "error": f"Failed to generate budget recommendations: {str(e)}"
        }

def predict_cash_flow(
    income_sources: List[Dict[str, Any]],
    recurring_expenses: List[Dict[str, Any]],
    months_ahead: int = 6
) -> Dict[str, Any]:
    """
    Predict future cash flow based on recurring income and expenses
    
    Args:
        income_sources: List of recurring income sources
        recurring_expenses: List of recurring expenses
        months_ahead: Number of months to project
        
    Returns:
        Dictionary with monthly cash flow projections
    """
    try:
        # Start from current month
        now = datetime.now()
        current_month = datetime(now.year, now.month, 1)
        
        # Generate months for projection
        months = [current_month + timedelta(days=30*i) for i in range(months_ahead)]
        month_labels = [month.strftime("%Y-%m") for month in months]
        
        # Initialize projection with zeros
        projections = {month: {"income": 0, "expenses": 0, "net": 0} for month in month_labels}
        
        # Process income sources
        for source in income_sources:
            amount = source.get("amount", 0)
            frequency = source.get("frequency", "monthly")
            
            for i, month in enumerate(month_labels):
                if frequency == "monthly":
                    projections[month]["income"] += amount
                elif frequency == "bi-weekly":
                    # Approximately 2.17 bi-weekly payments per month
                    projections[month]["income"] += amount * 2.17
                elif frequency == "weekly":
                    # Approximately 4.33 weeks per month
                    projections[month]["income"] += amount * 4.33
                elif frequency == "annual" and i == 0:
                    # Annual income only counted in first month
                    projections[month]["income"] += amount
                elif frequency == "quarterly" and i % 3 == 0:
                    # Quarterly income every 3 months
                    projections[month]["income"] += amount
        
        # Process recurring expenses
        for expense in recurring_expenses:
            amount = expense.get("amount", 0)
            frequency = expense.get("frequency", "monthly")
            
            for i, month in enumerate(month_labels):
                if frequency == "monthly":
                    projections[month]["expenses"] += amount
                elif frequency == "bi-weekly":
                    projections[month]["expenses"] += amount * 2.17
                elif frequency == "weekly":
                    projections[month]["expenses"] += amount * 4.33
                elif frequency == "annual" and i == 0:
                    projections[month]["expenses"] += amount
                elif frequency == "quarterly" and i % 3 == 0:
                    projections[month]["expenses"] += amount
        
        # Calculate net cash flow
        for month in month_labels:
            projections[month]["net"] = projections[month]["income"] - projections[month]["expenses"]
        
        # Format into a list for easier consumption
        projection_list = [
            {
                "month": month,
                "income": round(data["income"], 2),
                "expenses": round(data["expenses"], 2),
                "net": round(data["net"], 2)
            }
            for month, data in projections.items()
        ]
        
        # Calculate summary statistics
        total_income = sum(item["income"] for item in projection_list)
        total_expenses = sum(item["expenses"] for item in projection_list)
        total_net = sum(item["net"] for item in projection_list)
        
        return {
            "projections": projection_list,
            "summary": {
                "total_income": round(total_income, 2),
                "total_expenses": round(total_expenses, 2),
                "total_net": round(total_net, 2),
                "average_monthly_net": round(total_net / months_ahead, 2)
            }
        }
    
    except Exception as e:
        logger.error(f"Error predicting cash flow: {str(e)}")
        return {
            "error": f"Failed to predict cash flow: {str(e)}"
        }
