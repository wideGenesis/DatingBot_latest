from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
    Depends,
    HTTPException,
)
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi.openapi.models import APIKey

from core.api.auth import get_current_username
from core.crud.customer import (
    CustomerService,
    EXCLUDE_FOR_LIST,
    EXCLUDE_FOR_LIST_BY_CITY,
    EXCLUDE_FOR_GET,
    EXCLUDE_FOR_POST,
)
from core.services.api_service import ApiKeyService
from core.tables.models import Customer, Area, RedisChannel

router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
)


@router.post(
    "/create/customer",
    response_model=Customer,
    response_model_exclude=EXCLUDE_FOR_POST,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    customer: Customer, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    """
    {
      "nickname": "string",
      "phone": 0,
      "email": "string",
      "conversation_reference": "bytes",
      "member_id": 0,
      "lang": 0,
      "instagram_link": "string",
      "tiktok_link": "string",
      "is_active": true,
      "post_header": "bytes",
      "passcode": "string",
      "likes": 0,
      "city": {
        "id": 2
      },
      "premium_tier_id": {
        "id": 1,
        "tier": "string"
      },
      "redis_channel_id": {
        "id": 1,
        "redis_channel": "string"
      }
    }
    """
    return await Customer(**customer.__dict__).save()


@router.get(
    "/list",
    response_model=List[Customer],
    response_model_exclude=EXCLUDE_FOR_LIST,
    status_code=status.HTTP_201_CREATED,
)
async def list_customers(
    offset: int, limit: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return (
        await Customer.objects.offset(offset)
        .limit(limit)
        .select_related("premium_tier_id")
        .select_related("redis_channel_id")
        .all()
    )


@router.get(
    "/list-by-city/{city}",
    response_model=List[Customer],
    response_model_exclude=EXCLUDE_FOR_LIST_BY_CITY,
    status_code=status.HTTP_201_CREATED,
)
async def list_by_city(
    offset: int,
    limit: int,
    city: str,
    api_key: APIKey = Depends(ApiKeyService.get_api_key),
):
    city_obj = await Area.objects.get_or_none(city=city.lower())
    if city_obj is None:
        city_obj = await Area.objects.get_or_none(city_en=city.lower())
        if city_obj is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    city_id = city_obj.__dict__
    city_id = city_id["id"]
    return await Customer.objects.offset(offset).limit(limit).filter(city=city_id).all()


@router.get(
    "/list-by-redis_channel/{channel}",
    response_model=List[Customer],
    response_model_exclude=EXCLUDE_FOR_LIST_BY_CITY,
    status_code=status.HTTP_201_CREATED,
)
async def list_by_redis_channel(
    offset: int,
    limit: int,
    redis_channel: str,
    api_key: APIKey = Depends(ApiKeyService.get_api_key),
):
    channel_obj = await RedisChannel.objects.get_or_none(
        redis_channel=redis_channel.lower()
    )
    if channel_obj is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    channel_id = channel_obj.__dict__
    channel_id = channel_id["id"]
    return (
        await Customer.objects.offset(offset)
        .limit(limit)
        .filter(redis_channel_id=channel_id)
        .all()
    )


@router.get(
    "/get-member_id/{member_id}",
    response_model=Customer,
    response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_by_member_id(
    member_id: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    customer = await Customer.objects.get_or_none(member_id=member_id)
    if customer is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return customer


@router.get(
    "/get-phone/{phone}",
    response_model=Customer,
    response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_by_phone(
    phone: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    customer = await Customer.objects.get_or_none(phone=phone)
    if customer is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return customer


@router.get(
    "/get-nickname/{nickname}",
    response_model=Customer,
    response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_by_nickname(
    nickname: str, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    customer = await Customer.objects.get_or_none(nickname=nickname)
    if customer is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return customer


@router.put("/update", response_model=Customer)
async def update_customer(
    customer: Customer, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerService().update(customer)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_member_id(
    member_id: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    customer = await Customer.objects.get_or_none(member_id=member_id)
    if customer is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    try:
        await customer.delete()
    except ForeignKeyViolationError:
        return Response(status_code=status.HTTP_424_FAILED_DEPENDENCY)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
