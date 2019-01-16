# Work Log with a Database
---

Treehouse Techdegree Project 4

A command line application that will allow employees to enter their name, time worked, task worked on, and general notes about the task into a database. 

![Start](https://github.com/nauticalist/pythonfun_worklog_with_db/blob/master/screenshots/app.main.png)

## About

This project is an improved version of previous project (Worklog that saves user data to json) with the following features:

- User can create tasks with employee name, task title, date of the task, time spent (in minutes), and optionally add notes.
- Entries saved to a database(SQLite in our case)
- User can view all entries.

![Search](https://github.com/nauticalist/pythonfun_worklog_with_db/blob/master/screenshots/app.search.png)

- User can find entries that match an employee's name.
- User can find entries based on date and the date format to search is displayed, e.g. DD/MM/YYYY
- User can find entries based on time spent on a task.
- User can find entries based on a term in either the task name or notes.
- Main menu has quit option and search menu has return to main menu option
- Records can be deleted and edited, letting user change the date, task name, time spent, and/or notes.
- If multiple employees share a name (e.g. multiple people with the first name Beth), a list of possible matches is given.
- Can find entries based on a ranges of dates. For example between 01/01/2019 and 31/12/2019
- Records are displayed one at a time with the ability to stop paging through records (previous/next/back to list).
- Test coverage

![Start](https://github.com/nauticalist/pythonfun_worklog_with_db/blob/master/screenshots/coverage.png)

## Dependencies

- Python 3.6 or later
- coverage==4.5.2
- peewee==3.8.1

Refer to requirements.txt

## To start

```
git clone https://github.com/nauticalist/pythonfun_worklog_with_db.git
cd pythonfun_worklog_with_db
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python app.py
```