from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category, Expense, User
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


# Create a category
@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_category = db.query(Category).filter(
        Category.name == category_data.name,
        Category.user_id == current_user.id
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = Category(
        name=category_data.name,
        user_id=current_user.id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# Get all categories belonging to the logged-in user
@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Category).filter(
        Category.user_id == current_user.id
    ).all()
# Update a category
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category
# Delete a category
@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    existing_expenses = db.query(Expense).filter(
        Expense.category_id == category_id,
        Expense.user_id == current_user.id
    ).first()

    if existing_expenses:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete category because expenses are linked to it"
        )

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}