class HostDetails:
    STATE_ONLINE = ... # type: int
    STATE_OFFLINE = ... # type: int
    STATE_UNKNOWN = ... # type: int
    REACH_LOCAL = ... # type: int
    REACH_REMOTE = ... # type: int
    REACH_OFFLINE = ... # type: int
    REACH_UNKNOWN = ... # type: int
    name = ... # type: str
    uuid = ... # type: str
    mac_address = ... # type: str
    local_ip = ... # type: str
    remote_ip = ... # type: str
    pair_state = ... # type: int
    gpu_type = ... # type: str
    gamelist_id = ... # type: str
    key_dir = ... # type: str
    state = ... # type: int
    reachability = ... # type: int
    def __init__(self): ...
