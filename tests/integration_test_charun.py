"""integration tests for the charun class"""

import unittest2 as unittest
import marshal

import charun_tac
from charun import Charun


class integrationTestCharun(unittest.TestCase):
    """a integration-test class for the Charun module"""
    def setUp(self):
        """
        set up data used in the tests.

        this method is called before each test function execution.
        """
        self.charun = Charun(charun_tac.couchdb_url, charun_tac.test_db_name,
                             charun_tac.initial)
        self.cc = self.charun.couch_connect

    def test_20_receive_data(self):
        """test data reception: json-dict-object gets written

        other json strings not."""
        # this data has to be written to the db
        count_diff = self.call_and_compare_count(self.charun.datagramReceived,
                                                 ['{"122": "erre"}',
                                                 ("localhost", 30000)])
        self.assertNotEqual(*count_diff)
        # this data must not be written to the db (not castable to dict-type)
        count_diff = self.call_and_compare_count(self.charun.datagramReceived,
                                                 ['122', ("localhost", 30000)])
        self.assertEqual(*count_diff)
        count_diff = self.call_and_compare_count(self.charun.datagramReceived,
                                                 ['[122, 123, 124]', ("localhost", 30000)])
        self.assertEqual(*count_diff)

    def test_30_receive_function(self):
        """test function reception: a serialized function string gets
        integrated and applied.

        nothing is written to the DB and
        finally a modified functionality is observed.
        """
        count_diff = self.call_and_compare_count(self.charun.datagramReceived,
                            [marshal.dumps(charun_tac.test_initial.func_code),
                            ("localhost", 30000)])
        self.assertEqual(*count_diff)
        #time.sleep(1)
        id, ref = self.charun.datagramReceived('{"122": "erre"}',
                                              ("localhost", 30000))
        doc = self.cc.db.get(id)
        self.assertEqual(doc['122'], 'erreerre')

    def test_10_write_data_to_the_db(self):
        """test successful writing to the db by comparing the
        doc-count before and after"""
        count_diff = self.call_and_compare_count(self.charun.datagramReceived,
                                                ['{"122": "erre"}',
                                                ("localhost", 30000)])
        self.assertNotEqual(*count_diff)

    def call_and_compare_count(self, callable, *args):
        bef = self.cc.db.info()["doc_count"]
        apply(callable, *args)
        after = self.cc.db.info()["doc_count"]
        return bef, after


def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(integrationTestCharun))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
