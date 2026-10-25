"""A minimal to-do list manager backed by a JSON file."""

import argparse
import json
import os
from datetime import date
from pathlib import Path

PRIORITIES = {"high": 0, "normal": 1, "low": 2}


def default_path():
    return Path(os.environ.get("TODO_FILE", "todo.json"))
