import asyncio
import json
import sys

if '../cryptocoins' not in sys.path:
    sys.path.append('../cryptocoins')

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue
from cryptocoins import export_data
from time import time

from autobahn import wamp
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

class PoloniexBookClient(ApplicationSession):

    def __init__(self, *args, **kwargs):
        ApplicationSession.__init__(self, *args, **kwargs)
        self.event_count = 0
        self.events_per_file = 2000
        self.events = []
        self.events_file_queue = Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=20)
        self.currency_pairs = ['BTC_XMR']

    async def onJoin(self, details):
        print('Session Attached')
        for currency_pair in self.currency_pairs:
            subscription = await self.subscribe(self.onBook, currency_pair)
            if isinstance(subscription, wamp.protocol.Subscription):
                print(f"Subscribed to '{subscription.topic}' with id '{subscription.id}'")
            else:
                print(f"Failed to subscribe '{subscription}'")

    def onBook(self, *args, **kwargs):
        print(f'Event: {args}, {kwargs}')
        self.event_count += 1
        self.events.append(args)
        if self.event_count % self.events_per_file == 0:
            self.events_file_queue.put(self.events)
            self.events = []
            asyncio.get_event_loop().run_in_executor(self.thread_pool, self.export_to_s3)

    def onDisconnect(self):
        print('ERROR: Disconnected')
        asyncio.get_event_loop().stop()

    def export_to_s3(self):
        ticker_data = [self.event_to_json(event) for event in self.events_file_queue.get()]
        export_data.upload_to_s3('gly.fish', 'cryptocoins/poloniex/book', ticker_data)

    def event_to_json(self, event):
        return json.dumps({
            'currency_pair' : 'BTC_ETH',
        })

runner = ApplicationRunner(u'wss://api.poloniex.com', 'realm1')
runner.run(PoloniexBookClient)
