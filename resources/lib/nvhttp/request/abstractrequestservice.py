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

        logger.info("Trying to decode as: %s" % 'ASCII')
        try:
            xml_string = xml_string.decode(encoding='ascii')
        except UnicodeDecodeError as e:
            logger.info("Decoding as %s failed, trying as %s" % ('ASCII', 'UTF-8'))
            try:
                xml_string = xml_string.decode(encoding='UTF-8')
            except UnicodeDecodeError as e:
                logger.info("Decoding as %s failed, trying as %s" % ('UTF-8', 'UTF-16'))
                try:
                    xml_string = xml_string.decode(encoding='UTF-16')
                except UnicodeDecodeError as e:
                    logger.error("Decoding as UTF-16 failed, this was the last attempt. Offending string follows ...")
                    logger.error(xml_string)
                    raise ValueError("String Decode Failed")

        if specified_encoding is not None:
            try:
                logger.info("Trying to encode as specified in XML: %s" % specified_encoding.group(0))
                xml_string = xml_string.encode(encoding=specified_encoding.group(0))
            except UnicodeEncodeError as e:
                new_encode_setting = 'UTF-16' if specified_encoding.group(0) == 'UTF-8' else 'UTF-8'
                logger.info("Encoding as %s failed, trying as %s" % (specified_encoding.group(0), new_encode_setting))
                try:
                    xml_string = xml_string.encode(encoding=new_encode_setting)
                except UnicodeEncodeError as e:
                    logger.error(
                        "Encoding as %s failed, this was the last attempt. Offending string follows ..." %
                        new_encode_setting)
                    logger.error(xml_string)
                    raise ValueError("String Encode Failed")

            return xml_string
        else:
            logger.info("RegExp couldn't find a match in the XML string ...")
            try:
                logger.info("Trying to encode as: UTF-8")
                xml_string = xml_string.encode(encoding='UTF-8')
            except UnicodeEncodeError as e:
                logger.info("Encoding as UTF-8 failed, trying as UTF-16")
                try:
                    xml_string = xml_string.encode(encoding='UTF-16')
                except UnicodeEncodeError as e:
                    logger.error("Encoding as UTF-16 failed, this was the last attempt. Offending string follows ...")
                    logger.error(xml_string)
                    raise ValueError("String Encode Failed")

            return xml_string

    @staticmethod
    def build_etree(xml_string):
        try:
            etree = ETree.fromstring(AbstractRequestService.re_encode_string(xml_string))
        except ETree.ParseError as e:
            logger = RequiredFeature('logger').request()
            logger.error("Building ETree from XML failed: %s. Offending string follows ..." % e.message)
            logger.error(xml_string)
            raise ValueError("Building ETree Failed")

        return etree
