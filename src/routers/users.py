from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


from src.db import SessionDep
from src.tables import User
from src.routers.secure import get_current_user
from src.models.user import PatchUser, PublicUser

router = APIRouter(prefix="/api/v1/users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=PublicUser)
async def read_user(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    user = session.get(User, current_user.id)
    return user


@router.patch("/me", response_model=PublicUser)
async def patch_user(
    session: SessionDep,
    new_user_data: PatchUser,
    current_user: User = Depends(get_current_user),
):
    user = session.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    user_data = new_user_data.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/me/favorites")
def favorites(session: SessionDep, current_user=Depends(get_current_user)):
    user = session.get(User, current_user.id)
    return user.liked_adverts
