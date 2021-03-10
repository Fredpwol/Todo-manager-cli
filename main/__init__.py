import os
import sys


path = "USERPROFILE" if sys.platform == 'win32' else "HOME"
session = os.path.join(os.environ.get(path),".todosession")
FILENAME = os.path.join(os.environ.get(path),"todo_cli.db")