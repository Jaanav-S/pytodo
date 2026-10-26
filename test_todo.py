import pytest

import todo


def test_add_assigns_ids():
    tasks = []
    todo.add(tasks, "a")
    todo.add(tasks, "b")
    assert [t["id"] for t in tasks] == [1, 2]
