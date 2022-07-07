from typing import List

from fastapi import (
    APIRouter,
    status,
    Depends,
)
from fastapi.openapi.models import APIKey
from core.crud.customer_profile import CustomerProfileService
from core.services.api_service import ApiKeyService
from core.tables.models import CustomerProfile

router = APIRouter(
    prefix="/customer-profile",
    tags=["Customer Profile"],
)


@router.post(
    "/create/customer-profile/",
    response_model=CustomerProfile,
    response_model_exclude={"id", "created_at", "updated_at", "nickname"},
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_profile(
    customer_profile: CustomerProfile,
    api_key: APIKey = Depends(ApiKeyService.get_api_key),
):
    return await CustomerProfileService().create(customer_profile)


@router.get(
    "/list/",
    response_model=List[CustomerProfile],
    response_model_exclude={"id", "created_at", "updated_at", "customer"},
    status_code=status.HTTP_201_CREATED,
)
async def list_profiles(
        offset: int,
        limit: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerProfileService().list(offset, limit)


@router.get(
    "/list-by/{hiv-status}",
    response_model=List[CustomerProfile],
    status_code=status.HTTP_201_CREATED,
)
async def list_profiles_by_hiv_status(
    offset: int,
    limit: int,
    hiv_status: str,
    api_key: APIKey = Depends(ApiKeyService.get_api_key),
):
    return await CustomerProfileService().list_by_hiv_status(offset, limit, hiv_status)


@router.get(
    "/get-profile-by/{id}",
    response_model=CustomerProfile,
    status_code=status.HTTP_201_CREATED,
)
async def get_profile_by_id(
        _id: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerProfileService().get_by_id(_id)


@router.get(
    "/get-profile-by-member/{id}",
    response_model=CustomerProfile,
    status_code=status.HTTP_201_CREATED,
)
async def get_by_member_id(
        member_id: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerProfileService().get_by_member_id(member_id)


@router.put(
    "/update/",
    response_model=CustomerProfile,
    status_code=status.HTTP_201_CREATED,
)
async def update_profile(
        profile: CustomerProfile,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerProfileService().update(profile)


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_id(
        _id: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerProfileService().delete(_id)
