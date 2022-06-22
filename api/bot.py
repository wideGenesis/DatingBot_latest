from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    status,
)
from typing import Dict

from botbuilder.schema import Activity, ConversationReference
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE, HTTP_201_CREATED

from ms_bot.adapter.standalone_bot_adapter import APP_ID
from ms_bot.bot_init import ADAPTER, BOT


# Create a shared dictionary.  The Bot will add conversation references when users
# join the conversation and send messages.
CONVERSATION_REFERENCES: Dict[str, ConversationReference] = dict()

router = APIRouter(
    prefix='/api',
    tags=['Bot messages exchange'],
)


# Listen for incoming requests on /api/messages
@router.post(
    '/messages',
    response_model=None,
    status_code=status.HTTP_202_ACCEPTED,
)
async def messages(request: Request):
    # print('request>>>', request.headers)
    # print('request>>>', await request.body())

    if "application/json" in request.headers["Content-Type"]:
        body = await request.json()
    else:
        return Response(status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = (
        request.headers["Authorization"] if "Authorization" in request.headers else ""
    )

    try:
        await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        return Response(status_code=HTTP_201_CREATED)
    except Exception as e:
        raise e
