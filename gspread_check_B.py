import json, os, pprint
import gspread


CREDENTIALS: dict = json.loads( os.environ['PRIMO_F_TESTS__SHEET_CREDENTIALS_JSON'] )
SPREADSHEET_NAME = os.environ['PRIMO_F_TESTS__SHEET_NAME']

pprint.pprint( CREDENTIALS )
gc = gspread.service_account_from_dict( CREDENTIALS )

# pprint.pprint( credentials )
# gc = gspread.service_account_from_dict( credentials )

sh = gc.open( SPREADSHEET_NAME )

print(sh.sheet1.get('A1'))




# import os
# import gspread


# CREDENTIALS_PATH = os.environ['PRIMO_F_TESTS__SHEET_CREDENTIALS_PATH']
# SPREADSHEET_NAME = os.environ['PRIMO_F_TESTS__SHEET_NAME']


# gc = gspread.service_account( filename=CREDENTIALS_PATH )

# sh = gc.open( SPREADSHEET_NAME )

# print(sh.sheet1.get('A1'))
