from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

class PoloniexWAMPClient(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("Session Attached")
        subscriptions = yield self.subscribe(self)
        for subscription in subscriptions:
            if isinstance(subscription, wamp.protocol.Subscription):
                print(f"Subscribed to '{subscription.topic}' with id '{subscription.id}'")
            else:
                print(f"Failed to subscribe {subscription}")

    @wamp.subscribe(u"ticker")
    def onTicker(*args, **kwargs):
        print(f"Got Event {args}, {kwargs}")

    def onUserError(self, fail, msg):
        ApplicationSession.onUserError(self, fail, msg)
        print("Disconnecting")
        self.disconnect()

    def onDisconnect(self):
        print("Disconnected")
        reactor.stop()

runner = ApplicationRunner(u"wss://api.poloniex.com", "realm1")
runner.run(PoloniexWAMPClient)
