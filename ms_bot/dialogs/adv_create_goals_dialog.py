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

# from profanity_filter import ProfanityFilter

from settings.logger import CustomLogger
from helpers.copyright import (
    LOOKING_FOR_KB,
    all_in_one_buttons,
    sex_buttons,
    relationships_buttons,
    friends_buttons,
    goals_kb,
)

from ms_bot.bots_models.models import CustomerProfile
from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class CreateAdvGoalsDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(CreateAdvGoalsDialog, self).__init__(
            dialog_id or CreateAdvGoalsDialog.__name__
        )

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            TextPrompt(
                TextPrompt.__name__, CreateAdvGoalsDialog.answer_prompt_validator
            )
        )
        self.add_dialog(
            NumberPrompt(
                NumberPrompt.__name__, CreateAdvGoalsDialog.age_prompt_validator
            )
        )

        self.add_dialog(
            WaterfallDialog(
                "CreateAdvGoalsDialog",
                [
                    self.looking_for_step,
                    self.goals_type_step,
                    # self.member_step,
                    # self.request_phone_step,
                    # self.request_location_step,
                    # self.save_new_customer,
                    # self.upload_media_step,
                    # self.back_to_parent
                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "CreateAdvGoalsDialog"
        self.goals_type = None

    # area_id
    # text
    # has_place
    # dating_time
    # dating_day
    # file_attachment_1
    # file_attachment_2
    # goals_1 - goals_8

    async def looking_for_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("looking_for_step %s", CreateAdvGoalsDialog.__name__)

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
        result_from_previous_step = str(step_context.context.activity.text)
        result_from_previous_step = result_from_previous_step.strip()
        result_from_previous_step = result_from_previous_step.split("-")
        _result_from_previous_step = (
            str(result_from_previous_step[0]).strip()
            + str(result_from_previous_step[1]).strip()
        )
        result_from_previous_step = _result_from_previous_step.strip()

        user_data.prefer_age = result_from_previous_step

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(LOOKING_FOR_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Зробіть вибір, натиснувши на відповідну кнопку вище"
                ),
            ),
        )

    async def goals_type_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("goals_type_step %s", CreateAdvGoalsDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        result_from_previous_step = str(step_context.result).split(":")
        self.goals_type = result_from_previous_step[1]
        user_data.temp = result_from_previous_step[1]

        if self.goals_type == "relationships":
            buttons = relationships_buttons
        elif self.goals_type == "sex_fun":
            buttons = sex_buttons
        elif self.goals_type == "talking_friends":
            buttons = friends_buttons
        elif self.goals_type == "all_in_one":
            buttons = all_in_one_buttons
        else:
            return await step_context.cancel_all_dialogs(True)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(goals_kb(buttons, None)),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Зробіть вибір, натиснувши на відповідну кнопку вище"
                ),
            ),
        )

    async def back_to_parent(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug(f"back_to_main from %s", CreateAdvGoalsDialog.__name__)

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
        # await prompt_context.context.delete_activity(prompt_context.context.activity.id)

        return prompt_context.recognized.succeeded and condition

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:profile_region",
            "KEY_CALLBACK:find_region",
            "KEY_CALLBACK:Man",
            "KEY_CALLBACK:Woman",
            "KEY_CALLBACK:Both",
            "KEY_CALLBACK:Other to Other",
            "KEY_CALLBACK:relationships",
            "KEY_CALLBACK:sex_fun",
            "KEY_CALLBACK:talking_friends",
            "KEY_CALLBACK:all_in_one",
            "KEY_CALLBACK:4",
            "KEY_CALLBACK5",
            "KEY_CALLBACK:6",
            "KEY_CALLBACK:7",
            "KEY_CALLBACK:8",
            "KEY_CALLBACK:9",
            "KEY_CALLBACK:10",
            "KEY_CALLBACK:11",
            "KEY_CALLBACK:12",
            "KEY_CALLBACK:13",
            "KEY_CALLBACK:14",
            "KEY_CALLBACK:15",
            "KEY_CALLBACK:16",
            "KEY_CALLBACK:17",
            "KEY_CALLBACK:ready"
            "KEY_CALLBACK:family"
            "KEY_CALLBACK:relationships"
            "KEY_CALLBACK:dating"
            "KEY_CALLBACK:children",
        ]:
            condition = True
        else:
            condition = False
        # await prompt_context.context.delete_activity(prompt_context.context.activity.id)

        return prompt_context.recognized.succeeded and condition

    # @classmethod
    # async def _profanity_filter(cls, text: str) -> str:
    #     pf = ProfanityFilter(languages=['ru', 'en'])
    #     # pf.extra_profane_word_dictionaries = {'en': {'chocolate', 'orange'}}
    #
    #     return pf.censor(text)

    # @staticmethod
    # async def yield_goals_kb(
    #         step_context: WaterfallStepContext, user_data: CustomerProfile, step=None
    # ) -> DialogTurnResult:
    #
    #     return await step_context.prompt(
    #         TextPrompt.__name__, PromptOptions(
    #             prompt=Activity(
    #                 channel_data=json.dumps(SEND_MEDIA_KB),
    #                 type=ActivityTypes.message,
    #             ),
    #             retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
    #         )
    #     )
