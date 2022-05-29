import json, os, pprint
import gspread


CREDENTIALS: dict = json.loads( os.environ['PRIMO_F_TESTS__SHEET_CREDENTIALS_JSON'] )
SPREADSHEET_NAME = os.environ['PRIMO_F_TESTS__SHEET_NAME']


credentialed_connection = gspread.service_account_from_dict( CREDENTIALS )
sheet = credentialed_connection.open( SPREADSHEET_NAME )
wrksheet = sheet.worksheet( 'requested_checks' )


# print(sheet.sheet1.get('A1'))
print( wrksheet.get('A1') )

list_of_lists = wrksheet.get_values()  # includes column-header row
print( '' )
pprint.pprint( list_of_lists )

list_of_dicts = wrksheet.get_all_records()
print( '' )
pprint.pprint( list_of_dicts )