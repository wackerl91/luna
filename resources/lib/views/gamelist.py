import xbmcaddon
import xbmcgui


class GameList(xbmcgui.WindowXML):
    def __new__(cls, *args, **kwargs):
        return super(GameList, cls).__new__(cls, "gamelist.xml", xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, controller, host, game_list):
        super(GameList, self).__init__("gamelist.xml", xbmcaddon.Addon().getAddonInfo('path'))
        self.controller = controller
        self.host = host
        self.games = game_list
        self.list = None
        self.host_online_img = None
        self.host_offline_img = None
        self.host_name_label = None

    def onInit(self):
        self.games.sort(key=lambda x: x['label'], reverse=False)
        self.list = self.getControl(50)
        self.host_online_img = self.getControl(2)
        self.host_offline_img = self.getControl(3)
        self.host_name_label = self.getControl(4)

        if self.host.state == self.host.STATE_OFFLINE:
            self.host_online_img.setVisible(False)
        else:
            self.host_offline_img.setVisible(False)

        self.host_name_label.setLabel("%s | GPU: %s" % (self.host.name, self.host.gpu_type))

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

    def onAction(self, action):
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()
        elif self.getFocus() == self.list and action.getId() == xbmcgui.ACTION_CONTEXT_MENU:
            current_item = self.list.getListItem(self.list.getSelectedPosition())
            fanart_cache = current_item.getProperty('fanart')
            cover_cache = current_item.getProperty('icon')

            current_game = self.controller.get_game_by_id(self.host, current_item.getProperty('id'))

            refresh = self.controller.render('gamecontext_menu', {'host': self.host, 'list_item': current_item, 'game': current_game})

            loaded_game = self.controller.get_game_by_id(self.host, current_item.getProperty('id'))

            if fanart_cache != loaded_game.get_selected_fanart().get_original():
                self.list.getSelectedItem().setProperty('fanart', loaded_game.get_selected_fanart().get_original())

            if cover_cache != loaded_game.get_selected_poster():
                self.list.getSelectedItem().setProperty('icon', loaded_game.get_selected_poster())

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
