class Update:
    current_version = ... # type: str
    update_version = ... # type: str
    asset_url = ... # type: str
    asset_name = ... # type: str
    changelog = ... # type: str
    file_path = ... # type: str
    def __init__(self, current_version:str=None, update_version:str=None, asset_url:str=None, asset_name:str=None, changelog:str=None, file_path:str=None): ...
    def do_update(self) -> None: ...
