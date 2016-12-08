from xbmcgui import WindowXMLDialog as _WindowXMLDialog
from resources.lib.views.basewindow import _BaseWindow


class WindowXMLDialog(_BaseWindow, _WindowXMLDialog):
    def __init__(self, xml_filename, script_path):
        _WindowXMLDialog.__init__(self, xml_filename, script_path)
        _BaseWindow.__init__(self)
