import datetime
from typing import Optional

from botbuilder.core import UserState, BotTelemetryClient, NullTelemetryClient, TurnContext
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
)

from helpers.azure_storage import rm_user_blobs
from ms_bot.dialogs.telegram_registration_dialog import TelegramRegistrationDialog
from settings.logger import CustomLogger
from ms_bot.bots_models.models import CustomerProfile

from core.tables.models import Customer
from core.tables.models import UserMediaFile

logger = CustomLogger.get_logger("bot")


class ReloadCacheDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(ReloadCacheDialog, self).__init__(dialog_id or ReloadCacheDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            WaterfallDialog(
                "ReloadCacheDialog",
                [
                    self.is_user_exists_in_blob,
                    self.user_exists_in_db,
                ],
            )
        )
        TelegramRegistrationDialog.telemetry_client = self.telemetry_client

        self.initial_dialog_id = "ReloadCacheDialog"
        self.customer_exists = None
        self.customer_instance = None
        self.customer = None

    async def is_user_exists_in_blob(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        # print("updated_at >>> ", user_data.updated_at)
        member_id = int(step_context.context.activity.from_property.id)

        h, m, s = "0:01:00".split(":")
        threshold = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        time_now = datetime.datetime.utcnow()

        if user_data.updated_at is None:
            logger.debug("USER (%s) DOESN'T EXISTS IN CACHE", member_id)
            return await step_context.next([])

        timer = time_now - user_data.updated_at

        if timer < threshold and user_data.is_active:
            logger.debug("USER (%s) STATE LOADED SUCCESSFULLY", member_id)
            self.customer_exists = True
            return await step_context.end_dialog(self.customer_exists)

        return await step_context.next([])

    async def user_exists_in_db(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("user_exists_in_db %s", ReloadCacheDialog.__name__)

        member_id = int(step_context.context.activity.from_property.id)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        try:
            customer = await Customer.objects.get(member_id=member_id)
            logger.debug("USER (%s) FOUND IN DB", member_id)
            self.customer_exists = True
            self.customer_instance = customer

        except Exception:
            logger.warning("USER (%s) DOESN'T EXIST IN DB", member_id)
            self.customer_exists = None

        if self.customer_exists is None:
            return await step_context.end_dialog()

        files_in_storage = []

        try:
            user_files = (
                await UserMediaFile.objects.filter(
                    customer=self.customer_instance.id
                )
                .fields(
                    [
                        "file",
                        "file_type",
                        "privacy_type",
                        "is_archived",
                        "file_temp_url",
                        "created_at",
                    ]
                )
                .all()
            )

            for item in user_files:
                item = dict(item)

                if item["is_archived"]:
                    continue

                files_in_storage.append(
                    {
                        "id": item["id"],
                        "file": item["file"],
                        "file_type": item["file_type"],
                        "privacy_type": item["privacy_type"],
                        "is_archived": item["is_archived"],
                    }
                )
            logger.debug("USER FILES (%s) FOUND IN DB", member_id)
        except Exception:
            logger.exception(
                "USER {{{ FILES }}} (%s) NOT FOUND IN DB", self.customer_instance.member_id
            )

        await _reload_cache(user_data, self.customer_instance, files_in_storage, step_context.context)

        return await step_context.end_dialog(self.customer_exists)


async def _reload_cache(user_data, customer_instance, user_files, turn_context: TurnContext):
    member_id = turn_context.activity.from_property.id
    logger.debug('Drop cache before reload')
    try:
        rm_user_blobs(member_id)
    except Exception as e:
        logger.warning('Cache standard error, dont care about it')

    user_data.pk = customer_instance.id
    user_data.nickname = customer_instance.nickname
    user_data.phone = customer_instance.phone
    user_data.email = customer_instance.email
    user_data.description = customer_instance.description
    user_data.conversation_reference = customer_instance.conversation_reference
    user_data.member_id = customer_instance.member_id
    user_data.lang = customer_instance.lang
    user_data.self_sex = customer_instance.self_sex
    user_data.age = customer_instance.age
    user_data.is_active = customer_instance.is_active
    user_data.is_staff = customer_instance.is_staff
    user_data.is_superuser = customer_instance.is_superuser
    user_data.post_header = customer_instance.post_header
    user_data.password_hash = customer_instance.password_hash
    user_data.password_hint = customer_instance.password_hint
    user_data.premium_tier = customer_instance.premium_tier
    user_data.hiv_status = customer_instance.hiv_status
    user_data.alco_status = customer_instance.alco_status
    user_data.drugs_status = customer_instance.drugs_status
    user_data.safe_sex_status = customer_instance.safe_sex_status
    user_data.passion_sex = customer_instance.passion_sex
    user_data.if_same_sex_position = customer_instance.if_same_sex_position
    user_data.boobs_cock_size = customer_instance.boobs_cock_size
    user_data.is_sport = customer_instance.is_sport
    user_data.is_home_or_party = customer_instance.is_home_or_party
    user_data.body_type = customer_instance.body_type
    user_data.is_smoker = customer_instance.is_smoker
    user_data.is_tatoo = customer_instance.is_tatoo
    user_data.is_piercings = customer_instance.is_piercings
    user_data.instagram_link = customer_instance.instagram_link
    user_data.tiktok_link = customer_instance.tiktok_link
    user_data.likes = customer_instance.likes
    user_data.created_at = customer_instance.created_at
    user_data.updated_at = customer_instance.updated_at

    user_data.files_dict = user_files
    user_data.adv_list = customer_instance.adv_list
    user_data.authorised = True

    logger.debug("Cache for %s reloaded successfully!", customer_instance.member_id)
