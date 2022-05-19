"""
From <https://stackoverflow.com/a/61265000>.
"""

import random, time, timeit
from multiprocessing import current_process, Pool, Lock

NUM_WORKERS = 3

def job_manager( job ):
    print( f'starting process, ``{current_process().name}`` with job, ``{job}``' )
    start = timeit.default_timer()
    delay: int = job
    time.sleep( delay )
    end = timeit.default_timer()
    elapsed: str = str( end - start )
    print( f'process, ``{current_process().name}`` took, ``{elapsed}``' )
    return

if __name__ == '__main__':
    lock = Lock()
    ## set up jobs ------------------------------
    jobs = []
    for i in range( 9 ):
        delay: float = ( random.randint(400, 600) / 1000 )
        jobs.append( delay )
    ## start workers and send jobs --------------
    start = timeit.default_timer()
    with Pool( 3 ) as workers:
        rslt = workers.map ( job_manager, jobs )
    ## wind down --------------------------------
    end = timeit.default_timer()
    elapsed: str = str( end - start )
    print( f'total-elapsed, ``{elapsed}``' )
