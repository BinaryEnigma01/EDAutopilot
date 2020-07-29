import keyboard
import kthread
from PIL import Image
from pystray import Icon, MenuItem, Menu

from dev_autopilot import autopilot, resource_path, get_bindings, clear_input, set_autoFSS

tray_icon = None
main_thread = None
aFSS = False



def setup(icon):
    icon.visible = True


def exit_action():
    stop_action()
    if tray_icon:
        tray_icon.visible = False
        tray_icon.stop()



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
    global tray_icon
    tray_icon = None

    name = 'ED - Autopilot'
    tray_icon = Icon(name=name, title=name)
    logo = Image.open(resource_path('src/logo.png'))
    tray_icon.icon = logo

    tray_icon.menu = Menu(
        MenuItem('Start', lambda: start_action()),
        MenuItem('Stop', lambda: stop_action()),
        MenuItem('Auto-FSS', toggleFSS(), checked=getFSS()),
        MenuItem('Exit', lambda: exit_action())
    )

    keyboard.add_hotkey('page up', start_action)
    keyboard.add_hotkey('page down', stop_action)

    tray_icon.run(setup)


if __name__ == '__main__':
    tray()
