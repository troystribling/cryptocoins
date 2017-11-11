import asyncio

from cryptocoins import export_data


async def poll_coinlist():
        coin_list()
        await asyncio.sleep(86400)


async def poll_coin_snapshot_full():
    currencies = [1182, 7605]
    for currency in currencies:
        coin_snapshot_full(currency)
        await asyncio.sleep(10)


def coin_list():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    print(f"FETCH COIN LIST FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_list', [result])
    else:
        print("coint_list request failed")


def coin_snapshot_full(currency):
    url = f'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={currency}'
    print(f"FETCH COIN SNAP SHOT FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_snapshot_full', [result])
    else:
        print("coint_list request failed")


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(poll_coinlist(), poll_coin_snapshot_full()))
loop.close()
