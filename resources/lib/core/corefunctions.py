import os
import stat

from xbmcswift2 import Plugin, xbmcaddon

from resources.lib.moonlighthelper import MoonlightHelper

from resources.lib.confighelper import ConfigHelper

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
    'reset_cache_warning': 30208
}

plugin = Plugin('script.luna')
internal_path = xbmcaddon.Addon().getAddonInfo('path')

Config = ConfigHelper()
MLHelper = MoonlightHelper(Config)


def string(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id]).encode('utf-8')
    else:
        return string_id


def check_script_permissions():
    st = os.stat(internal_path + '/resources/lib/launch.sh')
    if not bool(st.st_mode & stat.S_IXUSR):
        os.chmod(internal_path + '/resources/lib/launch.sh', st.st_mode | 0111)
        Logger.info('Changed file permissions for launch')

    st = os.stat(internal_path + '/resources/lib/launch-helper-osmc.sh')
    if not bool(st.st_mode & stat.S_IXUSR):
        os.chmod(internal_path + '/resources/lib/launch-helper-osmc.sh', st.st_mode | 0111)
        Logger.info('Changed file permissions for launch-helper-osmc')

    st = os.stat(internal_path + '/resources/lib/moonlight-heartbeat.sh')
    if not bool(st.st_mode & stat.S_IXUSR):
        os.chmod(internal_path + '/resources/lib/moonlight-heartbeat.sh', st.st_mode | 0111)
        Logger.info('Changed file permissions for moonlight-heartbeat')


def get_storage():
    return plugin.get_storage('game_storage')


def get_moonlight():
    return MLHelper


def get_plugin():
    return plugin


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def info(text):
        plugin.log.info(text)

    @staticmethod
    def debug(text):
        plugin.log.debug(text)

    @staticmethod
    def error(text):
        plugin.log.error(text)
