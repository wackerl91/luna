import xbmcgui
from resources.lib.model.game import Game
from resources.lib.model.hostdetails import HostDetails
from resources.lib.views.gamecontextmenu import GameContextMenu as GameContextMenuType
from xbmcgui import ControlList


class GameContextMenu(xbmcgui.WindowXMLDialog):
    def __new__(cls:GameContextMenuType, *args, **kwargs): ...
    host = ... # type: HostDetails
    list_item = ... # type: xbmcgui.ListItem
    current_game = ... # type: Game
    list = ... # type: ControlList
    refresh_required = False
    def __init__(self:GameContextMenuType, host:HostDetails, list_item: xbmcgui.ListItem) -> GameContextMenuType: ...
    def onInit(self): ...
    def build_list(self): ...
    def onAction(self, action:xbmcgui.Action): ...
