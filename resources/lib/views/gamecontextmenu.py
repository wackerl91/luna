import xbmcaddon
import xbmcgui


class GameContextMenu(xbmcgui.WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        return super(GameContextMenu, cls).__new__(cls, 'lunacontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, controller, host, list_item, current_game):
        super(GameContextMenu, self).__init__('lunacontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.controller = controller
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
                self.controller.render('gameinfo_details', {'game': self.current_game, 'title': self.current_game.name})
            if selected_position == 1:
                self.refresh_required = True
                self.close()
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()
