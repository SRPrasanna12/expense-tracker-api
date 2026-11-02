from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Expense, Category, User
from app.schemas.expense import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# Create an expense
@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check whether the category belongs to the logged-in user
    category = db.query(Category).filter(
        Category.id == expense_data.category_id,
        Category.user_id == current_user.id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_expense = Expense(
        title=expense_data.title,
        amount=expense_data.amount,
        description=expense_data.description,
        category_id=expense_data.category_id,
        expense_date=expense_data.expense_date,
        user_id=current_user.id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# Get all expenses belonging to the logged-in user
@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).all()
# Update an existing expense
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    update_data = expense_data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = db.query(Category).filter(
            Category.id == update_data["category_id"],
            Category.user_id == current_user.id
        ).first()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    for key, value in update_data.items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)

    return expense
# Delete an existing expense
@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}