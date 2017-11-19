from time import sleep
import asyncio
from concurrent.futures import ThreadPoolExecutor

from cryptocoins import export_data
from cryptocoins.models.coins import Coins

thread_pool = ThreadPoolExecutor(max_workers=20)
loop = asyncio.get_event_loop()
