import json

FILEPATH = "data/todos.json"


def get_todos(filepath=FILEPATH):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_todos(todos, filepath=FILEPATH):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(todos, file, ensure_ascii=False, indent=4)