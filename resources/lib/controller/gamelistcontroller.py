import threading

from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.views.gamelist import GameList


class GameListController(BaseController):
    def __init__(self, game_manager, game_helper, moonlight_helper, logger):
        self.game_manager = game_manager
        self.game_helper = game_helper
        self.moonlight_helper = moonlight_helper
        self.logger = logger
        self.window = None

    @route(name='list')
    def index_action(self, host):
        self.window = GameList(controller=self, host=host, game_list=self.game_helper.get_games_as_list(host))
        self.window.doModal()
        del self.window

    @route(name='launch')
    def launch_game(self, game):
        self.logger.info("Starting game by name: %s" % game.name)
        self.moonlight_helper.launch_game(game.name)

    def refresh_list(self, host):
        refresh_game_list_thread = threading.Thread(target=self._refresh_list, args=(host,))
        refresh_game_list_thread.start()

    def _refresh_list(self, host):
        import xbmcgui
        background_dialog = xbmcgui.DialogProgressBG()
        background_dialog.create('Refreshing Game List', 'Host: %s' % host.name)
        games = self.game_helper.get_games_as_list(host, True)
        self.window.update(games)
        background_dialog.close()
        del background_dialog
        return

    def get_game_by_id(self, host, game_id):
        return self.game_manager.get_game_by_id(host, game_id)
