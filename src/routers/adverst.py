from fastapi import APIRouter, HTTPException, Depends

from sqlmodel import select, asc, desc
from sqlalchemy import or_
from src.models.advert import CreateAdvert, PublicAdvert, PatchAdvert
from src.db import SessionDep
from src.tables import Advert, User, Like
from src.routers.secure import get_current_user

router = APIRouter(prefix="/api/v1/adverts")


@router.post("/")
async def create_advert(
    advert: CreateAdvert,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    if advert.owner_id is not None and advert.owner_id != current_user.id:
        raise HTTPException(
            status_code=401, detail="you can`t create advert for another users"
        )
    advert_data = advert.model_dump(exclude={"owner_id"})
    advert = Advert(**advert_data, owner_id=current_user.id)
    session.add(advert)
    session.commit()
    session.refresh(advert)
    return advert


@router.post("/{advert_id}/like")
def toggle_like(
    advert_id: int, session: SessionDep, current_user=Depends(get_current_user)
):
    advert = session.get(Advert, advert_id)
    if not advert:
        raise HTTPException(status_code=404, detail="advert not found")
    like = session.exec(
        select(Like).where(Like.user_id == current_user.id, Like.advert_id == advert_id)
    ).first()

    if like:
        session.delete(like)
        advert.likes = max(0, advert.likes - 1)
        liked = False
    else:
        session.add(Like(user_id=current_user.id, advert_id=advert_id))
        advert.likes += 1
        liked = True

    session.add(advert)
    session.commit()

    return {"liked": liked, "likes": advert.likes}


@router.get("/{advert_id}/is-liked")
def is_liked(
    advert_id: int, session: SessionDep, current_user=Depends(get_current_user)
):
    like = session.exec(
        select(Like).where(Like.user_id == current_user.id, Like.advert_id == advert_id)
    ).first()

    return {"liked": like is not None}


@router.get("/", response_model=list[PublicAdvert])
async def read_all_adverts(
    session: SessionDep,
    sort_by: str = "popular",
    order: str = "desc",
    page: int = 1,  # номер страницы
    per_page: int = 20,  # количество на страницу
    q: str | None = None,
    category: str | None = None,
    location: str | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
):
    sort_columns = {
        "popular": Advert.likes,
        "latest": Advert.create_date,
        "price": Advert.price,
    }

    column = sort_columns.get(sort_by, Advert.likes)
    stmt = select(Advert)
    if q:
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(Advert.title.ilike(pattern), Advert.description.ilike(pattern))
        )
    if category:
        stmt = stmt.where(Advert.category == category)
    if location:
        stmt = stmt.where(Advert.location.ilike(f"%{location.strip()}%"))
    if price_min is not None:
        stmt = stmt.where(Advert.price >= price_min)
    if price_max is not None:
        stmt = stmt.where(Advert.price <= price_max)

    per_page = min(max(per_page, 1), 50)
    page = max(page, 1)
    stmt = stmt.order_by(desc(column) if order.lower() != "asc" else asc(column))
    stmt = stmt.offset((page - 1) * per_page).limit(per_page)

    adverts = session.exec(stmt).all()
    return adverts


@router.get("/mine", response_model=list[PublicAdvert])
async def read_my_adverts(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    stmt = select(Advert).where(Advert.owner_id == current_user.id).order_by(
        desc(Advert.create_date)
    )
    return session.exec(stmt).all()


@router.get("/{id}", response_model=PublicAdvert)
async def read_advert(id: int, session: SessionDep):
    advert = session.get(Advert, id)
    if not advert:
        raise HTTPException(status_code=404, detail=f"advert with id:{id} not found")
    advert.views += 1
    session.add(advert)
    session.commit()
    session.refresh(advert)
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
    if not advert:
        raise HTTPException(status_code=404, detail="advert not found")
    if advert.owner_id != user.id:
        raise HTTPException(
            status_code=401, detail="you can`t patch advert for another users"
        )
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
    advert = session.get(Advert, id)
    if not advert:
        raise HTTPException(status_code=404, detail="Advert not found")
    if advert.owner_id != current_user.id:
        raise HTTPException(
            status_code=401, detail="you can't delete advert for another users"
        )
    session.delete(advert)
    session.commit()
    return advert
