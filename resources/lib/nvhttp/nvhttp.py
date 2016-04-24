import os
import random
import uuid
import xml.etree.ElementTree as ET

import requests

from resources.lib.model.hostdetails import HostDetails
from resources.lib.model.nvapp import NvApp


class NvHTTP(object):
    HTTPS_PORT = 47984
    HTTP_PORT = 47989

    def __init__(self, pairing_manager, crypto_provider, config_helper):
        self.pairing_manager = pairing_manager
        self.crypto_provider = crypto_provider
        self.config_helper = config_helper
        self.config_helper.configure(False)
        self.host_ip = self.config_helper.host_ip
        self.key_dir = self.crypto_provider.get_key_dir()
        self.uid = self.load_or_generate_uid()
        self.base_url_https = 'https://%s:%s' % (self.host_ip, self.HTTPS_PORT)
        self.base_url_http = 'http://%s:%s' % (self.host_ip, self.HTTP_PORT)

    def build_uid_uuid_string(self):
        return 'uniqueid=%s&uuid=%s' % (self.uid, uuid.uuid4())

    @staticmethod
    def get_xml_string(server_info, tag):
        if isinstance(server_info, str):
            server_info = ET.ElementTree(ET.fromstring(server_info.encode('utf-16'))).getroot()

        if server_info.find(tag) is not None:
            text = server_info.find(tag).text
        else:
            text = ''

        return text

    @staticmethod
    def verify_response_status(response):
        server_info = ET.ElementTree(ET.fromstring(response.encode('utf-16'))).getroot()
        status_code = server_info.get('status_code')
        if int(status_code) != 200:
            raise AssertionError(status_code + ' ' + server_info.get('status_message'))

    def get_server_info(self):
        response = ''
        try:
            response = self.open_http_connection(
                self.base_url_https + '/serverinfo?' + self.build_uid_uuid_string(), True)
            self.get_server_version(response)
            self.verify_response_status(response)
        except AssertionError, e:
            if response.status_code == 401:
                response = self.open_http_connection(self.base_url_http + '/serverinfo', True)
            else:
                raise ValueError(e.message)

        return response

    def get_computer_details(self):
        server_info = ET.ElementTree(ET.fromstring(self.get_server_info())).getroot()

        host = HostDetails()
        host.name = self.get_xml_string(server_info, 'hostname')
        host.uuid = self.get_xml_string(server_info, 'uniqueid')
        host.mac_address = self.get_xml_string(server_info, 'mac')
        host.local_ip = self.get_xml_string(server_info, 'LocalIP')
        host.remote_ip = self.get_xml_string(server_info, 'ExternalIP')
        host.pair_state = int(self.get_xml_string(server_info, 'PairStatus'))
        host.state = HostDetails.STATE_ONLINE

        return host

    def open_http_connection(self, url, enable_read_timeout):
        cert = self.crypto_provider.get_cert_path()
        key = self.crypto_provider.get_key_path()
        if enable_read_timeout:
            # TODO: Only disable host name checking via custom transport: http://stackoverflow.com/questions/22758031/how-to-disable-hostname-checking-in-requests-python
            response = requests.get(url, timeout=(3, 5), cert=(cert, key),
                                    verify=False)
        else:
            response = requests.get(url, timeout=(3, None), cert=(cert, key),
                                    verify=False)

        return response.content

    def open_http_connection_to_string(self, url, enable_read_timeout):
        response = self.open_http_connection(url, enable_read_timeout)

        print response

    @staticmethod
    def get_server_version(server_info):
        return NvHTTP.get_xml_string(server_info, "appversion")

    def get_pair_state(self, server_info=None):
        if not server_info:
            return self.pairing_manager.get_pair_state(self, self.get_server_info())
        else:
            return self.pairing_manager.get_pair_state(self, server_info)

    def get_gpu_type(self, server_info):
        return self.get_xml_string(server_info, "gputype")

    def get_current_game(self, server_info):
        server_state = self.get_xml_string(server_info, "state")
        if server_state is not None and not server_state.endswith('_SERVER_AVAILABLE'):
            game = self.get_xml_string(server_info, "currentgame")
            return int(game)
        else:
            return 0

    def get_app_by_id(self, app_id):
        applist = self.get_app_list()
        for _app_id, _app_name in applist:
            if app_id == _app_id:
                app_idx = applist.index((_app_id, _app_name))
                return applist[app_idx]
        return None

    def get_app_list(self):
        response = self.open_http_connection(self.base_url_https + '/applist?' + self.build_uid_uuid_string(), True)
        applist = self.get_app_list_from_string(response)

        return applist

    def get_app_list_from_string(self, xml_string):
        applist_root = ET.ElementTree(ET.fromstring(xml_string)).getroot()
        applist = []

        for app in applist_root.findall('App'):
            nvapp = NvApp()
            if app.find('AppInstallPath') is not None:
                nvapp.install_path = app.find('AppInstallPath').text
            if app.find('AppTitle') is not None:
                nvapp.title = app.find('AppTitle').text
            if app.find('Distributor') is not None:
                nvapp.distributor = app.find('Distributor').text
            if app.find('ID') is not None:
                nvapp.id = app.find('ID').text
            if app.find('MaxControllersForSingleSession') is not None:
                nvapp.max_controllers = app.find('MaxControllersForSingleSession').text
            if app.find('ShortName') is not None:
                nvapp.short_name = app.find('ShortName').text
            applist.append(nvapp)

        return applist

    def get_box_art(self, app_id, asset_type=2, asset_idx=0):
        # TODO: What are the other asset types and indices?
        response = self.open_http_connection(
            '{0:s}/appasset?{1:s}&appid={2:s}&AssetType={3:s}&AssetIdx={4:s}'.format(self.base_url_https,
                                                                                     self.build_uid_uuid_string(),
                                                                                     app_id, asset_type, asset_idx),
            True)

        return response.content

    def pair(self, server_info, pin, dialog):
        return self.pairing_manager.pair(self, server_info, pin, dialog)

    def unpair(self):
        self.open_http_connection(self.base_url_https + '/unpair?' + self.build_uid_uuid_string(), True)

    @staticmethod
    def get_server_major_version(server_info):
        server_version = NvHTTP.get_server_version(server_info)
        return int(server_version[:1])

    def load_or_generate_uid(self):
        uid_file = os.path.join(self.key_dir, 'uniqueid.dat')
        if not os.path.isfile(uid_file):
            uid = hex(random.getrandbits(63)).rstrip("L").lstrip("0x")
            with open(uid_file, 'wb') as f:
                f.write(uid)
                f.close()

        else:
            with open(uid_file, 'rb') as f:
                uid = f.read()

        return str(uid)
