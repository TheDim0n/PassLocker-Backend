from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import DataBase
from app.dependencies import get_db, get_settings
from app.main import app


settings = get_settings()

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False, bind=engine)

DataBase.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app, base_url="http://localhost")

test_message = {"message": "test message"}


def get_user_token(login: str, password: str):
    payload = f"password={password}&username={login}"
    response = client.post(
        '/users/token/', data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()


def test_create_new_user():
    response = client.post("/users/", json={
        "login": settings.default_user_login,
        "password": settings.default_user_password
    })
    assert response.status_code == 201


def test_get_user_token():
    data = get_user_token(
        settings.default_user_login,
        settings.default_user_password
    )
    assert "access_token" in data


def test_create_existing_user():
    response = client.post("/users/", json={
        "login": settings.default_user_login,
        "password": settings.default_user_password
    })
    assert response.status_code == 409
