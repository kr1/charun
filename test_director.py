"""this script orchestrates the tests contained in the tests folder"""
import sys
import unittest2 as unittest
import tests.integration_test_charun as i_t_charun
import tests.unit_test_charun as u_t_charun

if __name__ == "__main__":
    uniT, integratioN = False, False
    print "script called with %r arguments" % sys.argv
    la = len(sys.argv) 
    if  la == 1:
        uniT,integratioN = True,True
    elif la > 1:
        what = sys.argv[1]
        if what == "unit": uniT = True
        elif what == "integration": integratioN = True
        else: print "Usage:\ncall the script with 'unit' XOR 'integration' arguments to run only the specified test-suite.\ncalling it without arguments will result in running all tests."
    if integratioN:
        print "starting integration tests...\n-----------------------------"
        unittest.TextTestRunner(verbosity=2).run(i_t_charun.suite())
    if uniT:
        print "starting unit tests...\n---------------------------"
        unittest.TextTestRunner(verbosity=2).run(u_t_charun.suite())
        unittest.TextTestRunner(verbosity=2).run(u_t_cc.suite())
