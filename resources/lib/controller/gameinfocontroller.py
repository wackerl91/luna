from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.views.gameinfo import GameInfo


class GameInfoController(BaseController):
    def __init__(self, core):
        self.core = core
        self.window = None

    @route(name='details')
    def show_game_info_action(self, game, title):
        self.window = GameInfo(self, game, title)
        self.window.doModal()
        del self.window

    def get_active_skin(self):
        return self.core.get_active_skin()

    def sync_storage(self):
        return self.core.get_storage().sync()
