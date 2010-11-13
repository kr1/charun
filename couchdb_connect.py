import json
import logging
import couchdb
from twisted.python import log

class CouchDBConnect():
    def __init__(self, url="http://localhost:5984" , db_name="charun"):
        self.couch = couchdb.Server(url)
        self.log = log
        try:
            all_dbs = self.couch.resource.get_json("_all_dbs")[2]
        except IOError as (errno, strerror):
            self.log.err("no CouchDB instance is listening on %s, shutting down...." % (url,))
            raise IOError
        if db_name not in all_dbs: 
            self.db = self.couch.create(db_name)
        else:
            self.db = self.couch[db_name]
    def store(self, _dict, origin):
        res = None
        if type(_dict).__name__ == "dict":
            log.msg("%s - data:%r" % (origin[0], _dict))
            res = self.db.save(_dict)
            log.msg("%s - data:%r" % (origin[0], _dict), logLevel=logging.DEBUG)
        else: 
            msg = "object to store must be of type 'dict' but was: '%s'" % (type(_dict).__name__,)
            log.msg("** TypeError: from: %s - msg: %s" % (origin[0], msg), logLevel=logging.ERROR) 
        return res

