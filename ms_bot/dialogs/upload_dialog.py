import json

from botbuilder.core import MessageFactory, UserState, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog, \
    PromptValidatorContext, AttachmentPrompt

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import Activity, ActivityTypes, Attachment

from sqlalchemy.exc import IntegrityError
from setup.logger import CustomLogger
from ..lib.messages import BOT_MESSAGES, UPLOAD_FILE_KB

from ..bots_models.models import CustomerProfile
from ..helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger('bot')


class UploadDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(UploadDialog, self).__init__(dialog_id or UploadDialog.__name__)

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            AttachmentPrompt(
                AttachmentPrompt.__name__, UploadDialog.file_prompt_validator
            )
        )

        self.add_dialog(
            WaterfallDialog(
                "UploadDialog",
                [
                    self.upload_file_step,
                    self.back_to_parent
                ]
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "UploadDialog"

    async def upload_file_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('upload_file_step %s', UploadDialog.__name__)

        return await step_context.prompt(
            AttachmentPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(UPLOAD_FILE_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['upload_file']}"),
            )
        )

    async def back_to_parent(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug(f'back_to_main from %s', UploadDialog.__name__)
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
        member_id = step_context.context.activity.from_property.id

        if result_from_previous_step[0] is None:
            return await step_context.end_dialog(user_data)

        attachment: Attachment = result_from_previous_step[0]
        # print('>>>> attachment', attachment)

        if result_from_previous_step:
            save_result = await self._save_file(member_id, attachment.content_url, attachment.content_type, user_data)

            user_data.photo_main = attachment.content_url
            await step_context.context.send_activity(save_result)

        return await step_context.end_dialog('need_replace_parent')

    @staticmethod
    async def file_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        if not prompt_context.recognized.succeeded:
            await prompt_context.context.send_activity(
                "Вкладень не отримано. Продовжуємо далі..."
            )
            # We can return true from a validator function even if recognized.succeeded is false.
            return True

        attachments = prompt_context.recognized.value

        valid_files = [
            attachment
            for attachment in attachments
            if attachment.content_type in ["image/jpeg", "image/png", "video/mp4"]
        ]

        prompt_context.recognized.value = valid_files

        # If none of the attachments are valid images, the retry prompt should be sent.
        return len(valid_files) > 0

    @classmethod
    async def _save_file(cls, member_id, file_url, content_type, user_data: CustomerProfile) -> str:
        from . import UserMediaFiles
        from . import Customer

        if user_data.files_dict is not None and len(user_data.files_dict) >= 4:
            logger.warning('Maximum files qty exceeded %s', len(user_data.files_dict))
            return BOT_MESSAGES['file_limit_reached']

        if content_type == 'video/mp4':
            _file_type = 0
        elif content_type == 'image/jpeg':
            _file_type = 1
        elif content_type == 'image/png':
            _file_type = 2
        else:
            return BOT_MESSAGES['file_bad_format']

        customer_photo = UserMediaFiles(
            publisher=Customer.objects.get(member_id=member_id),
            member_id=member_id,
            file_temp_url=file_url,
            file_type=_file_type,
            privacy_type=1
        )

        try:
            customer_photo.save()

        except IntegrityError:
            UserMediaFiles.objects.filter(publisher__member_id=member_id).update(
                file_temp_url=file_url,
                file_type=_file_type,
                privacy_type=1
            )
        except Exception:
            logger.exception('Save customer_photo to db error %s', member_id)

        return BOT_MESSAGES['file_uploaded']
