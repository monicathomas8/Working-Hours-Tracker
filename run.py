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

shift_date = None

def get_shift_date():
    """
    collects the date of the shift worked and checks it is valid 
    with the validate_date function the loop will continue until 
    valid date is entered.
    """
    global shift_date
    while True:
        collect_date = input("Please enter the date of your shift DD/MM/YYYY): \n")
        print("Checking data...\n")

        shift_date = validate_date(collect_date)
        if shift_date:
            print("Date is correct")
            break


def validate_date(collect_date):
    """
    Checks if the input is in the correct format and returns the 
    parsed date if valid, otherwise retuen None.
    """
    try:
        # attepmt to parse the date into the correct format.
        parsed_date = datetime.strptime(collect_date, '%d/%m/%Y').date()
        print(f"Date entered: {parsed_date}")
        return parsed_date

    except ValueError as e:
        # If the date is not valid, print an error message and return false
        print("Please enter the date in DD/MM/YYYY format to continue.\n")
        return None

def update_hours_worksheet():
    """
    updates the google worksheet with the user's data.
    """
    print("Updating Hours worksheet...\n")
    hours_worksheet = SHEET.worksheet("hours")
    hours_worksheet.append_row([shift_date.strftime('%d/%m/%Y')])
    print("Date added to Hours worksheet.\n")

#  call the function to start the process
get_shift_date()

#checks if shift date was correctly set
if shift_date:
    update_hours_worksheet()
