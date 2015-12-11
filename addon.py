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


@plugin.route('/')
def index():
    items = [{
        'label': 'Actions',
        'path': plugin.url_for(
            endpoint='show_actions'
        )
    }, {
        'label': 'Games',
        'path': plugin.url_for(
            endpoint='show_games'
        )
    }, {
        'label': 'Settings',
        'path': plugin.url_for(
            endpoint='open_settings'
        )
    }]
    return plugin.finish(items)


@plugin.route('/settings')
def open_settings():
    plugin.open_settings()


@plugin.route('/actions')
def show_actions():
    items = [{
        'label': 'Create Controller Mapping',
        'path': plugin.url_for(
            endpoint='create_mapping'
        )
    }, {
        'label': 'Pair Current Host',
        'path': plugin.url_for(
            endpoint='pair_host'
        )
    }, {
        'label': 'Force Quit Moonlight',
        'path': plugin.url_for(
            endpoint='quit_moonlight'
        )
    }]
    return plugin.finish(items)


@plugin.route('/actions/create-mapping')
def create_mapping():
    import subprocess
    print 'Starting mapping'
    progressDialog = xbmcgui.DialogProgress()
    progressDialog.create(
        _('name'),
        'Mapping is now starting...'
    )
    percent = 0
    print 'Trying to call subprocess'
    script_path = ''.join([addon_path, '/resources/lib/test.sh'])
    process = subprocess.Popen(['sh', script_path], stdout=subprocess.PIPE)
    while True:
        print 'meow'
        line = process.stdout.readline()
        progressDialog.update(percent, line)
        if not line:
            break
    progressDialog.close()
    print 'Done Mapping'


@plugin.route('/actions/pair-host')
def pair_host():
    ip = '192.168.2.105'
    code = launch_moonlight_pair(ip)
    xbmcgui.Dialog().ok(
        _('name'),
        code
    )


@plugin.route('/actions/quit-moonlight')
def quit_moonlight():
    return


@plugin.route('/games')
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
            )
        ]

    Config.dump_conf()
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


@plugin.route('/games/all/refresh')
def do_full_refresh():
    return get_games()


@plugin.route('/games/launch/<game_id>')
def launch_game(game_id):
    log('Launching game %s' % game_id)


def launch_moonlight_pair(ip):
    return ip + ' 1234'


def get_games():
    return ['Steam']


def get_binary():
    binary_locations = [
        '/usr/bin/moonlight',
        '/usr/local/bin/moonlight'
    ]

    if plugin.get_setting('use_custom_binary', bool):
        binary_locations.append(plugin.get_setting('custom_binary_path', unicode))

    for f in binary_locations:
        if os.path.isfile(f):
            return f

    # return None
    return '/usr/bin/moonlight'


def configure_helper(config, binary_path):
    """

    :param binary_path: string
    :type config: ConfigHelper
    """
    config.configure(
        addon_path,
        binary_path,
        plugin.get_setting('host', unicode),
        plugin.get_setting('enable_custom_res', bool),
        plugin.get_setting('resolution', str),
        plugin.get_setting('framerate', str),
        plugin.get_setting('graphic_optimizations', bool),
        plugin.get_setting('local_audio', bool),
        plugin.get_setting('enable_custom_bitrate', bool),
        plugin.get_setting('enable_custom_input', bool),
        plugin.get_setting('input_map', str),
        plugin.get_setting('input_device', str)
    )

    config.dump_conf()

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
    if plugin.get_setting('host', unicode) and get_binary():
        if configure_helper(Config, get_binary()):
            plugin.run()
    else:
        xbmcgui.Dialog().ok(
            _('name'),
            'Please configure the addon first.'
        )
