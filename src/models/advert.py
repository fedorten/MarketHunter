from sqlmodel import SQLModel


class CreateAdvert(SQLModel):
    title: str
    price: int
    description: str | None = None
    category: str | None = None
    images_paths: str | None = None
    location: str | None = None
    owner_id: int
