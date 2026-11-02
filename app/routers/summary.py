from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Expense, Category, User

router = APIRouter(prefix="/summary", tags=["Expense Summary"])


# Get total expenses for a selected month
@router.get("/monthly")
def monthly_summary(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.user_id == current_user.id,
        extract("year", Expense.expense_date) == year,
        extract("month", Expense.expense_date) == month
    ).scalar()

    return {
        "year": year,
        "month": month,
        "total_expenses": total
    }


# Get category-wise expense breakdown
@router.get("/category-wise")
def category_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        Category.name,
        func.sum(Expense.amount).label("total_amount")
    ).join(
        Expense, Expense.category_id == Category.id
    ).filter(
        Expense.user_id == current_user.id
    ).group_by(
        Category.name
    ).all()

    return [
        {
            "category": row.name,
            "total_amount": row.total_amount
        }
        for row in results
    ]