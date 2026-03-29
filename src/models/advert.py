from sqlmodel import SQLModel
from pydantic import ConfigDict


class CreateAdvert(SQLModel):
    title: str
    price: int
    description: str | None = None
    category: str | None = None
    images_paths: str | None = None
    location: str | None = None
    owner_id: int


class PublicAdvert(SQLModel):
    title: str
    price: int
    description: str | None = None
    category: str | None = None
    images_paths: str | None = None
    location: str | None = None


class PatchAdvert(SQLModel):
    model_config = ConfigDict(extra='forbid')
    
    title: str | None = None
    price: int | None = None
    description: str | None = None
    category: str | None = None
    images_paths: str | None = None
    location: str | None = None
