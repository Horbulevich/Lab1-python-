import os
import functions
from datetime import datetime
def check_date(date):
    if not date:
        return True
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def show_help():
    print("\nДоступні команди:")
    print("add текст      - додати завдання")
    print("show           - показати завдання")
    print("edit номер     - редагувати завдання")
    print("delete номер   - видалити завдання")
    print("done номер     - змінити статус")
    print("search слово   - пошук завдання")
    print("help           - показати команди")
    print("exit           - завершити програму")

def add_task(todos, text):
    if not text:
        print("\tВведіть текст завдання")
        return
    for todo in todos:
        if todo["text"].lower() == text.lower():
            print("\tТаке завдання вже існує")
            return
    deadline = input(
        "Введіть термін (РРРР-ММ-ДД) або Enter: "
    ).strip()

    if not check_date(deadline):
        print("\tНеправильний формат дати")
        return
    todo = {
        "text": text,
        "completed": False,
        "deadline": deadline
    }
    todos.append(todo)
    functions.write_todos(todos)
    print("\tЗавдання додано")

def show_tasks(todos):
    if not todos:
        print("\tСписок порожній")
        return

    for number, todo in enumerate(todos, start=1):
        status = "✓" if todo["completed"] else " "

        deadline = todo["deadline"] or "без терміну"

        print(
            f"{number}. [{status}] "
            f"{todo['text']} | до: {deadline}"
        )
def get_number(argument, todos):
    try:
        number = int(argument)

        if number < 1 or number > len(todos):
            print("\tНевірний номер завдання")
            return None
        return number - 1
    except ValueError:
        print("\tВведіть цілий номер завдання")
        return None
def edit_task(todos, argument):
    index = get_number(argument, todos)
    if index is None:
        return
    new_text = input("Введіть новий текст: ").strip()
    if not new_text:
        print("\tТекст не може бути порожнім")
        return
    deadline = input(
        "Новий термін або Enter, щоб залишити старий: "
    ).strip()
    if deadline and not check_date(deadline):
        print("\tНеправильний формат дати")
        return
    todos[index]["text"] = new_text
    if deadline:
        todos[index]["deadline"] = deadline
    functions.write_todos(todos)
    print("\tЗавдання змінено")
def delete_task(todos, argument):
    index = get_number(argument, todos)
    if index is None:
        return
    deleted = todos.pop(index)
    functions.write_todos(todos)
    print(f"\tВидалено: {deleted['text']}")
def done_task(todos, argument):
    index = get_number(argument, todos)
    if index is None:
        return
    todos[index]["completed"] = not todos[index]["completed"]
    functions.write_todos(todos)
    if todos[index]["completed"]:
        print("\tЗавдання виконано")
    else:
        print("\tЗавдання знову активне")
def search_task(todos, text):
    if not text:
        print("\tВведіть слово для пошуку")
        return
    found = False
    for number, todo in enumerate(todos, start=1):
        if text.lower() in todo["text"].lower():
            print(f"{number}. {todo['text']}")
            found = True
    if not found:
        print("\tЗавдань не знайдено")

def repl():
    todos = functions.get_todos()
    print("=== TASKHUB CLI ===")
    print("Введіть help, щоб переглянути команди")

    while True:
        parts = input("\nTaskHub > ").strip().split(maxsplit=1)
        if not parts:
            print("\tВведіть команду")
            continue
        command = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""
        if command == "add":
            add_task(todos, argument)
        elif command == "show":
            show_tasks(todos)
        elif command == "edit":
            edit_task(todos, argument)
        elif command == "delete":
            delete_task(todos, argument)
        elif command == "done":
            done_task(todos, argument)
        elif command == "search":
            search_task(todos, argument)
        elif command == "help":
            show_help()
        elif command == "exit":
            print("\tРоботу завершено")
            break
        else:
            print("\tНевідома команда. Введіть help")
def main():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(functions.FILEPATH):
        functions.write_todos([])
    repl()
if __name__ == "__main__":
    main()