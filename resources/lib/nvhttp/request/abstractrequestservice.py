import re
from abc import ABCMeta
import xml.etree.ElementTree as ETree

from resources.lib.di.requiredfeature import RequiredFeature


class AbstractRequestService(object):
    __metaclass__ = ABCMeta

    HTTPS_PORT = 47984
    HTTP_PORT = 47989

    @staticmethod
    def get_xml_string(server_info, tag):
        if isinstance(server_info, str):
            server_info = ETree.ElementTree(ETree.fromstring(server_info.encode('utf-16'))).getroot()

        if server_info.find(tag) is not None:
            text = server_info.find(tag).text
        else:
            text = ''

        return text

    @staticmethod
    def verify_response_status(response):
        try:
            server_info = ETree.ElementTree(ETree.fromstring(response.content.encode('utf-16'))).getroot()
            status_code = server_info.get('status_code')
            status_message = server_info.get('status_message')
        except ETree.ParseError:
            status_code = str(response.status_code)
            status_message = response.content
        if int(status_code) != 200:
            raise AssertionError(status_code + ' ' + status_message)

    @staticmethod
    def get_server_version(server_info):
        return AbstractRequestService.get_xml_string(server_info, "appversion")

    @staticmethod
    def get_server_major_version(server_info):
        server_version = AbstractRequestService.get_server_version(server_info)
        return int(server_version[:1])

    @staticmethod
    def re_encode_string(xml_string):
        logger = RequiredFeature('logger').request()
        regex = re.compile('UTF-\d{1,2}')

        specified_encoding = regex.search(xml_string)

        if specified_encoding is not None:
            try:
                logger.info("Trying to re-encode received XML as %s" % specified_encoding.group(0))
                xml_string = xml_string.decode(specified_encoding.group(0))
                xml_string = xml_string.encode(specified_encoding.group(0))
            except UnicodeDecodeError:
                logger.info("Re-encode failed, trying to decode as UTF-8 and re-encoding as specified.")
                xml_string = xml_string.decode('UTF-8')
                xml_string = xml_string.encode(specified_encoding.group(0))

        return xml_string
