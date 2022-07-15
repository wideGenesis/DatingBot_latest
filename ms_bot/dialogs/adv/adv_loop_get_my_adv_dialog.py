import datetime

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

from core.tables.models import Advertisement, Customer
from helpers.constants import remove_last_message
from settings.logger import CustomLogger
from helpers.copyright import (
    BOT_MESSAGES,
    send_my_adv_kb,
)

from ms_bot.bots_models.models import CustomerProfile

logger = CustomLogger.get_logger("bot")


class GetMyAdvLoopDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(GetMyAdvLoopDialog, self).__init__(dialog_id or GetMyAdvLoopDialog.__name__)

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            TextPrompt(TextPrompt.__name__, GetMyAdvLoopDialog.answer_prompt_validator)
        )
        self.add_dialog(
            WaterfallDialog(
                "GetMyAdvLoopDialog",
                [

                    self.get_first_adv_step,
                    self.parse_first_choice_step,
                    self.get_second_adv_step,
                    self.parse_second_choice_step,
                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "GetMyAdvLoopDialog"
        self.advs = None
        self.adv_number = None
        self.adv_id = None

    async def get_first_adv_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("get_first_adv_step %s", GetMyAdvLoopDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        threshold = (datetime.datetime.now() + datetime.timedelta(days=7))
        my_advs = await Advertisement.objects.filter(
            customer=user_data.pk).exclude(
            is_published=False).select_related(
            'redis_channel'
        ).order_by(
            Advertisement.created_at.desc()).all()
        if len(my_advs) == 0:
            await step_context.context.send_activity(BOT_MESSAGES['no_adv'])
            return await step_context.end_dialog()

        self.advs = my_advs[:2]
        self.adv_number = 0
        adv = self.advs[self.adv_number]
        self.adv_id = adv.id
        text = await self.text_formatter(adv)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(send_my_adv_kb(text)),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['age_reprompt']}"),
            ),
        )

    async def parse_first_choice_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_first_choice_step %s", GetMyAdvLoopDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        found_choice = str(step_context.result).split(':')
        found_choice = found_choice[1]

        if found_choice == 'adv_rm':
            await Advertisement.objects.filter(id=self.adv_id).update(is_published=False)
            return await step_context.next("continue")
        elif found_choice == 'adv_next':
            return await step_context.next("continue")

        elif found_choice == 'menu':
            return await step_context.end_dialog()

        else:
            pass

    async def get_second_adv_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("get_second_adv_step %s", GetMyAdvLoopDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')
        if len(self.advs) == 0:
            await step_context.context.send_activity(BOT_MESSAGES['no_adv'])
            return await step_context.end_dialog()

        self.adv_number = 1
        try:
            adv = self.advs[self.adv_number]
        except IndexError:
            adv = None
        if adv is None:
            await step_context.context.send_activity(BOT_MESSAGES['no_adv'])
            return await step_context.end_dialog()

        self.adv_id = adv.id
        text = await self.text_formatter(adv)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(send_my_adv_kb(text)),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['age_reprompt']}"),
            ),
        )

    async def parse_second_choice_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_second_choice_step %s", GetMyAdvLoopDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        found_choice = str(step_context.result).split(':')
        found_choice = found_choice[1]

        if found_choice == 'adv_rm':
            await Advertisement.objects.filter(id=self.adv_id).update(is_published=False)
            return await step_context.next("continue")

        elif found_choice == 'adv_next':
            return await step_context.end_dialog()

        elif found_choice == 'menu':
            return await step_context.end_dialog()

        else:
            pass

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:adv_rm",
            "KEY_CALLBACK:adv_next",
            "KEY_CALLBACK:menu",
        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition

    @classmethod
    async def text_formatter(cls, adv: Advertisement) -> str:
        return f'Я шукаю: {adv.who_for_whom} \n' \
                         f'Вік: {adv.prefer_age} \n' \
                         f'Місце: {adv.has_place} \n' \
                         f'Час зустрічі: {adv.dating_time} \n' \
                         f'День зустрічі: {adv.dating_day} \n' \
                         f'Текст оголошення: {adv.adv_text} \n' \
                         f'Цілі: {adv.goals} \n' \
                         f'Телефон: {adv.phone_is_hidden} \n' \
                         f'Телеграм: {adv.tg_nickname_is_hidden} \n' \
                         f'Активно до: {adv.valid_until_date} \n' \
                         f'Місто пошуку: {adv.redis_channel.city}'



