from io import StringIO
import unittest
import datetime
from unittest.mock import patch, call
from unittest import mock

from peewee import *

from task import Task
import utils
import menu


MODELS = [Task]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class TaskTestCase(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

        self.task1 = Task.create(
            username="Kagan Aksoy",
            title="Test this app",
            date='15/01/2019',
            time_spent=45,
            notes="Notes for test"
        )

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_check_task_table(self):
        """
        Check if table created
        """
        assert Task.table_exists()

    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def test_view_task(self, mock_stdout):
        """
        Test view task method viewing task content properly
        """
        Task.view_task(self.task1)
        self.assertIn("Test this app", mock_stdout.getvalue())
        self.assertIn("15/01/2019", mock_stdout.getvalue())
        self.assertIn("Notes for test", mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def test_view_tasks(self, mock_stdout):
        """
        Test view tasks method with task and title attributes
        """
        fake_input = mock.Mock(side_effect=['M'])
        with patch('builtins.input', fake_input):
            title = "Check this title"
            tasks = (Task.select().where((Task.title == "Test this app")))
            Task.view_tasks(tasks, title)
            self.assertIn("Test this app", mock_stdout.getvalue())
            self.assertIn("Check this title", mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def test_view_tasks_without_attr(self, mock_stdout):
        """
        Test view tasks method without task and title attributes
        """
        fake_input = mock.Mock(side_effect=['M'])
        with patch('builtins.input', fake_input):
            Task.view_tasks()
            self.assertIn("Test this app", mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def test_view_tasks_delete_option(self, mock_stdout):
        """
        Test view tasks method without task and title attributes
        """
        fake_input = mock.Mock(side_effect=['D', 'Y'])
        with patch('builtins.input', fake_input):
            Task.view_tasks()
            self.assertIn("Test this app", mock_stdout.getvalue())
        check_delete = (Task.select()
                        .where((Task.title == "Test this app") &
                               (Task.username == "Kagan Aksoy")))
        self.assertTrue(check_delete.count() == 0)

    def test_create_task(self):
        """
        Test create task method success fully creates task with
        user defined values
        """
        fake_input = mock.Mock(side_effect=['Oguz', '07/01/2019', 'Task Test',
                                            '10', 'Test Task Notes'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                Task.create_task()
                self.assertEqual(fake_input.call_count, 5)
        #Check if the task is created
        check_created = (Task.select().where(
            (Task.title == "Task Test")))
        self.assertTrue(check_created.count() == 1)

    def test_edit_task(self):
        """
        Test edit task function
        """
        fake_task = ['Edited test task', 'Jhon Doe', '10/01/2019',
                     '160', 'Edited task notes here']
        fake_input = mock.Mock(side_effect=fake_task)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                Task.edit_task(self.task1)
        # Check if the task is edited
        check_edited = (Task.select().where(
            (Task.title == "Edited test task")))
        self.assertTrue(check_edited.count() == 1)

    def test_search_by_keyword(self):
        """
        Test search by keyword
        Search for 'notes'
        Check the result title
        """
        fake_input = mock.Mock(side_effect=['Notes', ''])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                data = Task.search_by_keyword()
                self.assertEqual(data['tasks'][0].title, "Test this app")

    def test_search_by_time_spend(self):
        """
        Test search by time spent
        """
        fake_input = mock.Mock(side_effect=[45])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                data = Task.search_by_time_spend()
                self.assertEqual(data['tasks'][0].title, "Test this app")

    def test_search_by_date(self):
        """
        Test search date with fake input
        """
        fake_input = mock.Mock(side_effect=['s', '15/01/2019', 1])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                data = Task.search_by_date()
                self.assertEqual(fake_input.call_count, 3)
                self.assertEqual(data['tasks'][0].title, "Test this app")

    def test_search_by_date_range(self):
        """
        Test search by date range with fake input
        """
        fake_input = mock.Mock(side_effect=['14/01/2019', '16/01/2019'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                data = Task.search_by_date_range()
                self.assertEqual(fake_input.call_count, 2)
                self.assertEqual(data['tasks'][0].title, "Test this app")

    def test_search_by_employee(self):
        """
        test search by employee
        """
        fake_input = mock.Mock(side_effect=['Kagan Aksoy', "1"])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                data = Task.search_by_employee()
                self.assertEqual(fake_input.call_count, 2)
                self.assertEqual(data['tasks'][0].title, "Test this app")

    @patch('builtins.input', lambda x: 'y')
    def test_delete_task(self):
        """delete test data"""
        Task.delete_task(self.task1)
        check_delete = (Task.select()
                        .where((Task.title == "Test this app") &
                               (Task.username == "Kagan Aksoy")))
        self.assertTrue(check_delete.count() == 0)


class UtilsTest(unittest.TestCase):
    def test_get_date(self):
        """
        Test get date works properly and detects invalid dates
        """
        self.assertFalse(utils.get_date('02/20/1022'))
        self.assertTrue(utils.get_date('30/01/2019'))

    def test_get_time_spent(self):
        """
        Test get time spent for invalid integers
        """
        self.assertFalse(utils.get_time_spent("Hi"))
        self.assertTrue(utils.get_time_spent(15))

    def test_convert_string_to_date(self):
        """
        Test convert string to datetime object works properly
        """
        self.assertEqual(
            utils.convert_string_to_date("30/09/2018"),
            datetime.datetime(2018, 9, 30))


class MenuTest(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def test_show_main_menu(self, mock_stdout):
        """
        Test main manu includes search option
        """
        menu.show_main_menu()
        self.assertIn("a) Add new entry?", mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def test_show_search_menu(self, mock_stdout):
        """
        Test search menu displays search options
        """
        menu.show_search_menu()
        self.assertIn("Do you want to search by:", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
