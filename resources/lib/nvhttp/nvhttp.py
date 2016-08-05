import os
import random
import re
import uuid
import xml.etree.ElementTree as ET

import requests

from resources.lib.di.requiredfeature import RequiredFeature
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
        try:
            server_info = ET.ElementTree(ET.fromstring(response.content.encode('utf-16'))).getroot()
            status_code = server_info.get('status_code')
            status_message = server_info.get('status_message')
        except ET.ParseError, e:
            status_code = str(response.status_code)
            status_message = response.content
        if int(status_code) != 200:
            raise AssertionError(status_code + ' ' + status_message)

    def get_server_info(self):
        response = None
        try:
            response = self.open_http_connection(
                self.base_url_https + '/serverinfo?' + self.build_uid_uuid_string(), True, False)

            self.verify_response_status(response)
        except (AssertionError, IOError) as e:
            # Looks like GEN7 Servers are sending 404 instead of 401 if client is not authorized
            # GFE 2.11.3.5 returns 200 on my machine, only the response body has the right status code
            if response.status_code in [401, 404] or e.message.startswith('401'):
                response = self.open_http_connection(
                    self.base_url_http + '/serverinfo?' + self.build_uid_uuid_string(), True, False)
            else:
                raise ValueError(e.message)

        return response.content

    def get_computer_details(self):
        etree = self.build_etree(self.get_server_info())
        if etree is not None:
            server_info = ET.ElementTree(etree).getroot()

            host = HostDetails()
            host.name = self.get_xml_string(server_info, 'hostname')
            host.uuid = self.get_xml_string(server_info, 'uniqueid')
            host.mac_address = self.get_xml_string(server_info, 'mac')
            host.local_ip = self.get_xml_string(server_info, 'LocalIP')
            host.remote_ip = self.get_xml_string(server_info, 'ExternalIP')
            host.pair_state = int(self.get_xml_string(server_info, 'PairStatus'))
            host.state = HostDetails.STATE_ONLINE

            return host
        else:
            raise ValueError('ETree is not set.')

    def open_http_connection(self, url, enable_read_timeout, content_only=True):
        try:
            cert = self.crypto_provider.get_cert_path()
            key = self.crypto_provider.get_key_path()

            if not os.path.isfile(cert) or not os.path.isfile(key):
                raise IOError

            if enable_read_timeout:
                # TODO: Only disable host name checking via custom transport: http://stackoverflow.com/questions/22758031/how-to-disable-hostname-checking-in-requests-python
                response = requests.get(url, timeout=(3, 5), cert=(cert, key),
                                        verify=False)
            else:
                response = requests.get(url, timeout=(3, None), cert=(cert, key),
                                        verify=False)
        except IOError, e:
            response = requests.get(url, timeout=(3, 5), verify=False)

        if content_only:
            return response.content
        else:
            return response

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
        response = self.open_http_connection(self.base_url_https + '/applist?' + self.build_uid_uuid_string(), False,
                                             False)
        if response.status_code in [401, 404]:
            return []
        else:
            applist = self.get_app_list_from_string(response.content)

        return applist

    def get_app_list_from_string(self, xml_string):
        etree = self.build_etree(xml_string)
        if etree is not None:
            # ET.fromstring(self.re_encode_string(xml_string))
            applist_root = ET.ElementTree(etree).getroot()
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
            raise ValueError('ETree is not set.')

    def get_box_art(self, app_id, asset_type=2, asset_idx=0):
        # TODO: What are the other asset types and indices?
        response = self.open_http_connection(
            '{0:s}/appasset?{1:s}&appid={2:s}&AssetType={3:s}&AssetIdx={4:s}'.format(self.base_url_https,
                                                                                     self.build_uid_uuid_string(),
                                                                                     str(app_id), str(asset_type),
                                                                                     str(asset_idx)),
            True)

        return response

    def pair(self, server_info, dialog):
        return self.pairing_manager.pair(self, server_info, dialog)

    def unpair(self):
        self.open_http_connection(self.base_url_https + '/unpair?' + self.build_uid_uuid_string(), True)

    @staticmethod
    def get_server_major_version(server_info):
        server_version = NvHTTP.get_server_version(server_info)
        return int(server_version[:1])

    def load_or_generate_uid(self):
        uid_file = os.path.join(self.key_dir, 'uniqueid.dat')
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

    def re_encode_string(self, xml_string, only_encode=False):
        logger = RequiredFeature('logger').request()
        regex = re.compile('UTF-\d{1,2}')

        specified_encoding = regex.search(xml_string)

        if specified_encoding is not None:
            try:
                logger.info("Trying to re-encode received XML as %s" % specified_encoding.group(0))
                if not only_encode:
                    xml_string = xml_string.decode(specified_encoding.group(0))
                xml_string = xml_string.encode(specified_encoding.group(0))
            except (UnicodeDecodeError, UnicodeEncodeError) as e:
                if not only_encode:
                    logger.info(
                        "Re-encode failed, trying to decode as UTF-8")
                    xml_string = xml_string.decode('UTF-8')
                if isinstance(e, UnicodeEncodeError):
                    encoding = 'UTF-8' if specified_encoding.group(0) == 'UTF-8' else 'UTF-16'
                    logger.info("Trying to encode as: %s" % encoding)
                    xml_string = xml_string.encode(encoding)
                else:
                    logger.info("Trying to encode as: %s" % specified_encoding.group(0))
                    xml_string = xml_string.encode(specified_encoding.group(0))

        return xml_string

    def build_etree(self, xml_string):
        try:
            etree = ET.fromstring(self.re_encode_string(xml_string))
        except ET.ParseError:
            try:
                etree = ET.fromstring(self.re_encode_string(xml_string, only_encode=True))
            except ET.ParseError as e:
                logger = RequiredFeature('logger').request()
                logger.error("Building ETree from XML failed: %s" % e.message)
                logger.info(xml_string)
                return None

        return etree
