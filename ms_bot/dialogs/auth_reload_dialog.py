from botbuilder.core import UserState, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog

from ms_bot.dialogs.telegram_registration_dialog import TelegramRegistrationDialog
from settings.logger import CustomLogger
from ms_bot.bots_models.models import CustomerProfile

from db.models import Customer
from db.models import UserMediaFile


logger = CustomLogger.get_logger('bot')


class AuthReloadDialog(ComponentDialog):

    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),

    ):
        super(AuthReloadDialog, self).__init__(dialog_id or AuthReloadDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(TelegramRegistrationDialog(user_state, TelegramRegistrationDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "AuthReloadDialog",
                [
                    self.user_exists_in_db,
                ]
            )
        )
        TelegramRegistrationDialog.telemetry_client = self.telemetry_client

        self.initial_dialog_id = "AuthReloadDialog"
        self.customer_exists = None
        self.customer_instance = None

    async def user_exists_in_db(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('user_exists_in_db %s', AuthReloadDialog.__name__)
        member_id = int(step_context.context.activity.from_property.id)
        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)
        try:
            customer = await Customer.objects.get(member_id=member_id)
            logger.debug('USER (%s) FOUND IN DB', member_id)
            self.customer_exists = True
            self.customer_instance = customer

        except Exception:
            logger.warning('USER (%s) DOESN\'T EXIST IN DB', member_id)
            self.customer_exists = None

        if self.customer_exists is None:
            return await step_context.end_dialog()

        files_in_storage = []

        try:
            user_files = await UserMediaFile.objects.filter(member_id=member_id).fields(
                ['member_id',
                 'file',
                 'file_type',
                 'privacy_type',
                 'is_archived',
                 'file_temp_url',
                 'created_at']).all()

            for item in user_files:
                item = dict(item)

                if item['is_archived']:
                    continue
                files_in_storage.append(
                    {
                        'id': item['id'],
                        'file': item['file'],
                        'file_type': item['file_type'],
                        'privacy_type': item['privacy_type'],
                        'is_archived': item['is_archived'],
                    }
                )
            logger.debug('USER FILES (%s) FOUND IN DB', member_id)
        except Exception:
            logger.exception('USER FILES (%s) NOT FOUND IN DB', member_id)

        await self._reload_cache(user_data, self.customer_instance, files_in_storage)

        return await step_context.end_dialog()

    @classmethod
    async def _reload_cache(cls, user_data, customer_instance, user_files):
        user_data.lang = customer_instance.lang
        user_data.email = customer_instance.email
        user_data.phone = customer_instance.phone
        user_data.nickname = customer_instance.nickname
        user_data.conversation_reference = customer_instance.conversation_reference
        user_data.member_id = customer_instance.member_id
        user_data.premium_tier = customer_instance.premium_tier_id
        user_data.is_active = customer_instance.is_active
        user_data.files_dict = user_files
        user_data.updated_at = customer_instance.updated_at
        user_data.updated_at = customer_instance.id
        user_data.updated_at = customer_instance.post_header
        user_data.updated_at = customer_instance.passcode
