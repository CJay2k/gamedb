import json
import traceback

import aiohttp
from bs4 import BeautifulSoup

STORE_NAME = 'PlayStation Store'
HEADERS = {}

BASE_URL_API = 'https://web.np.playstation.com/api/graphql/v1//op'
BASE_URL = 'https://store.playstation.com/pl-pl/product/'


async def find_games(session: aiohttp.ClientSession, search_string) -> list:
    params = """
                ?operationName=getSearchResults
                &variables={
                    "countryCode":"PL",
                    "languageCode":"en",
                    "pageOffset":0,
                    "pageSize":50,
                    "searchTerm":"{search_string}"
                    }
                &extensions={
                    "persistedQuery":{
                        "version":1,
                        "sha256Hash":"1cf905427747fbe1fb20bf37fb700f10ad1e5b1c7c5aba3a12f330e62680ce79"
                    }
                }
            """.replace("{search_string}", search_string)

    async with session.get(BASE_URL_API, params=params) as response:
        data = await response.json()

    try:
        found_games = [
            {
                'title': _get_title(game),
                'thumbnail': _get_thumbnail(game),
                'data_for_details': _get_link(game),
                'platforms': _get_platforms(game),
            }
            for game in data['data']['universalSearch']['items']
            if _is_title_matching_search_string(search_string, game)
            and _is_game(game)
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
    if game['localizedStoreDisplayClassification'] != 'Full Game':
        return False
    return all(word not in _get_title(game).lower() for word in ['comic'])


def _get_title(game):
    return game['name']


def _get_thumbnail(game):
    for image in game['media']:
        if image['role'] == 'MASTER':
            return image['url']
    # else:
    #     return game['media'][0]['url']


def _get_link(game):
    return BASE_URL + game['id']


def _get_platforms(game):
    platforms = set()
    for item in game.get('platforms', []):
        if item == 'PS4':
            platforms.add('ps4')
        elif item == 'PS5':
            platforms.add('ps5')
    return platforms or []

# def is_duplicate(self, game, list_of_games):
#     return any(item['title'] == self.get_title(game) for item in list_of_games)


async def get_details(session: aiohttp.ClientSession, game) -> dict:
    endpoint = game['data_for_details']

    async with session.get(endpoint) as response:
        data = await response.read()

    soup = BeautifulSoup(data, 'html.parser')
    data_string = soup.find('script', id='mfe-jsonld-tags').string
    data = json.loads(data_string)
    try:
        game_details = {
            'store_name': STORE_NAME,
            'title': game['title'],
            'main_media': _get_main_media(soup),
            'description': _get_description(soup),
            'thumbnail_url': game['thumbnail'],
            'images': [],
            'game_url': endpoint,
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


def _get_description(soup):
    data = soup.find(
        'p', {'data-qa': 'mfe-game-overview#description'})
    return ''.join(str(word) for word in data)


def _get_price(data):
    return data['offers'].get('price') or 0


def _get_main_media(soup):
    if main_image_tag := soup.find('img', {'data-qa': 'gameBackgroundImage#heroImage#image-no-js'}):
        main_image = main_image_tag['src']
    else:
        main_image = ''
    return {
        'src': main_image,
        'type': 'image'
    }
