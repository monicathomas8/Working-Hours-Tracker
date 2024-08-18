import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Working-Hours-Tracker-PP3')

"""
the code above was learned from the loveSandwiches project
To install and work with googlesheets.
"""
#hours = SHEET.worksheet('hours')

def get_shift_date(collect_date):
    """
    collects the date of the shift worked and checks it the date is
    in the correct format
    """
collect_date = input("Please enter the date of your shift DD/MM/YYYY): \n")
print("Checking data...\n")

try:
    shift_date = datetime.strptime(collect_date, '%d/%m/%Y').date()
    print(f"Date entered: {shift_date}")
except ValueError as e:
  
    print("Please enter the date in DD/MM/YYYY format to continue.\n")

get_shift_date(collect_date)
