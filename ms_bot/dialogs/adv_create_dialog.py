import datetime
import pickle

from asyncpg import UniqueViolationError
from botbuilder.core import MessageFactory, UserState, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog, \
    PromptValidatorContext, NumberPrompt

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import Activity, ActivityTypes
import json

# from profanity_filter import ProfanityFilter
from sqlalchemy.exc import IntegrityError

from core.tables.models import Area, Customer, PremiumTier
from settings.logger import CustomLogger
from helpers.copyright import BOT_MESSAGES, CHOOSE_SEX_KB, LOOKING_FOR_SEX_KB, PREFER_AGE_KB, \
    CREATE_AREA_KB

from ms_bot.bots_models.models import CustomerProfile
from ms_bot.dialogs.adv_create_goals_dialog import CreateAdvGoalsDialog
from ms_bot.dialogs.location_dialog import RequestLocationDialog
from ms_bot.dialogs.phone_dialog import RequestPhoneDialog
from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger('bot')


class CreateAdvDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(CreateAdvDialog, self).__init__(dialog_id or CreateAdvDialog.__name__)

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(RequestPhoneDialog(user_state, RequestPhoneDialog.__name__))
        self.add_dialog(RequestLocationDialog(user_state, RequestLocationDialog.__name__))
        self.add_dialog(CreateAdvGoalsDialog(user_state, CreateAdvGoalsDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(TextPrompt(TextPrompt.__name__, CreateAdvDialog.answer_prompt_validator))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__, CreateAdvDialog.age_prompt_validator))

        self.add_dialog(
            WaterfallDialog(
                "CreateAdvDialog",
                [
                    self.gender_step,
                    self.looking_gender_step,
                    self.prefer_age_step,
                    self.goals_routing,
                    self.area_step,
                    self.parse_area_choice_step,

                    # self.member_step,
                    # self.request_phone_step,
                    # self.request_location_step,
                    # self.save_new_customer,
                    # self.upload_media_step,
                    # self.back_to_parent
                ]
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "CreateAdvDialog"

    async def gender_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('gender_step %s', CreateAdvDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(CHOOSE_SEX_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
            )
        )

    async def looking_gender_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('looking_gender_step %s', CreateAdvDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        result_from_previous_step = str(step_context.result).split(':')
        user_data.temp = result_from_previous_step[1]

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(LOOKING_FOR_SEX_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
            )
        )


    async def prefer_age_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('prefer_age_step %s', CreateAdvDialog.__name__)

        chat_id = f"{step_context.context.activity.channel_data['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        try:
            message_id_1 = f"{step_context.context.activity.channel_data['message']['reply_to_message']['message_id']}"
            await rm_tg_message(step_context.context, chat_id, message_id_1)
        except Exception:
            logger.debug('Customer drop reply and make direct answer')

        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        result_from_previous_step = step_context.result
        user_data.age = result_from_previous_step

        return await step_context.prompt(
            NumberPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(PREFER_AGE_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['age_reprompt']}"),
            )
        )

    async def goals_routing(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('goals_routing %s', CreateAdvDialog.__name__)
        return await step_context.begin_dialog(CreateAdvGoalsDialog.__name__)

    async def area_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('area_step %s', CreateAdvDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(CREATE_AREA_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
            )
        )

    async def parse_area_choice_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('parse_area_choice_step %s', CreateAdvDialog.__name__)

        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        result_from_previous_step = str(step_context.result).split(':')
        result_from_previous_step = result_from_previous_step[1]

        if result_from_previous_step == 'profile_region':
            return await step_context.next([])
        elif result_from_previous_step == 'find_region':
            return await step_context.begin_dialog(RequestLocationDialog.__name__)
        else:
            return await step_context.replace_dialog(CreateAdvDialog.__name__)

    async def member_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('member_step %s', CreateAdvDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        result_from_previous_step = str(step_context.result).split(':')

        member_id = int(step_context.context.activity.from_property.id)
        conversation_reference = pickle.dumps(
            step_context.context.get_conversation_reference(step_context.context.activity)
        )

        user_data.looking_for = result_from_previous_step[1]
        user_data.member_id = member_id
        user_data.conversation_reference = conversation_reference
        user_data.updated_at = datetime.datetime.utcnow()
        user_data.last_seen = user_data.updated_at
        user_data.channel_id = 0
        user_data.premium_tier = 0

        return await step_context.next([])

    async def request_location_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('request_location_step %s', RequestLocationDialog.__name__)
        return await step_context.begin_dialog(RequestLocationDialog.__name__)

    async def save_new_customer(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('save_new_customer %s', CreateAdvDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        try:
            area = await self._save_area(
                user_data,
            )
            logger.info('_save_area for %s was successful', user_data.member_id)
        except Exception:
            logger.exception('_save_area for %s was Unsuccessful', user_data.member_id)
            await step_context.context.send_activity('exceptions_occurs')
            return await step_context.replace_dialog(CreateAdvDialog.__name__)

        try:
            await self._save_customer(
                user_data,
                area
            )
            logger.info('save_customer_to_db for %s was successful', user_data.member_id)
        except Exception:
            logger.exception('save_customer_to_db for %s was unsuccessful', user_data.member_id)
            await step_context.context.send_activity('exceptions_occurs')
            return await step_context.replace_dialog(CreateAdvDialog.__name__)

        return await step_context.next([])

    async def back_to_parent(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug(f'back_to_main from %s', CreateAdvDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)
        return await step_context.end_dialog(user_data)

    @staticmethod
    async def age_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text
        _value = _value.strip()
        _value = _value.split('-')

        if len(_value) == 2:
            condition = 18 <= int(_value[0]) <= 69 and 18 <= int(_value[1]) <= 69

        elif len(_value) == 1:
            condition = 18 <= int(_value[0]) <= 69
        else:
            condition = False
        # await prompt_context.context.delete_activity(prompt_context.context.activity.id)

        return (
                prompt_context.recognized.succeeded
                and condition
        )

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            'KEY_CALLBACK:profile_region',
            'KEY_CALLBACK:find_region',
            'KEY_CALLBACK:Man',
            'KEY_CALLBACK:Woman',
            'KEY_CALLBACK:Both',
            'KEY_CALLBACK:Other to Other',
            'KEY_CALLBACK:relationships',
            'KEY_CALLBACK:sex_fun',
            'KEY_CALLBACK:talking_friends',
            'KEY_CALLBACK:all_in_one',
        ]:
            condition = True
        else:
            condition = False
        # await prompt_context.context.delete_activity(prompt_context.context.activity.id)

        return (
                prompt_context.recognized.succeeded
                and condition
        )

    @classmethod
    async def _save_area(cls, user_data):
        area = await Area(
            area=user_data.area_id
        )
        try:
            area.save()
            return area

        except UniqueViolationError:
            area = await Area.objects.get(area=user_data.area_id)
            return area

        except Exception:
            logger.exception('Save area to db error %s', user_data.area_id)

        return

    @classmethod
    async def _save_customer(cls, user_data, area):
        customer = Customer(
            nickname=user_data.nickname,
            lang=int(user_data.lang),
            gender=int(user_data.gender),
            looking_gender=int(user_data.looking_gender),
            age=int(user_data.age),
            prefer_age=int(user_data.prefer_age),
            looking_for=int(user_data.looking_for),
            location=user_data.location,
            phone=int(user_data.phone),
            conversation_reference=user_data.conversation_reference,
            member_id=user_data.member_id,
            channel_id=0,
            last_seen=datetime.datetime.now(),
            area_id=area,
            premium_tier=PremiumTier.objects.get(pk=1)
        )

        try:
            await customer.save()

        except IntegrityError:
            Customer.objects.filter(member_id=user_data.member_id).update(
                nickname=user_data.nickname,
                lang=int(user_data.lang),
                gender=int(user_data.gender),
                looking_gender=int(user_data.looking_gender),
                age=int(user_data.age),
                prefer_age=int(user_data.prefer_age),
                looking_for=int(user_data.looking_for),
                # photo_main=user_data.photo_main,
                location=user_data.location,
                phone=int(user_data.phone),
                conversation_reference=user_data.conversation_reference,
                member_id=user_data.member_id,
                channel_id=0,
                last_seen=datetime.datetime.now(),
                area_id=area,
                premium_tier=PremiumTier.objects.get(pk=1)


            )
        except Exception:
            logger.exception('Save customer to db error %s', user_data.member_id)

        return

    # @classmethod
    # async def _profanity_filter(cls, text: str) -> str:
    #     pf = ProfanityFilter(languages=['ru', 'en'])
    #     # pf.extra_profane_word_dictionaries = {'en': {'chocolate', 'orange'}}
    #
    #     return pf.censor(text)

    @classmethod
    async def _who_for_whom(cls, gender: str, looking_gender: str) -> int:
        if gender == 'Man' and looking_gender == 'Woman':
            return 0
        elif gender == 'Woman' and looking_gender == 'Man':
            return 1
        elif looking_gender == 'Both':
            return 2
        elif gender == 'Man' and looking_gender == 'Man':
            return 3
        elif gender == 'Woman' and looking_gender == 'Woman':
            return 4
        elif looking_gender == 'Other':
            return 5
        else:
            return None

