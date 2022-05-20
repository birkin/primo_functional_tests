"""
For 'lock' info, see <https://stackoverflow.com/a/61265000>.
"""

import datetime, json, pprint, random, time, timeit
from multiprocessing import current_process, Pool, Lock

NUM_WORKERS = 100
TRACKER_FILE_PATH = '../output_file/test_output.json'

def job_manager( job ):
    process_name = current_process().name
    print( f'starting process, ``{process_name}`` with job, ``{job}``' )
    start = timeit.default_timer()
    delay: int = job
    time.sleep( delay )
    end = timeit.default_timer()
    elapsed: str = str( end - start )
    print( f'process, ``{current_process().name}`` took, ``{elapsed}``' )
    update_tracker( job, process_name, elapsed )
    return

def update_tracker( job, process_name, elapsed ):
    print( f'tracker update starting: time, ``{datetime.datetime.now()}``; process, ``{process_name}``; job, ``{job}``' )
    
    jlist = []
    with open( TRACKER_FILE_PATH, 'r' ) as reader:
        jlist = json.loads( reader.read() )
    msg = f'job, ``{job}`` completed by process, ``{process_name}`` in, ``{elapsed}``'
    jlist.append( msg )
    with open( TRACKER_FILE_PATH, 'w' ) as writer:
        jsn = json.dumps( jlist, indent=2 )
        writer.write( jsn ) 

    print( f'tracker update ending: time, ``{datetime.datetime.now()}``; process, ``{process_name}``; job, ``{job}``' )
    return


if __name__ == '__main__':
    lock = Lock()
    ## set up tracker ---------------------------
    with open( TRACKER_FILE_PATH, 'w' ) as writer:
        jsn = json.dumps( [] )
        writer.write( jsn ) 
    ## set up jobs ------------------------------
    jobs = []
    for i in range( 1000 ):
        delay: float = ( random.randint(400, 600) / 1000 )
        jobs.append( delay )
    ## start workers and send jobs --------------
    start = timeit.default_timer()
    with Pool( NUM_WORKERS ) as workers:
        rslt = workers.map ( job_manager, jobs )
    ## wind down --------------------------------
    end = timeit.default_timer()
    elapsed: str = str( end - start )
    print( f'total-elapsed, ``{elapsed}``' )
