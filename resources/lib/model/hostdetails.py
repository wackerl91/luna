class HostDetails(object):
    STATE_ONLINE = 0
    STATE_OFFLINE = 1
    STATE_UNKNOWN = 2

    REACH_LOCAL = 0
    REACH_REMOTE = 1
    REACH_OFFLINE = 2
    REACH_UNKNOWN = 3

    def __init__(self):
        self.name = None
        self.uuid = None
        self.mac_address = None
        self.local_ip = None
        self.remote_ip = None
        self.pair_state = None
        self.state = self.STATE_UNKNOWN
        self.reachability = self.REACH_UNKNOWN
