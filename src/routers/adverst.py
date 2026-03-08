from fastapi import APIRouter


from src.models.advert import CreateAdvert
from src.db import SessionDep
from src.tables import Advert


router = APIRouter(prefix="/api/v1/adverts")


@router.post("/")
async def create_advert(advert: CreateAdvert, session: SessionDep):
    advert = Advert.model_validate(advert)
    session.add(advert)
    session.commit()
    session.refresh(advert)
    return advert
