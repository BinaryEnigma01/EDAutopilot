import os
from tkinter import Tk, Checkbutton, BooleanVar, Button, NORMAL, DISABLED, Label, Entry
from tkinter.messagebox import askyesnocancel, YES

import keyboard

from settings_api import getOptions, setOption


#
# Simple settings menu
# Makes use of the settings file interface
# Prone to visual errors due to hardcoded widget locations
#

curr_window = None


def getKeyForBtn(btn):
    key = keyboard.read_key()
    if key != "esc":
        btn['text'] = key
        from logger import logger
        logger.debug("(settings_menu) detected key '{}' with scancode {}".format(key, keyboard.key_to_scan_codes(key)))


def create_window():
    window = Tk()
    window.title("EDAutopilot Settings")
    window.geometry('280x300')
    window.resizable(False, False)
    from dev_autopilot import logger
    logger.debug(os.name)
    if "nt" == os.name:
        window.iconbitmap('src/logo.ico')

    defaults = getOptions()

    def on_closing():
        if unsaved():
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
        global curr_window
        curr_window = None
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    def toggleFSS():
        if dsState.get():
            fssCheck['state'] = NORMAL
        else:
            fssCheck['state'] = DISABLED

    dsState = BooleanVar()
    dsState.set(defaults['DiscoveryScan'])
    dsCheck = Checkbutton(window, text='Automatic Discovery Scan', var=dsState, command=toggleFSS)
    dsCheck.place(relx=0.02, rely=0.02)

    fssState = BooleanVar()
    fssState.set(defaults['AutoFSS'])
    fssCheck = Checkbutton(window, text='Automatic FSS Scan\n (Currently waits for user to operate FSS)',
                           var=fssState)
    fssCheck.place(relx=0.05, rely=0.09)

    startKeyLbl = Label(window, text='Start EDAutopilot Key:')
    startKeyLbl.place(relx=0.02, rely=0.23)

    def on_startKey():
        getKeyForBtn(startKeyBtn)

    startKeyBtn = Button(window, text=defaults['StartKey'], command=on_startKey, width=20)
    startKeyBtn.place(relx=0.46, rely=0.22)

    startKeyLbl = Label(window, text='End EDAutopilot Key:')
    startKeyLbl.place(relx=0.02, rely=0.33)

    def on_endKey():
        getKeyForBtn(endKeyBtn)

    endKeyBtn = Button(window, text=defaults['EndKey'], command=on_endKey, width=20)
    endKeyBtn.place(relx=0.46, rely=0.32)

    rtLbl = Label(window, text='Refuel threshold percentage:')
    rtLbl.place(relx=0.02, rely=0.43)


    def callback(strnum):
        return ((str.isdigit(strnum)) and (len(strnum) <= 3) and (0 <= int(strnum) <= 100)) or strnum == ""


    vcmd = (window.register(callback))

    refuelThreshold = Entry(window, validate='all', validatecommand=(vcmd, '%P'), width=10, justify='center')
    refuelThreshold.insert(0, defaults['RefuelThreshold'])
    refuelThreshold.place(relx=0.62, rely=0.44)


    def get_refuel_threshold(entry):
        if not entry:
            return defaults['RefuelThreshold']
        return str(int(entry.get()))  # Just to be triply sure it's an int in str form


    def unsaved():
        return str(fssState.get()) != defaults['AutoFSS'] or str(dsState.get()) != defaults['DiscoveryScan'] or \
               startKeyBtn['text'] != defaults['StartKey'] or endKeyBtn['text'] != defaults['EndKey'] or \
               get_refuel_threshold(refuelThreshold) != defaults['RefuelThreshold']


    def on_save():
        if not unsaved():
            return
        if str(fssState.get()) != defaults['AutoFSS']:
            setOption('AutoFSS', fssState.get())
        if str(dsState.get()) != defaults['DiscoveryScan']:
            setOption('DiscoveryScan', dsState.get())
        if startKeyBtn['text'] != defaults['StartKey']:
            setOption('StartKey', startKeyBtn['text'])
        if endKeyBtn['text'] != defaults['EndKey']:
            setOption('EndKey', endKeyBtn['text'])
        if get_refuel_threshold(refuelThreshold) != defaults['RefuelThreshold']:
            setOption('RefuelThreshold', get_refuel_threshold(refuelThreshold))

    saveBtn = Button(window, text="Save Settings", command=on_save)
    saveBtn.place(relx=0.70, rely=0.90)
    return window


def open_settings():
    global curr_window
    curr_window = create_window()
    curr_window.focus_force()
    curr_window.mainloop()


def force_close_settings():
    global curr_window
    if curr_window is not None:
        curr_window.destroy()
        curr_window = None
