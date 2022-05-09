"""
Tests flow...
- get arguments (eppn, password, dev-or-prod-instance)
- load created url-data
- load random url-data (get random mms-ids, then build urls)
- process urls asyncronously
  - assert page loads
  - grab title
  - click to display all locations if necessary
  - assert all locations are expected
  - assert all item-statuses are expected
  - assert all material-types are expected
  - given the 'item-status', 'location', and 'material-type', and non-logged-in-status:
    - check that any proper links exist at the bib-level.
    - check that any proper links exist at the item-level.
  - login
  - given the 'item-status', 'location', and 'material-type', and logged-in-status:
    - check that any proper links exist at the bib-level.
    - check that any proper links exist at the item-level.

Notes...
- results will be saved to a json file, and eventually written to a google-sheet.

Usage...
- cd to `primo_functional_tests` directory.
- $ source ../env/bin/activate
- $ python3 ./run_tests.py --auth_id AUTH_ID --password PASSWORD --server_type DEV-OR-PROD
"""

import argparse, datetime, json, logging, os, pprint, random

import trio
from selenium import webdriver

LOG_PATH: str = os.environ['PRIMO_F_TESTS__LOG_PATH']

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.debug( 'logging ready' )


## settings ---------------------------------------------------------

METADATA_TO_TEST = {
    'possible_locations': [ 'rock', 'scili', 'annex' ],
    'possible_statuses': [ 'Out of library', 'Available' ]
}

REQUESTED_TESTS = [  # TODO- load these from a spreadsheet    
    {'mmsid': '991038334049706966', 'comment': 'Guidebook to Zen and the Art of Motorcycle Maintenance'},
    {'mmsid': '991034268659706966', 'comment': 'Zen and Now: on the Trail of Robert Pirsig and Zen and the Art of Motorcycle Maintenance'},
    {'mmsid': '991014485429706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. Special anniversary ed.'},
    {'mmsid': '991007439769706966', 'comment': 'Audio | two-items | Zen and the Art of Motorcycle Maintenance an Inquiry into Values'},
    {'mmsid': '991023827329706966', 'comment': 'one-item | Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. 25th anniversary ed.'},
    {'mmsid': '991033548039706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: An Inquiry into Values'},
    {'mmsid': '991043286359006966', 'comment': 'The Buddha in the Machine: Art, Technology, and the Meeting of East and West.'},
]

RANDOM_TESTS = [  # TODO- load these from a script that pulls out some number of random mmsids from the POD export-data
    {'mmsid': 'foo', 'comment': 'bar'}
]

URL_PATTERN = 'https://bruknow.library.brown.edu/discovery/fulldisplay?docid=alma{mmsid}&context=L&vid=01BU_INST:BROWN&lang=en'
CONCURRENT_COUNT: int = int( os.environ['PRIMO_F_TESTS__CONCURRENT_REQUESTS'] )
OUTPUT_PATH = os.environ['PRIMO_F_TESTS__OUTPUT_FILE_PATH']


## get to work ------------------------------------------------------

def check_bibs( auth_id: str, password: str, server_type: str ) -> None:
    """ Main controller; calls loop. 
        Gets a set of bibs to process concurrently, processes them, then gets another set, etc...
        The number of bibs to process concurrently is set by CONCURRENT_COUNT.
        Note: this pattern of concurrency should be less efficient 
              than one where a new item is added to the queue whenever a job finishes, 
              but I think the management will be simpler. 
        Called by ``if __name__ == '__main__':`` """
    start_time = datetime.datetime.now()
    create_output_file()
    processed_requested_tests_count = 0
    while processed_requested_tests_count < len( REQUESTED_TESTS ):
        bib_set: list = load_queue( REQUESTED_TESTS, processed_requested_tests_count, CONCURRENT_COUNT )
        trio.run( process_bib_set, bib_set )  # the trio way of passing the argument `bib_set` to the function `process_bib_set()`
        processed_requested_tests_count += CONCURRENT_COUNT
    end_time = datetime.datetime.now()
    elapsed = end_time - start_time
    log.debug( f'elapsed total, ``{elapsed}``')
    return


def create_output_file() -> None:
    with open( OUTPUT_PATH, 'w' ) as handler:
        jsn = json.dumps( [] )
        handler.write( jsn )
    return


def load_queue( all_tests: list, processed_tests_count: int, concurrent_count: int ) -> list:
    """ Loads up the next set of MMS-IDs to proces.
        Called by test_bibs() """
    # log.debug( f'all_tests, ``{pprint.pformat(all_tests)}``' )
    index_start = processed_tests_count
    index_end = index_start + concurrent_count
    log.debug( f'index_start, ``{index_start}``; index_end, ``{index_end}``' )
    set_to_process: list = all_tests[index_start: index_end]
    log.debug( f'set_to_process, ``{pprint.pformat(set_to_process)}``' )
    return set_to_process

    
async def process_bib_set( bibs_data ):
    """ Processes each bib-data element in bibs_data concurrently.
        Returns after they're all finished. 
        Called by check_bibs() """
    start_time = datetime.datetime.now()
    async with trio.open_nursery() as nursery:
        for bib_data in bibs_data:
            nursery.start_soon( process_bib, bib_data )
    end_time = datetime.datetime.now()
    elapsed = end_time - start_time
    log.debug( f'elapsed for set, ``{elapsed}``')
    return

async def process_bib( bib_data ):
    rndm_id: int = random.randint( 1000, 9999 )
    rndm_slp1: float = random.randint( 450, 550 ) / 1000; log.debug( f'id, ``{rndm_id}``rndm_slp1, ``{rndm_slp1}``' )
    start_time = datetime.datetime.now()
    await trio.sleep( rndm_slp1 )
    log.debug( f'id, ``{rndm_id}``; message A')
    rndm_slp2: float = random.randint( 450, 550 ) / 1000; log.debug( f'id, ``{rndm_id}``rndm_slp2, ``{rndm_slp2}``' )
    await trio.sleep( rndm_slp2 )
    log.debug( f'id, ``{rndm_id}``; message B')
    end_time = datetime.datetime.now()
    elapsed = end_time - start_time
    msg = f'id, ``{rndm_id}``; elapsed for bib, ``{elapsed}``'
    log.debug( msg )
    with open( OUTPUT_PATH, 'r' ) as read_handler:
        data: list = json.loads( read_handler.read() )

        with open( OUTPUT_PATH, 'w' ) as write_handler:
            data.append( msg )
            jsn = json.dumps( data, indent=2 )
            write_handler.write( jsn )

    return


# def process_bib( bib_dct: dict ) -> str:
#     """ Controller for individual bib-processing.
#         Called by test_bibs() """
#     driver = webdriver.Firefox()  # type: ignore
#     log.debug( 'driver created' )
#     url: str = URL_PATTERN.replace( '{mmsid}', bib_dct['mmsid'] )
#     log.debug( f'url, ``{url}``' )
#     log.debug( 'about to call url' )
#     driver.get( url )
#     log.debug( 'about to get page_source' )
#     generated_html: str = driver.page_source
#     log.debug( f'generated_html, ``{generated_html}``' )
#     # driver.find_element_by_id("nav-search").send_keys("Selenium")
#     1/0


## -- script-caller helpers -----------------------------------------

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
    check_bibs( auth_id, password, server_type )









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

