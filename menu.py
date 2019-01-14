from utils import clear_screen


def show_main_menu():
    """
    Display main menu to user
    """
    welcome_text = "Welcome to work log!\nWhat would you like to do?"
    clear_screen()
    print("*"*len(welcome_text))
    print(welcome_text)
    print("*"*len(welcome_text))
    print("""
a) Add new entry?
b) View all entries
c) Search in existing entries
q) Quit program
""")


def show_search_menu():
    """
    Display search menu to user
    """
    clear_screen()
    print("*"*25)
    print("Do you want to search by:")
    print("*"*25)
    print("""
a) Employee
b) Date
c) Time spent
d) Keyword
e) Date Range
f) Return to menu
""")
