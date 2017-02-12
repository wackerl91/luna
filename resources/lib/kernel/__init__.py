import sys


def log_exception(exctype, value, tb):
    from resources.lib.di.requiredfeature import RequiredFeature
    import inspect
    eos_helper = RequiredFeature('eos-helper').request()

    trace = []
    for item in reversed(inspect.stack()):
        trace.append(item[1:])
    for item in inspect.trace():
        trace.append(item[1:])

    eos_helper.register_exception(exctype, value, trace)

    import xbmcgui
    xbmcgui.Dialog().notification(
        'Luna',
        'An exception occurred and has been reported to Eos. Please check the log for more information.',
        time=10000
    )

    import xbmc
    xbmc.log("[script.luna]: %s - %s" % (str(exctype), str(value)), xbmc.LOGERROR)
    xbmc.executebuiltin('Dialog.Close(all,true)')

sys.excepthook = log_exception
