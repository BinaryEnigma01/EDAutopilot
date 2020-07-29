import threading

import keyboard
import kthread
from PIL import Image
from pystray import Icon, MenuItem, Menu

from dev_autopilot import autopilot, resource_path, get_bindings, clear_input, set_autoFSS

STATE = 0
icon = None
thread = None
aFSS = False


def setup(icon):
    icon.visible = True


def exit_action():
    stop_action()
    icon.visible = False
    icon.stop()


main_thread = None


def start_action():
    global main_thread
    stop_action()
    main_thread = kthread.KThread(target=autopilot, name="EDAutopilot")
    main_thread.start()


def stop_action():
    global main_thread
    if main_thread:
        main_thread.kill()
        main_thread = None
    clear_input(get_bindings())


def toggleFSS():
    def inner(icon, item):
        global aFSS
        aFSS = ~aFSS
        set_autoFSS(aFSS)

    return inner


def getFSS():
    def inner(item):
        return aFSS

    return inner


def tray():
    global icon, thread
    icon = None
    thread = None

    name = 'ED - Autopilot'
    icon = Icon(name=name, title=name)
    logo = Image.open(resource_path('src/logo.png'))
    icon.icon = logo

    icon.menu = Menu(
        MenuItem('Start', lambda: start_action()),
        MenuItem('Stop', lambda: stop_action()),
        MenuItem('Auto-FSS', toggleFSS(), checked=getFSS()),
        MenuItem('Exit', lambda: exit_action())
    )

    keyboard.add_hotkey('page up', start_action)
    keyboard.add_hotkey('page down', stop_action)

    icon.run(setup)


if __name__ == '__main__':
    tray()
