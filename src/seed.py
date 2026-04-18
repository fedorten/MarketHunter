from sqlmodel import Session, select

from src.db import create_db_and_tables, engine
from src.routers.secure import get_password_hash
from src.tables import Advert, Chat, Like, Message, User


PASSWORD = "password123"


USERS = [
    {
        "username": "Анна",
        "phone": "+79000000001",
        "email": "anna@krug.local",
    },
    {
        "username": "Марк",
        "phone": "+79000000002",
        "email": "mark@krug.local",
    },
    {
        "username": "София",
        "phone": "+79000000003",
        "email": "sofia@krug.local",
    },
    {
        "username": "Илья",
        "phone": "+79000000004",
        "email": "ilya@krug.local",
    },
]


ADVERTS = [
    {
        "title": "iPhone 14 Pro 256 ГБ",
        "price": 63500,
        "description": "Аккумулятор 91%, корпус без трещин, полный комплект.",
        "category": "electronics",
        "location": "Москва",
        "owner_phone": "+79000000001",
        "images_paths": [
            "https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?auto=format&fit=crop&w=1200&q=80"
        ],
        "views": 148,
    },
    {
        "title": "MacBook Air M2 13",
        "price": 82500,
        "description": "Покупался для учебы, 16 ГБ RAM, зарядка в комплекте.",
        "category": "electronics",
        "location": "Санкт-Петербург",
        "owner_phone": "+79000000002",
        "images_paths": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80"
        ],
        "views": 96,
    },
    {
        "title": "Диван модульный серый",
        "price": 27900,
        "description": "Три модуля, ткань легко чистится, самовывоз.",
        "category": "home",
        "location": "Казань",
        "owner_phone": "+79000000003",
        "images_paths": [
            "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1200&q=80"
        ],
        "views": 212,
    },
    {
        "title": "Велосипед Trek Marlin",
        "price": 39500,
        "description": "Размер M, обслужен перед сезоном, есть документы.",
        "category": "transport",
        "location": "Екатеринбург",
        "owner_phone": "+79000000004",
        "images_paths": [
            "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80"
        ],
        "views": 73,
    },
    {
        "title": "Наушники Sony WH-1000XM4",
        "price": 15900,
        "description": "Шумодав работает отлично, амбушюры свежие.",
        "category": "electronics",
        "location": "Москва",
        "owner_phone": "+79000000002",
        "images_paths": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=80"
        ],
        "views": 187,
    },
    {
        "title": "Кроссовки Nike Air Max",
        "price": 7800,
        "description": "Размер 42, носились пару раз, коробка сохранилась.",
        "category": "clothes",
        "location": "Новосибирск",
        "owner_phone": "+79000000001",
        "images_paths": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=80"
        ],
        "views": 58,
    },
    {
        "title": "Кофемашина DeLonghi",
        "price": 22100,
        "description": "Готовит эспрессо и капучино, недавно была чистка.",
        "category": "home",
        "location": "Нижний Новгород",
        "owner_phone": "+79000000003",
        "images_paths": [
            "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=1200&q=80"
        ],
        "views": 134,
    },
    {
        "title": "Монитор LG UltraWide 34",
        "price": 31200,
        "description": "3440x1440, без битых пикселей, удобен для работы.",
        "category": "electronics",
        "location": "Москва",
        "owner_phone": "+79000000004",
        "images_paths": [
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=1200&q=80"
        ],
        "views": 119,
    },
]


MESSAGES = [
    "Здравствуйте, объявление еще актуально?",
    "Да, актуально. Могу показать сегодня вечером.",
    "Отлично, тогда напишу ближе к 18:00.",
]


def get_or_create_user(session: Session, data: dict) -> User:
    user = session.exec(select(User).where(User.phone == data["phone"])).first()
    if user:
        return user

    user = User(
        username=data["username"],
        phone=data["phone"],
        email=data["email"],
        password=get_password_hash(PASSWORD),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_or_create_advert(session: Session, data: dict, users_by_phone: dict[str, User]):
    advert = session.exec(select(Advert).where(Advert.title == data["title"])).first()
    if advert:
        return advert

    owner = users_by_phone[data["owner_phone"]]
    advert = Advert(
        title=data["title"],
        price=data["price"],
        description=data["description"],
        category=data["category"],
        location=data["location"],
        images_paths=data["images_paths"],
        views=data["views"],
        owner_id=owner.id,
    )
    session.add(advert)
    session.commit()
    session.refresh(advert)
    return advert


def get_or_create_chat(session: Session, advert: Advert, buyer: User) -> Chat:
    chat = session.exec(
        select(Chat).where(Chat.advert_id == advert.id, Chat.buyer_id == buyer.id)
    ).first()
    if chat:
        return chat

    chat = Chat(advert_id=advert.id, buyer_id=buyer.id)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat


def add_message_if_missing(session: Session, chat: Chat, sender_id: int, content: str):
    exists = session.exec(
        select(Message).where(
            Message.chat_id == chat.id,
            Message.sender_id == sender_id,
            Message.content == content,
        )
    ).first()
    if exists:
        return

    session.add(Message(chat_id=chat.id, sender_id=sender_id, content=content))


def add_like_if_missing(session: Session, user: User, advert: Advert):
    exists = session.exec(
        select(Like).where(Like.user_id == user.id, Like.advert_id == advert.id)
    ).first()
    if not exists:
        session.add(Like(user_id=user.id, advert_id=advert.id))


def refresh_likes_count(session: Session):
    adverts = session.exec(select(Advert)).all()
    for advert in adverts:
        count = len(
            session.exec(select(Like).where(Like.advert_id == advert.id)).all()
        )
        advert.likes = count
        session.add(advert)


def seed():
    create_db_and_tables()

    with Session(engine) as session:
        users_by_phone = {
            data["phone"]: get_or_create_user(session, data) for data in USERS
        }
        adverts = [
            get_or_create_advert(session, data, users_by_phone) for data in ADVERTS
        ]
        users = list(users_by_phone.values())

        for index, advert in enumerate(adverts):
            buyer = users[(index + 1) % len(users)]
            if buyer.id == advert.owner_id:
                buyer = users[(index + 2) % len(users)]

            chat = get_or_create_chat(session, advert, buyer)
            add_message_if_missing(session, chat, buyer.id, MESSAGES[0])
            add_message_if_missing(session, chat, advert.owner_id, MESSAGES[1])
            add_message_if_missing(session, chat, buyer.id, MESSAGES[2])

            for user in users[: 1 + (index % len(users))]:
                if user.id != advert.owner_id:
                    add_like_if_missing(session, user, advert)

        refresh_likes_count(session)
        session.commit()

    print(f"Seed complete: {len(USERS)} users, {len(ADVERTS)} adverts")
    print(f"Password for all test users: {PASSWORD}")


if __name__ == "__main__":
    seed()
