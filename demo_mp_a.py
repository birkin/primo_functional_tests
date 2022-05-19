import time
from timeit import default_timer as timer
from multiprocessing import Pool

import requests


URL_PATTERN = 'https://bruknow.library.brown.edu/discovery/fulldisplay?docid=alma{mmsid}&context=L&vid=01BU_INST:BROWN&lang=en'


def process_bib( element ) :
    start = timer()
    mmsid = element['mmsid']
    url = URL_PATTERN.replace( '{mmsid}', 'mmsid' )
    r = requests.get( url )
    end = timer()
    bib_elapsed = f'bib elapsed time: ``{end - start}``'
    msg = f'mmsid, ``{mmsid}`` took ``{bib_elapsed}`` seconds'
    return msg


def start_main():
    start = timer()
    values: list = [  # TODO- load these from a spreadsheet    
        {'mmsid': '991038334049706966', 'comment': 'Guidebook to Zen and the Art of Motorcycle Maintenance'},
        {'mmsid': '991034268659706966', 'comment': 'Zen and Now: on the Trail of Robert Pirsig and Zen and the Art of Motorcycle Maintenance'},
        {'mmsid': '991014485429706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. Special anniversary ed.'},
        {'mmsid': '991007439769706966', 'comment': 'Audio | two-items | Zen and the Art of Motorcycle Maintenance an Inquiry into Values'},
        {'mmsid': '991023827329706966', 'comment': 'one-item | Zen and the Art of Motorcycle Maintenance: an Inquiry into Values. 25th anniversary ed.'},
        {'mmsid': '991033548039706966', 'comment': 'Zen and the Art of Motorcycle Maintenance: An Inquiry into Values'},
        {'mmsid': '991043286359006966', 'comment': 'The Buddha in the Machine: Art, Technology, and the Meeting of East and West.'},
    ]
    with Pool() as pool:
        res = pool.map (process_bib, values)
    print (res)
    end = timer()
    print ( f'all elapsed time: ``{end - start}``' )


# def square(n) :
#     time.sleep(3)
#     return n * n


# def start_main():
#     start = timer()
#     print (f'starting computations on {cpu_count()} cores')
#     values = (4, 6, 8, 10)
#     with Pool() as pool:
#         res = pool.map (square, values)
#     print (res)
#     end = timer ()
#     print ( f'elapsed time: ``{end - start}``' )


if __name__ == '__main__':
    start_main()