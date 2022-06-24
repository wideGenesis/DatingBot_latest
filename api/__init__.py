from fastapi import APIRouter
import api.api_router as ap

from api import advertisement, auth, customer, bot, bot_proactive

router = APIRouter()
router.include_router(auth.router)
router.include_router(bot.router)
router.include_router(bot_proactive.router)
router.include_router(customer.router)
router.include_router(advertisement.router)

# CRUDRouter for fastApi
router.include_router(ap.area_router)
router.include_router(ap.redis_channel_router)
router.include_router(ap.customer_router)
router.include_router(ap.advertisement_router)
router.include_router(ap.blacklist_router)

