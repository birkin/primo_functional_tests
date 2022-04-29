"""
Flow...
- get arguments (eppn, password, dev-or-prod-instance)
- load desired url-data
- load random url-data (get random mms-ids, then build urls)
- process urls asyncronously, checking:
  - that 'status' is one of expected fields
  - that 'location' is one of expected fields
  - that 'material-type' is one of expected fields
  - that given the 'status', 'location', and 'material-type', 
    the proper links exist at the bib-level and item-level

Question(s)...
- Would the Primo-API indicate bib-level and item-level custom links?
"""

import argparse, logging, os

LOG_PATH: str = os.environ['PRIMO_F_TESTS__LOG_PATH']


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.debug( 'logging ready' )


def test_bibs( auth_id: str, password: str, server_type: str ) -> None:
  pass


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
