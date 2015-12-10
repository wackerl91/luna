import os

from xbmcswift2 import Plugin, xbmcgui, xbmc, xbmcaddon
from resources.lib.helper import ConfigHelper

addon = xbmcaddon.Addon()
addon_path = xbmcaddon.Addon.getAddonInfo(addon, 'path')

STRINGS = {
    'name': 30000,
    'addon_settings': 30100,
    'full_refresh': 30101
}

Config = ConfigHelper()

plugin = Plugin()
script = Script()


@plugin.route('/')
def show_games():
    def context_menu():
        return [
            (
                _('open_settings'),
                'XBMC.RunPlugin(%s)' % plugin.url_for(
                    endpoint='open_settings'
                )
            ),
            (
                _('full_refresh'),
                'XBMC.RunPlugin(%s)' % plugin.url_for(
                    endpoint='do_full_refresh'
                )
            ),
            (
                _('pair_host'),
                'XBMC.RunPlugin(%s)' % plugin.url_for(
                    endpoint='pair_host'
                )
            )
        ]

    print 'show_games'
    if check_binary():
        if Config.check_for_config_file() or plugin.get_setting('host_ip', unicode):
            Config.set_host_ip(plugin.get_setting('host_ip', str))
            Config.set_binary_path(check_binary())
            releases = plugin.get_storage('releases')
            releases.clear()
            games = get_games()
            items = []
            for i, game in enumerate(games):
                label = game
                items.append({
                    'label': label,
                    'replace_context_menu': True,
                    'context_menu': context_menu(),
                    'path': plugin.url_for(
                        endpoint='launch_game',
                        game_id=game
                    )
                })
            releases.sync()
            return plugin.finish(items)
        else:
            confirmed = xbmcgui.Dialog().yesno(
                _('name'),
                'No config file found.',
                'Do you want to open settings now?'
            )
            if confirmed:
                plugin.open_settings()
            else:
                exit()
    else:
        xbmcgui.Dialog().ok(
            _('name'),
            'Moonlight binary not found',
            'Please configure the addon first.'
        )


@plugin.route('/settings')
def open_settings():
    plugin.open_settings()


@plugin.route('/games/all/refresh')
def do_full_refresh():
    return get_games()


@plugin.route('/games/launch/<game_id>')
def launch_game(game_id):
    log('Launching game %s' % game_id)


@plugin.route('/host/pair')
def pair_host():
    ip = '192.168.2.105'
    code = launch_moonlight_pair(ip)
    xbmcgui.Dialog().ok(
        _('name'),
        code
    )


def launch_moonlight_pair(ip):
    return ip + ' 1234'


def get_games():
    return ['Steam']


def check_binary():
    print 'check binary'
    binary = ''
    binary_locations = [
        '/usr/bin/moonlight',
        '/usr/local/bin/moonlight'
    ]

    if plugin.get_setting('use_custom_binary', bool):
        binary_locations.append(plugin.get_setting('custom_binary_path', unicode))

    for f in binary_locations:
        if os.path.isfile(f):
            binary = f
            break

    # return os.path.isfile(binary)
    print 'check binary done'
    return '/usr/bin/moonlight'


def configure_helper(config):
    """

    :type config: ConfigHelper
    """
    print 'get_config_helper'
    config.configure(
        file_path=addon_path,
    )
    print 'get_config_helper done'
    return True


def log(text):
    plugin.log.info(text)


def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id]).encode('utf-8')
    else:
        log('String is missing: %s' % string_id)
        return string_id


if __name__ == '__main__':
    log('Launching Luna')
    if configure_helper(Config):
        plugin.run()
