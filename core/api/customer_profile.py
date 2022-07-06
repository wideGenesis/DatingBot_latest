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

# from core.api.auth import get_current_username
# from core.crud.customer import (
#     CustomerService,
#     EXCLUDE_FOR_LIST,
#     EXCLUDE_FOR_LIST_BY_CITY,
#     EXCLUDE_FOR_GET,
#     EXCLUDE_FOR_POST,
# )
from core.services.api_service import ApiKeyService
from core.tables.models import CustomerProfile, Customer

router = APIRouter(
    prefix="/customer-profile",
    tags=["Customer Profile"],
)


@router.post(
    "/create/customer-profile",
    response_model=CustomerProfile,
    # response_model_exclude=EXCLUDE_FOR_POST,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_profile(
        customer_profile: CustomerProfile, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerProfile(**customer_profile.__dict__).save()


@router.get(
    "/list",
    response_model=List[CustomerProfile],
    # response_model_exclude=EXCLUDE_FOR_LIST,
    status_code=status.HTTP_201_CREATED,
)
async def list_customer_profiles(
        offset: int, limit: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    profiles = (
        await CustomerProfile.objects.offset(offset)
        .limit(limit)
        .all()
    )
    if not profiles:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return profiles


@router.get(
    "/list-by-hiv/{hiv-status}",
    response_model=List[CustomerProfile],
    # response_model_exclude=EXCLUDE_FOR_LIST_BY_CITY,
    status_code=status.HTTP_201_CREATED,
)
async def list_profiles_by_hiv_status(
        offset: int,
        limit: int,
        hiv_status: str,
        api_key: APIKey = Depends(ApiKeyService.get_api_key),
):
    customer_hiv_status = await CustomerProfile.objects.offset(offset).limit(limit).filter(hiv_status=hiv_status).all()
    if not customer_hiv_status:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return customer_hiv_status


@router.get(
    "/get-id/{id}",
    response_model=CustomerProfile,
    # response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_profile_by_id(
        _id: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    profile = await CustomerProfile.objects.get_or_none(id=_id)
    if not profile:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return profile


@router.get(
    "/get-customer/{customer-id}",
    response_model=CustomerProfile,
    # response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_profile_by_customer_id(
        customer: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    profile = await CustomerProfile.objects.get_or_none(customer=customer)
    if not profile:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return profile


@router.get(
    "/get-customer/{customer-member-id}",
    response_model=CustomerProfile,
    # response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_by_profile_by__member_id(
        member_id: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    customer = await Customer.objects.get_or_none(member_id=member_id)
    if not customer:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    profile = await CustomerProfile.objects.get_or_none(customer=customer.id)
    if not profile:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return profile


@router.put("/update", response_model=CustomerProfile)
async def update_customer_profile(
        profile: CustomerProfile, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerProfile().update(**profile.__dict__)
    # return await CustomerService().update(profile)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_member_id(
        _id: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    profile = await CustomerProfile.objects.get_or_none(id=_id)
    if not profile:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    try:
        await profile.delete()
    except ForeignKeyViolationError:
        return Response(status_code=status.HTTP_424_FAILED_DEPENDENCY)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
