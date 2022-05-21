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
from multiprocessing import current_process, Lock, Pool
from timeit import default_timer as timer

# import trio
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

# REQUESTED_CHECKS: list = [  # TODO- load these from a spreadsheet    
#     {'mmsid': '991038334049706966', 'comment': 'Guidebook to Zen and the Art of Motorcycle Maintenance'},
#     {'mmsid': '991034268659706966', 'comment': 'Zen and Now: on the Trail of Robert Pirsig and Zen and the Art of Motorcycle Maintenance'},
#     {'mmsid': '991014485429706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. Special anniversary ed.'},
#     {'mmsid': '991007439769706966', 'comment': 'Audio | two-items | Zen and the Art of Motorcycle Maintenance an Inquiry into Values'},
#     {'mmsid': '991023827329706966', 'comment': 'one-item | Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. 25th anniversary ed.'},
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


# def check_bibs( auth_id: str, password: str, server_type: str ) -> None:
#     """ Main controller.
#         - Instantiates task_queue. 
#         - Creates specified number of processes.
#         Called by ``if __name__ == '__main__':`` """
#     start_time = timer()
#     create_output_file()
#     ## Create queues ----------------------------
#     task_queue = Queue()
#     done_queue = Queue()
#     ## Submit tasks -----------------------------
#     for task in REQUESTED_CHECKS:
#         task_queue.put( task )
#     ## Start worker processes -------------------
#     lock = Lock()
#     for i in range( NUMBER_OF_WORKERS ) :
#         Process( target=manage_job_queue, args=(task_queue, done_queue, lock) ).start()
#     ## Get results ------------------------------
#     """ I don't really understand why, but the `done_queue.get()` is required, or the code errors.
#         Nothing subsequently uses anything from the done-queue... 
#         It feels like how 'await' is needed to actually trigger an async process -- but there's no async here.
#         In other multiprocessing code examples, I've seen process.join() used similarly.
#     """
#     log.info( 'about to initiate all done_queue.get() calls...' )
#     for i in range( len(REQUESTED_CHECKS) ):
#         log.info( 'about to call done_queue.get()' )
#         done_queue.get()
#     ## Tell child processes to stop -------------
#     """
#     TODO- feels odd to be passing a string to do something like this. Investigate.
#     """
#     log.info( 'about to send stop to all workers...' )
#     for i in range( NUMBER_OF_WORKERS ):
#         task_queue.put( 'STOP' )
#     end_time = timer()
#     elapsed: str = str( end_time - start_time )
#     log.info( f'elapsed total, ``{elapsed}``')
#     return

#     ## end def check_bibs()


def check_bibs( auth_id: str, password: str, server_type: str ) -> None:
    """ Main controller.
        Instantiates pool of workers, and sends jobs to them. 
        Called by ``if __name__ == '__main__':`` """
    start_time = timer()
    create_output_file()

    ## Start worker processes -------------------
    lock = Lock()
    jobs: list = REQUESTED_CHECKS
    with Pool( NUMBER_OF_WORKERS, initializer=initialize_pool, initargs=[lock] ) as workers:
        rslt = workers.map( process_bib, jobs )

    end_time = timer()
    elapsed: str = str( end_time - start_time )
    log.info( f'elapsed total, ``{elapsed}``')
    update_tracker( start_time, end_time, elapsed, jobs  )
    return

    ## end def check_bibs()




def create_output_file() -> None:
    """ Creates json file that'll be used for output.
        Called by check_bibs() """
    with open( OUTPUT_PATH, 'w' ) as handler:
        jsn = json.dumps( [] )
        handler.write( jsn )
    return


def initialize_pool( lock ):
    """ Sets up global lock_manager that each worker has access to.
        Used to synchronously update the tracker for now.
        Eventually if a gsheet is updated the lock won't be necessary.
        Called by  check_bibs() """
    global lock_manager
    lock_manager = lock
    return lock_manager


def process_bib( bib_data: dict ):
    """ Processes a bib.
        Called by manage_job_queue() """
    start_time = timer()
    log_id: int = random.randint( 1000, 9999 )
    log.info( f'id, ``{log_id}``; bib_data, ``{bib_data}``' )
    result: dict = access_site( bib_data['mmsid'], log_id )
    end_time = timer()
    elapsed: str = str( end_time - start_time )
    # msg = f'id, ``{log_id}``; elapsed for bib, ``{elapsed}``'
    output_msg = {
        'id': log_id,
        'elapsed_for_bib': elapsed,
        'check_data': result
    }
    write_result( output_msg, log_id )
    title = f'{result["title"][0:10]}...'
    done_queue_message = f'process, ``{current_process().name}``; for item, ``{title}``; took, ``{elapsed}``'
    return done_queue_message


def access_site( mms_id: str, log_id: int ) -> dict:
    """ Actually uses selenium.
        This is a stand-in file that'll likely become a big suite of various tests.
        Called by process_bib() """
    driver = webdriver.Firefox()  # type: ignore
    url = URL_PATTERN.replace( '{mmsid}', mms_id )
    driver.get( url )
    WebDriverWait( driver, 30 ).until( expected_conditions.presence_of_element_located((By.CLASS_NAME, 'item-title')) )
    title_element = driver.find_element(by=By.CLASS_NAME, value='item-title')
    title = title_element.text
    driver.close()
    log.info( f'title, ``{title}``' )
    data = { 'title': title }
    return data


def write_result( msg: dict, log_id: int ) -> None:
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


def update_tracker( start_time, end_time, elapsed: str, jobs: list ) -> None:
    """ Adds info to tracker after all updates are done.
        Called by check_bibs() """
    data: list = []
    with open( OUTPUT_PATH, 'r' ) as read_handler:
        data: list = json.loads( read_handler.read() )
    final_data = { 
        'meta': { 
            'start_time': start_time,
            'end_time': end_time,
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
