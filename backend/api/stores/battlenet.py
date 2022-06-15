import traceback

import aiohttp
from currency_converter import CurrencyConverter

STORE_NAME = 'Battlenet'
HEADERS = {'Accept-Language': 'en-US,en;q=0.5'}
COOKIES = {'locale': 'pl_PL'}

BASE_URL = 'https://eu.shop.battle.net'


async def find_games(session: aiohttp.ClientSession, search_string: str) -> list:
    endpoint = f'{BASE_URL}/api/search'
    params = {
        'query': search_string
    }

    async with session.get(endpoint, params=params, headers=HEADERS) as response:
        data = await response.json()

    try:
        found_games = []
        for game in data:
            if (_is_game(game) and
                _is_base_game(game) and
                _is_not_on_list(game, found_games) and
                    _is_title_matching_search_string(search_string, game)):
                found_games.append({
                    'store_name': STORE_NAME,
                    'title': _get_title(game),
                    'slug': _get_name(game),
                    'thumbnail': _get_thumbnail(game),
                    'data_for_details': _get_destination(game),
                    'platforms': ['pc'],
                })
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
    return all(
        word not in _get_title(game).lower() for word in
        ['collection', 'kolekcja', 'chest', 'edition', 'edycja', 'pakiet'])


def _is_not_on_list(game, game_list):
    return all(_get_destination(game) != item['data_for_details'] for item in game_list)


def _is_base_game(game):
    return game['categoryId'] not in ['commanders', 'wild-only', 'pets', 'announcers', 'gear', 'game-services', 'mounts', 'toys', 'premium-arcade', 'card-packs', 'in-game-content']


def _get_title(game):
    return game['title']


def _get_name(game):
    return game['name']


def _get_destination(game):
    index = game['destination'].find('?p=')
    return game['destination'] if index == -1 else game['destination'][:index]


def _get_thumbnail(game):
    return game['cardImageUrl']


async def get_details(session: aiohttp.ClientSession, game) -> dict:
    destination = game['data_for_details']
    endpoint = f'{BASE_URL}/api{destination}'
    data = {}

    async with session.get(endpoint, headers=HEADERS) as response:
        data = await response.json()

    try:
        game_details = {
            'store_name': STORE_NAME,
            'title':  game['title'],
            'main_media': _get_main_media(data),
            'description': _get_description(data),
            'thumbnail_url':  game['thumbnail'],
            'images': [],
            'game_url': _get_link_to_game_in_store(destination),
            'price': _get_price(data),
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
    description = f"<h1>{data['heading']['title']}</h1>"
    description += data['heading']['summary']
    for section in data['featureSections']:
        description += f"<h2>{section['title']}</h2>"
        description += section['summary']
        for feature in section['features']:
            description += f"<h3>{feature['name']}</h3>"
            description += feature['description']
            description += f'<img src="https:{feature["imageUrl"]}"/>'
    return description


# def _get_thumbnail(data):
#     url = data['logoUrl']

#     if not url:
#         url = _get_main_media()['src']
#         if _get_main_media()['type'] == 'youtube':
#             url = f'http://img.youtube.com/vi/{url.split("/")[-1]}/maxresdefault.jpg'

#     return url


def _get_main_media(data):
    src = ''
    media_type = ''
    if videos := _get_videos(data):
        src = videos[0]
        media_type = 'youtube'
    else:
        for item in data['products']:
            if _is_base_version(item):
                src = item['imageUrl']
                media_type = 'image'
            if not src:
                src = item['imageUrl']
                media_type = 'image'

    return {
        'src': src,
        'type': media_type
    }


def _get_videos(data):
    videos = []
    try:
        for item in data.get('media', {}).get('items', []):
            src = item['videoUrl']
            index = src.find('?')
            if index != -1:
                src = src[:index]
            videos.append(src)
    except AttributeError:
        return []
    return videos


def _get_price(data):
    price = 0
    for item in data['products']:
        if _is_base_version(item) and item['price'].get('price'):
            price = item['price'].get('price', {}).get('raw', 0)
        if not price and item['price'].get('price'):
            price = item['price'].get('price', {}).get('raw', 0)
    converted_price = CurrencyConverter().convert(price, 'EUR', 'PLN')
    return round(converted_price, 2)


def _get_link_to_game_in_store(destination) -> str:
    return f'{BASE_URL}/pl-pl{destination}'


def _is_base_version(item):
    return item['name'].replace(u'\xa0', u' ').lower() in ["edycja standardowa", "base edition"]
