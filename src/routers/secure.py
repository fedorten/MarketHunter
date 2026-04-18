from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
import jwt
import os
import hashlib
import hmac
from jwt.exceptions import InvalidTokenError

from src.db import SessionDep
from src.tables import User
from src.models.user import CreateUser
from pwdlib import PasswordHash

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "a40f837cb1d8a0452f0d52c1322c30012574720c85be0ef6235e9ac4d17a890f",
)
ALGORITHM = "HS256"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

password_hash = PasswordHash.recommended()


# ----------------- Schemas -----------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


# ----------------- Password utils -----------------
def get_password_hash(password: str) -> str:
    if os.getenv("PYTEST_CURRENT_TEST"):
        digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return f"test-sha256${digest}"
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет введённый пароль с хэшем из БД"""
    if hashed_password.startswith("test-sha256$"):
        digest = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return hmac.compare_digest(hashed_password, f"test-sha256${digest}")
    return password_hash.verify(plain_password, hashed_password)


# ----------------- User utils -----------------
def get_user_by_phone(session: SessionDep, phone: str):
    statement = select(User).where(User.phone == phone)
    return session.exec(statement).first()


def get_user_by_email(session: SessionDep, email: str):
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def authenticate_user(session: SessionDep, phone: str, password: str):
    """Проверяет телефон и пароль пользователя"""
    user = get_user_by_phone(session, phone)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


# ----------------- JWT utils -----------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Создаёт JWT токен на основе данных и времени жизни"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=60 * 24 * 30)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    """Принимает токен конкретного юзера и возвращает его если он есть"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(subject))
    except (InvalidTokenError, ValueError):
        raise credentials_exception

    user = session.get(User, token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


# ----------------- Routes -----------------
@router.post("/registration")
async def registration_user(user_data: CreateUser, session: SessionDep):
    """Регистрация нового пользователя. Ошибка, если такой телефон уже занят"""
    existing_user_phone = get_user_by_phone(session, user_data.phone)
    if existing_user_phone:
        raise HTTPException(
            status_code=400, detail="User with this phone already exists"
        )
    if user_data.email:
        existing_user_email = get_user_by_email(session, user_data.email)
        if existing_user_email:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )
    user = User(
        username=user_data.username,
        phone=user_data.phone,
        password=get_password_hash(user_data.password),
        email=user_data.email,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"msg": "User created"}


@router.post("/login", response_model=Token)
async def login_for_access_token(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Создание токена на основе формы для существующего пользователя. Иначе ошибка"""
    # form_data.username фактически phone
    user = authenticate_user(
        session, phone=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=60 * 24 * 30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
