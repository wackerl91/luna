import xbmc


class HostContextService(object):
    def __init__(self):
        xbmc.log("[script.luna.host-context]: Initialized")
        self.host = None

    def get_current_context(self):
        xbmc.log("[script.luna.host-context]: Requesting current context")
        if self.host is not None:
            return self.host
        else:
            raise ValueError('Host Context has not been set')

    def set_current_context(self, host):
        xbmc.log("[script.luna.host-context]: Setting context to: %s" % host.uuid)
        self.host = host
