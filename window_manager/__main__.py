import keyboard

from .api import WindowManager

api = WindowManager()


def main():
    print("Listening to Global HotKeys")
    keyboard.add_hotkey("ctrl+alt+f1", api.launch_and_rename_windows)
    keyboard.add_hotkey("enter", api.swap_to_next_window)
    keyboard.add_hotkey("ctrl+e", api.swap_to_window, args=[0])
    for idx in list(range(1, 10)):
        keyboard.add_hotkey(f"ctrl+{idx}", api.swap_to_window, args=[idx])

    keyboard.wait("ctrl+alt+f12")


if __name__ == "__main__":
    main()
