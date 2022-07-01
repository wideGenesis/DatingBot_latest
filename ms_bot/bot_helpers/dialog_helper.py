# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Utility to run dialogs."""
import time

from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus
from botbuilder.schema import ErrorResponseException

from settings.logger import CustomLogger


logger = CustomLogger.get_logger("bot")


class DialogHelper:
    """Dialog Helper implementation."""

    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        """Run dialog."""
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)

        try:
            results = await dialog_context.continue_dialog()
            # logger.debug('continue_dialog %s', dialog.id)

        except ErrorResponseException:
            logger.exception(
                "Error response code. Member_id: %s",
                turn_context.activity.from_property.id,
            )
            time.sleep(10)
            return

        except Exception:
            logger.exception("EXCEPTION begin_dialog %s", dialog.id)
            time.sleep(10)
            results = None
            await dialog_context.begin_dialog(dialog.id)

        if not results:
            # logger.warning('if not results')
            return

        if results.status == DialogTurnStatus.Empty:
            # logger.debug('begin_dialog %s', dialog.id)
            await dialog_context.begin_dialog(dialog.id)

        # Original code
        # dialog_context = await dialog_set.create_context(turn_context)
        # results = await dialog_context.continue_dialog()
        # if results.status == DialogTurnStatus.Empty:
        #     await dialog_context.begin_dialog(dialog.id)
