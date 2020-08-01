# This code checks the active window's name every time windows are switched
# Taken straight out of StackOverflow:
# https://stackoverflow.com/questions/15849564/how-to-use-winapi-setwineventhook-in-python

import ctypes
import ctypes.wintypes
import sys

EVENT_OBJECT_FOCUS = 0x8005
WINEVENT_OUTOFCONTEXT = 0x0000

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32

ole32.CoInitialize(0)

WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)


def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    length = user32.GetWindowTextLengthA(hwnd)
    buff = ctypes.create_string_buffer(length + 1)
    user32.GetWindowTextA(hwnd, buff, length + 1)
    if str(buff.value) == "b'Elite - Dangerous (CLIENT)'":
        print("ED is the active window")  # TODO: Pause autopilot when this is not the case



WinEventProc = WinEventProcType(callback)

user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
hook = user32.SetWinEventHook(
    EVENT_OBJECT_FOCUS,
    EVENT_OBJECT_FOCUS,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT
)
if hook == 0:
    print('SetWinEventHook failed')
    sys.exit(1)

msg = ctypes.wintypes.MSG()
while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
    user32.TranslateMessageW(msg)
    user32.DispatchMessageW(msg)
print('SetWinEventHook succeeded')
user32.UnhookWinEvent(hook)
ole32.CoUninitialize()
