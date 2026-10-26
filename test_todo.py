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
