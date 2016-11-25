class NvApp:
    install_path = ... # type: str
    title = ... # type: str
    distributor = ... # type: str
    id = ... # type: str
    max_controllers = ... # type: int
    short_name = ... # type: str
    def __init__(self): ...
    def to_game(self) -> None: ...
