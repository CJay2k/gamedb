import asyncio

import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend

from api.serializers import GameAllDetailsSerializer
from api.stores import (battlenet, epic_games, gog, nintendo_store, origin,
                        playstation_store, steam, ubisoft)
from asgiref.sync import async_to_sync

STORES = {
    battlenet.STORE_NAME: battlenet,
    epic_games.STORE_NAME: epic_games,
    gog.STORE_NAME: gog,

    # nintendo_store.STORE_NAME: nintendo_store, # TODO

    origin.STORE_NAME: origin,
    playstation_store.STORE_NAME: playstation_store,
    steam.STORE_NAME: steam,

    # ubisoft.STORE_NAME: ubisoft,  # SLOW AF
}


async def search_all_stores(session: aiohttp.ClientSession, search_string: str) -> dict:
    """Combine search results from all stores"""
    actions = [asyncio.ensure_future(
        store.find_games(session, search_string))
        for store in STORES.values()]

    results = await asyncio.gather(*actions)

    return dict(zip(STORES.keys(), results))


@async_to_sync
async def get_details_all_stores(search_string: str) -> list:
    async with CachedSession(cache=SQLiteBackend('stores_cache')) as session:
        found_games = await search_all_stores(session, search_string)

        actions = []
        for k, v in found_games.items():
            if v['status'] == 'success':
                actions.extend(asyncio.ensure_future(
                    STORES[k].get_details(session, game)) for game in v['data'])

        data = await asyncio.gather(*actions)
    return data


def fetch_data_from_stores(search_string: str) -> list:
    found_games = get_details_all_stores(search_string)

    for game in found_games:
        if game['status'] == 'success':
            data = game['data']
            serializer = GameAllDetailsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.data)
                print(serializer.errors)

    return found_games
