from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from sqlalchemy import Column, JSON
from datetime import datetime


class Like(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    advert_id: int = Field(foreign_key="advert.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------- USER ----------------
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.utcnow)

    username: str
    phone: str = Field(unique=True)
    password: str
    email: str | None = Field(unique=True)

    # объявления где он продавец
    adverts: list["Advert"] = Relationship(back_populates="owner")

    # чаты где он покупатель
    buyer_chats: list["Chat"] = Relationship(back_populates="buyer")

    # отправленные сообщения
    sent_messages: list["Message"] = Relationship(back_populates="sender")
    # понравившееся
    liked_adverts: list["Advert"] = Relationship(
        back_populates="liked_by", link_model=Like
    )


# ---------------- ADVERT ----------------
class Advert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.utcnow)

    title: str = Field(index=True)
    price: int = Field(index=True)
    description: str | None = None
    category: str | None = Field(default=None, index=True)
    images_paths: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    location: str | None = Field(default=None, index=True)
    views: int = 0
    likes: int = 0

    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="adverts")
    # все чаты по объявлению
    chats: list["Chat"] = Relationship(back_populates="advert")
    liked_by: list["User"] = Relationship(
        back_populates="liked_adverts", link_model=Like
    )


# ---------------- CHAT ----------------
class Chat(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("advert_id", "buyer_id", name="unique_chat"),)
    id: int | None = Field(default=None, primary_key=True)

    advert_id: int = Field(foreign_key="advert.id")
    buyer_id: int = Field(foreign_key="user.id")

    advert: Advert = Relationship(back_populates="chats")
    buyer: User = Relationship(back_populates="buyer_chats")

    messages: list["Message"] = Relationship(back_populates="chat")


# ---------------- MESSAGE ----------------
class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    chat_id: int = Field(foreign_key="chat.id")
    sender_id: int = Field(foreign_key="user.id")

    content: str
    is_read: bool = Field(default=False)
    create_date: datetime = Field(default_factory=datetime.utcnow)

    chat: Chat = Relationship(back_populates="messages")
    sender: User = Relationship(back_populates="sent_messages")
