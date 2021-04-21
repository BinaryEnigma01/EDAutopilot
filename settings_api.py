import os.path

#
# Simple settings file interface, assumes the file is always generated
# by this interface and thus has correct syntax.
# This interface has 2 main 'public' methods, getOption(strOption) and setOption(strOption, value)
# HOW TO ADD SETTINGS: Add an entry in the 'settings' dict below with the default value
# for your setting, delete the Config File and run the program once, that's all
#

# Default settings
settings = dict(AutoFSS=False, DiscoveryScan=True, StartKey='home', EndKey='end',
                RefuelThreshold=40, JournalPath="", BindingsPath="")
CFGFILE = "./EDAutopilot.cfg"


def _readSettings():
    if os.path.isfile(CFGFILE):
        f = open(CFGFILE, "r")
        for line in f:
            key, value = line.split('=')
            settings[key] = value[0:-1]
        f.close()
    else:
        _writeSettings()


def _writeSettings(dictionary=None):
    if dictionary is None:
        dictionary = settings
    f = open(CFGFILE, "w")
    for key in dictionary:
        f.write('{}={}\n'.format(key, dictionary[key]))
    f.close()
    if dictionary is not settings:
        _on_change_all()


def _on_change(key, val=None):
    from logger import logger
    from dev_tray import updateSettings
    valStr = ""
    if val is not None:
        valStr = "to {}".format(val)

    logger.info("Setting {} changed value {}".format(key, valStr))
    updateSettings(key)


def _on_change_all():  # All or most keys changed value
    _readSettings()
    for key in settings:
        _on_change(key)


def setOption(key, value):
    _readSettings()
    settings[key] = value
    _writeSettings()
    _on_change(key, value)


def getOption(key):
    _readSettings()
    val = settings.get(key)
    if val == "False":
        return False
    return settings[key]


def getOptions():
    _readSettings()
    return settings
