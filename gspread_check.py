import os
import gspread


CREDENTIALS_PATH = os.environ['PRIMO_F_TESTS__SHEET_CREDENTIALS_PATH']
SPREADSHEET_NAME = os.environ['PRIMO_F_TESTS__SHEET_NAME']


gc = gspread.service_account( filename=CREDENTIALS_PATH )

sh = gc.open( SPREADSHEET_NAME )

print(sh.sheet1.get('A1'))
