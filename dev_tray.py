import keyboard
import kthread
from PIL import Image
from pystray import Icon, MenuItem, Menu

from settings_api import getOption, setOption

tray_icon = None
main_thread = None
startKey = None
endKey = None


def setup(icon):
    icon.visible = True


def exit_action():
    stop_action()
    from settings_menu import force_close_settings
    force_close_settings()
    if tray_icon:
        tray_icon.visible = False
        tray_icon.stop()


def start_action():
    global main_thread
    stop_action()
    from dev_autopilot import autopilot
    main_thread = kthread.KThread(target=autopilot, name="EDAutopilot")
    main_thread.isAlive = main_thread.is_alive  # KThread seems to have a bug where it uses isAlive()
    # (A method which does not exist) inside their own code
    main_thread.start()


def stop_action():
    from logger import logger
    logger.info("Stopping autopilot thread")
    global main_thread
    if main_thread and main_thread.is_alive():
        main_thread.kill()
    from dev_autopilot import get_bindings, clear_input
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
    from logger import logger
    logger.debug("OS + Software compatible with tray menu: " + str(tray_icon.HAS_MENU))
    from dev_autopilot import resource_path
    logo = Image.open(resource_path('src/logo.png'))
    tray_icon.icon = logo
    from settings_menu import open_settings
    tray_icon.menu = Menu(
        MenuItem('Start', lambda: start_action()),
        MenuItem('Stop', lambda: stop_action()),
        MenuItem('Auto-FSS', toggleFSS(), checked=getFSS()),
        MenuItem('Settings', lambda: open_settings()),
        MenuItem('Exit', lambda: exit_action())
    )

    global startKey, endKey
    startKey = keyboard.add_hotkey(getOption('StartKey'), start_action)
    # For some reason, if PyCharm is running as root, stop_action will not be triggered
    endKey = keyboard.add_hotkey(getOption('EndKey'), stop_action)

    tray_icon.run(setup)


if __name__ == '__main__':
    tray()
