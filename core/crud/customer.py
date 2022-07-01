from fastapi import HTTPException, status

from core.schemas.customer import CustomerCreate, CustomerUpdate
from core.tables import models


class CustomerService:

    async def create(self, customer: CustomerCreate) -> models.Customer:
        return await models.Customer(**customer.dict()).save()

    async def get_by_member_id(self, member_id: int) -> models.Customer:
        _customer = await models.Customer.objects.select_related(
            'premium_tier_id').select_related(
            'redis_channel_id').get_or_none(member_id=member_id)
        if not _customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _customer

    async def get_by_phone(self, phone: int) -> models.Customer:
        _customer = await models.Customer.objects.select_related(
            'premium_tier_id').select_related(
            'redis_channel_id').get_or_none(phone=phone)
        if not _customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _customer

    async def get_by_nickname(self, nickname: str) -> models.Customer:
        _customer = await models.Customer.objects.select_related(
            'premium_tier_id').select_related(
            'redis_channel_id').get_or_none(nickname=nickname)
        if not _customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _customer

    async def update(self, customer: CustomerUpdate) -> models.Customer:
        return await models.Customer(**customer.dict()).update()

    async def delete(self, member_id: int) -> models.Customer.id:
        _customer = await models.Customer.objects.get(member_id=member_id)
        deleted_id = await _customer.delete()
        return deleted_id

    async def list(self, offset: int, limit: int) -> models.Customer:
        return await models.Customer.objects.offset(offset).limit(limit).select_related(
            'premium_tier_id').select_related(
            'redis_channel_id').all()

    async def list_by_city(self, offset: int, limit: int, city: str) -> models.Customer:
        city_list = await models.Area.objects.offset(offset).limit(limit).filter(city=city).all()
        print('city_list', city_list)
        return city_list


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
    "rel_recipient_avatar"}

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
    "rel_gps_coordinates"
}

EXCLUDE_FOR_MEMBER_ID = {
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
    "rel_publisher"
}
