import importlib

import xbmc
import xbmcgui

from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.nvhttp.request.staticrequestservice import StaticRequestService
from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager
from resources.lib.views.hostlist import HostList
from xbmcgui import Dialog, INPUT_IPADDRESS


class HostController(BaseController):
    def __init__(self, logger, core, connection_manager, host_manager, host_context_service):
        self.logger = logger
        self.core = core
        self.connection_manager = connection_manager
        self.host_manager = host_manager
        self.host_context_service = host_context_service
        self.discovery_agent = None
        self._load_agent()

    @route(name='wake')
    def wake_host(self, host):
        """
        This partly taken from Dipl.-Ing. (FH) Georg Kainzbauer http://www.gtkdb.de/index_31_2254.html
        Magic packets aren't that magic after all, but it's nice to get some fast and working code.
        """
        progress_dialog = xbmcgui.DialogProgress()
        progress_dialog.create('Luna', 'Preparing to wake host: %s' % host.name)
        xbmc.sleep(2000)
        import struct
        import socket
        self.logger.info(
            "Wake Host called for host: %s (IP: %s / MAC: %s)" % (host.name, host.local_ip, host.mac_address))
        mac = host.mac_address.replace(':', '')
        self.logger.info("Cleared MAC: %s" % mac)

        magic_packet = ''.join(['FF' * 6, mac * 16])
        data = ''
        self.logger.info('Preparing data stream')
        for i in range(0, len(magic_packet), 2):
            data = ''.join([data, struct.pack('B', int(magic_packet[i: i + 2], 16))])

        self.logger.info('Preparing socket')
        socket_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_conn.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        socket_conn.sendto(data, ('255.255.255.255', 9))
        self.logger.info('Send data through socket; done')
        progress_dialog.update(0, line1='Done')
        xbmc.sleep(2000)
        progress_dialog.close()

    @route(name='add')
    def initiate(self):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        if self.discovery_agent is not None:
            try:
                self.discovery_agent.start_discovery()
                hosts = self.discovery_agent.available_hosts
                self.logger.info("Hosts discovered via zeroconf: %s" % len(hosts))
                if len(hosts) > 0:
                    self.logger.info("Passing hosts to select screen.")
                    xbmc.executebuiltin("Dialog.Close(busydialog)")
                    return self.select_host(hosts)
            except Exception as e:
                xbmc.executebuiltin("Dialog.Close(busydialog)")
                raise e

        self.logger.info("DiscoveryAgent failed to load or no hosts could be found, falling back to IP input.")
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        return self.enter_ip()

    @route(name='remove')
    def remove_host(self, host):
        self.host_context_service.set_current_context(host)
        self.connection_manager.unpair()

        self.host_manager.remove_host(host)

        return True

    def pair_selected_host(self, host):
        self.host_context_service.set_current_context(host)

        pair_dialog = xbmcgui.DialogProgress()
        pair_dialog.create(
            self.core.string('name'),
            'Starting Pairing'
        )

        message, state = self.connection_manager.pair(pair_dialog)
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
        host_details = {}
        for key, host in hosts.iteritems():
            self.logger.info("Host Address obtained via Zeroconf: %s" % host.address)
            _host = StaticRequestService.get_static_computer_details(host.address)
            host_details[_host.uuid] = _host

        window = HostList(host_details)
        window.doModal()
        selected_host = window.selected_host
        del window

        if selected_host is not None:
            return self.pair_selected_host(selected_host)
        else:
            self.logger.info('Host selection cancelled')
            return None

    def enter_ip(self):
        dialog = Dialog()
        ip = dialog.input('Enter Host IP', type=INPUT_IPADDRESS)

        if ip is not '':
            _host = StaticRequestService.get_static_computer_details(ip)
            return self.pair_selected_host(_host)
        else:
            return None

    def _load_agent(self):
        try:
            module = importlib.import_module('resources.lib.nvhttp.mdns.discoveryagent')
            class_name = 'DiscoveryAgent'
            class_ = getattr(module, class_name)
            self.discovery_agent = class_()
        except ImportError as e:
            self.logger.info("Couldn't load DiscoveryAgent: %s" % e.message)
