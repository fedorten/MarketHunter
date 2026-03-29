from sqlmodel import SQLModel
from pydantic import ConfigDict


class PublicUser(SQLModel):
    username: str
    phone: str
    email: str | None


class CreateUser(SQLModel):
    username: str
    phone: str
    password: str
    email: str | None = None


class PatchUser(SQLModel):
    model_config = ConfigDict(extra='forbid')
    
    username: str | None = None
    password: str | None = None
    email: str | None = None
