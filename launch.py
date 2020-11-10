import win32process as proc
import win32con as con
import win32event as event
import win32api as api

from pathlib import Path

from config import SETUP_PATH


exe_path = Path(SETUP_PATH) / "wow0" / "_retail_" / "WoW.exe"
exe_path2 = Path(SETUP_PATH) / "wow1" / "_retail_" / "WoW.exe"
test_path = r"C:\Program Files\Sublime Text 3\sublime_text.exe"


def LaunchWow(path):
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

    # exit_code = event.WaitForSingleObject(hProcess, (2 * 1000))
    # api.CloseHandle(hProcess)
    # print(exit_code, hProcess, hThread, dwProcessId, dwThreadId)


if __name__ == "__main__":
    try:
        LaunchWow(exe_path)
        LaunchWow(exe_path2)
        # input()
    except Exception as e:
        print(e)
        input()


# def LaunchWin32Process(self, command):
#     try:
#         StartupInfo = win32process.STARTUPINFO()
#         StartupInfo.dwFlags = win32process.STARTF_USESHOWWINDOW
#         StartupInfo.wShowWindow = win32con.SW_NORMAL
#         win32process.CreateProcess(
#             None,
#             command,
#             None,
#             None,
#             0,
#             win32process.NORMAL_PRIORITY_CLASS,
#             None,
#             None,
#             StartupInfo,
#         )
#     except Exception as e:
#         print(sys.exc_info())
#         print("Exception in LaunchWin32Process")
#         pass
