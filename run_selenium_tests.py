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
- $ python3 ./run_selenium_tests.py --auth_id AUTH_ID --password PASSWORD --server_type DEV-OR-PROD
"""

import argparse, datetime, difflib, json, logging, os, pprint, random, sys
from multiprocessing import current_process, Lock, Pool
from timeit import default_timer as timer

import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


LOG_PATH: str = os.environ['PRIMO_F_TESTS__LOG_PATH']

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.info( 'logging ready' )


## settings ---------------------------------------------------------
METADATA_TO_TEST = {
    'possible_locations': [ 'rock', 'scili', 'annex' ],
    'possible_statuses': [ 'Out of library', 'Available' ]
}

CREDENTIALS: dict = json.loads( os.environ['PRIMO_F_TESTS__SHEET_CREDENTIALS_JSON'] )
SPREADSHEET_NAME = os.environ['PRIMO_F_TESTS__SHEET_NAME']

# REQUESTED_CHECKS: list = [  # TODO- load these from a spreadsheet    
#     {'mmsid': '991038334049706966', 'comment': 'Guidebook to Zen and the Art of Motorcycle Maintenance'},
#     {'mmsid': '991034268659706966', 'comment': 'Zen and Now: on the Trail of Robert Pirsig and Zen and the Art of Motorcycle Maintenance'},
#     {'mmsid': '991014485429706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. Special anniversary ed.'},
#     {'mmsid': '991007439769706966', 'comment': 'Zen and the Art of Motorcycle Maintenance an Inquiry into Values'},
#     {'mmsid': '991023827329706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. 25th anniversary ed.'},
#     {'mmsid': '991033548039706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: An Inquiry into Values'},
#     {'mmsid': '991043286359006966', 'comment': 'The Buddha in the Machine: Art, Technology, and the Meeting of East and West.'},
# ]

REQUESTED_CHECKS: list = [  # TODO- load these from a spreadsheet    
    {'mmsid': '991038334049706966', 'comment': 'Guidebook to Zen and the Art of Motorcycle Maintenance'},
    {'mmsid': '991034268659706966', 'comment': 'Zen and Now: on the Trail of Robert Pirsig and Zen and the Art of Motorcycle Maintenance'},
]

RANDOM_CHECKS = [  # TODO- load these from a script that pulls out some number of random mmsids from the POD export-data
    {'mmsid': 'foo', 'comment': 'bar'}
]

URL_PATTERN = 'https://bruknow.library.brown.edu/discovery/fulldisplay?docid=alma{mmsid}&context=L&vid=01BU_INST:BROWN&lang=en'
NUMBER_OF_WORKERS: int = int( os.environ['PRIMO_F_TESTS__CONCURRENT_REQUESTS'] )
OUTPUT_PATH = os.environ['PRIMO_F_TESTS__OUTPUT_FILE_PATH']


## get to work ------------------------------------------------------


def check_bibs( auth_id: str, password: str, server_type: str ) -> None:
    """ Main manager.
        Instantiates pool of workers, and sends jobs to them. 
        Called by ``if __name__ == '__main__':`` """
    start_time = datetime.datetime.now()
    ## setup ------------------------------------
    create_output_file()
    jobs: list = get_requested_checks()
    ## start worker processes -------------------
    lock = Lock()

    with Pool( NUMBER_OF_WORKERS, initializer=initialize_pool, initargs=[lock] ) as workers:
        rslt = workers.map( process_bib, jobs )
        log.debug( f'rslt, ``{rslt}``' )

    ## wind down --------------------------------
    end_time = datetime.datetime.now()
    elapsed: str = str( end_time - start_time )
    log.info( f'elapsed total, ``{elapsed}``')
    make_final_tracker_update( start_time, end_time, elapsed, jobs  )
    return


def get_requested_checks() -> list:
    """ Grabs mms_ids to check from google-sheet.
        Called by check_bibs() """
    # jobs: list = REQUESTED_CHECKS
    credentialed_connection = gspread.service_account_from_dict( CREDENTIALS )
    sheet = credentialed_connection.open( SPREADSHEET_NAME )
    wrksheet = sheet.worksheet( 'requested_checks' )
    list_of_dicts = wrksheet.get_all_records()
    return list_of_dicts[0:2]


# def get_requested_checks() -> list:
#     jobs: list = REQUESTED_CHECKS
#     return jobs


def create_output_file() -> None:
    """ Creates json file that'll be used for output.
        Called by check_bibs() """
    with open( OUTPUT_PATH, 'w' ) as handler:
        jsn = json.dumps( [] )
        handler.write( jsn )
    return


def initialize_pool( lock ):
    """ Sets up global lock_manager that each worker has access to.
        (Pool `initializer` argument must be a callable, so I can't create a global lock and pass it directly.)
        Used to synchronously update the tracker for now...
        ...eventually if a gsheet is updated the lock won't be necessary.
        Called by  check_bibs() """
    global lock_manager
    lock_manager = lock
    return lock_manager


def process_bib( bib_data: dict ) -> None:
    """ Processes a bib.
        Called by check_bibs() """
    try:
        start_time = timer()
        log_id: str = str( random.randint(1000, 9999) )
        mmsid: str = str( bib_data['mms_id'] )
        log.info( f'log_id, ``{log_id}``; bib_data, ``{bib_data}``' )
        drvr = access_site( mmsid, log_id )
        log.debug( f'type(drvr), ``{type(drvr)}``' )
        title_check_result: str = check_title( drvr, bib_data['title'], log_id )
        drvr.close()
        end_time = timer()
        elapsed: str = str( end_time - start_time )
        summary = {
            mmsid: {
                'title_expected': bib_data['title'],
                'elapsed': elapsed,
                'process': current_process().name,
                'checks': {
                    'expected_title_found': title_check_result
                }
            }
        }
        write_result( summary, log_id )
    except Exception as e:
        log.exception( f'Problem processing bib; err, ``{repr(e)}``; traceback follows; processing continues.' )
        # sys.exit()
    return 


def access_site( mms_id: str, log_id: str ):
    """ Actually uses selenium.
        Just returns driver containing the get-url result.
        Called by process_bib() """
    driver = webdriver.Firefox()  # type: ignore
    try:
        url = URL_PATTERN.replace( '{mmsid}', mms_id )
        driver.get( url )
    except:
        log.exception( f'Problem accessing initial url; traceback follows; processing continues.' )
        log.debug( 'hereA' )
        driver.close()
        log.debug( 'hereB' )
    return driver


def check_title( driver, expected: str, log_id: str ) -> str:
    """ Finds title, and checks that found title closely matches expected title from spreadsheet.
        Called by process_bib() """
    WebDriverWait( driver, 30 ).until( expected_conditions.presence_of_element_located((By.CLASS_NAME, 'item-title')) )
    title_element = driver.find_element(by=By.CLASS_NAME, value='item-title')
    found_title = title_element.text
    match_score: float = difflib.SequenceMatcher( None, expected, found_title ).ratio()
    log.debug( f'log_id, ``{log_id}``; expected title, ``{expected}``' )
    log.debug( f'log_id, ``{log_id}``; found title, ``{found_title}``' )
    log.debug( f'log_id, ``{log_id}``; title match score, ``{match_score}``' )
    check_result = 'found'
    if match_score < 0.8:
        check_result = f'not-found; found ``{found_title}``'
    return check_result


def write_result( msg: dict, log_id: str ) -> None:
    """ Writes to json file with lock.
        Called by process_bib() """
    with lock_manager:
        data: list = []
        with open( OUTPUT_PATH, 'r' ) as read_handler:
            data: list = json.loads( read_handler.read() )
        with open( OUTPUT_PATH, 'w' ) as write_handler:
            data.append( msg )
            jsn = json.dumps( data, indent=2 )
            write_handler.write( jsn )
        log.info( f'id, ``{log_id}``; msg written, ``{msg}``' )
    return


def make_final_tracker_update( start_time: datetime.datetime, end_time:datetime.datetime, elapsed: str, jobs: list ) -> None:
    """ Adds info to tracker after all updates are done.
        Called by check_bibs() """
    data: list = []
    with open( OUTPUT_PATH, 'r' ) as read_handler:
        data: list = json.loads( read_handler.read() )
    final_data = { 
        'meta': { 
            'start_time': str( start_time ),
            'end_time': str( end_time ),
            'total-elapsed': elapsed,
            'number_of_workers': NUMBER_OF_WORKERS,
            'number_of_jobs': len( jobs )
            },
        'results': data
        }
    with open( OUTPUT_PATH, 'w' ) as write_handler:
        jsn = json.dumps( final_data, indent=2 )
        write_handler.write( jsn )
    log.info( 'tracker updated' )
    return


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
    log.info( f'starting args, ```{args}```' )
    auth_id: str = args['auth_id']
    password: str = args['password']
    server_type: str = args['server_type']
    check_bibs( auth_id, password, server_type )
