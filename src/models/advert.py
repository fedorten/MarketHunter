from sqlmodel import SQLModel


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
    title: str | None
    price: int | None
    description: str | None
    category: str | None
    images_paths: str | None
    location: str | None
