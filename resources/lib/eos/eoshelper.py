import json
import os
import threading

import requests

from uuid import getnode as get_mac

HTTP_GET = 'get'
HTTP_POST = 'post'
HTTP_PUT = 'put'


def async(func):
    def async_call(*args, **kwargs):
        async_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        return async_thread.start()

    return async_call


class EosHelper(object):
    def __init__(self, core, host_manager, game_manager):
        self.core = core
        self.host_manager = host_manager
        self.game_manager = game_manager
        from resources.lib.core.logger.logger import Logger
        self.logger = Logger('debug')

        self.base_url = 'https://www-eos.herokuapp.com/'
        self.uid = None

        self._load_or_get_uid()
        self.update_system_information()
        self.register_usage()

    @async
    def update_system_information(self):
        url = 'user/{userId}'

        host_details = []

        for key, host in self.host_manager.get_hosts().iteritems():
            server_version = ''
            if hasattr(host, 'server_version'):
                server_version = host.server_version
            host_details.append({
                'gfe_version': server_version,
                'number_of_games': len(self.game_manager.get_games(host)),
                'host_uuid': host.uuid
            })

        os_info = os.uname()
        os_version = ''

        release_file = '/etc/os-release'
        if os.path.isfile(release_file):
            with open(release_file) as f:
                for line in f.readlines():
                    if line.startswith('VERSION_ID'):
                        os_version = line.replace('VERSION_ID=', '').replace('"', '')
                        break
            f.close()

        if os_version == '':
            os_version = os_info[3]

        kodi_version = self.core.get_kodi_version()
        kodi_version = '%s.%s.%s - %s' % (kodi_version['major'], kodi_version['minor'],
                                           kodi_version['tagversion'], kodi_version['tag'])

        system_info = {
            'luna_version': self.core.addon.getAddonInfo('version'),
            'system_identifier': '%s %s %s' % (os_info[0], os_info[1], os_info[2]),
            'system_version': os_version,
            'kodi_version': kodi_version,
            'moonlight_version': '',
            'hosts': host_details
        }

        json_string = json.dumps(system_info)
        response = self._open_connection(url, HTTP_PUT, json_string)

        if response.status_code != 201:
            self.logger.warning("script.luna.eos", "Updating system information on EOS failed: %s - %s. JSON: %s. URL: %s" %
                                (response.status_code, response.content, json_string, url))

    @async
    def register_usage(self):
        url = 'user/{user}/usage/create'

        response = self._open_connection(url, HTTP_POST)

        if response.status_code != 201 and response.status_code != 208:
            self.logger.warning("script.luna.eos", "Registering usage failed: %s - %s" %
                                (response.status_code, response.content))

    @async
    def log(self, log_level, log_channel, log_message, additional_information=None):
        url = 'user/{user}/log/create'

        log_entry = {
            'log_level': log_level,
            'log_channel': log_channel,
            'log_message': log_message
        }

        if additional_information is not None:
            log_entry['additional_information'] = additional_information

        json_string = '%s' % json.dumps(log_entry)

        response = self._open_connection(url, HTTP_POST, json_string)

        if response.status_code != 201:
            self.logger.warning("script.luna.eos", "Sending log message to EOS failed: %s - %s. JSON: %s" %
                                (response.status_code, response.content, json_string))

    @async
    def register_exception(self, exc_type, exc_value, trace):
        url = 'user/{user}/exception/create'

        json_string = json.dumps(
            {
                'exception_type': str(exc_type),
                'exception_value': str(exc_value),
                'traceback': trace
            }
        )

        response = self._open_connection(url, HTTP_POST, json_string)

        if response.status_code != 201:
            self.logger.warning("script.luna.eos", "Sending exception to EOS failed: %s - %s" %
                                (response.status_code, response.content))

    def _load_or_get_uid(self):
        uid_file = os.path.join(self.core.storage_path, '.eos_uid')
        if not os.path.isfile(uid_file):
            uid = self._get_uid()

            if uid is not None:
                with open(uid_file, 'wb') as f:
                    f.write(uid)
                    f.close()
        else:
            with open(uid_file, 'rb') as f:
                uid = f.read()

        self.uid = uid.replace('"', '')

    def _get_uid(self):
        hardware_id = self._generate_hardware_id()
        url = os.path.join(self.base_url, 'request', hardware_id)
        try:
            response = requests.get(url, timeout=(3, 10))
        except requests.exceptions.ReadTimeout:
            # Try again, EOS might be sleeping
            try:
                response = requests.get(url, timeout=(3, 20))
            except requests.exceptions.ReadTimeout as e:
                self.logger.warning("script.luna.eos", "Connection to EOS timed out: %s" % e.message)

                return None

        if response.status_code == 200:

            return response.content
        else:

            return None

    def _generate_hardware_id(self):
        mac = str(get_mac())
        cpu_sn = ''
        cpu_info = '/proc/cpuinfo'

        if not os.path.isfile(cpu_info):
            return mac

        with open(cpu_info) as f:
            for line in f.readlines():
                if line.startswith('Serial'):
                    cpu_sn = line.replace('Serial', '').replace(':', '').lstrip()
                    break

            f.close()

        return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(mac, cpu_sn)).encode("hex")

    def _open_connection(self, url, request_type=HTTP_GET, data=None, timeout=None):
        if self.uid is None:
            self._load_or_get_uid()

            if self.uid is None:
                self.logger.warning("script.luna.eos", "Could not load / get user ID for EOS.")

                return

        url = url.replace('{user}', self.uid)
        url = url.replace('{userId}', self.uid)

        url = os.path.join(self.base_url, url)
        self.logger.info("script.luna.eos", "Calling URL: %s" % url)

        response = None

        if request_type == HTTP_GET:
            response = requests.get(url, timeout=timeout)
        elif request_type == HTTP_PUT:
            response = requests.put(url, data, timeout=timeout)
        elif request_type == HTTP_POST:
            response = requests.post(url, data=data, json=data, timeout=timeout)

        return response
