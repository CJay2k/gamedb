import traceback

import aiohttp
from bs4 import BeautifulSoup

STORE_NAME = 'GOG'

HEADERS = {'Accept-Language': 'pl'}
COOKIES = {'gog_lc': 'PL_PLN_en-US'}

BASE_URL = 'https://www.gog.com'


async def find_games(session: aiohttp.ClientSession, search_string: str) -> list:
    params = {
        'hide': 'dlc',
        'mediaType': 'game',
        'page': '1',
        'sort': 'popularity',
        'search': search_string,
    }
    endpoint = f'{BASE_URL}/games/ajax/filtered'

    async with session.get(endpoint, params=params, cookies=COOKIES) as response:
        data = await response.json()

    try:
        found_games = [
            {
                'title': _get_title(game),
                'thumbnail': _get_thumbnail(game),
                'data_for_details': _get_link(game),
                'platforms': ['pc'],
            }
            for game in data['products']
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
    return game['isComingSoon'] == False


def _get_title(game):
    return game['title']


def _get_thumbnail(game):
    return f"https:{game['image']}.jpg"


def _get_link(game):
    return f"{BASE_URL}{game['url']}"


async def get_details(session: aiohttp.ClientSession, game: dict) -> dict:
    endpoint = game['data_for_details']

    async with session.get(endpoint) as response:
        data = await response.read()

    soup = BeautifulSoup(data, 'html.parser')
    try:
        game_details = {
            'store_name': STORE_NAME,
            'title': game['title'],
            'main_media': _get_main_media(soup),
            'description': _get_description(soup),
            # 'reviews': await _get_game_reviews(session, soup),
            'thumbnail_url': game['thumbnail'],
            'images': _get_images(soup),
            'game_url': endpoint,
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


def _get_description(soup: BeautifulSoup) -> str:
    return "".join(
        str(item) for item in soup.find('div', class_="description").children if item.name != 'div'
    )


def _get_price(soup: BeautifulSoup) -> float:
    price = soup.find(
        'span', class_="product-actions-price__final-amount").text
    if price in ['ZA DARMO', 'FREE']:
        price = 0
    return float(price)


def _get_images(soup: BeautifulSoup) -> list:
    carousel = soup.find_all(
        'source', {'media': "(min-width: 640px) and (max-width: 855px)"})
    return [item['srcset'].split()[0] for item in carousel]


def _get_videos(soup: BeautifulSoup) -> list:
    videos_tags = soup.find_all('iframe', class_='_youtube-iframe')
    videos = []
    if videos_tags:
        for item in videos_tags:
            src = item['src']
            index = src.find('?')
            src = src if index == -1 else src[:index]
            videos.append(src)
    return videos


def _get_main_media(soup: BeautifulSoup) -> dict:
    src = ''
    media_type = ''
    if videos := _get_videos(soup):
        src = videos[0]
        media_type = 'youtube'
    elif images := _get_images(soup):
        src = images[0]
        media_type = 'image'
    return {
        'src': src,
        'type': media_type
    }


async def _get_game_reviews(session: aiohttp.ClientSession, soup: BeautifulSoup) -> dict:
    pid = soup.find('div', class_='layout')['card-product']
    endpoint = f'https://reviews.gog.com/v1/products/{pid}/averageRating'

    async with session.get(endpoint) as response:
        data = await response.json()

    return {
        'votes': data['count'],
        'rating': data['value'] * 2
    }
