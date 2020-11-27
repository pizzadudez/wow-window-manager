import os

from .config import PASSWORD


def copy_to_clipboard():
    command = "echo " + PASSWORD.strip() + "| clip"
    os.system(command)
    print("Clipboard copy")
