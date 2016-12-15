import os
import stat

from datetime import timedelta
from xml.etree.ElementTree import ElementTree

import re

import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.storageengine.storage import TimedStorage

STRINGS = {
    'name':                30000,
    'addon_settings':      30100,
    'full_refresh':        30101,
    'choose_ctrl_type':    30200,
    'enter_filename':      30201,
    'starting_mapping':    30202,
    'mapping_success':     30203,
    'set_mapping_active':  30204,
    'mapping_failure':     30205,
    'pair_failure_paired': 30206,
    'configure_first':     30207,
    'reset_cache_warning': 30208,
    'empty_game_list':     30209,
    'update_available':    30210,
    'no_update_available': 30211,
    'scraper_failed':      30212,
}


class Core:
    regexp = '(\d+\.)?(\d+\.)?(\*|\d+)'

    def __init__(self, logger):
        self.addon = xbmcaddon.Addon()
        self.logger = logger
        self._storage_path = xbmc.translatePath(
            'special://profile/addon_data/%s/.storage/' % self.addon.getAddonInfo('id'))
        self._current_version = re.match(self.regexp, self.addon.getAddonInfo('version')).group()
        self._internal_path = xbmcaddon.Addon().getAddonInfo('path')

        self._create_path()

    def string(self, string_id):
        if string_id in STRINGS:
            return self.addon.getLocalizedString(STRINGS[string_id]).encode('utf-8')
        elif isinstance(string_id, int):
            return self.addon.getLocalizedString(string_id).encode('utf-8')
        else:
            return string_id

    def check_script_permissions(self):
        st = os.stat(self.internal_path + '/resources/lib/launchscripts/osmc/launch.sh')
        if not bool(st.st_mode & stat.S_IXUSR):
            os.chmod(self.internal_path + '/resources/lib/launchscripts/osmc/launch.sh', st.st_mode | 0111)
            self.logger.info('Changed file permissions for launch')

        st = os.stat(self.internal_path + '/resources/lib/launchscripts/osmc/launch-helper-osmc.sh')
        if not bool(st.st_mode & stat.S_IXUSR):
            os.chmod(self.internal_path + '/resources/lib/launchscripts/osmc/launch-helper-osmc.sh', st.st_mode | 0111)
            self.logger.info('Changed file permissions for launch-helper-osmc')

        st = os.stat(self.internal_path + '/resources/lib/launchscripts/osmc/moonlight-heartbeat.sh')
        if not bool(st.st_mode & stat.S_IXUSR):
            os.chmod(self.internal_path + '/resources/lib/launchscripts/osmc/moonlight-heartbeat.sh', st.st_mode | 0111)
            self.logger.info('Changed file permissions for moonlight-heartbeat')

    def get_storage(self, name='game_storage', file_format='pickle', TTL=None):
        """
        This method was originally part of xbmcswift2 by Jonathan Beluch.
        Used in Luna in accordance with GPLv3; with the reason being that his storage engine didn't behave entirely
        correct in conjunction with Luna's underlying architecture, namely the DI. (June, 2016)

        This module contains persistent storage classes.

        :copyright: (c) 2012 by Jonathan Beluch
        :license: GPLv3, see LICENSE for more details.
        Returns a storage for the given name. The returned storage is a
        fully functioning python dictionary and is designed to be used that
        way. It is usually not necessary for the caller to load or save the
        storage manually. If the storage does not already exist, it will be
        created.

        .. seealso:: :class:`xbmcswift2.TimedStorage` for more details.

        :param name: The name  of the storage to retrieve.
        :param file_format: Choices are 'pickle', 'csv', and 'json'. Pickle is
                            recommended as it supports python objects.

                            .. note:: If a storage already exists for the given
                                      name, the file_format parameter is
                                      ignored. The format will be determined by
                                      the existing storage file.
        :param TTL: The time to live for storage items specified in minutes or None
                    for no expiration. Since storage items aren't expired until a
                    storage is loaded form disk, it is possible to call
                    get_storage() with a different TTL than when the storage was
                    created. The currently specified TTL is always honored.
        """

        if not hasattr(self, '_unsynced_storages'):
            self._unsynced_storages = {}
        filename = os.path.join(self.storage_path, name)
        try:
            storage = self._unsynced_storages[filename]
            self.logger.info('Loaded storage "%s" from memory' % name)
        except KeyError:
            if TTL:
                TTL = timedelta(minutes=TTL)

            try:
                storage = TimedStorage(filename, file_format, TTL)
            except ValueError:
                # Thrown when the storage file is corrupted and can't be read.
                # Prompt user to delete storage.
                choices = ['Clear storage', 'Cancel']
                ret = xbmcgui.Dialog().select('A storage file is corrupted. It'
                                              ' is recommended to clear it.',
                                              choices)
                if ret == 0:
                    os.remove(filename)
                    storage = TimedStorage(filename, file_format, TTL)
                else:
                    raise Exception('Corrupted storage file at %s' % filename)

            self._unsynced_storages[filename] = storage
            self.logger.info('Loaded storage "%s" from disk' % name)
        return storage

    def get_active_skin(self):
        userdata_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(self.storage_path))))
        guisettings_file = os.path.join(userdata_folder, 'guisettings.xml')
        xml_root = ElementTree(file=guisettings_file).getroot()
        active_skin = xml_root.find('lookandfeel').find('skin').text
        return active_skin

    def prepare_init_scripts(self):
        if not self.get_setting('enable_init_scripts', bool):
            self.logger.info("Init Scripts have been disabled, returning empty strings")
            return '', ''

        pre_script = self.get_setting('pre_script', str)
        post_script = self.get_setting('post_script', str)

        if pre_script != '' and not self._check_file(pre_script):
            self.logger.warning("Pre Script does not exist or is not executable: %s" % pre_script)
            xbmcgui.Dialog().notification(
                self.string('name'),
                'Pre Script does not exist or is not executable'
            )
            pre_script = ''

        if post_script != '' and not self._check_file(post_script):
            self.logger.warning("Pre Script does not exist or is not executable: %s" % pre_script)
            xbmcgui.Dialog().notification(
                self.string('name'),
                'Post Script does not exist or is not executable'
            )
            post_script = ''

        return pre_script, post_script

    def _check_file(self, file_path):
        if os.path.isfile(file_path):
            st = os.stat(file_path)
            if bool(st.st_mode & stat.S_IXUSR):
                return True

        return False

    def get_setting(self, setting_id, return_type=None):
        setting_value = self.addon.getSetting(setting_id)

        result = {
            str: lambda x: str(x),
            unicode: lambda x: x.decode('utf-8'),
            bool: lambda x: x == 'true',
            int: lambda x: int(x),
        }.get(return_type, lambda x: x)(setting_value)

        return result

    def set_setting(self, setting_id, setting_value):
        self.addon.setSetting(setting_id, str(setting_value))

    def _create_path(self):
        if os.path.exists(self._storage_path):
            return

        os.makedirs(self._storage_path)

    @property
    def current_version(self):
        return self._current_version

    @property
    def internal_path(self):
        return self._internal_path

    @property
    def storage_path(self):
        return self._storage_path
