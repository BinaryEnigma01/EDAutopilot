from tkinter import Tk, Checkbutton, BooleanVar, Button, NORMAL, DISABLED, Label, Entry
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

    rtLbl = Label(window, text='Refuel threshold percentage:')
    rtLbl.place(relx=0.02, rely=0.43)


    def callback(strnum):
        return ((str.isdigit(strnum)) and (len(strnum) <= 3) and (0 <= int(strnum) <= 100)) or strnum == ""


    vcmd = (window.register(callback))

    refuelThreshold = Entry(window, validate='all', validatecommand=(vcmd, '%P'), width=10, justify='center')
    refuelThreshold.insert(0, getOption('RefuelThreshold'))
    refuelThreshold.place(relx=0.62, rely=0.44)


    def get_refuel_threshold(entry):
        if not entry:
            return int(getOption('RefuelThreshold'))
        return int(entry.get())


    def on_save():
        # setOption('AutoFSS', fssState.get())
        # setOption('DiscoveryScan', dsState.get())
        # setOption('StartKey', startKeyBtn['text'])
        # setOption('EndKey', endKeyBtn['text'])
        # This operation isn't very safe, but it's better than the above:
        __writeSettings(dict(
                            AutoFSS=fssState.get(),
                            DiscoveryScan=dsState.get(),
                            StartKey=startKeyBtn['text'],
                            EndKey=endKeyBtn['text'],
                            RefuelThreshold=get_refuel_threshold(refuelThreshold)
        ))
        saved()

    saveBtn = Button(window, text="Save Settings", command=on_save)
    saveBtn.place(relx=0.70, rely=0.90)
    return window


curr_window = None


def open_settings():
    global curr_window
    saved()
    curr_window = create_window()
    curr_window.focus_force()
    curr_window.mainloop()


def force_close_settings():
    global curr_window
    if curr_window is not None:
        curr_window.destroy()
        curr_window = None
