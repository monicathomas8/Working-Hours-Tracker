import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from typing import Optional, Tuple


# Google Sheets setup
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



def get_date(prompt: str) -> datetime.date:
    """Prompt user for a date and validate the format."""
    while True:
        try:
            date_str = input(prompt)
            shift_date = datetime.strptime(date_str, '%d/%m/%Y').date()
            print(f"Date entered: {shift_date}\n")
            return shift_date
        except ValueError:
            print("Invalid date format! Please enter date as DD/MM/YYYY.\n")
        # ends the loop if input data is valid


def get_time(prompt: str) -> datetime.time:
    """Prompt user for a time and validate the format."""
    while True:
        try:
            time_str = input(prompt)
            time_value = datetime.strptime(time_str, '%H%M').time()
            print(f"Time entered: {time_value.strftime('%H:%M')}\n")
            return time_value
        except ValueError:
            print("Invalid time format! Please enter time as HHMM.\n")



def get_start_time():
    """
    This function will get the start time of the users shift.
    """
    global collect_start_time
    while True:
        try:
            start_time_input = input(
                "Enter your start time in 24hr format (HHMM): \n")
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
            end_time_input = input(
                "Enter you finished time in 24hr format (HHMM): \n")
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
            break_time_input = int(
                input("Enter your break time in munutes: \n"))
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
            hourly_wage_input = input(
                "Enter hourly rate of pay(e.g., £15.50 should be 15.50): \n")
            hourly_wage = float(hourly_wage_input)
            print("Checking data...\n")
            print("Hourly wage is valid.\n")
            return hourly_wage
        except ValueError:
            print("Checking data...\n")
            print("Invalid input!\n")
            print("Please enter a valid number for your wage(e.g., 14.00).\n")


def calculate_days_pay():
    """
    Calculate the total hours worked, paid hours after subracting break time,
    and total due.
    """
    global hours_worked, paid_hours, total_due

    time_diff = collect_end_time - collect_start_time
    hours_worked = time_diff.total_seconds() / 3600
    # Converts time difference to hours
    print(f"You worked a total of: {hours_worked:.2f} hours\n")

    paid_hours = hours_worked - (collect_break_time / 60)
    print(f"Your total paid hours are: {paid_hours:.2f} hours\n")

    total_due = paid_hours * hourly_wage
    print(f"For todays shift you are due: £{total_due:.2f}\n")


def pool_user_data():
    """
    Pulls user input data into a list and updates the google sheets
    """
    global hours_worked, paid_hours, total_due, hourly_wage
    pooled_data = [
        shift_date.strftime('%d/%m/%Y'),
        f"{collect_start_time.strftime('%H:%M')}",
        f"{collect_end_time.strftime('%H:%M')}",
        f"{hours_worked:.2f}",
        collect_break_time,
        f"{paid_hours:.2f}",
        f"{hourly_wage:.2f}",
        f"£{total_due:.2f}"
    ]
    print("Pulling data...\n")
    hours_worksheet = SHEET.worksheet("hours")
    hours_worksheet.append_row(pooled_data)
    print("Your Hours Worksheet has been updated.\n")


def main():
    """
    Main function to run the shift collection
    and calculation process in a loop.
    """
    print("Welcome to Monica's Auto Pay Tracking App.\n")
    print("Track your days and log your working hours here.\n")
    while True:
        # Collect and process data
        get_shift_date()
        get_start_time()
        get_end_time()
        get_break_times()
        get_wage()
        print("Thank you, calculating your pay...\n")
        calculate_days_pay()
        pool_user_data()

        # Ask user if they wamt to enter another shift
        while True:
            repeat = input(
                "Ready to enter another shift?(yes/no): \n").strip().lower()
            if repeat == "yes":
                break  # Continue the loop to enter another shift
            elif repeat == "no":
                print("Exiting the program. Your data has been saved.\n")
                print("Thank you for using Monica's Auto Pay Tracking App.\n")
                print("Until next time, goodbye! \n")
                exit()  # Exit the program
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")


# Run the main function
main()
