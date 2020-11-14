import time
import win32gui as gui
import win32process as proc
import win32con as con

from pathlib import Path

from .config import ACCOUNT_FOLDERS_ROOT

DEFAULT_TITLE = "World of Warcraft"
TITLE_PREFIX = "wow"


class WindowManager:
    def __init__(self):
        self.acc_indices = list(range(10))
        self.paths = [
            Path(ACCOUNT_FOLDERS_ROOT) / f"wow{x}" / "_retail_" / "WoW.exe"
            for x in self.acc_indices
        ]
        self.hwnd_list = []
        # Store acc_idx for launched processes
        self.process_acc_idx = {}
        # Store hwnd for windows by acc_idx
        self.acc_idx_hwnd = {}

        self.last_foreground_acc_idx = None

    def _launch_window(self, pathObj, acc_index):
        info = proc.STARTUPINFO()
        info.dwFlags = con.STARTF_USESHOWWINDOW
        info.wShowWindow = con.SW_NORMAL

        _, _, proc_id, _ = proc.CreateProcess(
            None,
            str(pathObj),
            None,
            None,
            False,
            con.DETACHED_PROCESS | con.CREATE_NEW_PROCESS_GROUP,
            None,
            None,
            info,
        )
        self.process_acc_idx[proc_id] = acc_index

    def _enum_windows_handle(self, hwnd, hwnd_list):
        title_match = gui.GetWindowText(hwnd) == DEFAULT_TITLE
        # Game launches an additional invisible window with the same name
        if title_match and gui.IsWindowVisible(hwnd):
            hwnd_list.append(hwnd)

    def _rename_windows(self):
        gui.EnumWindows(self._enum_windows_handle, self.hwnd_list)

        # Associate window_handle
        for hwnd in self.hwnd_list:
            _, proc_id = proc.GetWindowThreadProcessId(hwnd)
            acc_idx = self.process_acc_idx[proc_id]
            new_title = f"{TITLE_PREFIX}{acc_idx}"
            gui.SetWindowText(hwnd, new_title)

            self.acc_idx_hwnd[acc_idx] = hwnd

    def launch_and_rename_windows(self):
        print("Launching")
        for acc_idx, path in enumerate(self.paths):
            self._launch_window(path, acc_idx)

        # TODO: wait for windows to finish launching instead of sleeping
        time.sleep(7)
        self._rename_windows()

    def resize_and_position_windows(self):
        print("Resize and Position")
        for acc_idx, hwnd in self.acc_idx_hwnd.items():
            x = acc_idx % 4 * 450
            y = acc_idx // 4 * 320
            width = 450
            height = 320
            gui.SetWindowPos(
                hwnd, con.HWND_TOPMOST, x, y, width, height, con.SWP_SHOWWINDOW
            )

    def _set_foreground_window(self, acc_idx):
        hwnd = self.acc_idx_hwnd[acc_idx]

        gui.ShowWindow(hwnd, con.SW_SHOWMINIMIZED)
        gui.ShowWindow(hwnd, con.SW_RESTORE)

        self.last_foreground_acc_idx = acc_idx

    def swap_to_next_window(self):
        # TODO: handle foreground not being wow window
        print("Swap to next window")
        hwnd = gui.GetForegroundWindow()
        _, proc_id = proc.GetWindowThreadProcessId(hwnd)
        acc_idx = self.process_acc_idx.get(proc_id, None)
        if acc_idx == None:
            acc_idx = self.last_foreground_acc_idx or 0

        next_idx = (acc_idx + 1) % len(self.acc_indices)

        self._set_foreground_window(next_idx)

    def swap_to_window(self, acc_idx):
        print(f"Swap to {acc_idx}")
        self._set_foreground_window(acc_idx)
