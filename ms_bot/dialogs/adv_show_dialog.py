# import datetime
# import json
# import hashlib
# import uuid
#
# from botbuilder.core import (
#     MessageFactory,
#     BotTelemetryClient,
#     NullTelemetryClient,
#     UserState,
# )
# from botbuilder.dialogs import (
#     WaterfallDialog,
#     DialogTurnResult,
#     WaterfallStepContext,
#     ComponentDialog,
#     PromptValidatorContext,
# )
#
# from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
# from botbuilder.schema import ActivityTypes, Activity
#
# from core.tables.models import Advertisement
# from ms_bot.bots_models.models import CustomerProfile
# from settings.logger import CustomLogger
# from helpers.copyright import send_file_kb
# from ms_bot.bot_helpers.telegram_helper import rm_tg_message
#
#
# logger = CustomLogger.get_logger("bot")
#
#
# class MyAdvDialog(ComponentDialog):
#     def __init__(
#         self,
#         user_state: UserState,
#         dialog_id: str = None,
#         telemetry_client: BotTelemetryClient = NullTelemetryClient(),
#     ):
#         super(MyAdvDialog, self).__init__(dialog_id or MyAdvDialog.__name__)
#         self.telemetry_client = telemetry_client
#         self.user_state = user_state
#         self.user_profile_accessor = self.user_state.create_property("CustomerProfile")
#
#         self.add_dialog(
#             TextPrompt(TextPrompt.__name__, MyAdvDialog.answer_prompt_validator)
#         )
#
#         self.add_dialog(
#             WaterfallDialog(
#                 "MainMyAdvDialog",
#                 [
#                     # self.passcode_required_step,
#                     self.show_adv_0_step,
#                     self.parse_0_step,
#                     self.show_adv_1_step,
#                     self.parse_1_step,
#                 ],
#             )
#         )
#         TextPrompt.telemetry_client = self.telemetry_client
#         ChoicePrompt.telemetry_client = self.telemetry_client
#         self.initial_dialog_id = "MainMyAdvDialog"
#
#     async def passcode_required_step(
#         self, step_context: WaterfallStepContext
#     ) -> DialogTurnResult:
#         logger.debug("passcode_required_step %s", MyAdvDialog.__name__)
#         user_data: CustomerProfile = await self.user_profile_accessor.get(
#             step_context.context, CustomerProfile
#         )
#
#         # passcode = user_data.passcode
#         # change + worker + email
#
#         member_id = int(step_context.context.activity.from_property.id)
#         adv_in_storage = {}
#         try:
#             user_adv = Advertisement.objects.filter(
#                 publisher__member_id=member_id
#             ).values()
#
#             for item in user_adv:
#                 if item["is_published"]:
#                     continue
#                 adv_in_storage[item["id"]] = {
#                     "id": item["id"],
#                     "publisher": item["publisher"],
#                     "member_id": member_id,
#                     "who_for_whom": item["who_for_whom"],
#                     "age": item["age"],
#                     "prefer_age": item["prefer_age"],
#                     "has_place": item["has_place"],
#                     "dating_time": item["dating_time"],
#                     "dating_day": item["dating_day"],
#                     "adv_text": item["adv_text"],
#                     "location": item["location"],
#                     "area_id": item["area_id"],
#                     "large_city_near_id": item["large_city_near_id"],
#                     "phone_is_hidden": item["phone_is_hidden"],
#                     "money_support": item["money_support"],
#                     "redis_channel": item["redis_channel"],
#                     "is_published": item["is_published"],
#                     "created_at": item["created_at"],
#                 }
#
#             logger.debug("USER ADVs (%s) FOUND IN DB", member_id)
#         except Exception:
#             logger.exception("USER ADVs (%s) NOT FOUND IN DB", member_id)
#
#     async def show_adv_0_step(
#         self, step_context: WaterfallStepContext
#     ) -> DialogTurnResult:
#         logger.debug("show_adv_0_step %s", MyAdvDialog.__name__)
#         user_data: CustomerProfile = await self.user_profile_accessor.get(
#             step_context.context, CustomerProfile
#         )
#
#         return await self.yield_adv_and_kb(step_context, user_data, step=0)
#
#     async def parse_0_step(
#         self, step_context: WaterfallStepContext
#     ) -> DialogTurnResult:
#         logger.debug("parse_0_choice_step %s", MyAdvDialog.__name__)
#         chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
#         message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
#         await rm_tg_message(step_context.context, chat_id, message_id)
#
#         user_data: CustomerProfile = await self.user_profile_accessor.get(
#             step_context.context, CustomerProfile
#         )
#
#         found_choice = step_context.result
#         return await self.choice_route(step_context, found_choice, user_data, 0)
#
#     async def show_adv_1_step(
#         self, step_context: WaterfallStepContext
#     ) -> DialogTurnResult:
#         logger.debug("show_adv_1_step %s", MyAdvDialog.__name__)
#         user_data: CustomerProfile = await self.user_profile_accessor.get(
#             step_context.context, CustomerProfile
#         )
#         return await self.yield_adv_and_kb(step_context, user_data, step=1)
#
#     async def parse_1_step(
#         self, step_context: WaterfallStepContext
#     ) -> DialogTurnResult:
#         logger.debug("parse_1_step %s", MyAdvDialog.__name__)
#         chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
#         message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
#         await rm_tg_message(step_context.context, chat_id, message_id)
#
#         user_data: CustomerProfile = await self.user_profile_accessor.get(
#             step_context.context, CustomerProfile
#         )
#
#         found_choice = step_context.result
#         return await self.choice_route(step_context, found_choice, user_data, 1)
#
#     @staticmethod
#     async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
#         _value = prompt_context.context.activity.text
#
#         if _value in [
#             "KEY_CALLBACK:income_adv",
#             "KEY_CALLBACK:review_adv",
#             "KEY_CALLBACK:adv_rm",
#             "KEY_CALLBACK:create_adv",
#             "KEY_CALLBACK:back",
#         ]:
#             condition = True
#         else:
#             condition = False
#
#         return prompt_context.recognized.succeeded and condition
#
#     @staticmethod
#     async def choice_route(
#         step_context: WaterfallStepContext,
#         found_choice,
#         user_data: CustomerProfile,
#         list_id: int,
#     ) -> DialogTurnResult:
#         from . import UserMediaFiles
#
#         try:
#             item = user_data.files_dict[list_id]
#             pk = item["id"]
#         except Exception:
#             return await step_context.end_dialog("need_replace_parent")
#
#         if found_choice == "KEY_CALLBACK:file_open_hidden":
#             try:
#                 user_media_files = UserMediaFiles.objects.get(id=pk)
#                 logger.warning(
#                     "Obj: %s, privacy_type: %s, pk: %s",
#                     user_media_files,
#                     user_media_files.privacy_type,
#                     pk,
#                 )
#                 user_media_files.privacy_type = (
#                     1 if user_media_files.privacy_type == 0 else 0
#                 )
#                 user_media_files.save()
#             except Exception:
#                 logger.exception("Get Customer from bd error")
#             user_data.last_seen = datetime.datetime.utcnow()
#             user_data.files_dict.pop(list_id)
#             return await step_context.next([])
#
#         elif found_choice == "KEY_CALLBACK:file_rm":
#             try:
#                 user_media_files = UserMediaFiles.objects.get(id=pk)
#                 user_media_files.is_archived = 1
#                 user_media_files.save()
#             except Exception:
#                 logger.exception("Get Customer from bd error")
#             user_data.last_seen = datetime.datetime.utcnow()
#             user_data.files_dict.pop(list_id)
#
#             return await step_context.next([])
#
#         elif found_choice == "KEY_CALLBACK:back":
#             return await step_context.end_dialog("need_replace_parent")
#
#         else:
#             await step_context.context.send_activity("buy")
#             return await step_context.cancel_all_dialogs(True)
#
#     @staticmethod
#     async def yield_adv_and_kb(
#         step_context: WaterfallStepContext, user_data: CustomerProfile, step=None
#     ) -> DialogTurnResult:
#         # print('files', user_data.files_dict)
#
#         item = user_data.files_dict
#
#         if len(item) == 0:
#             await step_context.context.send_activity("У вас немає завантажених файлів")
#             return await step_context.end_dialog("need_replace_parent")
#
#         activities = []
#         try:
#             item = item[step]
#             print("file", item)
#         except Exception:
#             return await step_context.end_dialog("need_replace_parent")
#
#         if item.get("file_type") == 0:
#             activities.append(
#                 Activity(
#                     channel_data=json.dumps(
#                         send_video_kb(item["file"], item["privacy_type"])
#                     ),
#                     type=ActivityTypes.message,
#                 )
#             )
#         else:
#             activities.append(
#                 Activity(
#                     channel_data=json.dumps(
#                         send_file_kb(item["file"], item["privacy_type"])
#                     ),
#                     type=ActivityTypes.message,
#                 )
#             )
#
#         await step_context.context.send_activities(activities)
#         print(">>>>>>>>>>>>\n")
#         return await step_context.prompt(
#             TextPrompt.__name__,
#             PromptOptions(
#                 prompt=Activity(
#                     channel_data=json.dumps(SEND_MEDIA_KB),
#                     type=ActivityTypes.message,
#                 ),
#                 retry_prompt=MessageFactory.text(
#                     "Зробіть вибір, натиснувши на відповідну кнопку вище"
#                 ),
#             ),
#         )
#
#     @staticmethod
#     async def passcode_check(hashed_passcode, passcode):
#         phrase, salt = hashed_passcode.split(":")
#         return phrase == hashlib.sha256(salt.encode() + passcode.encode()).hexdigest()
#
#     @staticmethod
#     async def passcode_update(passcode):
#         salt = uuid.uuid4().hex
#         return (
#             hashlib.sha256(salt.encode() + passcode.encode()).hexdigest() + ":" + salt
#         )
