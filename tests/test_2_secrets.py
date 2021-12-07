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


def test_create_new_secret():
    data = get_user_token(
        settings.default_user_login,
        settings.default_user_password
    )
    access_token = data["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/secrets/", headers=headers, json={
        "secret": "test_secret"
    })
    assert response.status_code == 201


def test_delete_secret():
    data = get_user_token(
        settings.default_user_login,
        settings.default_user_password
    )
    access_token = data["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/secrets/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) != 0

    id = response.json()[-1]["id"]
    response = client.delete(f"/secrets/{id}/", headers=headers)
    assert response.status_code == 204

    response = client.get("/secrets/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0
