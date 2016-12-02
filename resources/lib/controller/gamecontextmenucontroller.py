from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.views.gamecontextmenu import GameContextMenu


class GameContextMenuController(BaseController):
    def __init__(self):
        self.window = None

    @route(name='menu')
    def show_context_action(self, host, list_item, game):
        self.window = GameContextMenu(self, host, list_item, game)
        self.window.doModal()
        refresh = self.window.refresh_required
        del self.window

        return refresh
