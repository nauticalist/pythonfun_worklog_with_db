from task import Task, initialize
import menu


if __name__ == '__main__':
    # Initialize database
    initialize()
    # Display main menu
    user_input = None
    while user_input != "d":
        menu.show_main_menu()
        user_input = input("> ")
        # Create new task
        if user_input.lower() == "a":
            Task.create_task()
        # View all entries
        elif user_input.lower() == "b":
            Task.view_tasks()
        # Search for entries
        elif user_input.lower() == "c":
            while user_input != "f":
                menu.show_search_menu()
                user_input = input("> ")
                if user_input == "a":
                    pass
                elif user_input == "b":
                    pass
                elif user_input == "c":
                    pass
                elif user_input == "d":
                    pass
                elif user_input == "e":
                    pass
                elif user_input.lower() == "f":
                    break
                else:
                    print("Invalid entry. Please retry!")
        # Quit
        elif user_input.lower() == "d":
            print("Thanks for using worklog app. See you later!")
        else:
            print("Invalid entry. Please retry!")