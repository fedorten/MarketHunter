from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.utcnow)
    username: str
    phone: str
    email: str | None = None

    adverts: list["Advert"] = Relationship(
        back_populates="owner"
    )  # это НЕ столбики в таблице. Это связь. Благодоря этому обьявления знают кто их юзер, но в юзере нет информации об обьявлениях
    chats: list["Chat"] = Relationship(back_populates="user")  # тут тоже самое


class Advert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.utcnow)
    title: str
    price: int

    description: str | None = None
    category: str | None = None
    images_paths: str | None = None
    location: str | None = None

    owner_id: int = Field(
        foreign_key="user.id"
    )  # сюда будет подтягиваться реальный айди и проверятся что он есть. Подтягивается он благодоря наличию Relationship
    owner: User = Relationship(
        back_populates="adverts"
    )  # это, опять же, не столбец в таблице и данные тут не хранятся, но это связь. back_population -  значит двусторонняя связь

    chats: list["Chat"] = Relationship(back_populates="advert")  #  тоже самое


class Chat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(
        foreign_key="user.id"
    )  #  реальный айди владельца подтянется автоматически
    advert_id: int = Field(foreign_key="advert.id")

    user: User = Relationship(back_populates="chats")  # благодоря вот этой связи
    advert: Advert = Relationship(back_populates="chats")


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chat.id")  # к какому чату принадлежит
    sender_id: int = Field(foreign_key="user.id")  # кто отправил сообщение
    content: str  # текст сообщения
    create_date: datetime = Field(default_factory=datetime.utcnow)

    chat: "Chat" = Relationship(back_populates="messages")  # связь с чатом
    sender: "User" = Relationship()
