from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


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


# ---------------- ADVERT ----------------
class Advert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.utcnow)

    title: str
    price: int
    description: str | None = None
    category: str | None = None
    images_paths: str | None = None
    location: str | None = None

    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="adverts")

    # все чаты по объявлению
    chats: list["Chat"] = Relationship(back_populates="advert")


# ---------------- CHAT ----------------
class Chat(SQLModel, table=True):
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
