import subprocess
import os

from pathlib import Path

from config import SETUP_PATH


exe_path = Path(SETUP_PATH) / "wow0" / "_retail_" / "WoW.exe"
exe_path2 = Path(SETUP_PATH) / "wow1" / "_retail_" / "WoW.exe"
test_path = Path(r"C:\Program Files\Sublime Text 3\sublime_text.exe")


def launch(path):
    # creationflags = (
    #     subprocess.DETACHED_PROCESS
    #     # | subprocess.CREATE_NEW_PROCESS_GROUP
    #     # | subprocess.CREATE_BREAKAWAY_FROM_JOB
    # )
    # subprocess.Popen(
    #     path,
    #     close_fds=True,
    #     creationflags=creationflags,
    #     # stdin=subprocess.PIPE,
    #     # stdout=subprocess.PIPE,
    #     # stderr=subprocess.PIPE,
    # )
    # os.spawnl(os.P_DETACH, path, "test")

    # p = subprocess.Popen(path, start_new_session=True)

    process = subprocess.Popen(
        [path],
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    )

    # os.startfile(path)


if __name__ == "__main__":
    launch(test_path)
    # launch(exe_path2)