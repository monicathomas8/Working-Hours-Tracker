import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

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

# Global variables 
shift_date = None
collect_start_time = None 
collect_end_time = None
collect_break_time = None
hourly_wage = None


def get_shift_date():
    """
    collects the date of the shift worked and checks it is valid 
    with the validate_date function. The loop will continue until 
    valid date is entered.
    """
    global shift_date
    while True:
        collect_date = input("Please enter the date of your shift DD/MM/YYYY): \n")
        print("Checking data...\n")
        shift_date = validate_date(collect_date)
        if shift_date:
            print("Date is correct.\n")
            break
        # ends the loop if input data is valid


def validate_date(collect_date):
    """
    Checks if the input is in the correct format and returns the 
    parsed date if valid, otherwise retuen None.
    """
    try:
        # Attepmt to parse the date into the correct format.
        parsed_date = datetime.strptime(collect_date, '%d/%m/%Y').date()
        print(f"Date entered: {parsed_date}\n")
        return parsed_date
    except ValueError:
        # If the date is not valid, print an error message and return false
        print("Please enter the date in DD/MM/YYYY format to continue.\n")
        return None


def get_start_time():
    """
    This function will get the start time of the users shift 
    """
    global collect_start_time
    while True:
        try:
            start_time_input = input("Enter your start time in 24hr format (HHMM): \n")
            collect_start_time = datetime.strptime(start_time_input, '%H%M')
            print("Checking data...\n")
            print("Start time is valid.\n")
            return collect_start_time
        except ValueError:
            print("Checking data...\n")
            print("Invalid time format! Please enter time as HHMM.\n")

def get_end_time():
    """
    Gets the end time of the user's shift in 24-hour format (HHMM). 
    """
    global collect_end_time
    while True:
        try:
            end_time_input = input("Enter you finished time in 24hr format (HHMM): \n")
            collect_end_time = datetime.strptime(end_time_input, '%H%M')
            print("Checking data...\n")
            print("Shift end time is valid.\n")
            return collect_end_time
        except ValueError:
            print("Checking data...\n")
            print("Invalid time format! Please enter time as HHMM.\n")


def get_break_times():
    """
    Gets the break time duration in minutes. 
    """
    global collect_break_time
    while True:
        try:
            break_time_input = int(input("Enter your break time in munutes: \n"))
            if break_time_input >= 0:
                collect_break_time = break_time_input
                print("Checking data...\n")
                print("break time is valid.\n")
                return collect_break_time
            else:
                print("Checking data...\n")
                print("Break time cannot be a negative number!\n")
        except ValueError:
            print("Checking data...\n")
            print("Invalid input! Please enter break time in minutes!\n")


def get_wage():
    """
    Gets the user's hourly wage as a float.
    """
    global hourly_wage
    while True:
        try:
            hourly_wage_input = input("Enter your hourly rate of pay (e.g., £15.50 should be 15.50): \n")
            hourly_wage = float(hourly_wage_input)
            print("Checking data...\n")
            print("Hourly wage is valid.\n")
            return hourly_wage
        except ValueError:
            print("Checking data...\n")
            print("Invalid input! Please enter a valid number for your wage (e.g., 14.00).\n")


# Call the function to start the process
get_shift_date()
get_start_time()
get_end_time()
get_break_times()
get_wage()

print("Thank you, calculating your pay...\n")

# Calculate the total hours worked
time_diff = collect_end_time - collect_start_time
hours_worked = time_diff.total_seconds() / 3600 #converts time difference to hours
print(f"You worked a total of: {hours_worked:.2f} hours\n")

# Calculate paid hours after subracting break time
paid_hours = hours_worked - (collect_break_time / 60)
print(f"Your total paid hours are: {paid_hours:.2f} hours\n")

# Calculate total due
total_due = paid_hours * hourly_wage
print(f"For todays shift you are due: £{total_due:.2f}\n")