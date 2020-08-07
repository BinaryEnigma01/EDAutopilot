from tkinter import Tk, Label
from win32gui import GetWindowText, GetForegroundWindow


#
# Autopilot information widget, supposedly to overlay on the game
# WIP (Nothing works)
#
info_widget = None


def create_widget():
    widget = Tk()
    widget.title("EDAutopilot Settings")
    widget.geometry('200x40')
    widget.resizable(False, False)
    widget.iconbitmap('src/logo.ico')
    widget.overrideredirect(1)

    startKeyLbl = Label(widget, text='EDAutopilot info: EXAMPLE')
    startKeyLbl.place(relx=0.02, rely=0.02)

    return widget


def iw_focus():
    if info_widget:
        info_widget.focus_set()


def open_widget():
    global info_widget
    info_widget = create_widget()
    info_widget.mainloop()
    info_widget.focus_set()
    info_widget = None


print(GetWindowText(GetForegroundWindow()))
open_widget()


