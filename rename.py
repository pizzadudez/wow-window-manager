"""Testing renaming with hidden wow window"""

import time
import win32gui as gui
import win32process as proc
import win32api as api
import win32con as con

from pathlib import Path

from config import SETUP_PATH


DEFAULT_TITLE = "World of Warcraft"
TITLE_PREFIX = "wow"

acc_idx_hwnd = {}


def launch_wow(pathObj, acc_idx):
    info = proc.STARTUPINFO()
    info.dwFlags = proc.STARTF_USESHOWWINDOW
    info.wShowWindow = con.SW_NORMAL

    hProcess, hThread, dwProcessId, dwThreadId = proc.CreateProcess(
        None,  # appName
        str(path),
        None,  # processAttributes
        None,  # threadAttributes
        False,  # bInheritHandles
        con.DETACHED_PROCESS | con.CREATE_NEW_PROCESS_GROUP,
        None,
        None,
        info,
    )

    return dwProcessId


def enum_windows_handler(hwnd, hwnd_list):
    """Get visible World of Warcraft window handles."""

    is_wow_title = gui.GetWindowText(hwnd) == DEFAULT_TITLE
    if is_wow_title and gui.IsWindowVisible(hwnd):
        hwnd_list.append(hwnd)


def rename_wows(process_acc_idx):
    hwnd_list = []
    gui.EnumWindows(enum_windows_handler, hwnd_list)

    # Associate window_handle with process_id and rename window\
    for hwnd in hwnd_list:
        _, process_id = proc.GetWindowThreadProcessId(hwnd)
        acc_idx = process_acc_idx[process_id]
        new_title = f"{TITLE_PREFIX}{acc_idx}"
        gui.SetWindowText(hwnd, new_title)

        # Store hwnd for acc_idx
        acc_idx_hwnd[acc_idx] = hwnd


def resize_and_position_wows():
    for acc_idx, hwnd in acc_idx_hwnd.items():
        x = acc_idx % 4 * 450
        y = acc_idx // 4 * 320
        width = 450
        height = 320
        gui.SetWindowPos(
            hwnd, con.HWND_TOPMOST, x, y, width, height, con.SWP_SHOWWINDOW
        )


if __name__ == "__main__":
    acc_indices = list(range(10))
    paths = [Path(SETUP_PATH) / f"wow{x}" / "_retail_" / "WoW.exe" for x in acc_indices]
    process_acc_idx = {}
    for acc_idx, path in enumerate(paths):
        process_id = launch_wow(path, acc_idx)
        process_acc_idx[process_id] = acc_idx
    # TODO: wait for windows to finish launching instead of sleeping
    time.sleep(7)
    rename_wows(process_acc_idx)
    resize_and_position_wows()

    time.sleep(5)

    input()
