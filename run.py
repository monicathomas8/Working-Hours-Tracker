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
#global var

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
        #checks users input and makes sure it is valid

        shift_date = validate_date(collect_date)
        if shift_date:
            print("Date is correct")
            break
        # ends the loop if input data is valid


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


collect_start_time = None 
collect_end_time = None
collect_break_time = None
hourly_wage = None
#global vars so they can be used inside and outside of different functions

def get_start_time():
    """
    This function will get the start time of the users shift 
    """
    collect_start_time = int(input("Enter your start time in 24hr format HHMM\n"))
    print("Checking data...\n")
    return collect_start_time

def get_end_time():
    """
    This function will get the end time of the users shift 
    """
    collect_end_time = int(input("Enter you finished time in 24hr format HHMM\n"))
    print("Checking data...\n")
    return collect_end_time

print("Calculating worked hours...\n")

def get_break_times():
    """
    This function will get the amount of break time the users had on shift 
    """
    collect_break_time = int(input("How long was your break? HHMM\n"))
    print("Checking data...\n")
    return collect_break_time

def get_wage():
    """
    This function will get the users hourly wage 
    """
    hourly_wage = int(input("How much is your hourly rate of pay? example £15.50 per hour should be entered like: 15.50 \n"))
    print("Checking data...\n")
    return hourly_wage



#def update_hours_worksheet():
 #   """
   # updates the google worksheet with the user's data.
    #"""
    #print("Updating Hours worksheet...\n")
    #hours_worksheet = SHEET.worksheet("hours")
   # hours_worksheet.append_row([shift_date.strftime('%d/%m/%Y')])
    #print("Date added to Hours worksheet.\n")


    #collect_break_time = int(input("Enter you break length in 24hr format HH:MM\n"))
    #print("Checking data...\n")


#  call the function to start the process
get_shift_date()
get_start_time()
get_end_time()
get_break_times()
get_wage()


hours_worked = collect_end_time - collect_start_time 
print(f" You worked a total of: {hours_worked}\n")

paid_hours = hours_worked - collect_break_time
print(f"Your total paid hours are: {paid_hours}\n")

total_due = paid_hours * hourly_wage
print(f"For todays shift you are due: £{total_due}")
#checks if shift date was correctly set
#if shift_date:
    #update_hours_worksheet()
