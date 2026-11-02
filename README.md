# Expense Tracker REST API

A backend REST API built with **FastAPI and PostgreSQL** to manage personal expenses securely. It supports user authentication, expense and category management, spending summaries, automated tests, and Docker deployment.

## Features

- User registration and login
- Password hashing using Argon2
- JWT-based authentication
- Create, read, update, and delete expenses
- Create, read, update, and delete categories
- User-specific data access and authorization
- Monthly expense summaries
- Category-wise spending summaries
- Input validation using Pydantic
- PostgreSQL database integration
- Database migrations using Alembic
- Automated API tests using Pytest
- Docker and Docker Compose support

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Validation:** Pydantic
- **Migrations:** Alembic
- **Testing:** Pytest, HTTPX
- **Containerization:** Docker, Docker Compose

## Project Structure

```text
expense-tracker-api/
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   ├── dependencies.py
│   ├── security.py
│   └── main.py
├── migrations/
├── tests/
│   └── test_api.py
├── .dockerignore
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/expense-tracker-api.git
cd expense-tracker-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=expense_tracker
SECRET_KEY=your_secret_key
```

Never commit your `.env` file or expose your secrets.

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://localhost:8000/docs

## Docker Setup

Make sure Docker Desktop is running and your `.env` file is configured.

Build and start the containers:

```bash
docker compose up --build -d
```

View running containers:

```bash
docker compose ps
```

Stop containers without deleting database data:

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Login and receive JWT |
| GET | `/users/me` | Get current user profile |
| POST | `/categories/` | Create category |
| GET | `/categories/` | List categories |
| PUT | `/categories/{id}` | Update category |
| DELETE | `/categories/{id}` | Delete category |
| POST | `/expenses/` | Create expense |
| GET | `/expenses/` | List expenses |
| PUT | `/expenses/{id}` | Update expense |
| DELETE | `/expenses/{id}` | Delete expense |
| GET | `/summary/monthly` | Monthly spending summary |
| GET | `/summary/category-wise` | Category-wise spending summary |

Protected endpoints require a valid JWT bearer token.

## Running Tests

```bash
python -m pytest -v
```

## Key Learning Outcomes

- Building REST APIs using FastAPI
- Designing relational database models
- Implementing authentication and authorization
- Writing user-scoped database queries
- Managing schema changes with Alembic
- Testing API endpoints and access controls
- Containerizing an application with Docker

## Author

Ratna Prasanna Sunkara

GitHub: https://github.com/SRPrasanna12