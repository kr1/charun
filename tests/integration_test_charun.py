import unittest
import marshal
import time
import json
import client
from charun import Charun
from couchdb_connect import CouchDBConnect
import charun_tac
class integrationTestCharun(unittest.TestCase):
    """a test class for the Charun module"""
    def setUp(self):
        """
        set up data used in the tests.

        this method is called before each test function execution.
        """
        self.charun = Charun(charun_tac.couchdb_url, charun_tac.test_db_name, charun_tac.initial)
        self.cc = self.charun.couch_connect

    def test_20_receive_data(self):
        """test data reception: json-dict-object gets written, other json strings not"""
        # this data has to be written to the db
        bef = self.cc.db.info()["doc_count"]
        self.charun.datagramReceived('{"122":"erre"}', ("localhost", 30000))
        after = self.cc.db.info()["doc_count"]
        self.assertNotEqual(bef, after) 
        # this data must not be written to the db (not castable to dict-type)
        bef = self.cc.db.info()["doc_count"]
        self.charun.datagramReceived('122', ("localhost", 30000))
        after = self.cc.db.info()["doc_count"]
        self.assertEqual(bef, after) 

    def test_30_receive_function(self):
        """test function reception: a serialized function string gets integrated and applied.
        
        nothing is written to the DB and
        finally a modified functionality is observed.
        """
        bef = self.cc.db.info()["doc_count"]
        self.charun.datagramReceived(marshal.dumps(charun_tac.test_initial.func_code), ("localhost", 30000))
        after = self.cc.db.info()["doc_count"]
        self.assertEqual(bef,after) 
        #time.sleep(1)
        id, ref = self.charun.datagramReceived('{"122":"erre"}', ("localhost", 30000))
        doc = self.cc.db.get(id)
        self.assertEqual(doc['122'],'erreerre')

    def test_10_write_data_to_the_db(self):
        """test successful writing to the db by comparing the doc-count before and after"""
        bef = self.cc.db.info()["doc_count"]
        self.charun.datagramReceived('{"122":"erre"}', ("localhost", 30000))
        after = self.cc.db.info()["doc_count"]
        self.assertNotEqual(bef,after) 

def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(integrationTestCharun))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())




