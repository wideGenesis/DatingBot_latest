from typing import Union

from asyncpg import ForeignKeyViolationError
from fastapi import status, Response

from core.tables import models
from core.tables.models import Customer
from settings.logger import CustomLogger

logger = CustomLogger.get_logger("bot")


class CustomerService:
    async def create(
            self,
            customer: Customer
    ) -> Union[models.Customer, Response]:
        try:
            return await models.Customer(**customer.dict()).save()
        except Exception:
            logger.exception('Something went wrong!')
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def list(
            self,
            offset: int,
            limit: int
    ) -> Union[models.Customer, Response]:
        customers = (
            await models.Customer.objects.offset(offset).limit(limit).all()
        )
        if not customers:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return customers

    async def list_by_city(
            self,
            offset: int,
            limit: int,
            city_id: int
    ) -> Union[models.Customer, Response]:
        customer_city_list = (
            await models.Customer.objects.offset(offset)
            .limit(limit)
            .filter(city=city_id)
            .all()
        )
        if not customer_city_list:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return customer_city_list

    async def get_by_id(
            self,
            _id: int
    ) -> Union[models.CustomerProfile, Response]:
        customer = await models.Customer.objects.get_or_none(id=_id)
        if not customer:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return customer

    async def get_by_member_id(
            self,
            member_id: int
    ) -> Union[models.Customer, Response]:
        customer = await models.Customer.objects.get_or_none(member_id=member_id)

        if not customer:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return customer

    async def get_by_phone(
            self,
            phone: int
    ) -> Union[models.Customer, Response]:
        customer = await models.Customer.objects.get_or_none(phone=phone)

        if not customer:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return customer

    async def get_by_nickname(
        self,
        nickname: str
    ) -> Union[models.Customer, Response]:
        customer = await models.Customer.objects.get_or_none(nickname=nickname)
        if not customer:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return customer

    async def update(
            self,
            customer: Customer
    ) -> models.Customer:
        intersection = {}
        update_customer = customer.dict()

        for k, v in update_customer.items():
            if v is None:
                continue
            intersection[k] = v

        return await models.Customer.objects.update_or_create(**intersection)

    async def delete(
            self,
            _id: int
    ) -> models.Customer.id:
        customer = await models.Customer.objects.get_or_none(id=_id)

        if not customer:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        try:
            await customer.delete()

        except ForeignKeyViolationError:
            return Response(status_code=status.HTTP_424_FAILED_DEPENDENCY)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


EXCLUDE_FOR_LIST = {
    "id",
    "phone",
    "conversation_reference",
    "post_header",
    "passcode",
    "gps_coordinates",
    "rel_redis_channel_from_adv",
    "rel_sender_id",
    "rel_publisher",
    "rel_sender_avatar",
    "rel_recipient_id",
    "rel_customer_from_usermediafile",
    "rel_customer_from_sex_profile",
    "rel_customer_from_blacklist",
    "city",
    "rel_customer_from_common_profile",
    "rel_recipient_avatar",
}

EXCLUDE_FOR_LIST_BY_CITY = {
    "id",
    "phone",
    "conversation_reference",
    "post_header",
    "passcode",
    "gps_coordinates",
    "rel_redis_channel_from_adv",
    "rel_sender_id",
    "rel_publisher",
    "rel_sender_avatar",
    "rel_recipient_id",
    "rel_customer_from_usermediafile",
    "rel_customer_from_sex_profile",
    "rel_customer_from_blacklist",
    "rel_customer_from_common_profile",
    "rel_recipient_avatar",
    "city",
    "rel_area_id",
    "rel_city",
    "rel_large_city_near_id",
    "rel_gps_coordinates",
}

EXCLUDE_FOR_GET = {
    "id",
    "phone",
    "conversation_reference",
    "post_header",
    "passcode",
    "gps_coordinates",
    "rel_recipient_avatar",
    "rel_sender_avatar",
    "rel_customer_from_usermediafile",
    "rel_customer_from_sex_profile",
    "rel_sender_id",
    "rel_recipient_id",
    "rel_customer_from_blacklist",
    "rel_customer_from_common_profile",
    "rel_publisher",
}

EXCLUDE_FOR_POST = {
    "id",
    "gps_coordinates",
    "rel_recipient_avatar",
    "rel_sender_avatar",
    "rel_customer_from_usermediafile",
    "rel_customer_from_sex_profile",
    "rel_sender_id",
    "rel_recipient_id",
    "rel_customer_from_blacklist",
    "rel_customer_from_common_profile",
    "rel_publisher",
}
