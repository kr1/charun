"""unit tests for the charun module

as the Charun class is a subclass of twisted.internet.protocol.DatagramProtocol
only the <datagramReceived> method is tested
"""
import unittest
import marshal
import time
import json
import client
from mock import Mock
from charun import Charun
from couchdb_connect import CouchDBConnect
import charun_tac

class testCharun(unittest.TestCase):
    """a test class for the Charun module"""
    def setUp(self):
        """
        set up data used and mock objects/methods in the tests.

        this method is called before each test function execution.
        """
        charun_tac.initial = Mock()
        charun_tac.initial.return_value == "transformed obj"
        self.charun = Charun(charun_tac.couchdb_url, charun_tac.db_name, charun_tac.initial)
        self.charun.couch_connect = Mock()
        self.charun.log = Mock()

    def test_10_receive_data(self):
        """test data reception: json-dict-object gets written"""
        self.charun.datagramReceived('{"122":"erre"}', ("localhost", 30000))
        self.assertTrue(self.charun.log.msg.called)
        self.assertTrue(self.charun.couch_connect.store.called, "storage function should have been called, but was not")

    def test_20_receive_data(self):
        """test data reception: json-non-dict-object does not get written"""
        self.charun.datagramReceived('122', ("localhost", 30000))
        self.assertTrue(self.charun.log.err.called)
        self.assertTrue(self.charun.log.msg.called)
        self.assertFalse(self.charun.couch_connect.store.called, "storage function has been erroneously called")
        #print self.charun.log.err.assert_called_with()

    def test_30_receive_data(self):
        """test data reception: non json object gets written"""
        self.charun.datagramReceived(122, ("localhost", 30000))
        self.assertTrue(self.charun.log.msg.called)
        self.assertFalse(self.charun.couch_connect.store.called, "storage function has been erroneously called")

    def test_40_receive_function(self):
        """test function reception: a serialized function string gets integrated."""
        self.charun.datagramReceived(marshal.dumps(charun_tac.test_initial.func_code), ("localhost", 30000))
        self.assertFalse(self.charun.log.err.called)
        self.assertFalse(self.charun.couch_connect.store.called, "storage function has been erroneously called")
        self.assertEqual(self.charun.func({}), charun_tac.test_initial({}))

def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testCharun))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())




