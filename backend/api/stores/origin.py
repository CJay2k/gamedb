import traceback

import aiohttp

STORE_NAME = 'Origin'
HEADERS = {'Accept-Language': 'pl'}

BASE_URL = 'https://www.origin.com/pol/pl-pl/store'
SEARCH_URL = 'https://api4.origin.com/xsearch/store/en_us/pol/products'
DETAIL_URL = 'https://api3.origin.com/supercat/PL/pl_PL/supercat-PCWIN_MAC-PL-pl_PL.json.gz'


async def find_games(session: aiohttp.ClientSession, search_string) -> list:
    params = {
        'facetField': 'subscriptionGroup,genre,gameType,availability,rating,players,language,platform,franchise,publisher,developer,price',
        'sort': 'rank desc,releaseDate desc,title desc',
        'start': 0,
        'rows': 30,
        'isGDP': 'true',
        'searchTerm': search_string,
        'filterQuery': 'gameType: "basegame"'
    }
    async with session.get(SEARCH_URL, params=params, headers=HEADERS) as response:
        part1 = await response.json()

    params['filterQuery'] = 'gameType: "freegames"'
    async with session.get(SEARCH_URL, params=params, headers=HEADERS) as response:
        part2 = await response.json()

    data = part1['games']['game'] or []
    data += part2['games']['game'] or []

    try:
        found_games = [
            {
                'title': _get_title(game),
                'thumbnail': _get_thumbnail(game),
                'data_for_details': _get_path(game),
                'platforms': ['pc'],
            }
            for game in data
            if _is_title_matching_search_string(search_string, game)
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


def _get_title(game):
    return game['gameName']


def _get_thumbnail(game):
    return game['image']


def _get_path(game):
    return game['path']


async def get_details(session: aiohttp.ClientSession, game) -> dict:
    path = game['data_for_details']
    endpoint = f"https://data1.origin.com/ocd/{path}.pl-pl.pol.ocd"

    async with session.get(DETAIL_URL, headers=HEADERS) as response:
        data = await response.json()

    async with session.get(endpoint, headers=HEADERS) as response:
        media = await response.json()

    details = None
    for item in data['offers']:
        if item['gdpPath'] == path and item['countries'].get('isPurchasable') == "Y" and (
                not details or item['gameEditionTypeFacetKey'] == 'Standard Edition'):
            details = item
    try:
        game_details = {
            'store_name': STORE_NAME,
            'title': game['title'],
            'main_media': _get_main_media(media),
            'description': _get_description(details),
            'thumbnail_url':  game['thumbnail'],
            'images': _get_images(media),
            'game_url': _get_link(path),
            'price': _get_price(details),
            'platforms': game['platforms']
        }
    except Exception as e:
        print(game)
        traceback.print_exc()
        return {'status': 'failed'}

    return {
        'status': 'success',
        'data': game_details
    }


def _get_description(details):
    text = details['i18n']['longDescription']
    index = text.find('<b>Uwaga!</b>')
    return text if index == -1 else text[:index]


def _get_link(path):
    return f'{BASE_URL}{path}'


def _get_price(details):
    return float(details['countries']['catalogPrice'])


def _get_main_media(media):
    if videos := _get_videos(media):
        return {
            'src': videos[0],
            'type': 'youtube'
        }

    for item in media['gamehub']['components']['items']:
        if item.get('origin-store-gdp-header'):
            return {
                'src': item['origin-store-gdp-header']['background'],
                'type': 'image'
            }


def _get_images(media):
    media_images = []
    for item in media['gamehub']['components']['items']:
        if item.get('origin-store-pdp-media-carousel-wrapper'):
            media_images = item['origin-store-pdp-media-carousel-wrapper']['items']
            break
    return [item['origin-store-pdp-media-carousel-img']['src'] for item in media_images if
            item.get('origin-store-pdp-media-carousel-img')]


def _get_videos(media):
    media_videos = []
    for item in media['gamehub']['components']['items']:
        if item.get('origin-store-pdp-media-carousel-wrapper'):
            media_videos = item['origin-store-pdp-media-carousel-wrapper']['items']
            break
    return [f"https://www.youtube.com/embed/{item['origin-store-pdp-media-carousel-video']['video-id']}" for item in
            media_videos if
            item.get('origin-store-pdp-media-carousel-video', {}).get('video-id')]
