import importlib

from importlib import resources
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import crud, schemas
from app.database.database import engine, SessionLocal
from app.dependencies import get_settings
from app.utils import password as passwd


settings = get_settings()

app = FastAPI(root_path=settings.root_path, title="PassLocker-Backend")

# include all routers
plugins = [f[:-3] for f in resources.contents("app.routers")
           if f.endswith(".py") and f[0] != "_"]
for plugin in plugins:
    router = importlib.import_module(f"app.routers.{plugin}")
    app.include_router(router.router)

# setup middleware
if settings.debug:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.on_event("startup")
async def on_startup():
    with Session(engine) as db:
        user_db = crud.get_user_by_login(db=db,
                                         login=settings.default_user_login)
        if not user_db:
            new_user = schemas.UserCreate(
                login=settings.default_user_login,
                password=settings.default_user_password
            )
            new_user.password = passwd.hash(new_user.password)
            _ = crud.create_user(db=db, new_user=new_user)
    return
