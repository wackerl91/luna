import xbmc
import xbmcaddon
import xbmcgui
from resources.lib.views.gameinfo import GameInfo


class GameContextMenu(xbmcgui.WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        xbmc.log("GameList Open")
        return super(GameContextMenu, cls).__new__(cls, 'lunacontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, host, list_item, current_game):
        super(GameContextMenu, self).__init__('lunacontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.host = host
        self.list_item = list_item
        self.current_game = current_game
        self.list = None
        self.refresh_required = False

    def onInit(self):
        self.list = self.getControl(70)
        self.build_list()
        self.setFocus(self.list)

    def build_list(self):
        items = ['Game Information', 'Refresh List']
        self.list.addItems(items)

    def onAction(self, action):
        if self.getFocus() == self.list and action.getId() == xbmcgui.ACTION_SELECT_ITEM:
            selected_position = self.list.getSelectedPosition()
            if selected_position == 0:
                window = GameInfo(self.current_game, self.current_game.name)
                window.doModal()
                del window
            if selected_position == 1:
                self.refresh_required = True
                self.close()
                xbmc.log('Clicked Full Refresh')
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()
