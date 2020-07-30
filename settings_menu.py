from tkinter import Tk, Checkbutton, BooleanVar, Button, NORMAL, DISABLED, Label
from tkinter.messagebox import askyesnocancel, YES

import keyboard

from settings_api import __writeSettings, getOption


#
# Simple settings menu
# Makes use of the settings file interface
#


unsaved = False


def modified():
    global unsaved
    unsaved = True


def saved():
    global unsaved
    unsaved = False


def getKeyForBtn(btn):
    global unsaved
    key = keyboard.read_key()
    if key is not "esc":
        btn['text'] = key
        modified()
        from dev_autopilot import logger
        logger.debug("(settings_menu) detected key '{}' with scancode {}".format(key, keyboard.key_to_scan_codes(key)))


def create_window():
    window = Tk()
    window.title("EDAutopilot Settings")
    window.geometry('280x300')
    window.resizable(False, False)
    window.iconbitmap('src/logo.ico')

    def on_closing():
        if unsaved:
            confirm = askyesnocancel(
                title="Save On Close",
                message="Do you want to save before closing?",
                default=YES,
                icon='warning'
            )
            if confirm:
                on_save()
            elif confirm is None:
                return False
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    def toggleFSS():
        modified()
        if dsState.get():
            fssCheck['state'] = NORMAL
        else:
            fssCheck['state'] = DISABLED

    dsState = BooleanVar()
    dsState.set(getOption('DiscoveryScan'))
    dsCheck = Checkbutton(window, text='Automatic Discovery Scan', var=dsState, command=toggleFSS)
    dsCheck.place(relx=0.02, rely=0.02)

    fssState = BooleanVar()
    fssState.set(getOption('AutoFSS'))
    fssCheck = Checkbutton(window, text='Automatic FSS Scan\n (Currently waits for user to operate FSS)',
                           var=fssState, command=modified)
    fssCheck.place(relx=0.05, rely=0.09)

    startKeyLbl = Label(window, text='Start EDAutopilot Key:')
    startKeyLbl.place(relx=0.02, rely=0.23)

    def on_startKey():
        getKeyForBtn(startKeyBtn)

    startKeyBtn = Button(window, text=getOption('StartKey'), command=on_startKey, width=20)
    startKeyBtn.place(relx=0.46, rely=0.22)

    startKeyLbl = Label(window, text='End EDAutopilot Key:')
    startKeyLbl.place(relx=0.02, rely=0.33)

    def on_endKey():
        getKeyForBtn(endKeyBtn)

    endKeyBtn = Button(window, text=getOption('EndKey'), command=on_endKey, width=20)
    endKeyBtn.place(relx=0.46, rely=0.32)

    def on_save():
        # setOption('AutoFSS', fssState.get())
        # setOption('DiscoveryScan', dsState.get())
        # setOption('StartKey', startKeyBtn['text'])
        # setOption('EndKey', endKeyBtn['text'])
        # This operation isn't very safe, but it's better than the above:
        __writeSettings(dict(AutoFSS=fssState.get(), DiscoveryScan=dsState.get(),
                             StartKey=startKeyBtn['text'], EndKey=endKeyBtn['text']))
        saved()

    saveBtn = Button(window, text="Save Settings", command=on_save)
    saveBtn.place(relx=0.70, rely=0.90)
    return window


def open_settings():
    saved()
    window = create_window()
    window.focus_force()
    window.mainloop()
