from task import Task, initialize
import menu


if __name__ == '__main__':
    # Initialize database
    initialize()
    # Display main menu
    user_input = None
    while user_input != "q":
        menu.show_main_menu()
        user_input = input("> ")
        # Create new task
        if user_input.lower() == "a":
            Task.create_task()
        # View all entries
        elif user_input.lower() == "b":
            Task.view_tasks()
        # View entries by employees
        elif user_input.lower() == "c":
            while user_input != "f":
                menu.show_search_menu()
                user_input = input("> ")
                if user_input == "a":
                    # Search by employee
                    data = Task.search_by_employee()
                    if data:
                        title = "Tasks for employee: {}".format(
                            data['employee'])
                        Task.view_tasks(data['tasks'], title)
                elif user_input == "b":
                    # Search by date
                    data = Task.search_by_date()
                    if data:
                        title = "Tasks for date: {}".format(
                            data['date'])
                        Task.view_tasks(data['tasks'], title)
                elif user_input == "c":
                    # Search by time spend
                    data = Task.search_by_time_spend()
                    if data:
                        title = "Tasks by time spent: {}".format(
                            data['time_spent'])
                        Task.view_tasks(data['tasks'], title)
                elif user_input == "d":
                    # Search by keyword
                    data = Task.search_by_keyword()
                    if data:
                        title = "Tasks includes keyword: {}".format(
                            data['keyword'])
                        Task.view_tasks(data['tasks'], title)
                elif user_input == "e":
                    # Search tasks between dates
                    data = Task.search_by_date_range()
                    if data:
                        title = "Tasks between {} and {}".format(
                            data['start_date'], data['end_date'])
                        Task.view_tasks(data['tasks'], title)
                elif user_input.lower() == "f":
                    # Return to main menu
                    break
                else:
                    print("Invalid entry. Please retry!")
        # Quit Program
        elif user_input.lower() == "q":
            print("Thanks for using worklog app. See you later!")
        else:
            print("Invalid entry. Please retry!")
