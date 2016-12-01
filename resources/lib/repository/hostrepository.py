class HostRepository(object):
    def __init__(self, core, logger):
        self.storage = core.get_storage('host')
        self.logger = logger

    def get_hosts(self):
        return self.storage

    def add_host(self, host, flush=True):
        self.storage[host.uuid] = host
        self.logger.info('Added host with name: ' + host.name)
        if flush:
            self.storage.sync()
            self.logger.info('Flush called, current dict length: ' + str(len(self.storage.raw_dict())))

    def remove_host(self, host, flush=True):
        self.logger.info('Remove Host called')
        self.remove_host_by_id(host.uuid, flush)

    def remove_host_by_id(self, host_id, flush=True):
        self.logger.info('Remove Host By ID called')
        if host_id in self.storage:
            del self.storage[host_id]
        if flush:
            self.storage.sync()

    def get_host_by_id(self, host_id):
        self.logger.info('Get Host By ID Called')
        try:
            return self.storage[host_id]
        except ValueError, e:
            return None
