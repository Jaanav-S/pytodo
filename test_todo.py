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
