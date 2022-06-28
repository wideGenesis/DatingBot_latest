from fastapi_crudrouter import OrmarCRUDRouter
from core.tables import models
from core.schemas import area

# https://fastapi-crudrouter.awtkns.com/


# router = SQLAlchemyCRUDRouter(
#     schema=models.Area,
#     create_schema=area.BaseArea,
#     db_model=models.Area,
#     db=get_session,
#     prefix='area'
# )
# @router.get('')
# def overloaded_get_all():
#     return 'My overloaded route that returns all the items'
#
# @router.get('/{item_id}')
# def overloaded_get_one():
#     return 'My overloaded route that returns one item'
# Async session and CRUDRouter + override methods "Authorization"

area_router = OrmarCRUDRouter(
    schema=models.Area,
    create_schema=area.BaseArea,
    update_schema=area.BaseArea,
    delete_all_route=False
)
# async def messages(request: Request):
#     # Main bot message handler.
#
#     if "application/json" in request.headers["Content-Type"]:
#         body = await request.json()
#     else:
#         return Response(status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE)
#
#     activity = Activity().deserialize(body)
#     auth_header = (
#         request.headers["Authorization"] if "Authorization" in request.headers else ""
#     )
#
#     try:
redis_channel_router = OrmarCRUDRouter(
    schema=models.RedisChannel,
)
customer_router = OrmarCRUDRouter(
    schema=models.Customer,
)
advertisement_router = OrmarCRUDRouter(
    schema=models.Advertisement,
)
blacklist_router = OrmarCRUDRouter(
    schema=models.Blacklist,
)

