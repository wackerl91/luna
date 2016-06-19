import xbmc
import xbmcaddon
import xbmcgui
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.views.gameinfo import GameInfo


class GameContextMenu(xbmcgui.WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        xbmc.log("GameList Open")
        return super(GameContextMenu, cls).__new__(cls, 'lunacontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, host, list_item):
        super(GameContextMenu, self).__init__('lunacontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.host = host
        self.list_item = list_item
        self.game_manger = RequiredFeature('game-manager').request()
        self.list = None
        self.refresh_required = False

    def onInit(self):
        self.list = self.getControl(70)
        self.build_list()
        self.setFocus(self.list)

    def build_list(self):
        items = ['Game Information', 'Addon Settings', 'Refresh List']
        self.list.addItems(items)

    def onAction(self, action):
        if self.getFocus() == self.list and action.getId() == xbmcgui.ACTION_SELECT_ITEM:
            selected_position = self.list.getSelectedPosition()
            if selected_position == 0:
                game = self.game_manger.get_game_by_id(self.host, self.list_item.getProperty('id'))
                window = GameInfo(game, game.name)
                window.doModal()
                del window
            if selected_position == 1:
                RequiredFeature('addon').request().openSettings()
            if selected_position == 2:
                self.refresh_required = True
                self.close()
                xbmc.log('Clicked Full Refresh')
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()
