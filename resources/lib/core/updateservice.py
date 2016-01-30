import json
import os
import urllib2

import re
import zipfile

from xbmcswift2 import xbmcaddon, xbmcgui, xbmc

from resources.lib.di.component import Component
from resources.lib.di.requiredfeature import RequiredFeature


class UpdateService(Component):
    logger = RequiredFeature('logger')
    core = RequiredFeature('core')
    plugin = RequiredFeature('plugin')
    regexp = '(\d+\.)?(\d+\.)?(\*|\d+)'

    def __init__(self):
        self.logger.info('[UpdateService] - initialized')
        self.api_url = 'https://api.github.com/repos/wackerl91/luna/releases'
        self.current_version = re.match(self.regexp, xbmcaddon.Addon().getAddonInfo('version')).group()
        self.update_version = None
        self.asset_url = None
        self.asset_name = None
        self.change_log = None

    def check_for_update(self, ignore_checked=False):
        update_storage = self.plugin.get_storage('update', TTL=60)
        if not update_storage.get('checked') or ignore_checked:
            response = json.load(urllib2.urlopen(self.api_url))
            for release in response:
                if re.match(self.regexp, release['tag_name'].strip('v')).group() > self.current_version:
                    self.update_version = re.match(self.regexp, release['tag_name'].strip('v')).group()
                    self.asset_url = release['assets'][0]['browser_download_url']
                    self.asset_name = release['assets'][0]['name']
                    self.change_log = release['body']

            if self.asset_name is not None:
                update_storage['checked'] = True
                xbmcgui.Dialog().notification(
                    self.core.string('name'),
                    'Update to version %s available' % self.update_version
                )
                return True

    def initiate_update(self):
        if self.asset_name is not None:
            confirmed = xbmcgui.Dialog().yesno(
                self.core.string('name'),
                'Update to version %s available' % self.update_version,
                'Do you want to update now?'
            )

            if confirmed:
                file_path = os.path.join(self.plugin.storage_path, self.asset_name)
                with open(file_path, 'wb') as asset:
                    asset.write(urllib2.urlopen(self.asset_url).read())
                    asset.close()
                zip_file = zipfile.ZipFile(file_path)
                zip_file.extractall(xbmcaddon.Addon().getAddonInfo('path'), self._get_members(zip_file))

                xbmcgui.Dialog().ok(
                    self.core.string('name'),
                    'Luna has been updated to version %s and will now relaunch.' % self.update_version
                )

                xbmc.executebuiltin('RunPlugin(\'script.luna\')')

    def _get_members(self, zip_file):
        parts = []
        for name in zip_file.namelist():
            if not name.endswith('/'):
                parts.append(name.split('/')[:-1])
        prefix = os.path.commonprefix(parts) or ''
        if prefix:
            prefix = '/'.join(prefix) + '/'
        offset = len(prefix)
        for zipinfo in zip_file.infolist():
            name = zipinfo.filename
            if len(name) > offset:
                zipinfo.filename = name[offset:]
                yield zipinfo
