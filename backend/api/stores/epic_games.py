import traceback
from datetime import datetime
from urllib.parse import urlparse
import aiohttp
import markdown2

STORE_NAME = 'Epic Games'
HEADERS = {'Content-type': 'application/json; charset=UTF-8'}

ENDPOINT = 'https://graphql.epicgames.com/graphql'
BASE_URL = 'https://store-content.ak.epicgames.com/api/pl/content/products'

SEARCH_QUERY = "query searchStoreQuery($allowCountries: String, $category: String, $count: Int, $country: String!, $keywords: String, $locale: String, $namespace: String, $withMapping: Boolean = false, $itemNs: String, $sortBy: String, $sortDir: String, $start: Int, $tag: String, $releaseDate: String, $withPrice: Boolean = false, $withPromotions: Boolean = false, $priceRange: String, $freeGame: Boolean, $onSale: Boolean, $effectiveDate: String) {\n  Catalog {\n    searchStore(\n      allowCountries: $allowCountries\n      category: $category\n      count: $count\n      country: $country\n      keywords: $keywords\n      locale: $locale\n      namespace: $namespace\n      itemNs: $itemNs\n      sortBy: $sortBy\n      sortDir: $sortDir\n      releaseDate: $releaseDate\n      start: $start\n      tag: $tag\n      priceRange: $priceRange\n      freeGame: $freeGame\n      onSale: $onSale\n      effectiveDate: $effectiveDate\n    ) {\n      elements {\n        title\n        id\n        namespace\n        description\n        effectiveDate\n        keyImages {\n          type\n          url\n        }\n        currentPrice\n        seller {\n          id\n          name\n        }\n        productSlug\n        urlSlug\n        url\n        tags {\n          id\n        }\n        items {\n          id\n          namespace\n        }\n        customAttributes {\n          key\n          value\n        }\n        categories {\n          path\n        }\n        offerMappings @include(if: $withMapping) {\n          pageSlug\n          pageType\n        }\n        price(country: $country) @include(if: $withPrice) {\n          totalPrice {\n            discountPrice\n            originalPrice\n            voucherDiscount\n            discount\n            currencyCode\n            currencyInfo {\n              decimals\n            }\n            fmtPrice(locale: $locale) {\n              originalPrice\n              discountPrice\n              intermediatePrice\n            }\n          }\n          lineOffers {\n            appliedRules {\n              id\n              endDate\n              discountSetting {\n                discountType\n              }\n            }\n          }\n        }\n        promotions(category: $category) @include(if: $withPromotions) {\n          promotionalOffers {\n            promotionalOffers {\n              startDate\n              endDate\n              discountSetting {\n                discountType\n                discountPercentage\n              }\n            }\n          }\n          upcomingPromotionalOffers {\n            promotionalOffers {\n              startDate\n              endDate\n              discountSetting {\n                discountType\n                discountPercentage\n              }\n            }\n          }\n        }\n      }\n      paging {\n        count\n        total\n      }\n    }\n  }\n}\n"
DETAILS_QUERY = "query catalogQuery($productNamespace: String!, $offerId: String!, $locale: String, $country: String!, $includeSubItems: Boolean!) {\n  Catalog {\n    catalogOffer(namespace: $productNamespace, id: $offerId, locale: $locale) {\n      title\n      id\n      namespace\n      description\n      effectiveDate\n      expiryDate\n      isCodeRedemptionOnly\n      keyImages {\n        type\n        url\n      }\n      seller {\n        id\n        name\n      }\n      productSlug\n      urlSlug\n      url\n      tags {\n        id\n      }\n      items {\n        id\n        namespace\n      }\n      customAttributes {\n        key\n        value\n      }\n      categories {\n        path\n      }\n      offerMappings {\n        pageSlug\n        pageType\n      }\n      price(country: $country) {\n        totalPrice {\n          discountPrice\n          originalPrice\n          voucherDiscount\n          discount\n          currencyCode\n          currencyInfo {\n            decimals\n          }\n          fmtPrice(locale: $locale) {\n            originalPrice\n            discountPrice\n            intermediatePrice\n          }\n        }\n        lineOffers {\n          appliedRules {\n            id\n            endDate\n            discountSetting {\n              discountType\n            }\n          }\n        }\n      }\n    }\n    offerSubItems(namespace: $productNamespace, id: $offerId) @include(if: $includeSubItems) {\n      namespace\n      id\n      releaseInfo {\n        appId\n        platform\n      }\n    }\n  }\n}\n"


async def find_games(session: aiohttp.ClientSession, search_string: str) -> list:
    variables = {
        'category': 'games/edition/base',
        'count': 30,
        'country': 'PL',
        'locale': 'pl',
        'sortDir': 'DESC',
        'allowCountries': 'PL',
        'start': 0,
        'tag': '',
        'withMapping': False,
        'withPrice': True,
        'keywords': search_string,
    }

    async with session.post(ENDPOINT, json={'query': SEARCH_QUERY, 'variables': variables},
                            headers=HEADERS) as response:
        data = await response.json()

    try:
        found_games = [
            {
                'title': _get_title(game),
                'thumbnail': _get_thumbnail(game),
                'data_for_details': _get_slug(game),
                'platforms': ['pc'],
            }
            for game in data['data']['Catalog']['searchStore']['elements']
            if _get_slug(game) and _is_released(game) and _is_title_matching_search_string(search_string, game)
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
    return game['title']


def _is_released(game):
    date = datetime.fromisoformat(game['effectiveDate'][:-1])
    return date <= datetime.now()


def _get_slug(game):
    return slug.split('/')[0] if (slug := game['productSlug']) else None


def _get_thumbnail(game):
    for image in game['keyImages']:
        if image['type'] == 'OfferImageWide':
            return image['url'].replace(' ', '%20')
    return game['keyImages'][0]['url']


async def get_details(session: aiohttp.ClientSession, game: dict) -> dict:
    slug = game['data_for_details']
    endpoint = f'{BASE_URL}/{slug}'

    async with session.get(endpoint) as response:
        data = await response.json()

    try:
        product = _get_product(data)
        product_namespace = _get_product_namespace(data)
        offer_id = _get_offer_id(data)
        game_details = {
            'store_name': STORE_NAME,
            'title': game['title'],
            'main_media': await _get_main_media(session, product),
            'description': _get_description(product),
            # 'reviews': await _get_game_reviews(session, slug),
            'thumbnail_url': game['thumbnail'],
            'images': _get_images(product),
            'game_url': _get_link(slug),
            'price': await _get_price(session, product_namespace, offer_id),
            'platforms': game['platforms']
        }
    except Exception as e:
        print(game['data_for_details'])
        traceback.print_exc()
        return {'status': 'failed'}

    return {
        'status': 'success',
        'data': game_details
    }


def _get_product(data):
    for item in data['pages']:
        if item['_title'] in ['home', 'strona główna']:
            return item
    return data['pages'][0]


def _get_product_namespace(data):
    for item in data['pages']:
        if item['_title'] == 'home':
            return item['offer']['namespace']
    return data['pages'][0]['offer']['namespace']


def _get_offer_id(data):
    for item in data['pages']:
        if item['_title'] == 'home':
            return item['offer']['id']
    return data['pages'][0]['offer']['id']


def _get_link(slug):
    return f'https://www.epicgames.com/store/pl/p/{slug}'


def _get_description(product):
    description = product['data']['about']['description']
    return markdown2.markdown(description)


def _get_images(product):
    return [
        image['src'] for image in product['data'].get('gallery', {}).get('galleryImages', [])
    ] or [
        item['image']['src'] for item in product['data']['carousel'].get('items', []) if
        True not in item['video'].values()
    ]


async def _get_main_media(session: aiohttp.ClientSession, product):
    src = ''
    media_type = ''
    # if video := await _get_videos(session, product):
    #     src = video
    #     media_type = 'video'
    # else:
    for item in product['data']['carousel'].get('items', []):
        if True not in item['video'].values() and item['image'].get('src'):
            src = item['image']['src']
            media_type = 'image'
            break
    return {
        'src': src,
        'type': media_type
    }


# async def _get_videos(session: aiohttp.ClientSession, product):
#     media_ref_id = ''
#     for item in product['data']['carousel'].get('items', []):
#         if item['video'].get('recipes'):
#             recipes = json.loads(item['video'].get('recipes')).get('pl') or json.loads(
#                 item['video'].get('recipes')).get('en-US')
#             for recipe in recipes:
#                 if recipe['recipe'] == 'video-webm':
#                     media_ref_id = recipe['mediaRefId']
#             break

#     params = {
#         'operationName': 'getVideo',
#         'variables': '{"mediaRefId": "' + media_ref_id + '"}',
#         'extensions': '{"persistedQuery": {"version": 1, "sha256Hash": "e631c6a22d716a93d05bcb023b0ef4ade869f5c2c241d88faf9187b51b282236"}}'
#     }
#     if media_ref_id:
#         async with session.get(ENDPOINT, params=params) as response:
#             data = await response.json()
#         with open('xd.json', 'w') as f:
#             f.write(json.dumps(data))
#         for item in data['data']['Media']['getMediaRef']['outputs']:
#             if item['key'] == 'high':
#                 return item['url']


async def _get_price(session: aiohttp.ClientSession, product_namespace, offer_id):
    variables = {
        'productNamespace': product_namespace,
        'offerId': offer_id,
        'locale': 'pl',
        'country': 'PL',
        'lineOffers': [{'offerId': f'{offer_id}', 'quantity': 1}],
        'calculateTax': False,
        'includeSubItems': True
    }

    async with session.post(ENDPOINT, json={'query': DETAILS_QUERY, 'variables': variables},
                            headers=HEADERS) as response:
        data = await response.json()

    return data['data']['Catalog']['catalogOffer']['price']['totalPrice'].get('discountPrice', 0) / 100


async def _get_game_reviews(session: aiohttp.ClientSession, slug) -> dict:
    sku = f'EPIC_{slug}'
    params = {
        'operationName': 'getCriticReviews',
        'variables': '{"sku": "' + sku + '", "includeMeta": true}',
        'extensions': '{"persistedQuery": {"version": 1, "sha256Hash": "c0568107dc6ae2c7cb5052d3bc5429a3d3a178803287db6006a7ec662dc8d9a5"}}'
    }

    async with session.get(ENDPOINT, params=params) as response:
        data = await response.json()

    result_list = data.get('data').get('OpenCritic').get('productReviews')
    if not result_list:
        return {}

    rating = result_list['openCriticScore'] / \
        10 if result_list['openCriticScore'] else 0
    votes = result_list['reviewCount']

    return {
        'votes': votes,
        'rating': rating
    }
