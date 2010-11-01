import json
import logging
import couchdb
from twisted.python import log

class CouchDBConnect():
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


