import xbmc
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.views.gamelist import GameList

from resources.lib.views.main import Main


class MainController(object):
    def __init__(self):
        self.addon = RequiredFeature('addon').request()
        self.logger = RequiredFeature('logger').request()
        self.window = None

    def render(self):
        self.window = Main(controller=self)
        # Manually close the spinning while since it gets stuck for fullscreen windows
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        self.window.doModal()

    def select_host(self, host):
        game_controller = RequiredFeature('game-controller').request()
        games = game_controller.get_games_as_list(host)
        window = GameList(host, games)
        window.doModal()

    def add_host(self):
        # import xbmc
        # xbmc.executebuiltin("RunPlugin(plugin://script.luna/add_host)")
        host_controller = RequiredFeature('host-controller').request()
        ret_val = host_controller.initiate()
        self.logger.info(ret_val)
        if ret_val:
            self.window.update()
        del host_controller

    def open_settings(self):
        self.addon.openSettings()
