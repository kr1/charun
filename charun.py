import time
import logging
import couchdb
import json
from twisted.application import internet, service
from twisted.internet.protocol import  DatagramProtocol
from twisted.internet import reactor
from twisted.python import log

class Charun(DatagramProtocol):
    def __init__(self,couch_connect):
        self.couch_connect = couch_connect
    def datagramReceived(self, data, (host, port)):
        log.msg("received %r , from %s" % (data, host), logLevel=logging.DEBUG)
        try:
            obj = json.loads(data)
            obj["_id"] = repr(time.time())
            origin = (host,port)
            self.couch_connect.store(obj, origin)
        except TypeError as error: 
            log.err(" - ".join(repr(error).split("\n")))

class CouchConnect():
    from twisted.python import log
    
    def __init__(self, url , db_name):
        self.couch = couchdb.Server(url)
        if db_name not in self.couch.resource.get_json("_all_dbs")[2]: 
            self.db = self.couch.create(db_name)
        else:
            self.db = self.couch[db_name]
    def store(self, _dict, origin):
        if type(_dict).__name__ == "dict":
            log.msg("%s - data:%r" % (origin[0], _dict))
            self.db.save(_dict)
            log.msg("%s - data:%r" % (origin[0], _dict), logLevel=logging.DEBUG)
        else: 
            msg = "object to store must be of type 'dict' but was: '%s'" % (type(_dict).__name__,)
            log.msg("** TypeError: from: %s - msg: %s" % (origin[0], msg), logLevel=logging.ERROR) 


if __name__ == "__main__":
    cc = CouchConnect("http://localhost:5984","charun")
    reactor.listenUDP(9999, Charun(cc))
    reactor.run()


