from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import DataBase
from app.dependencies import get_db
from app.main import app


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
        "login": "test_user",
        "password": "test_password"
    })
    assert response.status_code == 201


def test_get_user_token():
    data = get_user_token("test_user", "test_password")
    assert "access_token" in data
