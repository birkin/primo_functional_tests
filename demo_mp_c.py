import random, time
from multiprocessing import Process, Queue, current_process, freeze_support
from timeit import default_timer as timer

import requests


URL_PATTERN = 'https://bruknow.library.brown.edu/discovery/fulldisplay?docid=alma{mmsid}&context=L&vid=01BU_INST:BROWN&lang=en'

#
# Function run by worker processes
#

def web_worker(input, output):
    for element in iter(input.get, 'STOP'):
        bib_dict: dict = element
        # print( f'bib_dict, ``{bib_dict}``' )
        result = process_bib( bib_dict )
        output.put(result)


def process_bib( element: dict ):
    start_time = timer()
    mmsid = element['mmsid']
    url = URL_PATTERN.replace( '{mmsid}', mmsid )
    r = requests.get( url )
    end_time = timer()
    elapsed: str = str( end_time - start_time)
    print( f'bib elapsed time: ``{elapsed}``' )
    return_val = f'process, ``{current_process().name}`` took, ``{elapsed}``'
    return return_val

#
#
#

def test():
    start_time = timer()
    NUMBER_OF_PROCESSES = 4
    TASKS = [  
        {'mmsid': '991038334049706966', 'comment': 'Guidebook to Zen and the Art of Motorcycle Maintenance'},
        {'mmsid': '991034268659706966', 'comment': 'Zen and Now: on the Trail of Robert Pirsig and Zen and the Art of Motorcycle Maintenance'},
        {'mmsid': '991014485429706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. Special anniversary ed.'},
        {'mmsid': '991007439769706966', 'comment': 'Audio | two-items | Zen and the Art of Motorcycle Maintenance an Inquiry into Values'},
        {'mmsid': '991023827329706966', 'comment': 'one-item | Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. 25th anniversary ed.'},
        {'mmsid': '991033548039706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: An Inquiry into Values'},
        {'mmsid': '991043286359006966', 'comment': 'The Buddha in the Machine: Art, Technology, and the Meeting of East and West.'},
    ]

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS:
        task_queue.put( task )

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=web_worker, args=(task_queue, done_queue)).start()

    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS)):
        print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    end_time = timer()
    elapsed: str = str( end_time - start_time)
    print( f'all elapsed time: ``{elapsed}``' )



if __name__ == '__main__':
    freeze_support()
    test()
