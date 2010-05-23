from stompservice import StompClientFactory
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from random import random
from orbited import json

from SimpleXMLRPCServer import *
from threading import Thread




INTERVAL = 1000
CHANNEL_NAME = "/topic/message"

class DataProducer(StompClientFactory):
    def recv_connected(self, msg):
        print 'Connected; producing data'


    # the next two lines are probably the biggest workaround
    # for the weirdest bug I've seen in my entire life
    # it repeatedly calls a function that absolutely does nothing
    # however, if I remove them, there's a ten second delay
    # between when the DataProducer transmits a message to
    # when the browser actually receives the data. Me and my
    # friend were mindfucked thinking about how something like
    # this could possibly happen. But right now we are more worried
    # about the rest of the code
        self.timer = LoopingCall(self.send_data)
        self.timer.start(INTERVAL/1000.0)

    def send_data(self):
        self.send(CHANNEL_NAME, json.encode({'text':'test string'}))

#    def send_data(self, channel, data):
#        print "Transmitting: ", data
#    # modify our data elements
#        self.send(channel, json.encode(data))

#    def test_data(self):
#        # WHAT THE F***?
#        pass





class RPCServer(Thread):
    def __init__(self, orbited):
        print 'rpc server init...'
        self.orbited = orbited
        Thread.__init__(self)
    def run(self):
        class RequestHandler(SimpleXMLRPCRequestHandler):
            rpc_paths = ('/topic/message',)
        #create a server
        server = SimpleXMLRPCServer(("localhost",8045),requestHandler = RequestHandler)

        server.register_introspection_functions()

    def transmit_orbited(channel, message):
        """
        @param channel: The stomp channel to send to
        @param message: The message that needs to be transmitted
        """
        print '--=========--'
        self.orbited.send_data(channel, message)
        return ""

        server.register_function(transmit_orbited, 'transmit')
        server.serve_forever()

rpcthread = RPCServer(DataProducer())
rpcthread.start()

reactor.connectTCP('localhost', 61613, DataProducer())
reactor.run()

