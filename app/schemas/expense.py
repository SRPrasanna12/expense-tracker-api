from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    amount: float = Field(gt=0, allow_inf_nan=False)
    description: str | None = Field(default=None, max_length=500)
    category_id: int = Field(gt=0)
    expense_date: datetime | None = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    description: str | None
    category_id: int
    expense_date: datetime

    model_config = ConfigDict(from_attributes=True)


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    amount: float | None = Field(default=None, gt=0, allow_inf_nan=False)
    description: str | None = Field(default=None, max_length=500)
    category_id: int | None = Field(default=None, gt=0)
    expense_date: datetime | None = None