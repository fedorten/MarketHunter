from sqlmodel import SQLModel


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
    username: str | None
    password: str | None
    email: str | None
