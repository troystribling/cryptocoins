import asyncio
import aiohttp
import sys

if '../cryptocoins' not in sys.path:
    sys.path.append('../cryptocoins')

from cryptocoins import import_data

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)

poll_seconds = 10.0

async def poll():
    while True:
        content = await import_data.http_get(session, 'https://poloniex.com/public?command=return24hVolume')
        print(content)
        await asyncio.sleep(poll_seconds)

loop.run_until_complete(poll())
