class HostContextService(object):
    def __init__(self, logger):
        self.logger = logger
        self.host = None

        self.logger.info("Initialized")

    def get_current_context(self):
        self.logger.info("Requesting current context")
        if self.host is not None:
            return self.host
        else:
            raise ValueError('Host Context has not been set')

    def set_current_context(self, host):
        self.logger.info("Setting context to: %s" % host.uuid)
        self.host = host
