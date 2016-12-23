import xbmcgui
from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.views.gameinfo import GameInfo


class GameInfoController(BaseController):
    def __init__(self, core):
        self.core = core
        self.window = None

    @route(name='details')
    def show_game_info_action(self, host, game):
        self.window = GameInfo(self, host, game)
        self.window.doModal()
        del self.window

    def select_cover_art(self, game, list_item):
        browser = xbmcgui.Dialog().browse(2, 'Select Cover Art', 'files', '.jpg|.png', False, False,
                                          game.get_poster(0, ''))
        if browser:
            game.selected_poster = browser
            list_item.setThumbnailImage(browser)
            self.sync_storage()

    def select_fanart(self, game, list_item):
        browser = xbmcgui.Dialog().browse(2, 'Select Fanart', 'files', '.jpg|.png', False, False,
                                          game.get_selected_fanart().get_thumb())
        if browser:
            game.set_selected_fanart(browser)
            list_item.setProperty('fanart', browser)
            self.sync_storage()

    def sync_storage(self):
        return self.core.get_storage().sync()
