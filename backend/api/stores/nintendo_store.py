# from bs4 import BeautifulSoup
# import aiohttp
# from currency_converter import CurrencyConverter


# STORE_NAME = 'Nintendo Store'
# HEADERS = {'Accept-Language': 'pl'}

# BASE_URL = 'https://www.nintendo.com'
# ENDPOINT = 'https://u3b6gr4ua3-dsn.algolia.net/1/indexes/*/queries'

# PARAMS = {
#     'x-algolia-application-id': 'U3B6GR4UA3',
#     'x-algolia-api-key': 'c4da8be7fd29f0f5bfa42920b0a99dc7'
# }


# async def find_games(search_string, platforms='') -> list:
#     filters = []
#     if 'nintendo' in platforms:
#         filters.extend(('%22platform%3AWii%20U%22',
#                         '%22platform%3ANintendo%20Switch%22',
#                         '%22platform%3ANintendo%203DS%22'))
#     if 'android' in platforms:
#         filters.append('%22platform%3AAndroid%22')
#     if 'ios' in platforms:
#         filters.append('%22platform%3AiOS%22')
#     filters_string = '%2C'.join(filters)

#     query = {
#         "requests": [
#             {
#                 "indexName": "ncom_game_en_us",
#                 "params": f"hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B{filters_string}%5D%5D&query={search_string}"
#             }
#         ]
#     }

#     async with aiohttp.ClientSession(raise_for_status=True) as session:
#         async with session.post(ENDPOINT, params=PARAMS, json=query, headers=HEADERS) as response:
#             data = await response.json()
#     try:
#         return [
#             {
#                 'store_name': STORE_NAME,
#                 'title': _get_title(game),
#                 'thumbnail': _get_thumbnail(game),
#                 'data_for_details': _get_link(game),
#                 'platforms': _get_platforms(game),
#                 'status': 'success'
#             }
#             for game in data['results'][0]['hits']
#             if _is_title_matching_search_string(search_string, game)
#         ]
#     except Exception as e:
#         print(e)
#         return [{
#             'store_name': STORE_NAME,
#             'status': 'failed'
#         }]


# def _is_title_matching_search_string(search_string, game):
#     return all(word in _get_title(game).lower() for word in search_string.lower().split())


# def _get_title(game):
#     return game['title']


# def _get_thumbnail(game):
#     return game.get('horizontalHeaderImage') or game.get('boxart')


# def _get_link(game):
#     return BASE_URL + game['url']


# def _get_platforms(game):
#     platform = game.get('platform', [])
#     if platform in ['Nintendo Switch', 'Wii U', 'Nintendo 3DS']:
#         return ['nintendo']
#     elif platform == 'Android':
#         return ['android']
#     elif platform == 'iOS':
#         return ['ios']
#     return []


# async def get_details(game) -> dict:
#     endpoint = game['data_for_details']

#     async with aiohttp.ClientSession(raise_for_status=True) as session:
#         async with session.get(endpoint, headers=HEADERS) as response:
#             data = await response.read()
#     print(data)
#     soup = BeautifulSoup(data, 'html.parser')
#     # try:
#     return {
#         'store_name': STORE_NAME,
#         'title': game['title'],
#         'main_media': _get_main_media(soup),
#         'description': _get_description(soup),
#         'thumbnail': _get_thumbnail(soup),
#         'images': _get_images(soup),
#         'link': endpoint,
#         'price': _get_price(soup),
#         'platforms': game['platforms'],
#         'status': 'success'
#     }
#     # except Exception as e:
#     #     print(e)
#     #     return {
#     #         'store_name': STORE_NAME,
#     #         'status': 'failed'
#     #     }


# def _get_description(soup):
#     description_tag = soup.find('div', class_='overview-content') or soup.find('div',
#                                                                                class_='dp-description__text')
#     return description_tag.decode_contents()


# def _get_thumbnail(soup):
#     if header_image_tag := soup.find('div', {"class": "hero-illustration"}) or soup.find('div', {"class": "overview-illustration"}):
#         return header_image_tag.img['src']


# def _get_price(soup):
#     price_tag = soup.find('span', class_='msrp')
#     price = 0
#     if price_tag:
#         try:
#             price = float(price_tag.text.strip()[1:])
#         except ValueError:
#             price = 0
#     return price


# def _get_images(soup):
#     data = soup.find_all('product-gallery-item', {"type": "image"})
#     return [image['src'] for image in data]


# def _get_main_media(soup):
#     if images := _get_images(soup):
#         return {
#             'src': images[0],
#             'type': 'image'
#         }
#     else:
#         main_image = soup.find('div', {"class": "hero-illustration"})
#         if main_image:
#             return {
#                 'src': main_image.img['src'],
#                 'type': 'image'
#             }
