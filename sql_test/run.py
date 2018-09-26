import sqlite3

from collections import namedtuple


Task = namedtuple("Task", ["id", "description", "answer"])


def get_tasks_from_database(sqlite_file):
    tasks = list()
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM tasks;"):
        new_task = Task(row[0], row[1], row[2])
        tasks.append(new_task)
    conn.close()
    return tasks


def set_task(task):
    result = False
    answer = input("\n{0} {1}\n".format(task.id, task.description))
    if answer == task.answer:
        result = True
    else:
        if answer == "help":
            print(task.answer)
        else:
            print("Неверно")
        set_task(task)
    return result


def start_test(tasks):
    test_results = dict()
    for task in tasks:
        result = set_task(task)
        test_results[task.id] = result
    for task_id in test_results:
        print(task_id, test_results[task_id])


if __name__ == "__main__":
    tasks = get_tasks_from_database("sql_tasks.db")
    start_test(tasks)
