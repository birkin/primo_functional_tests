"""
Flow...
- get arguments (eppn, password, dev-or-prod-instance)
- load desired url-data
- load random url-data (get random mms-ids, then build urls)
- process urls asyncronously, checking:
  - that 'status' is one of expected values
  - that 'location' is one of expected values
  - that 'material-type' is one of expected value  ???
  - that given the 'status', 'location', and 'material-type', 
    the proper links exist at the bib-level and item-level

Question(s)...
- Would the Primo-API indicate bib-level and item-level custom links?
"""

import argparse, logging, os

from selenium import webdriver

LOG_PATH: str = os.environ['PRIMO_F_TESTS__LOG_PATH']

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.debug( 'logging ready' )


METADATA_TO_TEST = {
    'possible_locations': [ 'rock', 'scili', 'annex' ],
    'possible_statuses': [ 'Out of library', 'Available' ]
}

BIBS_TO_TEST = [
    {'comment': 'ZMM audio', 'mmsid': '991007439769706966'},
    # {'comment': 'ZMM with two items', 'mmsid': '991007439769706966'},
    # {'comment': 'ZMM with one item', 'mmsid': '991023827329706966'}
]

URL_PATTERN = 'https://bruknow.library.brown.edu/discovery/fulldisplay?docid=alma{mmsid}&context=L&vid=01BU_INST:BROWN&lang=en'


# driver = webdriver.Firefox()

def test_bibs( auth_id: str, password: str, server_type: str ) -> None:
    """" Main controller; calls loop. """
    for bib_dct in BIBS_TO_TEST:
        result: str = process_bib( bib_dct )
        ## do something with result
    return


def process_bib( bib_dct: dict ) -> str:
    """ Controller for individual bib-processing.
        Called by test_bibs() """
    driver = webdriver.Firefox()  # type: ignore
    log.debug( 'driver created' )
    url: str = URL_PATTERN.replace( '{mmsid}', bib_dct['mmsid'] )
    log.debug( f'url, ``{url}``' )
    log.debug( 'about to call url' )
    driver.get( url )
    log.debug( 'about to get page_source' )
    generated_html: str = driver.page_source
    log.debug( f'generated_html, ``{generated_html}``' )
    # driver.find_element_by_id("nav-search").send_keys("Selenium")
    1/0



# ## old! verify.
# def _log_into_shib( self, driver ):
#     """ Helper function for tests.
#         Takes driver; logs in user; returns driver.
#         Called by module test functions. """
#     driver.find_element_by_id("username").clear()
#     driver.find_element_by_id("username").send_keys( self.USERNAME )
#     driver.find_element_by_id("password").clear()
#     driver.find_element_by_id("password").send_keys( self.PASSWORD )
#     driver.find_element_by_css_selector("button[type=\"submit\"]").click()
#     return driver


def parse_args() -> dict:
    """ Parses arguments when module called via __main__ """
    parser = argparse.ArgumentParser( description='Required: auth_id and password (for logging in to BruKnow), and server_type.' )
    parser.add_argument( '--auth_id', '-a', help='auth_id required', required=True )
    parser.add_argument( '--password', '-p', help='password required', required=True )
    parser.add_argument( '--server_type', '-s', choices=['dev', 'prod'], help='"dev" or "prod" required', required=True )
    args: dict = vars( parser.parse_args() )
    return args


if __name__ == '__main__':
    args: dict = parse_args()
    log.debug( f'args, ```{args}```' )
    auth_id: str = args['auth_id']
    password: str = args['password']
    server_type: str = args['server_type']
    test_bibs( auth_id, password, server_type )
