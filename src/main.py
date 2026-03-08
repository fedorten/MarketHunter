from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db import create_db_and_tables
from src.routers import users, adverst, secure
from src.admin import create_admin_page


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router, tags=["users"])
app.include_router(adverst.router, tags=["advers"])
app.include_router(secure.router, tags=["secure"])
create_admin_page(app)
