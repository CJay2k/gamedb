import traceback
from re import sub

import aiohttp
from bs4 import BeautifulSoup

STORE_NAME = 'Ubisoft'
HEADERS = {'Accept-Language': 'pl'}

ENDPOINT_SEARCH = 'https://xely3u4lod-dsn.algolia.net/1/indexes/*/queries'
PARAMS_SEARCH = {
    'x-algolia-api-key': '5638539fd9edb8f2c6b024b49ec375bd',
    'x-algolia-application-id': 'XELY3U4LOD'
}

BASE_URL_DETAILS = 'https://store.ubi.com/s/eu_ubisoft/dw/shop/v19_8/products/'


async def find_games(session: aiohttp.ClientSession, search_string) -> list:
    json_ = {
        'requests': [
            {
                'indexName': 'eu_best_sellers',
                'params': f'hitsPerPage=100&query={search_string}'
            }
        ]
    }

    async with session.post(ENDPOINT_SEARCH, params=PARAMS_SEARCH, json=json_, headers=HEADERS) as response:
        data = await response.json()

    try:
        found_games = [
            {
                'title': _get_title(game),
                'thumbnail': _get_thumbnail(game),
                'data_for_details': _get_master_id(game),
                'platforms': _get_platforms(game),
            }
            for game in data['results'][0]['hits']
            if _is_title_matching_search_string(search_string, game) and _is_game(game)
        ]
    except Exception as e:
        traceback.print_exc()
        return {'status': 'failed'}

    return {
        'status': 'success',
        'data': found_games
    }


def _is_title_matching_search_string(search_string, game):
    return all(word in _get_title(game).lower() for word in search_string.lower().split())


def _is_game(game):
    return game['product_type'][0]['en_SK'] == 'Games'


def _get_title(game):
    return game['title']


def _get_thumbnail(game):
    return game['image_link']


def _get_master_id(game):
    return game['MasterID']


def _get_platforms(game):
    platforms = set()
    platforms_availability = game.get('platforms_availability', [])
    if any(platform in platforms_availability for platform in ['PC (Download)', 'PC DVD']):
        platforms.add('pc')
    if 'PS4' in platforms_availability:
        platforms.add('ps4')
    if 'PS5' in platforms_availability:
        platforms.add('ps5')
    if any(platform in platforms_availability for platform in ['Xbox (Download)', 'Xbox One']):
        platforms.add('xbox')
    if any(platform in platforms_availability for platform in ['Switch (Download version)', 'Switch']):
        platforms.add('nintendo')
    if 'Android' in platforms_availability:
        platforms.add('android')
    if 'iOS' in platforms_availability:
        platforms.add('ios')
    return platforms


async def get_details(session: aiohttp.ClientSession, game) -> dict:
    app_id = game['data_for_details']

    endpoint = f'{BASE_URL_DETAILS}{app_id}'
    params = {
        'currency': 'PLN',
        'client_id': '2a3b13e8-a80b-4795-853a-4cd52645919b'
    }
    async with session.get(endpoint, params=params, headers=HEADERS) as response:
        data = await response.json()

    params = {
        'lang': 'en-SK',
        'pid': app_id
    }

    async with session.get('https://store.ubi.com/eu/game/', params=params) as response:
        html = await response.read()

    soup = BeautifulSoup(html, 'html.parser')

    try:
        game_details = {
            'store_name': STORE_NAME,
            'title': game['title'],
            'main_media': _get_main_media(soup),
            'description': _get_description(data),
            'thumbnail_url': game['thumbnail'],
            'images': _get_images(soup),
            'game_url': _get_link(app_id),
            'price': _get_price(soup),
            'platforms': game['platforms']
        }
    except Exception as e:
        traceback.print_exc()
        return {'status': 'failed'}

    return {
        'status': 'success',
        'data': game_details
    }


def _get_description(data):
    return data['long_description']


def _get_link(app_id):
    return f'https://store.ubi.com/eu/game?lang=en-SK&pid={app_id}'


def _get_price(soup):
    if price_tag := soup.find(class_='product-add-to-cart'):
        raw_price = price_tag.find(class_='standard-price').text.strip()[:-3]
        value = sub(r'[^\d,]', '', raw_price)
        value = value.replace(',', '.')
        return float(value)
    return 0


def _get_images(soup):
    result = soup.find_all(class_='media-lightbox-image')
    return [item['data-desktop-src'] for item in result]


def _get_main_media(soup):
    src = ''
    media_type = ''

    if video_tag := soup.find('div', {'data-filter': 'media-slide-video'}):
        src = video_tag['data-ga-label']
        index = src.find('?')
        src = src if index == -1 else src[:index]
        media_type = 'youtube'
    elif image_tag := soup.find(class_='product_image-banner'):
        src = image_tag['data-desktop-src']
        media_type = 'image'

    return {
        'src': src,
        'type': media_type
    }
