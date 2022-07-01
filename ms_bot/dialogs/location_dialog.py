import json

from botbuilder.core import (
    MessageFactory,
    BotTelemetryClient,
    NullTelemetryClient,
    UserState,
)
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    PromptValidatorContext,
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import ActivityTypes, Activity
from ms_bot.bots_models.models import CustomerProfile

from settings.logger import CustomLogger
from helpers.copyright import BOT_MESSAGES, REQUEST_GEO
from ms_bot.bot_helpers.telegram_helper import reverse_geocode

logger = CustomLogger.get_logger("bot")


class RequestLocationDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(RequestLocationDialog, self).__init__(
            dialog_id or RequestLocationDialog.__name__
        )
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            TextPrompt(
                TextPrompt.__name__, RequestLocationDialog.answer_prompt_validator
            )
        )
        self.add_dialog(
            WaterfallDialog(
                "RequestLocationDialog",
                [self.request_location_step, self.back_to_parent],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "RequestLocationDialog"

    async def request_location_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("request_location_step %s", RequestLocationDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(REQUEST_GEO),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(BOT_MESSAGES["location_error"]),
            ),
        )

    async def back_to_parent(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("back_to_parent from %s", RequestLocationDialog.__name__)
        result_from_previous_step = step_context.context.activity.channel_data[
            "message"
        ]["location"]
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        # {'latitude': 46.412231, 'longitude': 30.74354}
        lat = result_from_previous_step.get("latitude")
        long = result_from_previous_step.get("longitude")
        _loc = f"{lat}:{long}"
        user_data.location = _loc
        user_data.is_active = 1

        area = await reverse_geocode(_loc)
        user_data.area_id = f"{area[2]}:{area[1]}:{area[0]}".lower()

        chat_id = (
            f"{step_context.context.activity.channel_data['message']['chat']['id']}"
        )
        message_id_2 = (
            f"{step_context.context.activity.channel_data['message']['message_id']}"
        )

        _activities = []

        try:
            message_id_1 = f"{step_context.context.activity.channel_data['message']['reply_to_message']['message_id']}"
            delete_geo_request = {
                "method": "deleteMessage",
                "parameters": {
                    "chat_id": int(chat_id),
                    "message_id": int(message_id_1),
                },
            }
            _activities.append(
                Activity(
                    channel_data=json.dumps(delete_geo_request),
                    type=ActivityTypes.message,
                )
            )
        except KeyError:
            pass

        delete_geo = {
            "method": "deleteMessage",
            "parameters": {"chat_id": int(chat_id), "message_id": int(message_id_2)},
        }
        _activities.append(
            Activity(
                channel_data=json.dumps(delete_geo),
                type=ActivityTypes.message,
            )
        )
        rm_geo_kb = {
            "method": "sendMessage",
            "parameters": {
                "text": f"{BOT_MESSAGES['location_verified']}",
                "reply_markup": {
                    "remove_keyboard": True,
                },
            },
        }
        _activities.append(
            Activity(
                channel_data=json.dumps(rm_geo_kb),
                type=ActivityTypes.message,
            )
        )

        await step_context.context.send_activities(_activities)

        return await step_context.end_dialog()

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:

        _location = prompt_context.context.activity.channel_data["message"].get(
            "location"
        )
        if _location is not None:
            condition = True
        else:
            condition = False

        return condition
