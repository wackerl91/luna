from xml.etree.ElementTree import ElementTree

from typing import Dict

from resources.lib.core.corefunctions import Core
from resources.lib.core.logger import Logger
from resources.lib.model.settings.category import Category


class SettingsParser:
    settings_path = ... # type: str
    settings_tree = ... # type: ElementTree
    settings_hash = ... # type: str
    logger = ... # type: Logger
    settings_dict = ... # type: Dict
    core = ... # type: Core
    def __init__(self, core: Core, logger: Logger) -> None: ...
    def _get_settings_hash(self) -> str: ...
    def _reload_settings(self) -> None: ...
    def get_settings(self) -> Dict[Category]: ...
    def update_values(self) -> None: ...
