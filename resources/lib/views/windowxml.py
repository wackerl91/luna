from xbmcgui import WindowXML as _WindowXML
from resources.lib.views.basewindow import _BaseWindow


class WindowXML(_BaseWindow, _WindowXML):
    def __init__(self, xml_filename, script_path):
        _WindowXML.__init__(self, xml_filename, script_path)
        _BaseWindow.__init__(self)
