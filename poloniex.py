import asyncio
from multiprocessing import Queue

from autobahn import wamp
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

class PoloniexWAMPClient(ApplicationSession):

    def __init__(self, *args, **kwargs):
        ApplicationSession.__init__(self, *args, **kwargs)
        self.ticker_event_count = 0
        self.ticker_events_per_file = 2000
        self.ticker_events = []
        self.ticker_events_file_queue = Queue()

    async def onJoin(self, details):
        print("Session Attached")
        subscriptions = await self.subscribe(self)
        for subscription in subscriptions:
            if isinstance(subscription, wamp.protocol.Subscription):
                print(f"Subscribed to '{subscription.topic}' with id '{subscription.id}'")
            else:
                print(f"Failed to subscribe {subscription}")

    @wamp.subscribe(u"ticker")
    def onTicker(*args, **kwargs):
        print(f"Got Event {args}, {kwargs}")
        self.ticker_event_count = self.ticker_event_count + 1
        if self.ticker_event_count % self.ticker_events_per_file == 0:
            self.ticker_events_file_queue.put(self.ticker_events)
            self.ticker_events = []
            self.upload_to_s3()

    def onDisconnect(self):
        print("Disconnected")
        asyncio.get_event_loop().stop()

    def upload_to_s3():
        print("Upload file to s3")

runner = ApplicationRunner(u"wss://api.poloniex.com", "realm1")
runner.run(PoloniexWAMPClient)
