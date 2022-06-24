#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import configuration


class DefaultConfig(object):
    """ Bot Configuration """

    PORT = configuration.MS_BOT_PORT
    APP_ID = configuration.MicrosoftAppId
    APP_PASSWORD = configuration.MicrosoftAppPassword
    BLOB_CONNECTION_STRING = configuration.AZURE_STORAGE_CONNECTION_STRING
    BLOB_CONTAINER_NAME = configuration.AZURE_BLOB_CONTAINER_NAME
    APP_INSIGHTS_INSTRUMENTATION_KEY = configuration.APP_INSIGHTS_INSTRUMENTATION_KEY
