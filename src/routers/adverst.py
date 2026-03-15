from fastapi import APIRouter, HTTPException, Depends


from src.models.advert import CreateAdvert, PublicAdvert, PatchAdvert
from src.db import SessionDep
from src.tables import Advert
from src.tables import User
from src.routers.secure import get_current_user

router = APIRouter(prefix="/api/v1/adverts")


@router.post("/")
async def create_advert(
    advert: CreateAdvert,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    user = session.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    advert = Advert.model_validate(advert)
    if advert.owner_id != user.id:
        raise HTTPException(
            status_code=401, detail="you can`t create advert for another users"
        )
    session.add(advert)
    session.commit()
    session.refresh(advert)
    return advert


@router.get("/", response_model=list[PublicAdvert])
async def read_all_adverts(session: SessionDep):
    adverts = session.query(Advert).all()
    return adverts


@router.get("/{id}", response_model=PublicAdvert)
async def read_advert(id: int, session: SessionDep):
    advert = session.get(Advert, id)
    if not advert:
        raise HTTPException(status_code=404, detail=f"advert with id:{id} not found")
    return advert


@router.patch("/{id}", response_model=PublicAdvert)
async def patch_user(
    session: SessionDep,
    new_advert_data: PatchAdvert,
    id: int,
    current_user: User = Depends(get_current_user),
):
    user = session.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    advert = session.get(Advert, id)
    if advert.owner_id != user.id:
        raise HTTPException(
            status_code=401, detail="you can`t patch advert for another users"
        )
    if not advert:
        raise HTTPException(status_code=404, detail="advert not found")
    advert_data = new_advert_data.model_dump(exclude_unset=True)

    advert.sqlmodel_update(advert_data)
    session.add(advert)
    session.commit()
    session.refresh(advert)
    return advert


@router.delete("/{id}")
async def delete_advert(
    session: SessionDep, id: int, current_user: User = Depends(get_current_user)
):
    user = session.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    advert = session.get(Advert, id)
    if not advert:
        raise HTTPException(status_code=404, detail="Advert not found")
    session.delete(advert)
    session.commit()
    return advert
