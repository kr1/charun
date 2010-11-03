"""This module creates a subclass of twisted.internet.protocol.DatagramProtocol

whis is used as the main class of the reactor.
Public methods:
datagramReceived -- try to create an object from json and check its well-formedness or try to extract a function in order to replace the current. 
"""

import marshal
import time
import types
import logging
import couchdb
import json
from twisted.application import internet, service
from twisted.internet.protocol import  DatagramProtocol
from twisted.internet import reactor
from twisted.python import log
from couchdb_connect import CouchDBConnect

class Charun(DatagramProtocol):
    def __init__(self, couch_connect, func):
        self.func = func
        self.couch_connect = couch_connect
    def datagramReceived(self, data, (host, port)):
        """try to create an object from incoming json.

        and check its well-formedness or try to extract a function in order to replace the 
        current function that is applied to incoming data.
        hand over the data to storage by calling the store function on the CouchDBConnection instance.
        this functions is called upon every data reception on the socket the app is listening on.
        """

        log.msg("received %r , from %s" % (data, host), logLevel=logging.DEBUG)
        res = None
        try:
            obj = json.loads(data)
            obj["_id"] = repr(time.time())
            obj = self.func(obj)
            origin = (host,port)
            res = self.couch_connect.store(obj, origin)
        except TypeError as error: 
            log.err(" - ".join(repr(error).split("\n")))
        except ValueError as error:
            try:
                _data = marshal.loads(data)
                self.func = types.FunctionType(_data, globals(), "some_func_name")
                log.msg("received function: %r" % self.func)
            except:
                log.err("received undecipherable object")
        return res    

if __name__ == "__main__":
    cc = CouchDBConnect("http://localhost:5984","charun")
    reactor.listenUDP(9999, Charun(cc, lambda x: x))
    reactor.run()


