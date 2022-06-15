import traceback

import aiohttp
import bbcode
from bs4 import BeautifulSoup

STORE_NAME = 'Steam'
HEADERS = {'Accept-Language': 'pl'}

BASE_URL = 'https://store.steampowered.com'


async def find_games(session: aiohttp.ClientSession, search_string) -> list:
    endpoint = f"{BASE_URL}/search/results/"
    params = {
        'count': '100',
        'sort_by': '_ASC',
        'category1': '998',
        'term': search_string,
    }

    async with session.get(endpoint, params=params) as response:
        data = await response.read()

    parsed_data = BeautifulSoup(data, 'html.parser')
    raw_search_results = parsed_data.find(
        id='search_resultsRows') or BeautifulSoup()
    try:
        found_games = [
            {
                'title': _get_title(game),
                'thumbnail': _get_thumbnail(game),
                'game_type': 'package' if _get_package_id(game) else 'game',
                'data_for_details': _get_package_id(game) or _get_app_id(game),
                'platforms': ['pc'],

            }
            for game in raw_search_results.findAll('a', href=True)
            if _is_title_matching_search_string(search_string, game) and _is_released(game)
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


def _is_released(game):
    return game.find('div', class_='search_price').get_text().strip() != ''


def _get_title(game):
    return game.find('span', class_='title').get_text()


def _get_thumbnail(game):
    if _get_package_id(game):
        return f'https://cdn.akamai.steamstatic.com/steam/subs/{_get_package_id(game)}/capsule_231x87.jpg'
    else:
        return f'https://cdn.akamai.steamstatic.com/steam/apps/{_get_app_id(game)}/capsule_231x87.jpg'


def _get_app_id(game):
    return game['data-ds-appid']


def _get_package_id(game):
    return game.get('data-ds-packageid')


# def _get_link(game):
#     return f"{BASE_URL}{game['url']}"


async def get_details(session: aiohttp.ClientSession, game) -> dict:
    game_id = game['data_for_details']
    game_type = game['game_type']

    if game_type == 'game':
        endpoint = f'{BASE_URL}/api/appdetails'
        params = {
            'appids': game_id,
            'l': 'polish'
        }
    else:
        params = {
            'packageids': game_id,
            'l': 'polish'
        }
        endpoint = f'{BASE_URL}/api/packagedetails'

    async with session.get(endpoint, params=params) as response:
        data = await response.json()

    data = data[f'{game_id}']['data']
    try:
        game_details = {
            'store_name': STORE_NAME,
            'title': game['title'],
            'main_media': _get_main_media(game_type, data),
            'description': _get_description(game_type, data),
            # 'reviews': await _get_game_reviews(session, game_type, game_id, data),
            'thumbnail_url': game['thumbnail'],
            'images': _get_images(data),
            'game_url': _get_link(game_type, game_id),
            'price': _get_price(game_type, data),
            'platforms': game['platforms']
        }
    except Exception as e:
        traceback.print_exc()
        return {'status': 'failed'}

    return {
        'status': 'success',
        'data': game_details
    }


def _get_description(game_type, data):
    if game_type == 'game':
        return data['about_the_game']
    description = data.get('page_content', '')
    return bbcode.render_html(description)


def _get_main_media(game_type, data):
    media = ''
    media_type = ''
    if game_type == 'game':
        videos = [item['webm']['max']
                  for item in data.get('movies', [])]
    else:
        videos = data.get('movies', [])

    if videos:
        media = videos[0]
        media_type = 'video'
    elif images := _get_images(data):
        media = images[0]
        media_type = 'image'

    return {
        'src': media,
        'type': media_type
    }


def _get_images(data):
    return [item['path_full'] for item in data.get('screenshots', [])]


def _get_price(game_type, data):
    if game_type == 'game':
        return data.get('price_overview', {}).get('final', 0) / 100
    else:
        return data.get('price').get('final', 0) / 100


def _get_link(game_type, game_id):
    if game_type == 'game':
        return f'{BASE_URL}/app/{game_id}'
    else:
        return f'{BASE_URL}/sub/{game_id}'


async def _get_game_reviews(session: aiohttp.ClientSession, game_type, game_id, data) -> dict:
    params = {
        'review_score_preference': 0,
        'l': 'polish'
    }
    if game_type == 'game':
        endpoint = f'{BASE_URL}/appreviewhistogram/{game_id}'
    else:
        items_id_in_package = [game['id'] for game in data['apps']]
        endpoint = f"{BASE_URL}/appreviewhistogram/{min(items_id_in_package)}"

    async with session.get(endpoint, params=params) as response:
        data = await response.json()

    result_list = data.get('results').get('rollups')

    if not result_list:
        return {}

    positive = 0
    negative = 0
    for review in result_list:
        positive += review['recommendations_up']
        negative += review['recommendations_down']

    votes = positive + negative
    try:
        rating = positive * 10 / votes
    except ZeroDivisionError:
        return {}

    return {
        'votes': votes,
        'rating': round(rating, 2)
    }
