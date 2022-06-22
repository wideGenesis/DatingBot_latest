# from geopy.geocoders import Nominatim, GoogleV3
#
#
# def reverse_geocode(coordinates: str):
#     coordinates = coordinates.split(':')
#     coordinates = f'{coordinates[0]}, {coordinates[1]}'
#
#     try:
#         # locator = Nominatim(user_agent='myGeocoder')
#         # location = locator.reverse(coordinates)
#         # print(location.raw['address'].get('city'))
#         # print(location.raw['address'].get('state'))
#         # print(location.raw['address'].get('country'))
#         locator = GoogleV3(api_key='AIzaSyDfcXWMsl8JeD8bi9q-lUipN-liJwQbWWM', user_agent='myGeocoder')
#         location = locator.reverse(coordinates)
#         print(location.raw['address_components'][3]['long_name'])
#         print(location.raw['address_components'][5]['long_name'])
#         print(location.raw['address_components'][6]['long_name'])
#
#     except Exception:
#         locator = GoogleV3(api_key='AIzaSyDfcXWMsl8JeD8bi9q-lUipN-liJwQbWWM', user_agent='myGeocoder')
#         location = locator.reverse(coordinates)
#         print(location.raw)


if __name__ == "__main__":
    reverse_geocode('46.412231:30.74354')
