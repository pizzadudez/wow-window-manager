import win32gui
import time


# class WowWindowManager:
#     """"""

#     def __init__(self):
#         pass


# win32gui.SetActiveWindow(hwnd)
# win32gui.SetFocus(hwnd)
# hwnd2 = win32gui.GetForegroundWindow()


def window_enum_handler(hwnd, resultList):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_app_list(handles=[]):
    mlst = []
    win32gui.EnumWindows(window_enum_handler, handles)
    for handle in handles:
        mlst.append(handle)
    return mlst


appwindows = get_app_list()
for i in appwindows:
    print(i)


def rename_wow():
    dummy = win32gui.FindWindow(None, "World of Warcraft")
    win32gui.SetWindowText(dummy, "wow_dummy")
    wow = win32gui.FindWindow(None, "World of Warcraft")
    win32gui.SetWindowText(wow, "wow1")
    time.sleep(2)


# rename_wow()

vscode = win32gui.FindWindow(None, "main.py - wow-na2 (Workspace) - Visual Studio Code")
typora = win32gui.FindWindow(None, "*Untitled - Notepad")
excel = win32gui.FindWindow(None, "Book1 - Excel")
wow = win32gui.FindWindow(None, "wow1")


# win32gui.SetWindowPos(wow, typora, 0, 0, 800, 600, 0x0004)
while True:
    win32gui.SetWindowPos(typora, excel, 0, 0, 900, 500, 0x0004)
    win32gui.SetWindowPos(excel, typora, 901, 0, 900, 500, 0x0004)
    time.sleep(2)
    win32gui.SetWindowPos(typora, excel, 901, 0, 900, 500, 0x0004)
    win32gui.SetWindowPos(excel, typora, 0, 0, 900, 500, 0x0004)
    time.sleep(2)
    print("swap")
# time.sleep(2)
# win32gui.SetWindowPos(excel, typora, 600, 0, 500, 500, 0x0004)
# win32gui.SetWindowPos(typora, excel, 0, 0, 500, 500, 0x0004)
# win32gui.SetForegroundWindow(vscode)
# win32gui.SetForegroundWindow(hwnd)


# test = input()
