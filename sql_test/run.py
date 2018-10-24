import sqlite3

from collections import namedtuple


class Task:
    def __init__(self, tsak_id, description, answer, attempts, completed):
        self.id = tsak_id
        self.description = description
        self.answer = answer
        self.attempts = attempts
        self.completed = completed


def get_progress(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(completed) FROM tasks;")
    response = cursor.fetchone()
    tasks_count = response[0]
    tasks_completed = response[1]
    conn.close()
    return tasks_count, tasks_completed


def reset_test(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET attempts=0, completed=0;")
    conn.commit()
    conn.close()


def get_tasks_from_database(sqlite_file):
    tasks = list()
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM tasks;"):
        new_task = Task(row[0], row[1], row[2], row[3], row[4])
        tasks.append(new_task)
    conn.close()
    return tasks


def set_task(task):
    while True:
        answer = input("\n{0} {1}\n".format(task.id, task.description))
        right = answer == task.answer
        yield right

        if right:
            break
        elif answer == "help":
            print(task.answer)
        else:
            print("Неверно")


def start_test(tasks, sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    for task in tasks:
        if task.completed:
            continue

        for result in set_task(task):
            task.attempts += 1
            if result:
                task.completed = 1
            cursor.execute("UPDATE tasks SET attempts=attempts+1, completed={0} WHERE id={1};".format(
                task.completed, task.id))
            conn.commit()

    conn.close()


if __name__ == "__main__":
    tasks_count, tasks_completed = get_progress("sql_tasks.db")
    print(tasks_completed, tasks_count)
    if tasks_completed == tasks_count:
        reset_test("sql_tasks.db")
    elif 0 < tasks_completed < tasks_count:
        print("Прошлый тест не закончен. Успешно выполнено {0} из {1} заданий".format(tasks_completed, tasks_count))
        while True:
            answer = input("Продолжить? (да/нет)\n")
            if answer in ["да", "нет"]:
                break

        if answer == "нет":
            reset_test("sql_tasks.db")
    tasks = get_tasks_from_database("sql_tasks.db")
    start_test(tasks, "sql_tasks.db")
