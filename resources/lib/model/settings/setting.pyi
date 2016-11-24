from typing import Dict
from typing import List


class Setting:
    setting_id = ...  # type: int
    setting_label = ...  # type: str
    priority = ...  # type: int

    type = ...  # type: str
    default = ...  # type: str
    visible = ...  # type: bool
    enable = ...  # type: bool
    values = ...  # type: List[str]
    range = ...  # type: List[int] | List[str]
    option = ...  # type: str
    subsetting = ...  # type: bool
    def __init__(self, setting_id: int, setting_label: str, priority: int, *args: tuple, **kwargs: Dict) -> None: ...