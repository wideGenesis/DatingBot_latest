from fastapi import HTTPException, status

from core.schemas.customer_profile import CustomerProfileCreate, CustomerProfileUpdate
from core.tables import models
from core.tables.models import Customer


class CustomerProfileService:
    async def create(self, customer_profile: CustomerProfileCreate) -> models.CustomerProfile:
        return await models.CustomerProfile(**customer_profile.dict()).save()

    async def get_by_id(self, _id: int) -> models.CustomerProfile:
        _customer = (
            await models.CustomerProfile.objects.get_or_none(id=_id)
        )
        if not _customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _customer

    async def get_by_customer(self, customer: Customer) -> models.CustomerProfile:
        _customer = (
            await models.CustomerProfile.objects.get_or_none(customer=customer)
        )
        if not _customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _customer

    async def update(self, customer_profile: CustomerProfileUpdate) -> models.CustomerProfile:
        return await models.CustomerProfile(**customer_profile.dict()).update()

    async def delete(self, _id: int) -> models.CustomerProfile.id:
        _customer = await models.CustomerProfile.objects.get(id=_id)
        deleted_id = await _customer.delete()
        return deleted_id

    async def list(self, offset: int, limit: int) -> models.CustomerProfile:
        return await models.CustomerProfile.objects.offset(offset).limit(limit).all()

    async def list_by_hiv(self, offset: int, limit: int, hiv_status: int) -> models.CustomerProfile:
        hiv_status_list = (
            await models.CustomerProfile.objects.offset(offset)
            .limit(limit)
            .filter(hiv_status=hiv_status)
            .all()
        )
        return hiv_status_list
