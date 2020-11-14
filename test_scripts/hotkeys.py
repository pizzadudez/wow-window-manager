from pynput import keyboard


def on_activate():
    print("Global hotkey activated!")


def for_canonical(f):
    return lambda k: f(l.canonical(k))


hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+q"), on_activate)
with keyboard.Listener(
    on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release)
) as l:
    l.join()


# from pynput import keyboard

# def on_activate_h():
#     print('<ctrl>+<alt>+h pressed')

# def on_activate_i():
#     print('<ctrl>+<alt>+i pressed')

# with keyboard.GlobalHotKeys({
#         '<ctrl>+<alt>+h': on_activate_h,
#         '<ctrl>+<alt>+i': on_activate_i}) as h:
#     h.join()