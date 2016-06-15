import os

import xbmc
import xbmcaddon
import xbmcgui
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.views.gamecontextmenu import GameContextMenu


class GameList(xbmcgui.WindowXML):
    def __new__(cls, *args, **kwargs):
        xbmc.log("GameList Open")
        return super(GameList, cls).__new__(cls, "gamelist.xml", xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, host, games):
        xbmc.log("GameList Init")
        _ADDON_NAME = 'script.module.pyxbmct'
        _addon = xbmcaddon.Addon(id=_ADDON_NAME)
        _addon_path = _addon.getAddonInfo('path')
        self._images = os.path.join(_addon_path, 'lib', 'pyxbmct', 'textures', 'default')
        del _ADDON_NAME
        del _addon
        del _addon_path

        super(GameList, self).__init__("gamelist.xml", xbmcaddon.Addon().getAddonInfo('path'))
        self.host = host
        self.games = games
        self.game_manager = RequiredFeature('game-manager').request()
        self.list = None
        self.cover = None
        self.fanart = None

    def onInit(self):
        xbmc.log("GameList onInit")
        self.games.sort(key=lambda x: x['label'], reverse=False)
        self.setFocusId(50)
        self.list = self.getControl(50)
        self.cover = self.getControl(1)
        self.fanart = self.getControl(2)
        self.buildList()

    def buildList(self):
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
        currentItem = self.list.getListItem(self.list.getSelectedPosition())
        self.cover.setImage(currentItem.getProperty('icon'))

    def onAction(self, action):
        if self.getFocus() == self.list and (action.getId() == xbmcgui.ACTION_MOVE_UP or action.getId() == xbmcgui.ACTION_MOVE_DOWN):
            currentItem = self.list.getListItem(self.list.getSelectedPosition())
            self.cover.setImage(currentItem.getProperty('icon'))
            self.fanart.setImage(currentItem.getProperty('fanart'))
        elif self.getFocus() == self.list and action.getId() == xbmcgui.ACTION_CONTEXT_MENU:
            currentItem = self.list.getListItem(self.list.getSelectedPosition())
            fanartCache = currentItem.getProperty('fanart')
            coverCache = currentItem.getProperty('icon')

            window = GameContextMenu(self.host, currentItem)
            window.doModal()
            del window

            loaded_game = self.game_manager.get_game_by_id(self.host, currentItem.getProperty('id'))
            if fanartCache != loaded_game.selected_fanart:
                self.list.getSelectedItem().setProperty('fanart', loaded_game.selected_fanart)
                self.fanart.setImage(loaded_game.selected_fanart)
            if coverCache != loaded_game.selected_poster:
                self.list.getSelectedItem().setProperty('icon', loaded_game.selected_poster)
                self.cover.setImage(loaded_game.selected_poster)

            self.setFocus(self.list)
        elif action == xbmcgui.ACTION_NAV_BACK:
            self.close()
