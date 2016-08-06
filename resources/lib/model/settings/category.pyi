from typing import List

from resources.lib.model.settings.setting import Setting


class Category:
    cat_id = ... # type: int
    cat_label = ... # type: str
    priority = ... # type: int
    settings = ... # type: List[Setting]
    def __init__(self, cat_id: int, cat_label: str, priority: int) -> None: ...
