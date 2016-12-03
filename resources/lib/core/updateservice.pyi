from typing import Union, Dict
from zipfile import ZipFile, ZipInfo
from xbmcaddon import Addon

from resources.lib.core.corefunctions import Core
from resources.lib.core.logger import Logger
from resources.lib.model.update import Update


class UpdateService:
    regexp = ... # type: str
    api_url = ... # type: str
    pre_api_url = ... # type: str
    addon = ... # type: Addon
    core = ... # type: Core
    logger = ... # type: Logger
    current_version = ... # type: str
    update_version = ... # type: str
    asset_url = ... # type: str
    asset_name = ... # type: str
    changelog = ... # type: str
    def __init__(self, addon: Addon, core: Core, logger: Logger): ...
    def check_for_update(self, ignore_checked:bool) -> Union(Update, None): ...
    def initiate_update(self, update: Update) -> None: ...
    def do_update(self, update: Update) -> None: ...
    def _get_members(self, zip_file: ZipFile) -> ZipInfo: ...
    def parse_release_information(self, release:Dict) -> Update: ...
