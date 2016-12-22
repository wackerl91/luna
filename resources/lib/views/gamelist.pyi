from typing import List

import xbmcgui
from xbmcgui import Action, ControlImage, ControlList, ControlLabel

from resources.lib.controller import gamelistcontroller
from resources.lib.controller.gamelistcontroller import GameListController
from resources.lib.core.logger import Logger
from resources.lib.model.game import Game
from resources.lib.model.hostdetails import HostDetails
from resources.lib.views.gamelist import GameList as GameListType


class GameList(xbmcgui.WindowXML):
    def __new__(cls:GameListType, *args, **kwargs): ...
    controller = ... # type: GameListController
    host = ... # type: HostDetails
    games = ... # type: List(Game)
    logger = ... # type: Logger
    list = ... # type: ControlList
    host_online_img = ... # type: ControlImage
    host_offline_img = ... # type: ControlImage
    host_name_label = ... # type: ControlLabel
    def __init__(self:GameListType, controller: gamelistcontroller, host:HostDetails, game_list:List[object]): ...
    def onInit(self): ...
    def build_list(self): ...
    def onAction(self, action:Action): ...
    def update(self): ...
