from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

import schemas
from crud.auth import get_current_user
from crud.advertisement import AdvertisementService


router = APIRouter(
    prefix='/advertisement',
    tags=['Advertisement'],
)


@router.get(
    '/',
    response_model=List[schemas.Advertisement],
)
def get_advertisements(
    user: schemas.User = Depends(get_current_user),
    advertisement_service: AdvertisementService = Depends(),
):
    return advertisement_service.get_many(user.id)


@router.post(
    '/',
    response_model=schemas.Advertisement,
    status_code=status.HTTP_201_CREATED,
)
def create_advertisement(
    advertisement_data: schemas.AdvertisementCreate,
    user: schemas.User = Depends(get_current_user),
    advertisement_service: AdvertisementService = Depends(),
):
    return advertisement_service.create(
        user.id,
        advertisement_data,
    )


@router.get(
    '/{advertisement_id}',
    response_model=schemas.Advertisement,
)
def get_advertisement(
    advertisement_id: int,
    user: schemas.User = Depends(get_current_user),
    advertisement_service: AdvertisementService = Depends(),
):
    return advertisement_service.get(
        user.id,
        advertisement_id,
    )


@router.put(
    '/{advertisement_id}',
    response_model=schemas.Advertisement,
)
def update_advertisement(
    advertisement_id: int,
    advertisement_data: schemas.AdvertisementUpdate,
    user: schemas.User = Depends(get_current_user),
    advertisement_service: AdvertisementService = Depends(),
):
    return advertisement_service.update(
        user.id,
        advertisement_id,
        advertisement_data,
    )


@router.delete(
    '/{advertisement_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_advertisement(
    advertisement_id: int,
    user: schemas.User = Depends(get_current_user),
    advertisement_service: AdvertisementService = Depends(),
):
    advertisement_service.delete(
        user.id,
        advertisement_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
