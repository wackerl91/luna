from typing import List

import pyxbmct

from resources.lib.model.inputdevice import InputDevice


class CtrlSelectionWrapper:
    id = ... # type: str
    idx = ... # type: int
    label = ... # type: str
    input_select_btn = ... # type: pyxbmct.Button
    trigger_adv_mapping_btn = ... # type: pyxbmct.Button
    remove_btn = ... # type: pyxbmct.Button
    adv_row = ... # type: int
    adv_select_mapping = ... # type: pyxbmct.Button
    adv_create_mapping = ... # type: pyxbmct.Button
    adv_remove_mapping = ... # type: pyxbmct.Button
    adv_on_flag = ... # type: bool
    device = ... # type: InputDevice
    def __init__(self): ...
    def set_internal_navigation(self) -> None: ...
    def adv_on(self, view) -> None: ...
    def adv_off(self, view) -> None: ...
    def controls_as_list(self) -> List[pyxbmct.Button]: ...
    def advanced_controls_as_list(self) -> List[pyxbmct.Button]: ...
    def set_mapping_file(self, browser) -> None: ...
    def unset_mapping_file(self) -> None: ...
