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
        username = input("Enter your username: ")
        utils.clear_screen()
        print("Date of the task")
        date = utils.get_date()
        date = utils.convert_date_to_string(date)
        utils.clear_screen()
        title = input("Title of the task: ")
        utils.clear_screen()
        time_spent = utils.get_time_spent()
        utils.clear_screen()
        notes = input("Notes (Optional, you can leave this empty): ")
        utils.clear_screen()
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
        title = input("Title of the task: ")
        username = input("Username: ")
        print("Date of the task")
        date = utils.get_date()
        date = utils.convert_date_to_string(date)
        time_spent = utils.get_time_spent()
        notes = input("Notes (Optional, you can leave this empty): ")
        task.title = title
        task.username = username
        task.date = date
        task.time_spent = time_spent
        task.notes = notes
        task.save()
        print("Task updated")

    @classmethod
    def view_tasks(cls, tasks=None, title=None):
        """
        View and iterate over tasks
        """
        if tasks is None:
            tasks = Task.select()
        total_tasks = len(tasks)
        index = 0
        while index < total_tasks:
            utils.clear_screen()
            if title:
                print("{}\n".format(title))

            Task.view_task(tasks[index])
            print("\nTask {} of {}\n".format(index + 1, total_tasks))
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
        utils.clear_screen()
        print("Please enter name of the employee")
        print("or enter 'q' to return to search menu\n")
        index = 0
        total_employees = 0
        while total_employees == 0:
            search_string = input("Employee name: ")
            employees = Task.select(
                Task.username).where(
                Task.username.contains(search_string)).distinct()
            total_employees = len(employees)
            print("No results found. Please retry")
            if search_string.lower() == "q":
                break
        else:
            print("\nFound {} employees. Please select one:\n".format(
                total_employees))
            for employee in employees:
                print("{}: {}".format(index + 1, employee.username))
                index += 1
            usernumber = None
            while usernumber is None:
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


            employees_tasks = Task.select().where(
                Task.username == employees[usernumber - 1].username)
            return {'tasks': employees_tasks,
                    'employee': employees[usernumber - 1].username}




def initialize():
    """
    Create the database and the table if not exists
    """
    db.connect()
    db.create_tables([Task], safe=True)
