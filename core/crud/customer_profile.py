from typing import Union
from fastapi import status, Response
from core.tables import models
from asyncpg.exceptions import ForeignKeyViolationError
from settings.logger import CustomLogger


logger = CustomLogger.get_logger("bot")


class CustomerProfileService:
    async def create(
            self, customer_profile: models.CustomerProfile
    ) -> models.CustomerProfile:
        return await models.CustomerProfile(**customer_profile.dict()).save()

    async def list(self, offset: int, limit: int) -> Union[models.CustomerProfile, Response]:
        profiles = await models.CustomerProfile.objects.offset(offset).limit(limit).all()
        if not profiles:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return profiles

    async def list_by_hiv_status(
            self, offset: int, limit: int, hiv_status: str) -> Union[models.CustomerProfile, Response]:
        customer_hiv_status = await models.CustomerProfile.objects.offset(offset).limit(limit).filter(
            hiv_status=hiv_status).all()
        if not customer_hiv_status:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return customer_hiv_status

    async def get_by_id(self, _id: int) -> Union[models.CustomerProfile, Response]:
        profile = await models.CustomerProfile.objects.get_or_none(id=_id)
        if not profile:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return profile

    async def get_by_member_id(self, member_id: int) -> Union[models.CustomerProfile, Response]:
        customer = await models.Customer.objects.get_or_none(member_id=member_id)
        if not customer:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        profile = await models.CustomerProfile.objects.get_or_none(customer=customer.id)

        if not profile:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return profile

    async def update(
            self, customer_profile: models.CustomerProfile
    ) -> models.CustomerProfile:
        intersection = {}
        update_customer_profile = customer_profile.dict()

        for k, v in update_customer_profile.items():
            if v is None:
                continue
            intersection[k] = v

        return await models.CustomerProfile.objects.update_or_create(**intersection)

    async def delete(self, _id: int) -> models.CustomerProfile.id:
        profile = await models.CustomerProfile.objects.get_or_none(id=_id)

        if not profile:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        try:
            await profile.delete()

        except ForeignKeyViolationError:
            return Response(status_code=status.HTTP_424_FAILED_DEPENDENCY)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


