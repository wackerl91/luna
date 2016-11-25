from typing import Any, Tuple


class InputMap:
    STATUS_DONE = ... # type: str
    STATUS_PENDING = ... # type: str
    STATUS_ERROR = ... # type: str
    file_name = ... # type: str
    abs_x = ... # type: int
    abs_y = ... # type: int
    abs_z = ... # type: int
    reverse_x = ... # type: bool
    reverse_y = ... # type: bool
    abs_rx = ... # type: int
    abs_ry = ... # type: int
    abs_rz = ... # type: int
    reverse_rx = ... # type: bool
    reverse_ry = ... # type: bool
    abs_deadzone = ... # type: int
    abs_dpad_x = ... # type: int
    abs_dpad_y = ... # type: int
    reverse_dpad_x = ... # type: bool
    reverse_dpad_y = ... # type: bool
    btn_north = ... # type: int
    btn_east = ... # type: int
    btn_south = ... # type: int
    btn_west = ... # type: int
    btn_select = ... # type: int
    btn_start = ... # type: int
    btn_mode = ... # type: int
    btn_thumbl = ... # type: int
    btn_thumbr = ... # type: int
    btn_tl = ... # type: int
    btn_tr = ... # type: int
    btn_tl2 = ... # type: int
    btn_tr2 = ... # type: int
    btn_dpad_up = ... # type: int
    btn_dpad_down = ... # type: int
    btn_dpad_left = ... # type: int
    btn_dpad_right = ... # type: int
    status = ... # type: str
    def __init__(self, file_name:str): ...
    def __iter__(self) -> Tuple(Any, Any): ...
    def set_btn(self, attr, btn_no) -> None: ...
    def write(self) -> None: ...
