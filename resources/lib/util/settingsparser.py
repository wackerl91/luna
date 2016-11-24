import hashlib
import os

import xml.etree.ElementTree as ET

from resources.lib.model.settings.category import Category
from resources.lib.model.settings.setting import Setting


class SettingsParser(object):
    def __init__(self, addon, logger):
        self.settings_path = os.path.join(addon.getAddonInfo('path'), 'resources', 'settings.xml')
        self.addon = addon
        self.logger = logger
        self.settings_tree = None
        self.settings_hash = None
        self._reload_settings()
        self.settings_hash = self._get_settings_hash()
        self.settings_dict = {}

    def _get_settings_hash(self):
        settings_file = open(self.settings_path, 'rb')
        hasher = hashlib.sha256()
        blocksize = 65536
        buf = settings_file.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = settings_file.read(blocksize)
        return hasher.hexdigest()

    def _reload_settings(self):
        if self._get_settings_hash() != self.settings_hash:
            etree = ET.ElementTree(file=self.settings_path)
            self.settings_tree = etree.getroot()

    def get_settings(self):
        if self.settings_hash == self._get_settings_hash() and len(self.settings_dict) > 0:
            self.update_values()
            return self.settings_dict
        else:
            self._reload_settings()

            cat_prio = 1

            for category in self.settings_tree.findall('category'):
                cat_label_id = category.get('label')
                cat_label = self.addon.getLocalizedString(int(cat_label_id))
                cat = Category(cat_label_id, cat_label, cat_prio)
                cat_prio += 1

                setting_prio = 1
                for setting in category.findall('setting'):
                    if setting.get('label') is not None:
                        setting_label_id = setting.get('label')
                        setting_id = setting.get('id')
                        setting_label = self.addon.getLocalizedString(int(setting_label_id))

                        setting_args = {}
                        for item in setting.items():
                            setting_args[item[0]] = item[1]

                        current_value = self.addon.getSetting(setting_id)
                        setting_args['current_value'] = current_value

                        _setting = Setting(setting_id, setting_label, setting_prio, **setting_args)

                        setting_prio += 1
                        cat.settings[setting_id] = _setting
                        self.logger.info("Setting added: %s -> %s" % (cat_label, setting_label))

                self.settings_dict[cat_label] = cat
                self.logger.info("Category added: %s" % cat_label)

            return self.settings_dict

    def update_values(self):
        for key, category in self.settings_dict.iteritems():
            for setting_key, setting in category.settings.iteritems():
                setting.current_value = self.addon.getSetting(setting.setting_id)
