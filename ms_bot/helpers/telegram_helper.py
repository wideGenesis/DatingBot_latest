import json

from botbuilder.core import TurnContext
from botbuilder.schema import Activity, ActivityTypes
from geopy.geocoders import Nominatim, GoogleV3
from setup.logger import CustomLogger
from config.conf import PROJECT_CONF


logger = CustomLogger.get_logger('bot')


async def reverse_geocode(coordinates: str):
    coordinates = coordinates.split(':')
    coordinates = f'{coordinates[0]}, {coordinates[1]}'

    try:
        locator = Nominatim(user_agent='myGeocoder')
        location = locator.reverse(coordinates)
        # print(location.raw['address'].get('city'))
        # print(location.raw['address'].get('state'))
        # print(location.raw['address'].get('country'))
        return (
            location.raw['address'].get('city'),
            location.raw['address'].get('state'),
            location.raw['address'].get('country')
        )

    except Exception:
        locator = GoogleV3(api_key=PROJECT_CONF.GOOGLE_API_KEY, user_agent='myGeocoder')
        location = locator.reverse(coordinates)
        # print(location.raw['address_components'][3]['long_name'])
        # print(location.raw['address_components'][5]['long_name'])
        # print(location.raw['address_components'][6]['long_name'])
        return (
            location.raw['address_components'][3]['long_name'],
            location.raw['address_components'][5]['long_name'],
            location.raw['address_components'][6]['long_name']
        )


async def rm_tg_message(turn_context: TurnContext, chat_id, message_id):
    delete_message = {
        'method': 'deleteMessage',
        'parameters': {
            'chat_id': int(chat_id),
            'message_id': int(message_id)
        }
    }

    await turn_context.send_activities(
        [
            Activity(
                channel_data=json.dumps(delete_message),
                type=ActivityTypes.message,
            )
        ]
    )
    return
