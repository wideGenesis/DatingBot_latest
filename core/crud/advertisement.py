from typing import (
    List,
    Optional, Union, Dict,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from core.schemas.advertisement import AdvertisementUpdate, AdvertisementCreate
from core.tables import models
from core.tables.models import RedisChannel, Customer
from db.engine import get_session


class AdvertisementService:

    async def create(self, advertisement: AdvertisementCreate) -> models.Advertisement:
        return await models.Advertisement(**advertisement.dict()).save()

    async def get_by_location(self, location: str) -> models.Advertisement:
        _advertisement = await models.Advertisement.objects.get_or_none(location=location)
        if not _advertisement:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _advertisement

    async def get_by_redis_channel_id(self, redis_channel_id: Optional[Union[RedisChannel, Dict]]) -> models.Advertisement:
        _advertisement = await models.Advertisement.objects.get_or_none(redis_channel_id=phone)
        if not _advertisement:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _advertisement

    async def get_by_publisher_id(self, publisher_id: Optional[Union[Customer, Dict]]) -> models.Advertisement:
        _advertisement = await models.Advertisement.objects.get_or_none(publisher_id=nickname)
        if not _advertisement:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _advertisement

    async def update(self, advertisement: AdvertisementUpdate) -> models.Advertisement:
        return await models.Advertisement(**advertisement.dict()).update()

    async def delete(self, member_id: int) -> models.Advertisement.id:
        _advertisement = await models.Advertisement.objects.get(member_id=member_id)
        deleted_id = await _advertisement.delete()
        return deleted_id

    async def list(self, offset: int, limit: int) -> models.Advertisement:
        return await models.Advertisement.objects.offset(offset).limit(limit).all()




    # def __init__(self, session: Session = Depends(get_session)):
    #     self.session = session
    #
    # def get_many(self, user_id: int) -> List[models.Advertisement]:
    #     operations = (
    #         self.session
    #         .query(models.Advertisement)
    #         .filter(models.Advertisement.user_id == user_id)
    #         .order_by(
    #             models.Advertisement.date.desc(),
    #             models.Advertisement.id.desc(),
    #         )
    #         .all()
    #     )
    #     return operations
    #
    # def get(
    #     self,
    #     user_id: int,
    #     operation_id: int
    # ) -> models.Advertisement:
    #     operation = self._get(user_id, operation_id)
    #     return operation
    #
    # def create_many(
    #     self,
    #     user_id: int,
    #     operations_data: List[schemas.AdvertisementCreate],
    # ) -> List[models.Advertisement]:
    #     operations = [
    #         models.Advertisement(
    #             **operation_data.dict(),
    #             user_id=user_id,
    #         )
    #         for operation_data in operations_data
    #     ]
    #     self.session.add_all(operations)
    #     self.session.commit()
    #     return operations
    #
    # def create(
    #     self,
    #     user_id: int,
    #     operation_data: schemas.AdvertisementCreate,
    # ) -> models.Advertisement:
    #     operation = models.Advertisement(
    #         **operation_data.dict(),
    #         user_id=user_id,
    #     )
    #     self.session.add(operation)
    #     self.session.commit()
    #     return operation
    #
    # def update(
    #     self,
    #     user_id: int,
    #     operation_id: int,
    #     operation_data: schemas.AdvertisementUpdate,
    # ) -> models.Advertisement:
    #     operation = self._get(user_id, operation_id)
    #     for field, value in operation_data:
    #         setattr(operation, field, value)
    #     self.session.commit()
    #     return operation
    #
    # def delete(
    #     self,
    #     user_id: int,
    #     operation_id: int,
    # ):
    #     operation = self._get(user_id, operation_id)
    #     self.session.delete(operation)
    #     self.session.commit()
    #
    # def _get(self, user_id: int, operation_id: int) -> Optional[models.Advertisement]:
    #     operation = (
    #         self.session
    #         .query(models.Advertisement)
    #         .filter(
    #             models.Advertisement.user_id == user_id,
    #             models.Advertisement.id == operation_id,
    #         )
    #         .first()
    #     )
    #     if not operation:
    #         raise HTTPException(status.HTTP_404_NOT_FOUND)
    #     return operation
