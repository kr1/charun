"""This module creates a subclass of twisted.internet.protocol.DatagramProtocol

which is used as the main class of the reactor.
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
    def __init__(self, couchdb_url, db_name, func):
        self.func = func
        self.log = log
        self.couch_connect = CouchDBConnect(couchdb_url, db_name)

    def datagramReceived(self, data, (host, port)):
        """try to create an object from incoming json.

        and check its well-formedness or try to extract a function in order to replace the 
        current function that is applied to incoming data.
        hand over the data to storage by calling the store function on the CouchDBConnection instance.
        this functions is called upon every data reception on the socket the app is listening on.
        """

        self.log.msg("received %r , from %s" % (data, host), logLevel=logging.DEBUG)
        res = None
        try:
            obj = json.loads(data)
            obj["_id"] = repr(time.time())
            obj = self.func(obj)
            origin = (host,port)
            res = self.couch_connect.store(obj, origin)
        except TypeError as error: 
            self.log.err(" - ".join(repr(error).split("\n")))
        except ValueError as error:
            try:
                _data = marshal.loads(data)
                self.func = types.FunctionType(_data, globals(), "some_func_name")
                self.log.msg("received function: %r" % self.func)
            except:
                self.log.err("received undecipherable object")
        return res    

if __name__ == "__main__":
    print "Warning:\nThis module should be run as a twisted application.\nrun with:\ntwistd -y charun_tac.py\n"
    time.sleep(1)
    print "tring to initialize a connection to CouchDB with default url "
    cc = CouchDBConnect("http://localhost:5984","charun")
    print "starting twisted reactor listening for udp-datagrams on localhost:9999"
    reactor.listenUDP(9999, Charun("http://localhost:5984" , "charun", lambda x: x))
    reactor.run()


