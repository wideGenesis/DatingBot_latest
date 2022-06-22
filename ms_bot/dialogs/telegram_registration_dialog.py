import pickle

from botbuilder.core import MessageFactory, UserState, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog, \
    PromptValidatorContext, NumberPrompt

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import Activity, ActivityTypes
import json

from sqlalchemy.exc import IntegrityError
from setup.logger import CustomLogger
from ms_bot.lib.messages import WITHOUT_LANG_WELCOME_KB

from ms_bot.bots_models.models import CustomerProfile
from ms_bot.dialogs.location_dialog import RequestLocationDialog
from ms_bot.dialogs.phone_dialog import RequestPhoneDialog
from ms_bot.dialogs.upload_dialog import UploadDialog
from ms_bot.helpers.telegram_helper import rm_tg_message

from db.models import Area
from db.models import Customer
from db.models import PremiumTier

logger = CustomLogger.get_logger('bot')


class TelegramRegistrationDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(TelegramRegistrationDialog, self).__init__(dialog_id or TelegramRegistrationDialog.__name__)

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(RequestPhoneDialog(user_state, RequestPhoneDialog.__name__))
        self.add_dialog(RequestLocationDialog(user_state, RequestLocationDialog.__name__))
        self.add_dialog(UploadDialog(user_state, UploadDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(TextPrompt(TextPrompt.__name__, TelegramRegistrationDialog.answer_prompt_validator))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__, TelegramRegistrationDialog.age_prompt_validator))

        self.add_dialog(
            WaterfallDialog(
                "TelegramRegistrationDialog",
                [
                    self.welcome_step,
                    self.member_step,
                    self.request_phone_step,
                    self.save_new_customer,
                    self.back_to_parent
                ]
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "TelegramRegistrationDialog"

    async def welcome_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('welcome_step %s', TelegramRegistrationDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(WITHOUT_LANG_WELCOME_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
            )
        )

    async def member_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('member_step %s', TelegramRegistrationDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        lang = str(step_context.result).split(':')
        member_id = step_context.context.activity.from_property.id
        conversation_reference = pickle.dumps(
            step_context.context.get_conversation_reference(step_context.context.activity)
        )
        nickname = step_context.context.activity.channel_data['callback_query']['from'].get('username')

        user_data.nickname = nickname
        user_data.premium_tier = 0
        user_data.conversation_reference = conversation_reference
        user_data.member_id = member_id
        user_data.lang = lang[1]
        user_data.is_active = 1

        return await step_context.next([])

    async def request_phone_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('request_phone_step %s', TelegramRegistrationDialog.__name__)
        return await step_context.begin_dialog(RequestPhoneDialog.__name__)

    # async def request_location_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
    #     logger.debug('request_location_step %s', RequestLocationDialog.__name__)
    #     return await step_context.begin_dialog(RequestLocationDialog.__name__)

    async def save_new_customer(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('save_new_customer %s', TelegramRegistrationDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        # try:
        #     area = await self._save_area(
        #         user_data,
        #     )
        #     logger.info('_save_area for %s was successful', user_data.member_id)
        # except Exception:
        #     logger.exception('_save_area for %s was Unsuccessful', user_data.member_id)
        #     await step_context.context.send_activity('exceptions_occurs')
        #     return await step_context.replace_dialog(TelegramRegistrationDialog.__name__)

        try:
            await self._save_customer(
                user_data,
            )
            logger.info('save_customer_to_db for %s was successful', user_data.member_id)
        except Exception:
            logger.exception('save_customer_to_db for %s was unsuccessful', user_data.member_id)
            await step_context.context.send_activity('exceptions_occurs')
            return await step_context.replace_dialog(TelegramRegistrationDialog.__name__)

        return await step_context.next([])

    async def upload_media_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('upload_media_step %s', TelegramRegistrationDialog.__name__)
        return await step_context.begin_dialog(UploadDialog.__name__)

    async def back_to_parent(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug(f'back_to_main from %s', TelegramRegistrationDialog.__name__)

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
            'KEY_CALLBACK:0',
            'KEY_CALLBACK:1',
            'KEY_CALLBACK:2',
            'KEY_CALLBACK:3',
            'KEY_CALLBACK:4',
            'KEY_CALLBACK:5',
            'KEY_CALLBACK:6',
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

        except IntegrityError:
            area = await Area.objects.get(area=user_data.area_id)
            return area

        except Exception:
            logger.exception('Save area to db error %s', user_data.area_id)

        return

    @classmethod
    async def _save_customer(cls, user_data):
        customer = await Customer(
            nickname=user_data.nickname,
            phone=int(user_data.phone),
            premium_tier_id=1,
            conversation_reference=user_data.conversation_reference,
            member_id=user_data.member_id,
            lang=int(user_data.lang),
            is_active=int(user_data.is_active)
        )

        try:
            customer.save()

        except IntegrityError:
            await Customer.objects.filter(member_id=user_data.member_id).update(
                nickname=user_data.nickname,
                phone=int(user_data.phone),
                premium_tier_id=1,
                conversation_reference=user_data.conversation_reference,
                member_id=user_data.member_id,
                lang=int(user_data.lang),
                is_active=int(user_data.is_active)

            )
        except Exception:
            logger.exception('Save customer to db error %s', user_data.member_id)

        return

#
# class ObjectDoesNotExist(ValueError):
#     pass

    # async def send_otp_to_tg_user(self, step_context: WaterfallStepContext) -> DialogTurnResult:
    #     logger.debug('send_otp_to_tg_user %s',
    #                  TelegramRegistrationDialog.__name__)
    #
    #     user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)
    #
    #     if user_data.authorised == 'verified':
    #         return await step_context.next([])
    #
    #     otp = generate_otp()
    #     user_data.otp = otp
    #     # await self.user_profile_accessor.set(step_context.context, user_data)
    #
    #     # logger.debug('sms will sent to: %s', user_data.mobilePhones)
    #     if project_settings.KS_ON_PROD and len(user_data.mobilePhones) > 0:
    #         # logger.debug('>>> IF %s', project_settings.KS_ON_PROD and len(user_data.mobilePhones) > 0)
    #
    #         for item in user_data.mobilePhones:
    #             try:
    #                 # result = send_sms_via_middleware(item.replace('+', ''), str(otp))
    #                 result = send_sms(item.replace('+', ''), str(otp))
    #                 logger.info('>>> Sending sms, Mobile is: %s, result is: %s', item, result)
    #             except Exception:
    #                 logger.exception('Send sms error')
    #                 return await step_context.replace_dialog(EmployeeIdAuthDialog.__name__)
    #
    #         # logger.debug('OTP SMS to: %s sent!', user_data.employeeId)
    #
    #     recipients = [user_data.userPrincipalName]
    #     if user_data.mail and user_data.mail != user_data.userPrincipalName:
    #         recipients.append(user_data.mail)
    #     logger.debug('recipients %s', recipients)
    #
    #     if not project_settings.IS_LOCAL_ENV:
    #         try:
    #             result = otp_send_to_email(recipients, str(otp))
    #         except Exception:
    #             logger.exception('Send otp email error')
    #             return await step_context.replace_dialog(EmployeeIdAuthDialog.__name__)
    #         logger.info('Email: %s, %s sent to: ', result, user_data.employeeId)
    #
    #     user_data.otp = str(otp)
    #     logger.debug('>>> OTP IS: %s', user_data.otp)
    #
    #     # redis_client.set(project_settings.REDIS_OTP_TMPL.format(otp), otp, ex=60 * 60 * 12)
    #
    #     return await step_context.next(user_data)
    #
    # async def prompt_otp(self, step_context: WaterfallStepContext) -> DialogTurnResult:
    #     logger.debug('prompt_otp %s', TelegramRegistrationDialog.__name__)
    #     user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)
    #
    #     if user_data.authorised == 'verified':
    #         return await step_context.next([])
    #
    #     prompt_options = PromptOptions(
    #         prompt=MessageFactory.text(BOT_MESSAGES['prompt_otp'])
    #     )
    #     return await step_context.prompt(TextPrompt.__name__, prompt_options)
    #
    # async def check_otp(self, step_context: WaterfallStepContext) -> DialogTurnResult:
    #     logger.debug('check_otp for dialog')
    #
    #
    #     user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)
    #
    #     if user_data.authorised == 'verified':
    #         return await step_context.next([])
    #
    #
    #     if not user_data.otp or step_context.result != user_data.otp:
    #         await step_context.context.send_activity(BOT_MESSAGES['otp_failed'])
    #         return await step_context.replace_dialog(TelegramRegistrationDialog.__name__)
    #
    #     user_data.authorised = 'verified'
    #     return await step_context.next([])
    #
