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

class PoloniexTickerClient(ApplicationSession):

    def __init__(self, *args, **kwargs):
        ApplicationSession.__init__(self, *args, **kwargs)
        self.event_count = 0
        self.events_per_file = 6000
        self.events = []
        self.events_file_queue = Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=20)

    async def onJoin(self, details):
        print('Session Attached')
        subscriptions = await self.subscribe(self)
        for subscription in subscriptions:
            if isinstance(subscription, wamp.protocol.Subscription):
                print(f"Subscribed to '{subscription.topic}' with id '{subscription.id}'")
            else:
                print(f"Failed to subscribe '{subscription}'")

    @wamp.subscribe(u"ticker")
    def onTicker(self, *args, **kwargs):
        self.event_count += 1
        self.events.append(args + (time(),))
        if self.event_count % self.events_per_file == 0:
            self.events_file_queue.put(self.events)
            self.events = []
            asyncio.get_event_loop().run_in_executor(self.thread_pool, self.export_to_s3)

    def onDisconnect(self):
        print('ERROR: Disconnected')
        asyncio.get_event_loop().stop()

    def export_to_s3(self):
        ticker_data = [self.event_to_json(event) for event in self.events_file_queue.get()]
        export_data.upload_to_s3('gly.fish', 'cryptocoins/poloniex/ticker', ticker_data)

    def event_to_json(self, event):
        return json.dumps({
            'currency_pair' : event[0],
            'last' : event[1],
            'lowest_ask' : event[2],
            'highest_bid' : event[3],
            'percent_change' : event[4],
            'base_volume' : event[5],
            'quote_volume' : event[6],
            'is_frozen' : event[7],
            '24_hr_high' : event[8],
            '24_hr_low' : event[9],
            'timestamp' : event[10]
        })

runner = ApplicationRunner(u'wss://api.poloniex.com', 'realm1')
runner.run(PoloniexTickerClient)
