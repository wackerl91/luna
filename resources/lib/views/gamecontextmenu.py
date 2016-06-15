import xbmc
import xbmcaddon
import xbmcgui
from resources.lib.di.requiredfeature import RequiredFeature


class GameContextMenu(xbmcgui.WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        xbmc.log("GameList Open")
        return super(GameContextMenu, cls).__new__(cls, "gamecontextmenu.xml", xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, host, list_item):
        super(GameContextMenu, self).__init__('gamecontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.host = host
        self.list_item = list_item
        self.game_manger = RequiredFeature('game-manager').request()
        self.list = None

    def onInit(self):
        self.list = self.getControl(70)
        self.build_list()
        self.setFocus(self.list)

    def build_list(self):
        items = ['Game Information', 'Addon Settings', 'Full Refresh']
        self.list.addItems(items)

    def onAction(self, action):
        if self.getFocus() == self.list and action.getId() == xbmcgui.ACTION_SELECT_ITEM:
            currentItem = self.list.getListItem(self.list.getSelectedPosition())
            selected_position = self.list.getSelectedPosition()
            if selected_position == 0:
                xbmc.log('Clicked Game Information')
            if selected_position == 1:
                xbmc.log('Clicked Addon Settings')
            if selected_position == 2:
                xbmc.log('Clicked Full Refresh')
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()
