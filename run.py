from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
from typing import Tuple

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

def get_date(prompt: str) -> datetime.date:
    """Prompt user for a date and validate the format."""
    while True:
        try:
            date_str = input(prompt)
            shift_date = datetime.strptime(date_str, '%d/%m/%Y').date()
            print(f"Date entered: {shift_date.strftime('%d/%m/%Y')}\n")
            return shift_date
        except ValueError:
            print("Invalid date format! Please enter date as DD/MM/YYYY.\n")

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

def get_positive_float(prompt: str) -> float:
    """Prompt user for a positive float value and validate the input."""
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                print(f"Value entered: {value}\n")
                return value
            else:
                print("Value cannot be negative.\n")
        except ValueError:
            print("Invalid input! Please enter a number.\n")

def calculate_pay(start_time: datetime.time, end_time: datetime.time, break_minutes: int, hourly_wage: float) -> Tuple[float, float, float]:
    """Calculate total hours worked, paid hours, and total due."""
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    
    time_diff = end_datetime - start_datetime
    hours_worked = time_diff.total_seconds() / 3600
    print(f"You worked a total of: {hours_worked:.2f} hours\n")

    paid_hours = hours_worked - (break_minutes / 60)
    print(f"Your total paid hours are: {paid_hours:.2f} hours\n")

    total_due = paid_hours * hourly_wage
    print(f"For today's shift you are due: £{total_due:.2f}\n")

    return hours_worked, paid_hours, total_due

def pool_user_data(shift_date: datetime.date, start_time: datetime.time, end_time: datetime.time, break_minutes: int, hours_worked: float, paid_hours: float, hourly_wage: float, total_due: float):
    """Pool user data into a list and update the Google Sheet."""
    pooled_data = [
        shift_date.strftime('%d/%m/%Y'),
        start_time.strftime('%H:%M'),
        end_time.strftime('%H:%M'),
        f"{hours_worked:.2f}",
        break_minutes,
        f"{paid_hours:.2f}",
        f"{hourly_wage:.2f}",
        f"£{total_due:.2f}"
    ]
    print("Pulling data...\n")
    hours_worksheet = SHEET.worksheet("hours")
    hours_worksheet.append_row(pooled_data)
    print("Your Hours Worksheet has been updated.\n")

def main():
    """Main function to run the shift collection and calculation process."""
    print("Welcome to the Auto Pay Tracking App.\n")
    print("Track your days and log your working hours here.\n")
    
    while True:
        # Collect and process data
        shift_date = get_date("Please enter the date of your shift (DD/MM/YYYY): \n")
        start_time = get_time("Enter your start time in 24hr format (HHMM): \n")
        end_time = get_time("Enter your end time in 24hr format (HHMM): \n")
        break_minutes = int(get_positive_float("Enter your break time in minutes: \n"))
        hourly_wage = get_positive_float("Enter hourly rate of pay (e.g., 15.50): \n")

        print("Thank you, calculating your pay...\n")
        hours_worked, paid_hours, total_due = calculate_pay(
            start_time, end_time, break_minutes, hourly_wage
        )
        
        pool_user_data(shift_date, start_time, end_time, break_minutes, hours_worked, paid_hours, hourly_wage, total_due)

        # Ask user if they want to enter another shift
        repeat = input("Ready to enter another shift? (yes/no): \n").strip().lower()
        if repeat != "yes":
            print("Exiting the program. Your data has been saved.\n")
            print("Thank you for using the Auto Pay Tracking App.\n")
            break

# Run the main function
if __name__ == "__main__":
    main()
