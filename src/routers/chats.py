from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends, HTTPException
from src.db import SessionDep
from src.tables import Chat, Message, User, Advert
from src.routers.secure import get_current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
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


# <-- добавил отдельную функцию для auth в websocket
async def get_user_ws(websocket: WebSocket, session: SessionDep):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close()
        return None

    try:
        payload = jwt.decode(
            token,
            "a40f837cb1d8a0452f0d52c1322c30012574720c85be0ef6235e9ac4d17a890f",
            algorithms=["HS256"],
        )
        user_id = payload.get("sub")
    except:
        await websocket.close()
        return None

    user = session.get(User, user_id)
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
            msg = Message(chat_id=chat_id, sender_id=current_user.id, content=data)
            session.add(msg)
            session.commit()
            session.refresh(msg)

            await manager.broadcast(chat_id, msg.model_dump(mode="json"))
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
