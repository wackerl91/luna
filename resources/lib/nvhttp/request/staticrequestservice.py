import os
import random
import uuid
import xml.etree.ElementTree as ETree

import requests

from resources.lib.model.hostdetails import HostDetails
from resources.lib.nvhttp.request.abstractrequestservice import AbstractRequestService


class StaticRequestService(AbstractRequestService):
    @staticmethod
    def get_static_server_info(host_ip):
        base_url_http = 'http://%s:%s' % (host_ip, StaticRequestService.HTTP_PORT)
        response = StaticRequestService.open_static_http_connection(
            base_url_http + '/serverinfo?' + StaticRequestService.build_static_uid_uuid_string(), False)

        return response.content

    @staticmethod
    def get_static_computer_details(host_ip):
        from resources.lib.nvhttp.cryptoprovider.abstractcryptoprovider import AbstractCryptoProvider
        server_info = ETree.ElementTree(
            ETree.fromstring(StaticRequestService.get_static_server_info(host_ip).encode('utf-16'))).getroot()

        host = HostDetails()
        host.name = StaticRequestService.get_xml_string(server_info, 'hostname')
        host.uuid = StaticRequestService.get_xml_string(server_info, 'uniqueid')
        host.mac_address = StaticRequestService.get_xml_string(server_info, 'mac')
        host.local_ip = StaticRequestService.get_xml_string(server_info, 'LocalIP')
        host.remote_ip = StaticRequestService.get_xml_string(server_info, 'ExternalIP')
        host.pair_state = int(StaticRequestService.get_xml_string(server_info, 'PairStatus'))
        host.gpu_type = StaticRequestService.get_xml_string(server_info, 'gputype')
        host.gamelist_id = StaticRequestService.get_xml_string(server_info, 'gamelistid')
        host.key_dir = os.path.join(AbstractCryptoProvider.get_key_base_path(), host.uuid)
        host.state = HostDetails.STATE_ONLINE

        return host

    @staticmethod
    def open_static_http_connection(url, content_only=True):
        response = requests.get(url, timeout=(3, 5))

        if content_only:
            return response.content
        else:
            return response

    @staticmethod
    def build_static_uid_uuid_string():
        uid = hex(random.getrandbits(63)).rstrip("L").lstrip("0x")
        return 'uniqueid=%s&uuid=%s' % (uid, uuid.uuid4())
