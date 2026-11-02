from app.routers.summary import router as summary_router
from app.routers.expenses import router as expenses_router
from app.routers.categories import router as categories_router
from app.routers.users import router as users_router
from fastapi import FastAPI

from app.database import engine, Base
from app.models import User, Category, Expense
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="A REST API to manage personal expenses",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(summary_router)

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running!"}
