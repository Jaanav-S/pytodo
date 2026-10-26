import pytest

import todo


def test_add_assigns_ids():
    tasks = []
    todo.add(tasks, "a")
    todo.add(tasks, "b")
    assert [t["id"] for t in tasks] == [1, 2]


def test_add_validates_priority_and_date():
    with pytest.raises(ValueError):
        todo.add([], "x", priority="urgent")
    with pytest.raises(ValueError):
        todo.add([], "x", due="next tuesday")


def test_mark_done_and_clear():
    tasks = []
    todo.add(tasks, "a")
    todo.add(tasks, "b")
    todo.mark_done(tasks, 1)
    assert todo.clear_done(tasks) == 1
    assert [t["title"] for t in tasks] == ["b"]


def test_remove_missing_raises():
    with pytest.raises(KeyError):
        todo.remove([], 5)


def test_sort_key_orders_by_priority_then_due():
    tasks = []
    todo.add(tasks, "later", due="2030-01-01")
    todo.add(tasks, "soon", due="2026-01-01")
    todo.add(tasks, "urgent", priority="high")
    assert [t["title"] for t in sorted(tasks, key=todo.sort_key)] == ["urgent", "soon", "later"]


def test_format_task_marks_overdue():
    task = {"id": 1, "title": "pay rent", "priority": "normal", "due": "2026-01-01", "done": False}
    assert "OVERDUE" in todo.format_task(task, today="2026-02-01")
