import win32gui as gui
import win32process as proc

from pathlib import Path

from .config import ACCOUNT_FOLDERS_ROOT


class WindowManager:
    def __init__(self):
        self.path = ACCOUNT_FOLDERS_ROOT

    def test_print(self):
        print(self.path)
