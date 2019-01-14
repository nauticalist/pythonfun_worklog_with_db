import os
from datetime import datetime

def clear_screen():
    """
    Clear screen for windows or others
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_date(raw_date=None):
    """
    Check date format and return it in DD/MM/YYYY format (string)
    """
    date = None
    while not date:
        try:
            if raw_date:
                date = datetime.strptime(raw_date, '%d/%m/%Y')
            else:
                date_input = input("Please use DD/MM/YYYY: ")
                date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError:
            print("That's not a valid date. Please try again.")
            if raw_date:
                break
    return date


def convert_date_to_string(date):
    """
    Convert date to string to save in json file
    """
    return date.strftime('%d/%m/%Y')


def convert_string_to_date(date_str):
    """
    Convert date in a string to datetime obj
    """
    return datetime.strptime(date_str, '%d/%m/%Y')


def get_time_spent(minutes=None):
    """
    Check time_spent is a valid integer
    """
    time_spent = None
    while not time_spent:
        try:
            if minutes:
                time_spent = int(minutes)
            else:
                time_spent = int(input("Time spent(rounded minutes): "))
        except ValueError:
            print("That's not a valid number. Please enter the number",
                  "of minutes you spent on this task.")
            if minutes:
                break
    return time_spent
