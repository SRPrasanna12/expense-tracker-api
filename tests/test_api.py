import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Expense Tracker API is running!"
    }


def test_register_user():
    unique_id = uuid.uuid4().hex[:8]

    response = client.post(
        "/auth/register",
        json={
            "username": f"pytest_{unique_id}",
            "email": f"pytest_{unique_id}@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == f"pytest_{unique_id}"
    assert "hashed_password" not in response.json()

def test_login_user():
    response = client.post(
        "/auth/login",
        json={
            "email": "pytest_user@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_password():
    response = client.post(
        "/auth/login",
        json={
            "email": "pytest_user@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_access_profile_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_access_profile_with_token():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "pytest_user@example.com",
            "password": "TestPassword123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "pytest_user@example.com"

def test_access_profile_with_invalid_token():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"

def test_create_expense():
    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "pytest_user@example.com",
            "password": "TestPassword123"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a unique category
    unique_id = uuid.uuid4().hex[:8]

    category_response = client.post(
        "/categories/",
        json={"name": f"Food_{unique_id}"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert category_response.status_code == 201, category_response.json()

    category_id = category_response.json()["id"]

    # Create expense
    response = client.post(
        "/expenses/",
        json={
            "title": "Test Lunch",
            "amount": 250,
            "description": "Automated test expense",
            "category_id": category_id,
            "expense_date": "2026-11-01T12:00:00"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Lunch"
    assert response.json()["amount"] == 250

def test_users_cannot_access_other_users_expenses():
    unique_id = uuid.uuid4().hex[:8]

    # Register User A
    user_a_email = f"user_a_{unique_id}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "username": f"user_a_{unique_id}",
            "email": user_a_email,
            "password": "TestPassword123"
        }
    )
    assert response.status_code == 200

    # Login User A
    response = client.post(
        "/auth/login",
        json={
            "email": user_a_email,
            "password": "TestPassword123"
        }
    )
    token_a = response.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Create category for User A
    response = client.post(
        "/categories/",
        json={"name": "Food"},
        headers=headers_a
    )
    assert response.status_code == 201
    category_id = response.json()["id"]

    # Create expense for User A
    response = client.post(
        "/expenses/",
        json={
            "title": "User A Lunch",
            "amount": 500,
            "category_id": category_id
        },
        headers=headers_a
    )
    assert response.status_code == 201
    expense_id = response.json()["id"]

    # Register User B
    user_b_email = f"user_b_{unique_id}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "username": f"user_b_{unique_id}",
            "email": user_b_email,
            "password": "TestPassword123"
        }
    )
    assert response.status_code == 200

    # Login User B
    response = client.post(
        "/auth/login",
        json={
            "email": user_b_email,
            "password": "TestPassword123"
        }
    )
    token_b = response.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B must not see User A's expenses
    response = client.get("/expenses/", headers=headers_b)
    assert response.status_code == 200
    assert response.json() == []

    # User B must not update User A's expense
    response = client.put(
        f"/expenses/{expense_id}",
        json={"title": "Hacked Expense"},
        headers=headers_b
    )
    assert response.status_code == 404

    # User B must not delete User A's expense
    response = client.delete(
        f"/expenses/{expense_id}",
        headers=headers_b
    )
    assert response.status_code == 404