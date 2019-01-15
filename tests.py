from io import StringIO
import unittest
import datetime
from unittest.mock import patch
from unittest import mock

from peewee import *

from task import Task
import utils

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
                date=datetime.datetime(2019, 1, 15),
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
        assert Task.table_exists()

    # def test_create_task(self):
    #     fake_input = mock.Mock(side_effect=['Oguz', '0/01/2019', 'Task Test',
    #                                         '10', 'Test Task Notes'])
    #     with patch('sys.stdout', new=StringIO()) as fake_out:
    #         with patch('builtins.input', fake_input):
    #             test_task = Task()
    #             self.assertEqual(fake_input.call_count, 5)
    #             test_task.delete_task()

    def test_search_by_keyword(self):
        fake_input = mock.Mock(side_effect=['¥®œ¬ø^~ç', ''])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                Task.search_by_keyword()

    # def test_search_by_time_spend(self):
    #     fake_input = mock.Mock(side_effect=['99999999', ''])
    #     with patch('sys.stdout', new=StringIO()) as fake_out:
    #         with patch('builtins.input', fake_input):
    #             Task.search_by_time_spend()


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
        self.assertFalse(utils.get_date('02/20/1022'))
        self.assertTrue(utils.get_date('30/01/2019'))

    def test_get_time_spent(self):
        self.assertFalse(utils.get_time_spent("Hi"))
        self.assertTrue(utils.get_time_spent(15))

    def test_convert_date_to_string(self):
        self.assertEqual(
            utils.convert_date_to_string(
                datetime.datetime(2018, 9, 30, 7, 6, 5)), "30/09/2018")

    def test_convert_string_to_date(self):
        self.assertEqual(
            utils.convert_string_to_date("30/09/2018"),
            datetime.datetime(2018, 9, 30))


if __name__ == '__main__':
    unittest.main()
