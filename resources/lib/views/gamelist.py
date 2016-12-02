import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.views.gamecontextmenu import GameContextMenu


class GameList(xbmcgui.WindowXML):
    def __new__(cls, *args, **kwargs):
        xbmc.log("GameList Open")
        return super(GameList, cls).__new__(cls, "gamelist.xml", xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, controller, host, game_list):
        xbmc.log("GameList Init")
        super(GameList, self).__init__("gamelist.xml", xbmcaddon.Addon().getAddonInfo('path'))
        self.controller = controller
        self.host = host
        self.games = game_list
        self.list = None
        self.cover = None
        self.fanart = None
        xbmc.log("GameList Init - Done")

    def onInit(self):
        xbmc.log("GameList onInit")
        self.games.sort(key=lambda x: x['label'], reverse=False)
        self.list = self.getControl(50)
        self.cover = self.getControl(1)
        self.fanart = self.getControl(2)
        self.build_list()
        self.setFocusId(50)

    def build_list(self):
        items = []
        # game = self.games[0]
        for game in self.games:
            item = xbmcgui.ListItem()
            item.setLabel(game['label'])
            item.setIconImage(game['icon'])
            item.setThumbnailImage(game['thumbnail'])
            item.setInfo('video', game['info'])
            item.setProperty('icon', game['thumbnail'])
            item.setProperty('fanart', game['properties']['fanart_image'])
            item.setProperty('id', game['properties']['id'])

            items.append(item)

        self.list.addItems(items)
        try:
            current_item = self.list.getListItem(self.list.getSelectedPosition())
            self.cover.setImage(current_item.getProperty('icon'))
            self.fanart.setImage(current_item.getProperty('fanart'))
        except RuntimeError:
            pass

    def onAction(self, action):
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()

        if self.getFocus() == self.list and (
                action.getId() == xbmcgui.ACTION_MOVE_UP or action.getId() == xbmcgui.ACTION_MOVE_DOWN):
            current_item = self.list.getListItem(self.list.getSelectedPosition())
            self.cover.setImage(current_item.getProperty('icon'))
            self.fanart.setImage(current_item.getProperty('fanart'))
        elif self.getFocus() == self.list and action.getId() == xbmcgui.ACTION_CONTEXT_MENU:
            current_item = self.list.getListItem(self.list.getSelectedPosition())
            fanart_cache = current_item.getProperty('fanart')
            cover_cache = current_item.getProperty('icon')

            current_game = self.controller.get_game_by_id(self.host, current_item.getProperty('id'))
            window = GameContextMenu(self.host, current_item, current_game)
            window.doModal()
            refresh = window.refresh_required
            del window

            loaded_game = self.controller.get_game_by_id(self.host, current_item.getProperty('id'))
            if fanart_cache != loaded_game.get_selected_fanart().get_original():
                self.list.getSelectedItem().setProperty('fanart', loaded_game.get_selected_fanart().get_original())
                self.fanart.setImage(loaded_game.get_selected_fanart().get_original())
            if cover_cache != loaded_game.get_selected_poster():
                self.list.getSelectedItem().setProperty('icon', loaded_game.get_selected_poster())
                self.cover.setImage(loaded_game.get_selected_poster())

            if refresh:
                self.controller.refresh_list(self.host)

            self.setFocus(self.list)

        elif self.getFocus() == self.list and action == xbmcgui.ACTION_SELECT_ITEM:
            current_item = self.list.getListItem(self.list.getSelectedPosition())
            loaded_game = self.controller.get_game_by_id(self.host, current_item.getProperty('id'))

            self.controller.launch_game(loaded_game)

    def update(self, games):
        self.games = games
        self.games.sort(key=lambda x: x['label'], reverse=False)
        self.list.reset()
        self.build_list()
        return
