from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from pathlib import Path
import os


connect_args = {"check_same_thread": False}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'marketplace.db'}")
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


async def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
