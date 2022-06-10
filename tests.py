"""
Usage:
- to run all tests:
    - cd to `primo_functional_tests` directory
    - $ python3 ./tests.py
- to run one test:
    - cd to `primo_functional_tests` directory
    - example: $ python3 ./tests.py SomeTest.test_something
"""

import datetime, logging, os, sys, unittest

import run_selenium_tests

# sys.path.append( os.environ['(enclosing-project-path)'] )
# from primo_functional_tests.lib.module import SomeClass


LOG_PATH: str = os.environ['PRIMO_F_TESTS__LOG_PATH']

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.debug( 'test-logging ready' )


class MiscTest( unittest.TestCase ):

    def setUp( self ):
        pass

    def test_prep_end_range_column(self):
        self.assertEqual( 'B', run_selenium_tests.prep_end_range_column(2) )
        self.assertEqual( 'E', run_selenium_tests.prep_end_range_column(5) )


if __name__ == '__main__':
  unittest.main()
