import couchdb
import json
from twisted.application import internet, service
from twisted.internet.protocol import  DatagramProtocol
from twisted.internet import reactor

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
        db_name = "charun_usage"
        if db_name not in self.couch.resource.get_json("_all_dbs")[2]: 
            self.db = self.couch.create(db_name)
        else:
            self.db = self.couch[db_name]
    def store(self, _dict, origin):
        if type(_dict).__name__ == "dict":
            self.db.save(_dict)
        else: 
            msg = "object to store must be of type 'dict' but was: '%s'" % (type(_dict).__name__,)
            log.msg("** TypeError: from: %s - msg: %s" % (origin[0], msg), logLevel=logging.ERROR) 


if __name__ == "__main__":
    cc = CouchConnect()
    reactor.listenUDP(9999, Charun(cc))
    reactor.run()


