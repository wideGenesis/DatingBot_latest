import json

from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient, UserState
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    PromptValidatorContext
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import ActivityTypes, Activity
from ..bots_models.models import CustomerProfile

from setup.logger import CustomLogger
from ..lib.messages import BOT_MESSAGES

logger = CustomLogger.get_logger('bot')


class RequestPhoneDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),

    ):
        super(RequestPhoneDialog, self).__init__(dialog_id or RequestPhoneDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(TextPrompt(TextPrompt.__name__, RequestPhoneDialog.answer_prompt_validator))
        self.add_dialog(
            WaterfallDialog(
                "RequestPhoneDialog",
                [
                    self.request_phone_step,
                    self.back_to_parent
                ]
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "RequestPhoneDialog"

    async def request_phone_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('request_phone_step %s', RequestPhoneDialog.__name__)

        request_geo = {
            'method': 'sendMessage',
            'parameters': {
                'text': f"{BOT_MESSAGES['phone_request']}",
                'reply_markup': {
                    "one_time_keyboard": True,
                    "resize_keyboard": True,
                    'keyboard': [
                        [
                            {
                                'text': '✅ Підтвердити',
                                'request_contact': True
                            }
                        ]
                    ]
                }
            }
        }

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(request_geo),
                    type=ActivityTypes.message,

                ),
                retry_prompt=MessageFactory.text(BOT_MESSAGES['phone_error']),
            )
        )

    async def back_to_parent(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('back_to_parent from %s', RequestPhoneDialog.__name__)
        result_from_previous_step = step_context.context.activity.channel_data['message']['contact']['phone_number']
        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        user_data.phone = result_from_previous_step.replace('+', '')
        chat_id = f"{step_context.context.activity.channel_data['message']['chat']['id']}"
        message_id_2 = f"{step_context.context.activity.channel_data['message']['message_id']}"

        _activities = []

        try:
            message_id_1 = f"{step_context.context.activity.channel_data['message']['reply_to_message']['message_id']}"

        except KeyError:
            await step_context.context.send_activity(BOT_MESSAGES['contact_not_my_phone'])
            return await step_context.replace_dialog(RequestPhoneDialog.__name__)

        delete_phone_request = {
            'method': 'deleteMessage',
            'parameters': {
                'chat_id': int(chat_id),
                'message_id': int(message_id_1)
            }
        }

        delete_phone = {
            'method': 'deleteMessage',
            'parameters': {
                'chat_id': int(chat_id),
                'message_id': int(message_id_2)
            }
        }

        rm_phone_kb = {
            'method': 'sendMessage',
            'parameters': {
                'text': f"{BOT_MESSAGES['phone_verified']}",
                'reply_markup': {
                    "remove_keyboard": True,
                }
            }
        }

        await step_context.context.send_activities(
            [
                Activity(
                    channel_data=json.dumps(delete_phone_request),
                    type=ActivityTypes.message,
                ),
                Activity(
                    channel_data=json.dumps(delete_phone),
                    type=ActivityTypes.message,
                ),
                Activity(
                    channel_data=json.dumps(rm_phone_kb),
                    type=ActivityTypes.message,
                ),
            ]
        )

        return await step_context.end_dialog()

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _contact = prompt_context.context.activity.channel_data['message'].get('contact')
        _phone = _contact.get('phone_number').replace('+', '')
        if _contact is not None and len(_phone) == 12:
            condition = True
        else:
            condition = False

        return condition
