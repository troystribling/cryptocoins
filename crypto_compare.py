from time import sleep
import asyncio

from cryptocoins import export_data


async def poll_daily():
        coin_list()
        await asyncio.sleep(86400)


async def poll_hourly():
    await asyncio.sleep(3600)


def coin_list():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    print(f"FETCH COIN LIST FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_list', [result])
    else:
        print("coint_list request failed")


def coin_compare():
    results = []
    currencies = [1182, 7605]
    for currency in currencies:
        url = f'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={currency}'
        print(f"FETCH COIN SNAP SHOT FROM: {url}")
        result = export_data.getURL(url)
        if result is not None:
            results.append(result)
            sleep(1)
    if results:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_compare', results)
    else:
        print("REQUESTS HAVE NO RESULTS")


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(poll_daily(), poll_hourly()))
loop.close()
