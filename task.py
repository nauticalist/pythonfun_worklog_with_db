import datetime


from peewee import *
import utils


db = SqliteDatabase('worklog.db')


class Task(Model):
    """
    Model of a work-log task
    """
    username = CharField(max_length=100)
    title = CharField(max_length=255)
    date = DateTimeField()
    time_spent = IntegerField()
    notes = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ('-created_at',)

    def view_task(task):
        """
        view a single task
        """
        print(task.title)
        print("=" * len(task.title))
        print("User: {}".format(task.username))
        print("Date: {}".format(task.date))
        print("Time spent: {}".format(task.time_spent))
        print("Notes: {}".format(task.notes))

    @classmethod
    def create_task(cls):
        """
        Get user input and create users task
        """
        utils.clear_screen()
        # Request data from user
        username = input("Enter your username: ")
        utils.clear_screen()
        print("Date of the task")
        date = utils.get_date()
        utils.clear_screen()
        title = input("Title of the task: ")
        utils.clear_screen()
        time_spent = utils.get_time_spent()
        utils.clear_screen()
        notes = input("Notes (Optional, you can leave this empty): ")
        utils.clear_screen()
        # Now create task
        Task.create(username=username,
                    date=date,
                    title=title,
                    time_spent=time_spent,
                    notes=notes)
        print("Task successfully logged.\n")

    def delete_task(task):
        """Delete an entry."""
        if input("Are you sure? [yN]  ").lower() == "y":
            task.delete_instance()
            print("Entry deleted!")

    def edit_task(task):
        """
        Edit and update selected task
        """
        print("*" * 25)
        print("Editing task:")
        print("*" * 25)
        print(task.title)
        print("*" * 25)
        print("New Values:")
        print("*" * 25)
        # Request updated values of task from user
        title = input("Title of the task: ")
        username = input("Username: ")
        print("Date of the task")
        date = utils.get_date()
        time_spent = utils.get_time_spent()
        notes = input("Notes (Optional, you can leave this empty): ")
        task.title = title
        task.username = username
        task.date = date
        task.time_spent = time_spent
        task.notes = notes
        # Now save task to database
        task.save()
        print("Task updated")

    @classmethod
    def view_tasks(cls, tasks=None, title=None):
        """
        View and iterate over tasks
        """
        # If tasks is none display all tasks
        if tasks is None:
            tasks = Task.select()
        total_tasks = len(tasks)
        index = 0
        while index < total_tasks:
            utils.clear_screen()
            # If title exists display it for search results
            if title:
                print("{}\n".format(title))

            Task.view_task(tasks[index])
            print("\nTask {} of {}\n".format(index + 1, total_tasks))
            # If result is only one task omit next and previous options
            if total_tasks == 1:
                user_choice = input("\n[E]dit [D]elete [M]ain Menu\n> ")
            else:
                user_choice = input("\n[N]ext [P]revious" +
                                    " [E]dit [D]elete [M]ain Menu\n> ")
            if user_choice.upper() == "N":
                if index == total_tasks - 1:
                    index = 0
                else:
                    index += 1
            elif user_choice.upper() == "P":
                if index == 0:
                    index = total_tasks - 1
                else:
                    index -= 1
            elif user_choice.upper() == "E":
                Task.edit_task(tasks[index])
            elif user_choice.upper() == "D":
                Task.delete_task(tasks[index])
                tasks = Task.select()
                total_tasks = len(tasks)
                index = 0
            elif user_choice.upper() == "M":
                break
            else:
                print("Invalid entry. Please retry")

    @classmethod
    def search_by_employee(cls):
        """
        Search tasks by employees
        Lists matching employees
        User needs to select one to view employees tasks
        """
        utils.clear_screen()
        print("Please enter name of the employee" +
              "\nor leave blank and press enter to view all employees")
        print("or enter 'q' to return to search menu\n")
        index = 0
        total_employees = 0
        while total_employees == 0:
            search_string = input("Employee name: ")
            # Search employees for search string
            if search_string:
                employees = Task.select(
                    Task.username).where(
                    Task.username.contains(search_string)).distinct()
            else:
                employees = Task.select(Task.username).distinct()
            total_employees = len(employees)
            if not employees:
                print("No results found. Please retry")
            if search_string.lower() == "q":
                break
        else:
            print("\nFound {} employees. Please select one:\n".format(
                total_employees))
            # List employees with the name that includes the search string
            for employee in employees:
                print("{}: {}".format(index + 1, employee.username))
                index += 1
            usernumber = None
            while usernumber is None:
                # Request user to select one from search results
                try:
                    user_input = int(input(
                        "\nPlease enter the number of the employee: "))
                    if user_input not in range(1, total_employees + 1):
                        raise ValueError("Can not find the user by id.")
                except ValueError as err:
                    print(err)
                    print("Invalid entry. Please enter a number in the list.")
                else:
                    usernumber = user_input
            # Return tasks of selected user
            employees_tasks = Task.select().where(
                Task.username == employees[usernumber - 1].username)
            return {'tasks': employees_tasks,
                    'employee': employees[usernumber - 1].username}

    @classmethod
    def search_by_date(cls):
        """
        Search tasks by employees
        Lists matching employees
        User needs to select one to view employees tasks
        """
        utils.clear_screen()
        print("Please select an option")
        print("s) search for a date")
        print("v) to view all dates")
        print("q) to return to search menu\n")
        total = 0
        while total == 0:
            user_input = input("> ")
            # Search for a date
            if user_input == "s":
                date = utils.get_date()
                tasks = Task.select(
                    Task.date).where(
                    Task.date == date).distinct()
            elif user_input == "v":
                # View all dates from db
                tasks = Task.select(Task.date).distinct()
            elif user_input == "q":
                break
            else:
                print("Invalid entry. Please retry!")
                break
            index = 0
            total = len(tasks)
            print("\nFound {} dates. Please select one:\n".format(
                total))
            for dates in tasks:
                print("{}: {}".format(index + 1, dates.date))
                index += 1
            usernumber = None
            # Request user to select a date
            while usernumber is None:
                try:
                    user_input = int(input(
                        "\nPlease enter the number of the date: "))
                    if user_input not in range(1, total + 1):
                        raise ValueError("Can not find the date by id.")
                except ValueError as err:
                    print(err)
                    print("Invalid entry. Please enter a number in the list.")
                else:
                    usernumber = user_input
            # return tasks at selected date
            tasks_by_date = Task.select().where(
                Task.date == tasks[usernumber - 1].date)
            return {'tasks': tasks_by_date,
                    'date': tasks[usernumber - 1].date}

    @classmethod
    def search_by_keyword(cls):
        """
        Search for task title and notes by keyword
        """
        utils.clear_screen()
        print("Please enter a keyword to search:")
        print("Enter 'q' to quit!.\n")
        total = 0
        while total == 0:
            keyword = input("Keyword: ")
            if keyword.lower() == "q":
                break
            tasks = Task.select().where(
                (Task.title.contains(keyword)) |
                (Task.notes.contains(keyword)))
            print("No results found... Please retry")
            total = len(tasks)
        else:
            return {'tasks': tasks,
                    'keyword': keyword,
                    }

    @classmethod
    def search_by_time_spend(cls):
        """
        Search for tasks by time spent
        """
        utils.clear_screen()
        print("Please enter time spent on task:")
        total = 0
        while total == 0:
            timespent = utils.get_time_spent(
                input("Time spent(rounded minutes): "))
            tasks = Task.select().where(Task.time_spent == timespent)
            print("No results found... Please retry.")
            total = len(tasks)
        else:
            return {'tasks': tasks,
                    'time_spent': timespent,
                    }

    @classmethod
    def search_by_date_range(cls):
        """
        List tasks in date range
        """
        utils.clear_screen()
        print("Please enter start and end dates to search for a date range:\n")
        total = 0
        while total == 0:
            start_date = None
            end_date = None
            while not start_date:
                print("Start Date:")
                start_date = utils.get_date()
            while not end_date:
                print("End Date:")
                end_date = utils.get_date()

            tasks = Task.select().where(
                (Task.date > start_date) &
                (Task.date < end_date)).order_by(Task.date.desc())
            print("No results found... Please retry.")
            total = len(tasks)
        else:
            return {
                'tasks': tasks,
                'start_date': start_date,
                'end_date': end_date,
            }


def initialize():
    """
    Create the database and the table if not exists
    """
    db.connect()
    db.create_tables([Task], safe=True)
