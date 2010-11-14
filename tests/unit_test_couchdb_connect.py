"""unit tests for the CouchDBConnect class"""

import unittest2 as unittest
import socket
import marshal
import client
import couchdb
from mock import Mock
from couchdb_connect import CouchDBConnect
import charun_tac

class testCouchDBConnect(unittest.TestCase):
    """a unit-test class for the CouchDBConnect class"""
    def setUp(self):
        """
        set up data used and mock objects/methods in the tests.

        this method is called before each test function execution.
        """
        self.cc = Mock()
        charun_tac.initial = Mock()
        charun_tac.initial.return_value == "transformed obj"

    def test_10_create_instance(self):
        """couchdb_connect: test that a couchdbconnect instance is created"""
        cc = CouchDBConnect()
        self.assertTrue(cc)

    def test_12_failing_create_instance_without_couchdb_running(self):
        """couchdb_connect: test that no couchdbconnect instance is created without couch listening"""
        self.assertRaises(IOError, CouchDBConnect,"http://localhost:8899","should have raised an error but didn't")
    
    def test_20_store_dict(self):
        """an incoming dict should get stored"""
        cc = CouchDBConnect()
        cc.db = Mock()
        cc.store({12:13},("localhost",30000))
        self.assertTrue(cc.db.save.called)
         
    def test_30_do_not_store_non_dict(self):
        """an incoming non-dict should not get stored and an error message written"""
        cc = CouchDBConnect()
        cc.db = Mock()
        cc.log = Mock()
        cc.store("am I a dict?",("localhost",30000))
        self.assertFalse(cc.db.save.called)
        self.assertFalse(cc.log.msg.called)
        self.assertTrue(cc.log.err.called)



def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testCouchDBConnect))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())




