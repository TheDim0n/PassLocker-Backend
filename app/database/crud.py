from sqlalchemy.orm import Session

from . import models, schemas


def create_user(db: Session, new_user: schemas.UserCreate):
    db_user = models.User(**new_user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def delete_user_by_id(db: Session, id: int):
    _ = db.query(models.User).filter(models.User.id == id).delete()
    db.commit()
    return


def create_secret(db: Session, new_secret: schemas.SecretCreate):
    secret_db = models.Secret(**new_secret.dict())
    db.add(secret_db)
    db.commit()
    db.refresh(secret_db)
    return


def get_user_secrets(db: Session, user_id: int):
    return db.query(models.Secret.id, models.Secret.secret).filter(
        models.Secret.user_id == user_id).all()


def delete_secret_by_id(db: Session, id: int):
    _ = db.query(models.Secret).filter(models.Secret.id == id).delete()
    db.commit()
    return
