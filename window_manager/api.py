import time
import win32gui as gui
import win32process as proc
import win32con as con

from pathlib import Path

from .db import get_acc_indices
from .config import ACCOUNT_FOLDERS_ROOT


ACCOUNT_INDICES = [2, 5, 6, 8, 9]
# ACCOUNT_INDICES = [0, 1, 2, 3, 4, 5, 7, 9]
# ACCOUNT_INDICES = [5, 7, 9]
# ACCOUNT_INDICES = [0, 1, 2, 3, 4]
# ACCOUNT_INDICES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

DEFAULT_TITLE = "World of Warcraft"
TITLE_PREFIX = "wow"

SWAP_DELAY = 0.16

OVERLAY_PATH = Path(r"D:\_repos\select-overlay\dist\win-unpacked\WowSelectOverlay")
OVERLAY_TITLE = "WoWSelectOverlay"


class WindowManager:
    def __init__(self):
        self.acc_indices = get_acc_indices()
        self.paths = {
            x: Path(ACCOUNT_FOLDERS_ROOT) / f"wow{x}" / "_retail_" / "WoW.exe"
            for x in self.acc_indices
        }
        self.hwnd_list = []
        # Store acc_idx for launched processes
        self.process_acc_idx = {}
        # Store hwnd for windows by acc_idx
        self.acc_idx_hwnd = {}
        # Store proccess handle by acc_idx
        self.acc_idx_proc_handle = {}

        self.last_foreground_acc_idx = None

        # scroll lock on enables certain keys to work only when active
        self.scroll_lock_on = False

        self.overlay = {
            "proc_id": None,
            "proc_handle": None,
            "hwnd": None,
        }

    def toggle_scroll_lock(self):
        self.scroll_lock_on = not self.scroll_lock_on
        print("Scroll-Lock " + ("ON" if self.scroll_lock_on else "OFF"))

    def _launch_window(self, pathObj, acc_idx):
        info = proc.STARTUPINFO()
        info.dwFlags = con.STARTF_USESHOWWINDOW
        info.wShowWindow = con.SW_NORMAL

        proc_handle, _, proc_id, _ = proc.CreateProcess(
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
        return proc_handle, proc_id

    def launch_overlay(self):
        info = proc.STARTUPINFO()
        info.dwFlags = con.STARTF_USESHOWWINDOW
        info.wShowWindow = con.SW_SHOWMAXIMIZED

        proc_handle, _, proc_id, _ = proc.CreateProcess(
            None,
            str(OVERLAY_PATH),
            None,
            None,
            False,
            con.DETACHED_PROCESS | con.CREATE_NEW_PROCESS_GROUP,
            None,
            None,
            info,
        )
        self.overlay["proc_handle"] = proc_handle
        self.overlay["proc_id"] = proc_id

    def close_overlay(self):
        proc_handle = self.overlay.get("proc_handle", None)
        if not proc_handle:
            return
        exit_code = proc.GetExitCodeProcess(proc_handle)
        proc.TerminateProcess(proc_handle, exit_code)

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
            acc_idx = self.process_acc_idx.get(proc_id, None)
            if acc_idx is None:
                continue  # Fix for finding false positives wow windows
            new_title = f"{TITLE_PREFIX}{acc_idx}"
            gui.SetWindowText(hwnd, new_title)

            self.acc_idx_hwnd[acc_idx] = hwnd

    def _fix_focus_bug(self):
        """Minimize and restore each window once so SetWinEventHook
        works properly."""

        for acc_idx in self.acc_idx_hwnd.keys():
            self._set_foreground_window(acc_idx)

    def launch_and_rename_windows(self):
        print("Launching")
        for acc_idx, path in self.paths.items():
            proc_handle, proc_id = self._launch_window(path, acc_idx)
            self.acc_idx_proc_handle[acc_idx] = proc_handle
            self.process_acc_idx[proc_id] = acc_idx

        # TODO: wait for windows to finish launching instead of sleeping
        time.sleep(8)
        self._rename_windows()
        self._fix_focus_bug()
        # self.launch_overlay()

    def launch_wow_window(self, acc_idx):
        """Launch individual Wow window"""

        print(f"Launching acc: {acc_idx}")
        path = Path(ACCOUNT_FOLDERS_ROOT) / f"wow{acc_idx}" / "_retail_" / "WoW.exe"
        proc_handle, proc_id = self._launch_window(path, acc_idx)
        self.acc_idx_proc_handle[acc_idx] = proc_handle
        self.process_acc_idx[proc_id] = acc_idx
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

    def _set_foreground_window(self, acc_idx, minimize_current=False):
        # Delay
        time.sleep(SWAP_DELAY)

        # Maximize wanted window
        hwnd_cur = self.acc_idx_hwnd[acc_idx]
        if not gui.IsIconic(hwnd_cur):
            print("not min", acc_idx)
            gui.ShowWindow(hwnd_cur, con.SW_SHOWMINIMIZED)
        gui.ShowWindow(hwnd_cur, con.SW_RESTORE)
        # Minimize current window
        if minimize_current:
            prev_acc_idx = self.last_foreground_acc_idx
            if prev_acc_idx is not None:
                hwnd_prev = self.acc_idx_hwnd[prev_acc_idx]
                if hwnd_prev and not gui.IsIconic(hwnd_prev):
                    gui.ShowWindow(hwnd_prev, con.SW_SHOWMINIMIZED)
        # Minimize window after wanted to prevent min+max at the same time
        # on the next step
        if minimize_current:
            next_acc_idx = self._get_next_acc_idx(acc_idx)
            if next_acc_idx is not None:
                hwnd_next = self.acc_idx_hwnd.get(next_acc_idx, None)
                if hwnd_next and not gui.IsIconic(hwnd_next):
                    gui.ShowWindow(hwnd_next, con.SW_SHOWMINIMIZED)

        self.last_foreground_acc_idx = acc_idx

    def _set_foreground_window_new(self, acc_idx):
        # TODO new idea
        # Delay
        time.sleep(SWAP_DELAY)
        # Minimize current
        prev_acc_idx = self.last_foreground_acc_idx
        if prev_acc_idx is not None:
            hwnd_prev = self.acc_idx_hwnd[prev_acc_idx]
            gui.ShowWindow(hwnd_prev, con.SW_SHOWMINIMIZED)
        # Maximize (or min-max next window to get it ready)
        next_acc_idx = self._get_next_acc_idx(acc_idx)
        hwnd_next = self.acc_idx_hwnd[next_acc_idx]
        if not gui.IsIconic(hwnd_next):
            # print("not min", acc_idx)
            gui.ShowWindow(hwnd_next, con.SW_SHOWMINIMIZED)
        gui.ShowWindow(hwnd_next, con.SW_RESTORE)

        self.last_foreground_acc_idx = acc_idx

    def _get_next_acc_idx(self, prev_acc_idx):
        """Get next acc index in list"""

        prev_idx = self.acc_indices.index(prev_acc_idx)

        if prev_idx == len(self.acc_indices) - 1:
            return self.acc_indices[0]
        else:
            return self.acc_indices[prev_idx + 1]

    def swap_to_next_window(self, locked=False, minimize_current=False):
        """Pass locked arg true to block swap when scroll_lock_off"""
        if locked and not self.scroll_lock_on:
            print(">> SCROLL LOCK - OFF")
            return

        # TODO: handle foreground not being wow window
        print("Swap to next window")
        hwnd = gui.GetForegroundWindow()
        _, proc_id = proc.GetWindowThreadProcessId(hwnd)
        acc_idx = self.process_acc_idx.get(proc_id, None)
        if acc_idx is None:
            # Set last window to last in list of indices
            acc_idx = (
                self.last_foreground_acc_idx
                or self.acc_indices[len(self.acc_indices) - 1]
            )
            self.last_foreground_acc_idx = acc_idx

        next_idx = self._get_next_acc_idx(acc_idx)

        self._set_foreground_window(next_idx, minimize_current)

    def swap_to_window(self, acc_idx):
        if not self.acc_idx_hwnd.get(acc_idx, None):
            return

        print(f"Swap to {acc_idx}")
        self._set_foreground_window(acc_idx)

    def close_window(self, acc_idx):
        proc_handle = self.acc_idx_proc_handle.get(acc_idx, None)
        if not proc_handle:
            return
        exit_code = proc.GetExitCodeProcess(proc_handle)
        proc.TerminateProcess(proc_handle, exit_code)

    def close_all_windows(self):
        for acc_idx in self.acc_indices:
            self.close_window(acc_idx)
