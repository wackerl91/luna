import xbmcaddon
import xbmcgui
from resources.lib.di.requiredfeature import RequiredFeature


class Settings(xbmcgui.WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        return super(Settings, cls).__new__(cls, 'settings.xml', xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, controller):
        super(Settings, self).__init__('settings.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.controller = controller
        self.logger = RequiredFeature('logger').request()
