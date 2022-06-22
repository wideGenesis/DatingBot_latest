from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    status,
)
from typing import Dict

from botbuilder.schema import Activity, ConversationReference
from starlette.status import HTTP_201_CREATED

from ms_bot.adapter.standalone_bot_adapter import APP_ID
from ms_bot.bot_init import ADAPTER


# Create a shared dictionary.  The Bot will add conversation references when users
# join the conversation and send messages.
CONVERSATION_REFERENCES: Dict[str, ConversationReference] = dict()

router = APIRouter(
    prefix='/api',
    tags=['Bot notification exchange'],
)


# Listen for incoming requests on /api/messages
@router.post(
    '/notify',
    response_model=None,
    status_code=status.HTTP_202_ACCEPTED,
)
# Listen for requests on /api/notify, and send a messages to all conversation members.
async def notify(req: Request) -> Response:  # pylint: disable=unused-argument
    await _send_proactive_message()
    return Response(status_code=HTTP_201_CREATED)


async def _send_proactive_message():
    for conversation_reference in CONVERSATION_REFERENCES.values():
        try:
            await ADAPTER.continue_conversation(
                conversation_reference,
                lambda turn_context: turn_context.send_activity("proactive hello"),
                APP_ID,
            )
            return Response(status_code=HTTP_201_CREATED)
        except Exception as e:
            raise e
