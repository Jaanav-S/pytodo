"""A minimal to-do list manager backed by a JSON file."""

import argparse
import json
import os
from datetime import date
from pathlib import Path

PRIORITIES = {"high": 0, "normal": 1, "low": 2}


def default_path():
    return Path(os.environ.get("TODO_FILE", "todo.json"))


def load(path):
    """Load tasks from disk, returning an empty list if the file is missing."""
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, tasks):
    path.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def add(tasks, title, priority="normal", due=None):
    """Append a task and return it."""
    if priority not in PRIORITIES:
        raise ValueError(f"unknown priority: {priority}")
    if due is not None:
        date.fromisoformat(due)  # validates the format
    task = {"id": next_id(tasks), "title": title, "priority": priority, "due": due, "done": False}
    tasks.append(task)
    return task


def find(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise KeyError(f"no task with id {task_id}")


def mark_done(tasks, task_id):
    find(tasks, task_id)["done"] = True


def remove(tasks, task_id):
    tasks.remove(find(tasks, task_id))


def clear_done(tasks):
    """Drop finished tasks, returning how many were removed."""
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    return before - len(tasks)


def sort_key(task):
    return (task["done"], PRIORITIES[task["priority"]], task["due"] or "9999-12-31", task["id"])


def format_task(task, today=None):
    today = today or date.today().isoformat()
    box = "[x]" if task["done"] else "[ ]"
    line = f"{task['id']:>3} {box} {task['title']}"
    if task["priority"] != "normal":
        line += f"  ({task['priority']})"
    if task["due"]:
        overdue = not task["done"] and task["due"] < today
        line += f"  due {task['due']}" + ("  OVERDUE" if overdue else "")
    return line


def build_parser():
    parser = argparse.ArgumentParser(description="Terminal to-do list")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="add a task")
    p.add_argument("title")
    p.add_argument("--priority", choices=PRIORITIES, default="normal")
    p.add_argument("--due", help="due date as YYYY-MM-DD")

    p = sub.add_parser("list", help="show tasks")
    p.add_argument("--all", action="store_true", help="include finished tasks")

    for name in ("done", "remove"):
        p = sub.add_parser(name)
        p.add_argument("id", type=int)

    sub.add_parser("clear", help="remove finished tasks")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    path = default_path()
    tasks = load(path)

    if args.command == "add":
        task = add(tasks, args.title, args.priority, args.due)
        print(f"Added #{task['id']}: {task['title']}")
    elif args.command == "list":
        shown = [t for t in tasks if args.all or not t["done"]]
        for task in sorted(shown, key=sort_key):
            print(format_task(task))
        if not shown:
            print("Nothing to do.")
    elif args.command == "done":
        mark_done(tasks, args.id)
    elif args.command == "remove":
        remove(tasks, args.id)
    elif args.command == "clear":
        print(f"Removed {clear_done(tasks)} finished task(s).")

    save(path, tasks)


if __name__ == "__main__":
    main()
