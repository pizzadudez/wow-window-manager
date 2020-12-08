import keyboard

from .api import WindowManager
from .utils import copy_to_clipboard
from .mouse_custom import on_click_modified


api = WindowManager()


def ctrl_left_click(event):
    # ignore events fired ages ago
    if event.time < api.last_swap_end + 0.05:
        return
    if not api.scroll_lock_on or not keyboard.is_pressed("ctrl"):
        return
    api.swap_to_next_window(locked=True, minimize_current=True)


def main():
    print("Listening to Global HotKeys")

    # @@test mouse click
    on_click_modified(ctrl_left_click)

    # @@helpers
    keyboard.add_hotkey("scroll lock", api.toggle_scroll_lock)
    keyboard.add_hotkey("ctrl+alt+f3", copy_to_clipboard)

    # @@launch
    keyboard.add_hotkey("ctrl+alt+f1", api.launch_and_rename_windows)
    # close all
    keyboard.add_hotkey("ctrl+alt+f4", api.close_all_windows)
    # overlay
    keyboard.add_hotkey("ctrl+alt+f5", api.launch_overlay)
    keyboard.add_hotkey("ctrl+alt+f5", api.close_overlay)

    # @@cylce swapping
    keyboard.add_hotkey("ctrl+enter", api.swap_to_next_window)
    keyboard.add_hotkey("ctrl+q", api.swap_to_next_window)
    keyboard.add_hotkey("c", api.swap_to_next_window, args=[True])
    # iwm
    keyboard.add_hotkey("r", api.swap_to_next_window, args=[True, True])
    # abilities/macros
    keyboard.add_hotkey("shift+q", api.swap_to_next_window, args=[True])
    keyboard.add_hotkey("shift+e", api.swap_to_next_window, args=[True])
    keyboard.add_hotkey("x", api.swap_to_next_window, args=[True])
    # misc utility
    keyboard.add_hotkey("f3", api.swap_to_next_window, args=[True])
    keyboard.add_hotkey("f4", api.swap_to_next_window, args=[True])
    keyboard.add_hotkey("f5", api.swap_to_next_window, args=[True])
    keyboard.add_hotkey("f6", api.swap_to_next_window, args=[True])

    # @@swap specific
    keyboard.add_hotkey("shift+c", api.swap_to_window, args=[0])
    for idx in list(range(0, 10)):
        # swap to acc_idx
        keyboard.add_hotkey(f"ctrl+{idx}", api.swap_to_window, args=[idx])
        # launch acc_idx
        keyboard.add_hotkey(f"ctrl+shift+{idx}", api.launch_wow_window, args=[idx])
        # close acc_idx
        keyboard.add_hotkey(f"ctrl+alt+{idx}", api.close_window, args=[idx])

    # @@testing
    # keyboard.add_hotkey("ctrl+alt+s", api.test_end_proc)
    keyboard.wait("ctrl+alt+f12")


if __name__ == "__main__":
    main()

    # close all windows
    # close window hotkey
    # get open windows and store their stuff
