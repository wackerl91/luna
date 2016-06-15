import json
import os
import urllib2

import re
import zipfile

from xbmcswift2 import xbmcaddon, xbmcgui, xbmc

from resources.lib.model.update import Update
from resources.lib.views.updateinfo import UpdateInfo


class UpdateService:
    regexp = '(\d+\.)?(\d+\.)?(\*|\d+)'
    api_url = 'https://api.github.com/repos/wackerl91/luna/releases/latest'
    pre_api_url = 'https://api.github.com/repos/wackerl91/luna/releases'

    def __init__(self, plugin, core, logger):
        self.plugin = plugin
        self.core = core
        self.logger = logger
        self.current_version = re.match(self.regexp, xbmcaddon.Addon().getAddonInfo('version')).group()
        self.update_version = None
        self.asset_url = None
        self.asset_name = None
        self.changelog = None

    def check_for_update(self, ignore_checked=False):
        update_storage = self.plugin.get_storage('update', TTL=24*60)
        update = None

        if not update_storage.get('checked') or ignore_checked:
            if self.plugin.get_setting('enable_pre_updates', bool):
                response = json.load(urllib2.urlopen(self.pre_api_url))
            else:
                try:
                    response = json.load(urllib2.urlopen(self.api_url))
                except urllib2.HTTPError, e:
                    if e.code == 404:
                        update = None
                        response = ''
                    else:
                        self.logger.error("An error occurred when trying to get latest release: %s" % e)
                        return None
            if self.plugin.get_setting('enable_pre_updates', bool):
                for release in response:
                    if re.match(self.regexp, release['tag_name'].strip('v')).group() > self.current_version:
                        update = Update()
                        print self.current_version
                        update.current_version = self.current_version
                        update.update_version = re.match(self.regexp, release['tag_name'].strip('v')).group()
                        update.asset_url = release['assets'][0]['browser_download_url']
                        update.asset_name = release['assets'][0]['name']
                        update.changelog = release['body']
                        update.file_path = os.path.join(self.plugin.storage_path, update.asset_name)
            else:
                if re.match(self.regexp, response['tag_name'].strip('v')).group() > self.current_version:
                    update = Update()
                    print self.current_version
                    update.current_version = self.current_version
                    update.update_version = re.match(self.regexp, response['tag_name'].strip('v')).group()
                    update.asset_url = response['assets'][0]['browser_download_url']
                    update.asset_name = response['assets'][0]['name']
                    update.changelog = response['body']
                    update.file_path = os.path.join(self.plugin.storage_path, update.asset_name)

            update_storage['checked'] = True
            update_storage.sync()

            if update is not None:
                xbmcgui.Dialog().notification(
                    self.core.string('name'),
                    self.core.string('update_available') % update.update_version
                )
                return update
            else:
                xbmcgui.Dialog().notification(
                    self.core.string('name'),
                    self.core.string('no_update_available')
                )
                return None

    def initiate_update(self, update):
        if update.asset_name is not None:
            window = UpdateInfo(update, 'Update to Luna %s' % self.update_version)
            window.doModal()
            del window

    def do_update(self, update):
        file_path = update.file_path
        with open(file_path, 'wb') as asset:
            asset.write(urllib2.urlopen(update.asset_url).read())
            asset.close()
        zip_file = zipfile.ZipFile(file_path)
        zip_file.extractall(xbmcaddon.Addon().getAddonInfo('path'), self._get_members(zip_file))

        xbmcgui.Dialog().ok(
            self.core.string('name'),
            'Luna has been updated to version %s and will now relaunch.' % update.update_version
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
