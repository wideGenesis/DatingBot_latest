from fastapi import (
    HTTPException,
    status,
)

from a_del.core.schemas import AdvertisementUpdate, AdvertisementCreate
from core.tables import models


class AdvertisementService:
    async def create(self, advertisement: AdvertisementCreate) -> models.Advertisement:
        return await models.Advertisement(**advertisement.dict()).save()

    async def get_by_area(self, area_id: int) -> models.Advertisement:
        _advertisement = (
            await models.Advertisement.objects.select_related("area_id")
            .select_related("large_city_near_id")
            .select_related("redis_channel_id")
            .select_related("publisher_id")
            .get_or_none(area_id=area_id)
        )
        if not _advertisement:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _advertisement

    async def get_by_redis_channel(self, redis_channel: int) -> models.Advertisement:
        _advertisement = (
            await models.Advertisement.objects.select_related("area_id")
            .select_related("large_city_near_id")
            .select_related("redis_channel_id")
            .select_related("publisher_id")
            .get_or_none(redis_channel=redis_channel)
        )
        if not _advertisement:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _advertisement

    async def get_by_large_city_near(
        self, large_city_near_id: int
    ) -> models.Advertisement:
        _advertisement = (
            await models.Advertisement.objects.select_related("area_id")
            .select_related("large_city_near_id")
            .select_related("redis_channel_id")
            .select_related("publisher_id")
            .get_or_none(large_city_near_id=large_city_near_id)
        )
        if not _advertisement:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _advertisement

    async def get_by_publisher_id(self, publisher_id: int) -> models.Advertisement:
        _advertisement = (
            await models.Advertisement.objects.select_related("area_id")
            .select_related("large_city_near_id")
            .select_related("redis_channel_id")
            .select_related("publisher_id")
            .get_or_none(publisher_id=publisher_id)
        )
        if not _advertisement:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _advertisement

    async def update(self, advertisement: AdvertisementUpdate) -> models.Advertisement:
        return await models.Advertisement(**advertisement.dict()).update()

    async def delete(self, _id: int) -> models.Advertisement.id:
        _advertisement = await models.Advertisement.objects.get(id=_id)
        deleted_id = await _advertisement.delete()
        return deleted_id

    async def list(self, offset: int, limit: int) -> models.Advertisement:
        return (
            await models.Advertisement.objects.offset(offset)
            .limit(limit)
            .select_related("area_id")
            .select_related("large_city_near_id")
            .select_related("redis_channel_id")
            .select_related("publisher_id")
            .all()
        )

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
