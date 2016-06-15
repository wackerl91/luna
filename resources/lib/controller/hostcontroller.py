import importlib

import xbmcgui
from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager
from xbmcgui import Dialog, INPUT_IPADDRESS


class HostController(object):
    def __init__(self, logger, core, nvhttp, connection_manager, host_manager):
        self.logger = logger
        self.core = core
        self.nvhttp = nvhttp
        self.connection_manager = connection_manager
        self.host_manager = host_manager
        self.discovery_agent = None
        self.__load_agent()

    def initiate(self):
        try:
            if self.discovery_agent is not None:
                self.discovery_agent.start_discovery()
                hosts = self.discovery_agent.available_hosts
                # if len(hosts) > 0:
                #    self.select_host(hosts)
                # else:
                raise AttributeError
        except AttributeError:
            return self.enter_ip()

    def pair_selected_host(self, host):
        pair_dialog = xbmcgui.DialogProgress()
        pair_dialog.create(
            self.core.string('name'),
            'Starting Pairing'
        )

        message, state = self.connection_manager.pair(pair_dialog, host)
        pair_dialog.close()

        if state == AbstractPairingManager.STATE_PAIRED:
            self.host_manager.add_host(host)
            self.logger.info(self.host_manager)
            self.logger.info('Added host with name: ' + host.name)
            xbmcgui.Dialog().ok(
                self.core.string('name'),
                message
            )

            return host
        else:
            confirmed = xbmcgui.Dialog().yesno(
                self.core.string('name'),
                '%s - Do you want to try again?' % message
            )
            if confirmed:
                self.pair_selected_host(host)

    def select_host(self, hosts):
        # TODO: Select Host Controller -> Render view with all available Hosts + additional information
        # -> needs to be a dedicated controller because we need to pass the selected host back to the caller, which would clutter this module
        pass

    def enter_ip(self):
        dialog = Dialog()
        ip = dialog.input('Enter Host IP', type=INPUT_IPADDRESS)

        if ip is not '':
            self.nvhttp.set_host_ip(ip)
            return self.pair_selected_host(self.nvhttp.get_computer_details())
        else:
            return None

    def __load_agent(self):
        try:
            module = importlib.import_module('resources.lib.nvhttp.mdns.discoveryagent')
            class_name = 'DiscoveryAgent'
            class_ = getattr(module, class_name)
            self.discovery_agent = class_()
        except ImportError:
            pass
