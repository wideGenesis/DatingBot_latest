from typing import Union
from fastapi import status, Response
from asyncpg.exceptions import ForeignKeyViolationError
from settings.logger import CustomLogger
from core.tables import models


logger = CustomLogger.get_logger("bot")


class AdvertisementService:
    async def create(
            self,
            advertisement: models.Advertisement
    ) -> models.Advertisement:
        try:
            return await models.Advertisement(**advertisement.dict()).save()
        except Exception:
            logger.exception('Something went wrong!')

    async def list(
            self,
            offset: int,
            limit: int
    ) -> Union[models.Advertisement, Response]:
        advertisements = await models.Advertisement.objects.offset(offset).limit(limit).all()
        if not advertisements:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return advertisements

    async def get_by_area(
            self,
            area_id: int
    ) -> Union[models.Advertisement, Response]:
        advertisement = await models.Advertisement.objects.get_or_none(area_id=area_id)

        if not advertisement:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return advertisement

    async def get_by_redis_channel(
            self,
            redis_channel: int
    ) -> Union[models.Advertisement, Response]:
        advertisement = await models.Advertisement.objects.get_or_none(redis_channel=redis_channel)

        if not advertisement:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return advertisement

    async def get_by_large_city_near(
            self,
            large_city_near_id: int
    ) -> Union[models.Advertisement, Response]:
        advertisement = (
            await models.Advertisement.objects.get_or_none(large_city_near_id=large_city_near_id)
        )
        if not advertisement:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return advertisement

    async def get_by_customer(
            self,
            customer: int
    ) -> Union[models.Advertisement, Response]:
        advertisement = await models.Advertisement.objects.get_or_none(customer=customer)

        if not advertisement:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return advertisement

    async def update(
            self,
            advertisement: models.Advertisement
    ) -> Union[models.Advertisement, Response]:
        intersection = {}
        update_advertisement = advertisement.dict()

        for k, v in update_advertisement.items():
            if v is None:
                continue
            intersection[k] = v

        return await models.Advertisement.objects.update_or_create(**intersection)

    async def delete(
            self,
            _id: int
    ) -> models.Advertisement.id:
        advertisement = await models.Advertisement.objects.get(id=_id)
        if not advertisement:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        try:
            await advertisement.delete()

        except ForeignKeyViolationError:
            return Response(status_code=status.HTTP_424_FAILED_DEPENDENCY)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
