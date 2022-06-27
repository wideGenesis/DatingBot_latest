import json
import os
import uuid
from tempfile import NamedTemporaryFile
from typing import Union

from django.core.files import File

import requests


from botbuilder.core import MessageFactory, UserState, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    PromptValidatorContext,
    AttachmentPrompt
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import Activity, ActivityTypes, Attachment

from db.models import Customer, UserMediaFile
from helpers.azure_storage import upload_blob
from settings.logger import CustomLogger
from helpers.copyright import BOT_MESSAGES, UPLOAD_FILE_KB

from ms_bot.bots_models.models import CustomerProfile
from ms_bot.bot_helpers.telegram_helper import rm_tg_message

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
        member_id = int(step_context.context.activity.from_property.id)

        if result_from_previous_step[0] is None:
            return await step_context.end_dialog(user_data)

        attachment: Attachment = result_from_previous_step[0]
        # print('>>>> attachment', attachment)

        if result_from_previous_step:
            save_result = await self._save_file_to_blob(
                member_id,
                attachment.content_url,
                attachment.content_type,
                attachment.name,
                user_data)

            user_data.photo_main = attachment.content_url
            await step_context.context.send_activity(save_result)
        return await step_context.end_dialog('need_replace_parent')

    @staticmethod
    async def file_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        if not prompt_context.recognized.succeeded:
            await prompt_context.context.send_activity(BOT_MESSAGES['file_not_uploaded'])
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
    async def _save_file_to_blob(
            cls,
            member_id: int,
            file_url: str,
            content_type: str,
            step_context: WaterfallStepContext,
            user_data: CustomerProfile) -> Union[None, DialogTurnResult]:

        if user_data.files_dict is not None and len(user_data.files_dict) >= 4:
            logger.warning('Maximum files qty exceeded %s', len(user_data.files_dict))
            return BOT_MESSAGES['file_limit_reached']

        if content_type == 'video/mp4':
            _file_type = 0
            suffix = '.mp4'
        elif content_type == 'image/jpeg':
            _file_type = 1
            suffix = '.jpg'
        elif content_type == 'image/png':
            _file_type = 2
            suffix = '.png'
        else:
            return BOT_MESSAGES['file_bad_format']

        _file_name = str(uuid.uuid4()).replace('-', '') + suffix
        file = os.path.join('ms_bot/temp_media', _file_name)
        result = requests.get(file_url)

        if result.status_code == 200:
            with open(file, 'wb') as f:
                f.write(result.content)
            size = os.path.getsize(file)
            if size > 4194304:
                await step_context.context.send_activity('File > 4Mb')
                return await step_context.replace_dialog(UploadDialog.__name__)

        upload_result = await upload_blob(suffix.replace('.', ''), _file_name, str(member_id))
        if upload_result:
            os.remove(file)

        member_id = int(member_id)
        customer_id = await Customer.objects.get(member_id=member_id)

        customer_photo = UserMediaFile(
            customer_id=customer_id.id,
            file=_file_name,
            member_id=member_id,
            file_type=_file_type,
            privacy_type=1,
            is_archived=False
        )

        try:
            await customer_photo.save()
        except Exception:
            logger.exception('Save customer_photo to db error %s', member_id)

        return BOT_MESSAGES['file_uploaded']


# def save(self, *args, **kwargs):
#     file_tmp = NamedTemporaryFile(delete=True)
#
#     _file_name = file_tmp.name.split('/')
#     _file_name = str(uuid.uuid4()).replace('-', '') + suffix
#
#     result = requests.get(self.file_temp_url)
#     if result.status_code == 200:
#         file_tmp.write(result.content)
#         file_tmp.flush()
#         _f = File(file_tmp, name=_file_name)
#         if _f.size > 4194304:
#             logger.warning('UserMediaFiles has not been saved. File size: %s', _f.size)
#             return
#
#         self.file = _f
#         self.file_temp_url = None
