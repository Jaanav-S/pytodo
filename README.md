# todo

A to-do list for the terminal. Tasks live in a plain JSON file so they are
easy to back up or sync.

## Commands

```
python todo.py add "Buy milk" --priority high --due 2026-11-02
python todo.py list
python todo.py done 1
python todo.py remove 2
python todo.py clear
```

`list` shows open tasks first, sorted by priority and then due date.
Pass `--all` to include finished tasks.
