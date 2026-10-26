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
