class HostManager(object):
    def __init__(self, repository):
        self.repository = repository

    def get_hosts(self):
        return self.repository.get_hosts()

    def add_host(self, host, flush=True):
        self.repository.add_host(host, flush)

    def remove_host(self, host, flush=True):
        self.repository.remove_host(host, flush)

    def remove_host_by_id(self, host_id, flush=True):
        self.repository.remove_host_by_id(host_id, flush)

    def get_host_by_id(self, host_id):
        self.repository.get_host_by_id(host_id)
