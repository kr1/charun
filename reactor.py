import couchdb
import json
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Charun(DatagramProtocol):
    def __init__(self,couch_connect):
        self.couch_connect = couch_connect
    def datagramReceived(self, data, (host, port)):
        print "received %r , from %s:%d" % (data, host, port)
        obj = json.loads(data)
        print "received %r ,transformed it to %r , from %s:%d" % (data, obj, host, port)
        self.couch_connect.store(obj)
        #self.transport.write(data, (host, port))

class CouchConnect():
    def __init__(self, url = "http://localhost:5984"):
        self.couch = couchdb.Server(url)
        db_name = "charun_usage"
        if db_name not in self.couch.resource.get_json("_all_dbs")[2]: 
            self.db = self.couch.create(db_name)
        else:
            self.db = self.couch[db_name]
    def store(self, _dict):
        if type(_dict).__name__ == "dict":
            self.db.save(_dict)
        else: 
            raise TypeError("object to store must be of type 'dict'\nwas: %s" % type(_dict).__name__)
            
        

if __name__ == "__main__":
    cc = CouchConnect()
    reactor.listenUDP(9999, Charun(cc))
    reactor.run()


