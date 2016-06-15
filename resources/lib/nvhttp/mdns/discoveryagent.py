import time
from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange

from resources.lib.model.mdnscomputer import MdnsComputer


class DiscoveryAgent(object):
    service_type = '_nvstream._tcp.local.'

    def __init__(self):
        self.available_hosts = {}
        self.zeroconf = None
        self.browser = None

    def service_state_change(self, zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            self.available_hosts[name] = MdnsComputer.from_service_info(info)

    def start_discovery(self, timeout=3):
        start_time = time.time()
        self.zeroconf = Zeroconf()
        self.browser = ServiceBrowser(self.zeroconf, self.service_type, handlers=[self.service_state_change])
        try:
            while time.time() - start_time < timeout:
                time.sleep(0.1)
        except:
            pass
        finally:
            self.zeroconf.close()
