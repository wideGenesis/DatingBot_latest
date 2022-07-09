from fastapi import APIRouter
import core.api.api_router as ap

from core.api import index, advertisement, bot, auth, bot_proactive, customer_profile
from core.api import customer

router = APIRouter()
router.include_router(auth.router)
router.include_router(customer_profile.router)
router.include_router(customer.router)
router.include_router(advertisement.router)
router.include_router(bot.router)
router.include_router(bot_proactive.router)
# router.include_router(index.index)


# CRUDRouter for fastApi
# router.include_router(ap.area_router)
# router.include_router(ap.redis_channel_router)
# router.include_router(ap.customer_router)
# router.include_router(ap.advertisement_router)
# router.include_router(ap.blacklist_router)
