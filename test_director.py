import unittest
import tests.unittest_charun as ut_char




if __name__ == "__main__":
    
    unittest.TextTestRunner(verbosity=2).run(ut_char.suite())
