import asyncio
import json
import sys

if '../cryptocoins' not in sys.path:
    sys.path.append('../cryptocoins')

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue
from cryptocoins import export_data
from time import time

import json

from autobahn import wamp
from autobahn.asyncio.wamp import ApplicationSession
from cryptocoins.autobahn_autoreconnect import AutoreconnectingApplicationRunner

class PoloniexBookClient(ApplicationSession):

    def __init__(self, *args, **kwargs):
        ApplicationSession.__init__(self, *args, **kwargs)
        self.event_count = 0
        self.events_per_file = 6000
        self.events = []
        self.events_file_queue = Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=20)
        self.currency_pairs = ['BTC_ETH']

    async def onJoin(self, details):
        print('Session Attached')
        for currency_pair in self.currency_pairs:
            subscription = await self.subscribe(self.onBook, currency_pair)
            if isinstance(subscription, wamp.protocol.Subscription):
                print(f"Subscribed to '{subscription.topic}' with id '{subscription.id}'")
            else:
                print(f"Failed to subscribe '{subscription}'")

    def onBook(self, *args, **kwargs):
        self.event_count += 1
        self.events.append({**{"book": list(args), "timestamp" : time()}, "seq" : kwargs["seq"]})
        if self.event_count % self.events_per_file == 0:
            self.events_file_queue.put(self.events)
            self.events = []
            asyncio.get_event_loop().run_in_executor(self.thread_pool, self.export_to_s3)

    def onDisconnect(self):
        print('ERROR: Disconnected')

    def export_to_s3(self):
        book_data = [self.event_to_json(event) for event in self.events_file_queue.get()]
        export_data.upload_to_s3('gly.fish', 'cryptocoins/poloniex/book', book_data)

    def event_to_json(self, event):
        return json.dumps(event)

runner = AutoreconnectingApplicationRunner(u'wss://api.poloniex.com', 'realm1', open_handshake_timeout=90, auto_ping_interval=10, auto_ping_timeout=90)
runner.run(PoloniexBookClient)
