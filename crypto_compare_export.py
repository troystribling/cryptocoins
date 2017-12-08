import asyncio

from concurrent.futures import ThreadPoolExecutor

from cryptocoins.crypto_compare.export import request_coin_list
from cryptocoins.crypto_compare.export import request_coin_snapshot
from cryptocoins.crypto_compare.export import request_coin_price_history
from cryptocoins.crypto_compare.export import request_top_currency_pairs

from cryptocoins.models.coins import Coins
from cryptocoins.models.collections import Collections
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory

thread_pool = ThreadPoolExecutor(max_workers=20)
loop = asyncio.get_event_loop()

# pollers
async def poll_coin_list():
        while True:
            loop.run_in_executor(thread_pool, request_coin_list)
            await asyncio.sleep(86400)


async def poll_coin_snapshot(coin_limit):
    while True:
        for coin in Coins.select().order_by(Coins.rank.asc()).limit(coin_limit):
            loop.run_in_executor(thread_pool, request_coin_snapshot, coin)
            await asyncio.sleep(60)
        await asyncio.sleep(300)


if __name__ == "__main__":
    loop.run_until_complete(asyncio.gather(poll_coin_list(), poll_coin_snapshot(10)))
