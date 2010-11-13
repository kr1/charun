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
        cc = Mock()
        charun_tac.initial = Mock()
        charun_tac.initial.return_value == "transformed obj"

    def test_10_create_instance(self):
        """couchdb_connect: test that a couchdbconnect instance is created"""
        cc = CouchDBConnect()
        self.assertTrue(cc)

    def test_12_failing_create_instance_without_couchdb_running(self):
        """couchdb_connect: test that no couchdbconnect instance is created without couch listening"""
        self.assertRaises(IOError, CouchDBConnect,"http://localhost:8899","should have raised an error but didn't")

    def est_20_receive_data(self):
        """test data reception: json-non-dict-object does not get written"""
        self.charun.datagramReceived('122', ("localhost", 30000))
        self.assertTrue(self.charun.log.err.called)
        self.assertTrue(self.charun.log.msg.called)
        self.assertFalse(self.charun.couch_connect.store.called, "storage function has been erroneously called")
        #print self.charun.log.err.assert_called_with()

    def est_30_receive_data(self):
        """test data reception: non json object gets written"""
        self.charun.datagramReceived(122, ("localhost", 30000))
        self.assertTrue(self.charun.log.msg.called)
        self.assertFalse(self.charun.couch_connect.store.called, "storage function has been erroneously called")

    def est_40_receive_function(self):
        """test function reception: a serialized function string gets integrated."""
        self.charun.datagramReceived(marshal.dumps(charun_tac.test_initial.func_code), ("localhost", 30000))
        self.assertFalse(self.charun.log.err.called)
        self.assertFalse(self.charun.couch_connect.store.called, "storage function has been erroneously called")
        self.assertEqual(self.charun.func({}), charun_tac.test_initial({}))

def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testCouchDBConnect))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())




