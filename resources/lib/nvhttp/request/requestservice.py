import os
import random
import uuid
import xml.etree.ElementTree as ETree

import requests

from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.model.hostdetails import HostDetails
from resources.lib.model.nvapp import NvApp
from resources.lib.nvhttp.cryptoprovider.abstractcryptoprovider import AbstractCryptoProvider
from resources.lib.nvhttp.request.abstractrequestservice import AbstractRequestService


class RequestService(AbstractRequestService):
    def __init__(self, crypto_provider, config_helper):
        self.crypto_provider = crypto_provider
        self.config_helper = config_helper
        self.config_helper.configure(False)

        self.logger = RequiredFeature('logger').request()
        # next settings should be set as they can change depending on the host
        self.host_ip = ''
        self.base_url_https = ''
        self.base_url_http = ''
        self.key_dir = ''
        self.uid = ''

    """
    def set_host_ip(self, ip):
        self.host_ip = ip
        self.base_url_https = 'https://%s:%s' % (self.host_ip, self.HTTPS_PORT)
        self.base_url_http = 'http://%s:%s' % (self.host_ip, self.HTTP_PORT)
        # self.crypto_provider.set_base_path(os.path.join(os.path.expanduser('~'), '.cache/moonlight'))
        # TODO: Where and when to load UID when configuring only via IP?
    """

    def configure(self, host_details):
        self.host_ip = host_details.local_ip
        self.key_dir = host_details.key_dir
        self.base_url_https = 'https://%s:%s' % (self.host_ip, self.HTTPS_PORT)
        self.base_url_http = 'http://%s:%s' % (self.host_ip, self.HTTP_PORT)
        self.uid = self.load_or_generate_uid()

    def build_uid_uuid_string(self):
        return 'uniqueid=%s&uuid=%s' % (self.uid, uuid.uuid4())

    def get_server_info(self):
        response = None
        try:
            response = self.open_http_connection(
                self.base_url_https + '/serverinfo?' + self.build_uid_uuid_string(), True, False)

            self.verify_response_status(response)
        except (AssertionError, IOError) as e:
            # Looks like GEN7 Servers are sending 404 instead of 401 if client is not authorized
            # GFE 2.11.3.5 returns 200 on my machine, only the response body has the right status code
            if response is not None and response.status_code in [401, 404] or isinstance(e.message, str) and \
                    e.message.startswith('401'):
                response = self.open_http_connection(
                    self.base_url_http + '/serverinfo?' + self.build_uid_uuid_string(), True, False)
            else:
                raise ValueError(e.message)

        return response.content

    def get_computer_details(self):
        server_info = ETree.ElementTree(ETree.fromstring(self.re_encode_string(self.get_server_info()))).getroot()

        host = HostDetails()
        host.name = self.get_xml_string(server_info, 'hostname')
        host.uuid = self.get_xml_string(server_info, 'uniqueid')
        host.mac_address = self.get_xml_string(server_info, 'mac')
        host.local_ip = self.get_xml_string(server_info, 'LocalIP')
        host.remote_ip = self.get_xml_string(server_info, 'ExternalIP')
        host.pair_state = int(self.get_xml_string(server_info, 'PairStatus'))
        host.gpu_type = self.get_xml_string(server_info, 'gputype')
        host.gamelist_id = self.get_xml_string(server_info, 'gamelistid')
        host.key_dir = os.path.join(AbstractCryptoProvider.get_key_base_path(), host.uuid)
        host.state = HostDetails.STATE_ONLINE

        self.key_dir = host.key_dir

        return host

    def open_http_connection(self, url, enable_read_timeout, content_only=True):
        try:
            cert = self.crypto_provider.get_cert_path()
            key = self.crypto_provider.get_key_path()

            if not os.path.isfile(cert) or not os.path.isfile(key):
                raise IOError

            if enable_read_timeout:
                # TODO: Only disable host name checking via custom transport:
                # http://stackoverflow.com/questions/22758031/how-to-disable-hostname-checking-in-requests-python
                response = requests.get(url, timeout=(3, 5), cert=(cert, key),
                                        verify=False)
            else:
                response = requests.get(url, timeout=(3, None), cert=(cert, key),
                                        verify=False)
        except (IOError, ValueError):
            response = requests.get(url, timeout=(3, 5), verify=False)

        if content_only:
            return response.content
        else:
            return response

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
        response = self.open_http_connection(self.base_url_https + '/applist?' + self.build_uid_uuid_string(), False,
                                             False)
        if response.status_code in [401, 404]:
            return []
        else:
            self.logger.info(response.content)
            app_list = self.get_app_list_from_string(response.content)

        return app_list

    def get_app_list_from_string(self, xml_string):
        etree = self.build_etree(xml_string)
        if etree is not None:
            applist_root = ETree.ElementTree(etree).getroot()
            applist = []

            for app in applist_root.findall('App'):
                nvapp = NvApp()
                if app.find('AppInstallPath') is not None:
                    nvapp.install_path = app.find('AppInstallPath').text
                if app.find('AppTitle') is not None:
                    nvapp.title = app.find('AppTitle').text.encode('UTF-8')
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
        else:
            raise ValueError("ETree is not set.")

    def get_box_art(self, app_id, asset_type=2, asset_idx=0):
        # TODO: What are the other asset types and indices?
        response = self.open_http_connection(
            '{0:s}/appasset?{1:s}&appid={2:s}&AssetType={3:s}&AssetIdx={4:s}'.format(self.base_url_https,
                                                                                     self.build_uid_uuid_string(),
                                                                                     str(app_id), str(asset_type),
                                                                                     str(asset_idx)),
            True)

        return response

#    def unpair(self):
#        self.open_http_connection(self.base_url_https + '/unpair?' + self.build_uid_uuid_string(), True)

    def load_or_generate_uid(self):
        uid_file = os.path.join(self.key_dir, 'uniqueid.dat')
        self.logger.info(self.key_dir)
        if not os.path.isdir(self.key_dir):
            os.makedirs(self.key_dir)
        if not os.path.isfile(uid_file):
            uid = hex(random.getrandbits(63)).rstrip("L").lstrip("0x")
            with open(uid_file, 'wb') as f:
                f.write(uid)
                f.close()

        else:
            with open(uid_file, 'rb') as f:
                uid = f.read()

        return str(uid)
