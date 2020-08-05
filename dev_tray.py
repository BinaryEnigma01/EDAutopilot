import keyboard
import kthread
from PIL import Image
from pystray import Icon, MenuItem, Menu

from dev_autopilot import autopilot, resource_path, get_bindings, clear_input
from settings_api import getOption, setOption
from settings_menu import open_settings, force_close_settings

tray_icon = None
main_thread = None
startKey = None
endKey = None


def setup(icon):
    icon.visible = True


def exit_action():
    stop_action()
    force_close_settings()
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
    if main_thread and main_thread.is_alive():
        main_thread.kill()
    clear_input(get_bindings())


def toggleFSS():
    def inner(icon, item):
        setOption('AutoFSS', not getOption('AutoFSS'))

    return inner


def getFSS():
    def inner(item):
        return getOption('AutoFSS')

    return inner


def updateSettings(key):
    if key == 'StartKey':
        global startKey
        keyboard.remove_hotkey(startKey)
        startKey = keyboard.add_hotkey(getOption('StartKey'), start_action)
    elif key == 'EndKey':
        global endKey
        keyboard.remove_hotkey(endKey)
        endKey = keyboard.add_hotkey(getOption('EndKey'), stop_action)
    elif (tray_icon is not None) and (key == 'AutoFSS'):
        tray_icon.update_menu()



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
        MenuItem('Settings', lambda: open_settings()),
        MenuItem('Exit', lambda: exit_action())
    )

    global startKey, endKey
    startKey = keyboard.add_hotkey(getOption('StartKey'), start_action)
    endKey = keyboard.add_hotkey(getOption('EndKey'), stop_action)

    tray_icon.run(setup)


if __name__ == '__main__':
    tray()
