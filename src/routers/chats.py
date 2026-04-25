from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends, HTTPException
from src.db import SessionDep
from src.tables import Chat, Message, User, Advert
from src.routers.secure import SECRET_KEY, ALGORITHM, get_current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from sqlmodel import select
from pydantic import BaseModel
import jwt


router = APIRouter(prefix="/api/v1/chats")


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, chat_id, websocket: WebSocket):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id, websocket):
        if chat_id in self.active_connections:
            if websocket in self.active_connections[chat_id]:
                self.active_connections[chat_id].remove(websocket)
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast(self, chat_id, message: dict):
        dead = []
        for connection in self.active_connections.get(chat_id, []):
            try:
                await connection.send_json(message)
            except:
                dead.append(connection)

        for conn in dead:
            self.disconnect(chat_id, conn)


manager = ConnectionManager()


class SendMessage(BaseModel):
    content: str


def serialize_message(message: Message):
    return {
        "id": message.id,
        "chat_id": message.chat_id,
        "sender_id": message.sender_id,
        "content": message.content,
        "is_read": message.is_read,
        "create_date": message.create_date.isoformat(),
    }


def serialize_chat(chat: Chat, current_user_id: int):
    messages = sorted(chat.messages, key=lambda item: item.create_date)
    last_message = messages[-1] if messages else None
    seller = chat.advert.owner
    companion = chat.buyer if current_user_id == seller.id else seller
    return {
        "id": chat.id,
        "advert_id": chat.advert_id,
        "advert_title": chat.advert.title,
        "advert_price": chat.advert.price,
        "advert_image": chat.advert.images_paths[0]
        if chat.advert.images_paths
        else None,
        "buyer_id": chat.buyer_id,
        "seller_id": seller.id,
        "companion": {
            "id": companion.id,
            "username": companion.username,
        },
        "last_message": serialize_message(last_message) if last_message else None,
        "unread_count": len(
            [
                message
                for message in messages
                if message.sender_id != current_user_id and not message.is_read
            ]
        ),
    }


@router.post("/{advert_id}")
async def create_chat(
    advert_id: int, session: SessionDep, current_user: User = Depends(get_current_user)
):
    advert = session.get(Advert, advert_id)
    if not advert:
        raise HTTPException(status_code=404, detail="this advert is not found")
    if current_user.id == advert.owner_id:
        raise HTTPException(status_code=404, detail="you can`t write yourself")
    try:
        chat = Chat(buyer_id=current_user.id, advert_id=advert_id)
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return {"chat_id": chat.id, "is_new": True}
    except IntegrityError:
        session.rollback()
        statement = select(Chat).where(
            Chat.advert_id == advert_id,
            Chat.buyer_id == current_user.id,
        )
        existing_chat = session.exec(statement).one()
        return {"chat_id": existing_chat.id, "is_new": False}


@router.get("/")
async def read_chats(
    session: SessionDep, current_user: User = Depends(get_current_user)
):
    statement = (
        select(Chat)
        .join(Advert)
        .where(
            or_(Chat.buyer_id == current_user.id, Advert.owner_id == current_user.id)
        )
    )
    chats = session.exec(statement).all()
    chats = sorted(
        chats,
        key=lambda chat: max(
            [message.create_date for message in chat.messages],
            default=chat.advert.create_date,
        ),
        reverse=True,
    )
    return [serialize_chat(chat, current_user.id) for chat in chats]


@router.get("/{chat_id}")
async def read_chat(
    chat_id: int, session: SessionDep, current_user: User = Depends(get_current_user)
):
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="chat not found")
    if current_user.id not in [chat.buyer_id, chat.advert.owner_id]:
        raise HTTPException(status_code=403, detail="chat is not available")
    return serialize_chat(chat, current_user.id)


@router.get("/{chat_id}/messages")
async def read_messages(
    chat_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    page: int = 1,
    per_page: int = 50,
):
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="chat not found")
    if current_user.id not in [chat.buyer_id, chat.advert.owner_id]:
        raise HTTPException(status_code=403, detail="chat is not available")

    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)
    statement = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.create_date)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return [serialize_message(message) for message in session.exec(statement).all()]


@router.post("/{chat_id}/messages")
async def send_message(
    chat_id: int,
    payload: SendMessage,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="chat not found")
    if current_user.id not in [chat.buyer_id, chat.advert.owner_id]:
        raise HTTPException(status_code=403, detail="chat is not available")

    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="message is empty")

    message = Message(chat_id=chat_id, sender_id=current_user.id, content=content)
    session.add(message)
    session.commit()
    session.refresh(message)
    serialized = serialize_message(message)
    await manager.broadcast(chat_id, serialized)
    return serialized


@router.patch("/{chat_id}/read")
async def mark_messages_read(
    chat_id: int, session: SessionDep, current_user: User = Depends(get_current_user)
):
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="chat not found")
    if current_user.id not in [chat.buyer_id, chat.advert.owner_id]:
        raise HTTPException(status_code=403, detail="chat is not available")

    statement = select(Message).where(
        Message.chat_id == chat_id,
        Message.sender_id != current_user.id,
        Message.is_read == False,
    )
    messages = session.exec(statement).all()
    for message in messages:
        message.is_read = True
        session.add(message)
    session.commit()
    return {"updated": len(messages)}


# <-- добавил отдельную функцию для auth в websocket
async def get_user_ws(websocket: WebSocket, session: SessionDep):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close()
        return None

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        user_id = payload.get("sub")
    except Exception:
        await websocket.close()
        return None

    try:
        user = session.get(User, int(user_id))
    except (TypeError, ValueError):
        await websocket.close()
        return None
    if not user:
        await websocket.close()
        return None

    return user


@router.websocket("/ws/{chat_id}")
async def websocket_life(
    websocket: WebSocket,
    chat_id: int,
    session: SessionDep,
):
    current_user = await get_user_ws(websocket, session)  # <-- заменил Depends
    if not current_user:
        return

    chat = session.get(Chat, chat_id)
    if not chat:
        await websocket.close()
        return

    # <-- проверка доступа к чату
    if current_user.id not in [chat.buyer_id, chat.advert.owner_id]:
        await websocket.close()
        return

    await manager.connect(chat_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            content = data.strip()
            if not content:
                continue
            msg = Message(chat_id=chat_id, sender_id=current_user.id, content=content)
            session.add(msg)
            session.commit()
            session.refresh(msg)

            await manager.broadcast(chat_id, serialize_message(msg))
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
