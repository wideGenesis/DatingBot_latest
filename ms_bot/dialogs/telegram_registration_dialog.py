import pickle

from asyncpg import UniqueViolationError
from botbuilder.core import (
    MessageFactory,
    UserState,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    PromptValidatorContext,
    NumberPrompt,
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import Activity, ActivityTypes
import json

from helpers.constants import remove_last_message, remove_last_dropped_message
from ms_bot.bot_helpers.telegram_helper import rm_tg_message
from settings.logger import CustomLogger
from helpers.copyright import CHOOSE_LANG, CHOOSE_SEX_KB, MY_AGE_KB, BOT_MESSAGES

from ms_bot.bots_models.models import CustomerProfile
from ms_bot.dialogs.location_dialog import RequestLocationDialog
from ms_bot.dialogs.phone_dialog import RequestPhoneDialog
from ms_bot.dialogs.upload_dialog import UploadDialog
from core.tables.models import Customer, PremiumTier

logger = CustomLogger.get_logger("bot")


class TelegramRegistrationDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(TelegramRegistrationDialog, self).__init__(
            dialog_id or TelegramRegistrationDialog.__name__
        )

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(RequestPhoneDialog(user_state, RequestPhoneDialog.__name__))
        self.add_dialog(
            RequestLocationDialog(user_state, RequestLocationDialog.__name__)
        )
        self.add_dialog(UploadDialog(user_state, UploadDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            TextPrompt(
                TextPrompt.__name__, TelegramRegistrationDialog.answer_prompt_validator
            )
        )
        self.add_dialog(
            NumberPrompt(
                NumberPrompt.__name__, TelegramRegistrationDialog.age_prompt_validator
            )
        )

        self.add_dialog(
            WaterfallDialog(
                "TelegramRegistrationDialog",
                [
                    self.choose_lang_step,
                    self.member_step,
                    self.choose_sex_step,
                    self.age_step,
                    self.request_phone_step,
                    self.save_new_customer,
                    self.upload_media_step,
                    self.back_to_parent,
                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "TelegramRegistrationDialog"

    async def choose_lang_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("choose_lang_step %s", TelegramRegistrationDialog.__name__)

        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(CHOOSE_LANG),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def member_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("member_step %s", TelegramRegistrationDialog.__name__)
        await remove_last_message(step_context, True)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        lang = str(step_context.result).split(":")
        member_id = int(step_context.context.activity.from_property.id)
        conversation_reference = pickle.dumps(
            step_context.context.get_conversation_reference(
                step_context.context.activity
            )
        )

        nickname = step_context.context.activity.channel_data["callback_query"][
            "from"
        ].get("username")

        user_data.nickname = nickname
        user_data.premium_tier = 0
        user_data.conversation_reference = conversation_reference
        user_data.member_id = member_id
        user_data.lang = lang[1]
        user_data.is_active = 1
        return await step_context.next([])

    async def choose_sex_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("choose_sex_step %s", TelegramRegistrationDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(CHOOSE_SEX_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['reprompt']}"),
            ),
        )

    async def age_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("age_step %s", TelegramRegistrationDialog.__name__)
        await remove_last_message(step_context, True)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        result_from_previous_step = str(step_context.result).split(":")
        user_data.self_sex = result_from_previous_step[1]

        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(MY_AGE_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['age_reprompt']}"),
            ),
        )

    async def request_phone_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("request_phone_step %s", TelegramRegistrationDialog.__name__)
        chat_id = (
            f"{step_context.context.activity.channel_data['message']['chat']['id']}"
        )
        message_id = (
            f"{step_context.context.activity.channel_data['message']['message_id']}"
        )
        await rm_tg_message(step_context.context, chat_id, message_id)

        try:
            message_id_1 = f"{step_context.context.activity.channel_data['message']['reply_to_message']['message_id']}"
            await rm_tg_message(step_context.context, chat_id, message_id_1)
        except Exception:
            logger.debug("Customer drop reply and make direct answer")

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        user_data.age = step_context.result

        return await step_context.begin_dialog(RequestPhoneDialog.__name__)

    async def save_new_customer(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("save_new_customer %s", TelegramRegistrationDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        try:
            await self._save_customer(
                user_data,
            )
            logger.info(
                "save_customer_to_db for %s was successful", user_data.member_id
            )
        except Exception:
            logger.exception(
                "save_customer_to_db for %s was unsuccessful", user_data.member_id
            )
            await step_context.context.send_activity("exceptions_occurs")
            return await step_context.replace_dialog(
                TelegramRegistrationDialog.__name__
            )

        return await step_context.next([])

    async def upload_media_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("upload_media_step %s", TelegramRegistrationDialog.__name__)
        return await step_context.begin_dialog(UploadDialog.__name__)

    async def back_to_parent(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug(f"back_to_main from %s", TelegramRegistrationDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        return await step_context.end_dialog(user_data)

    @staticmethod
    async def age_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text
        _value = _value.strip()
        _value = _value.split("-")

        if len(_value) == 2:
            condition = 18 <= int(_value[0]) <= 69 and 18 <= int(_value[1]) <= 69

        elif len(_value) == 1:
            condition = 18 <= int(_value[0]) <= 69
        else:
            condition = False
        return prompt_context.recognized.succeeded and condition

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:en",
            "KEY_CALLBACK:ua",
            "KEY_CALLBACK:es",
            "KEY_CALLBACK:ru",
            "KEY_CALLBACK:0",
            "KEY_CALLBACK:1",
            "KEY_CALLBACK:Man",
            "KEY_CALLBACK:Woman",
        ]:
            condition = True
        else:
            condition = False
        return prompt_context.recognized.succeeded and condition

    @classmethod
    async def _save_customer(cls, user_data):
        try:
            premium_tier_id = await PremiumTier.objects.get_or_none(tier="free")
            premium_tier_id = premium_tier_id.__dict__
            premium_tier_id = premium_tier_id["id"]
        except Exception as e:
            raise Exception("Something went wrong! %s" % e)

        customer = Customer(
            nickname=user_data.nickname,
            phone=int(user_data.phone),
            premium_tier_id=premium_tier_id,
            conversation_reference=user_data.conversation_reference,
            member_id=int(user_data.member_id),
            lang=user_data.lang,
            self_sex=int(user_data.self_sex),
            age=int(user_data.age),
            is_active=int(user_data.is_active),
        )
        try:
            await customer.save()
        except UniqueViolationError:
            await Customer.objects.filter(member_id=int(user_data.member_id)).update(
                nickname=user_data.nickname,
                phone=int(user_data.phone),
                premium_tier_id=premium_tier_id,
                conversation_reference=user_data.conversation_reference,
                member_id=int(user_data.member_id),
                lang=int(user_data.lang),
                self_sex=int(user_data.self_sex),
                age=int(user_data.age),
                is_active=int(user_data.is_active),
            )
        except Exception:
            logger.exception("Save customer to db error %s", user_data.member_id)

        return
