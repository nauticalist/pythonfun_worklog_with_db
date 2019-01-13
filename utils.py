import os
from datetime import datetime

def clear_screen():
    """
    Clear screen for windows or others
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_date():
    """
    Check date format and return it in DD/MM/YYYY format (string)
    """
    date = None
    while not date:
        date_input = input("Please use DD/MM/YYYY: ")
        try:
            date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError:
            print("That's not a valid date. Please try again.")
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


def get_time_spent():
    """
    Check time_spent is a valid integer
    """
    time_spent = None
    while not time_spent:
        try:
            time_spent = int(input("Time spent(rounded minutes): "))
        except ValueError:
            print("That's not a valid number. Please enter the number",
                  "of minutes you spent on this task.")
    return time_spent
