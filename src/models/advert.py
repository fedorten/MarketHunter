from sqlmodel import SQLModel
from pydantic import ConfigDict
from datetime import datetime


class CreateAdvert(SQLModel):
    title: str
    price: int
    description: str | None = None
    category: str | None = None
    images_paths: list[str] | None = None
    location: str | None = None
    owner_id: int | None = None


class PublicAdvert(SQLModel):
    id: int
    title: str
    price: int
    description: str | None = None
    category: str | None = None
    images_paths: list[str] | None = None
    location: str | None = None
    views: int = 0
    likes: int = 0
    owner_id: int
    create_date: datetime


class PatchAdvert(SQLModel):
    model_config = ConfigDict(extra='forbid')
    
    title: str | None = None
    price: int | None = None
    description: str | None = None
    category: str | None = None
    images_paths: list[str] | None = None
    location: str | None = None
