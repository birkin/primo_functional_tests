import json, os, pprint
import gspread


CREDENTIALS: dict = json.loads( os.environ['PRIMO_F_TESTS__SHEET_CREDENTIALS_JSON'] )
SPREADSHEET_NAME = os.environ['PRIMO_F_TESTS__SHEET_NAME']


gc = gspread.service_account_from_dict( CREDENTIALS )
sh = gc.open( SPREADSHEET_NAME )

print(sh.sheet1.get('A1'))
