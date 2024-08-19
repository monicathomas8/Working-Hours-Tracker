from datetime import datetime, timedelta, date
from typing import Tuple
import gspread
from google.oauth2.service_account import Credentials

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


def get_date(prompt: str) -> date:
    """Prompt user for a date and validate the format and range."""
    today = date.today()
    five_years_ago = today - timedelta(days=5*365)  # Approximate 5 years

    while True:
        date_str = input(prompt).strip()
        try:
            shift_date = datetime.strptime(date_str, '%d/%m/%Y').date()
            if shift_date > today:
                print("The date cannot be in the future.\n")
            elif shift_date < five_years_ago:
                print("The date cannot be more than 5 years old.\n")
            else:
                print(f"Date entered: {shift_date.strftime('%d/%m/%Y')}\n")
                return shift_date
        except ValueError:
            print("Invalid date format! Please enter date as DD/MM/YYYY.\n")


def get_time(prompt: str) -> datetime.time:
    """Prompt user for a time and validate the format."""
    while True:
        time_str = input(prompt).strip()
        if len(time_str) != 4 or not time_str.isdigit():
            print("Invalid input! Please enter time as 4 digits (HHMM).\n")
            continue
        try:
            time_value = datetime.strptime(time_str, '%H%M').time()
            print(f"Time entered: {time_value.strftime('%H:%M')}\n")
            return time_value
        except ValueError:
            print("Invalid time format! Please enter time as HHMM.\n")


def validate_range(value: float, min_value: float, max_value: float) -> bool:
    """Validate if the value is within the given range."""
    return min_value <= value <= max_value


def get_break_time(prompt: str, total_shift_hours: float) -> int:
    """
    Prompt user for break time and validate it is
    within range and less than total shift time.
    """
    while True:
        try:
            break_time = int(input(prompt).strip())
            if validate_range(break_time, 1, 120):
                if break_time < total_shift_hours * 60:
                    print(f"Break time entered: {break_time} minutes\n")
                    return break_time
                else:
                    print(
                        "Break cannot be longer than the shift time.\n"
                        )
            else:
                print("Break time must be between 1 and 120 minutes.\n")
        except ValueError:
            print(
                "Invalid input! Please enter a whole number for break time.\n"
                )


def get_hourly_wage(prompt: str) -> float:
    """
    Prompt user for hourly wage and validate that
    it's a positive value within the specified range.
    """
    while True:
        try:
            wage = float(input(prompt).strip())
            if validate_range(wage, 1, 250):
                print(f"Hourly wage entered: £{wage:.2f}\n")
                return wage
            else:
                print("Hourly wage must be between £1 and £250.\n")
        except ValueError:
            print(
                "Invalid input! Please enter a number for the hourly wage.\n"
                )


def validate_times(start_time: datetime.time, end_time: datetime.time) -> bool:
    """
    Validates that the end time is after
    the start time and they are not the same.
    """
    if end_time <= start_time:
        return False
    return True


def calculate_pay(
    start_time: datetime.time,
    end_time: datetime.time,
    break_minutes: int,
    hourly_wage: float
) -> Tuple[float, float, float]:
    """
    Calculates the total hours worked, total paid hours
    and the total due.
    """
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)

    if not validate_times(start_time, end_time):
        print(
            "Error: End time must be later than start time.\n"
            )
        return 0, 0, 0  # Return zeros if times are invalid

    time_diff = end_datetime - start_datetime
    hours_worked = time_diff.total_seconds() / 3600
    print(f"You worked a total of: {hours_worked:.2f} hours\n")

    if break_minutes >= hours_worked * 60:
        print(
            "Error: Break time cannot be longer than the total shift time.\n"
            )
        return 0, 0, 0  # Return zeros if break time is invalid

    paid_hours = hours_worked - (break_minutes / 60)
    print(f"Your total paid hours are: {paid_hours:.2f} hours\n")

    total_due = paid_hours * hourly_wage
    print(f"For today's shift you are due: £{total_due:.2f}\n")

    return hours_worked, paid_hours, total_due


def pool_user_data(
    shift_date: date,
    start_time: datetime.time,
    end_time: datetime.time,
    break_minutes: int,
    hours_worked: float,
    paid_hours: float,
    hourly_wage: float,
    total_due: float
):
    """
    Pools user data into a list and updates
    the hours worksheet within the Google Sheet.
    """
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


def display_last_7_entries():
    """
    Display the last 7 entries from the Google Sheet,
    including the header row,
    with data aligned under each header.
    """
    hours_worksheet = SHEET.worksheet("hours")
    # Fetch all records
    all_records = hours_worksheet.get_all_values()

    if len(all_records) == 0:
        print("No entries found in the sheet.\n")
        return

    # Include the header row
    header = all_records[0]
    # Get the last 7 entries, including the header row
    if len(all_records) > 8:
        last_7_entries = [header] + all_records[-7:]
    else:
        last_7_entries = all_records
        # If there are fewer than 8 rows, include all

    # Determine the width of each column
    col_widths = [
        max(len(item) for item in col) for col in zip(*last_7_entries)
        ]

    # Print the header row
    header_row = " | ".join(
        f"{header[i]:<{col_widths[i]}}" for i in range(len(header)))
    print(header_row)
    print("-" * len(header_row))  # Print a line separator

    # Print each entry
    for entry in last_7_entries:
        row = " | ".join(
            f"{entry[i]:<{col_widths[i]}}" for i in range(len(entry)))
        print(row)

    print()  # Add a newline for readability


def main():
    """
    Main function to run the shift
    collection and calculation process.
    """
    print(f"""
    Welcome to the Auto Pay Tracking App.
    Track your days and log your working hours here.
    """)

    while True:
        # Collect and process data
        shift_date = get_date(
            "Please enter the date of your shift (DD/MM/YYYY): \n"
            )
        start_time = get_time(
            "Enter your start time in 24hr format (HHMM): \n"
            )
        end_time = get_time(
            "Enter your end time in 24hr format (HHMM): \n"
            )

        """
        Ensures that start time and end time
        are within the same 24-hour period and are not the same.
        """
        while not validate_times(start_time, end_time):
            print(
                "Error: End time must be after start time and not the same.\n"
                )
            start_time = get_time(
                "Re-enter your start time in 24hr format (HHMM): \n"
                )
            end_time = get_time(
                "Re-enter your end time in 24hr format (HHMM): \n"
                )
            total_shift_hours = (
             datetime.combine(datetime.today(), end_time)
             - datetime.combin(datetime.today(), start_time)
             ).total_seconds() / 3600
        break_minutes = get_break_time(
            "Enter your break time in minutes (1-120): \n",
            total_shift_hours
            )
        hourly_wage = get_hourly_wage(
            "Enter hourly rate of pay (e.g., 15.50): \n"
            )

        print("Thank you, calculating your pay...\n")
        hours_worked, paid_hours, total_due = calculate_pay(
            start_time, end_time, break_minutes, hourly_wage
            )

        # Only pool data if times and break are valid
        if hours_worked > 0:
            pool_user_data(
                shift_date,
                start_time,
                end_time,
                break_minutes,
                hours_worked,
                paid_hours,
                hourly_wage,
                total_due
                )

        # Ask user if they want to enter another shift or exit
        while True:
            repeat = input(
                "Ready to enter another shift? (yes/no): \n"
                ).strip().lower()
            if repeat == "yes":
                break
            elif repeat == "no":
                print("Exiting the program. Your data has been saved.\n")
                while True:
                    show_entries = input(
                        "Would you like to see the last 7 entries? (yes/no):"
                        ).strip().lower()
                    if show_entries == "yes":
                        display_last_7_entries()
                        print(
                            "Thank you for using the Auto Pay Tracking App.\n"
                            )
                        return  # Exit the function to end the program
                    elif show_entries == "no":
                        print(
                            "Thank you for using the Auto Pay Tracking App.\n"
                            )
                        return  # Exit the function to end the program
                    else:
                        print(f"""
                            Invalid input!
                            Please enter 'yes' or 'no'
                            without extra spaces or characters.
                            """)
                # Exit the main loop after showing entries or not
                return
            else:
                print(f"""
                Invalid input!
                Please enter 'yes' or 'no' without extra spaces or characters.
                """)


# Run the main function
if __name__ == "__main__":
    main()
