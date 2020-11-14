from pynput import keyboard

from .api import WindowManager

api = WindowManager()


class StopException(Exception):
    pass


def stop_listener():
    raise StopException


swap_callbacks = [lambda: api.swap_to_window(x) for x in list(range(10))]


def swap_next():
    api.swap_to_next_window()


def launch():
    api.launch_and_rename_windows()


def test1():
    print(1)


def test2():
    print(2)


hotkey_handlers = {
    "<alt>+q": swap_next,
    "<ctrl>+<alt>+<f12>": stop_listener,
    "<ctrl>+<alt>+<f1>": launch,
}


def main():
    print("Listening to Global HotKeys")
    # Keyboard Listener thread
    with keyboard.GlobalHotKeys(hotkey_handlers) as listener:
        try:
            listener.join()
        except StopException:
            print("Closing Listener")


if __name__ == "__main__":
    main()
