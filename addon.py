import os
import shutil
import stat
import subprocess
import threading

from xbmcswift2 import Plugin, xbmcgui, xbmc, xbmcaddon

from resources.lib.model.game import Game
from resources.lib.moonlighthelper import MoonlightHelper

from resources.lib.confighelper import ConfigHelper
from resources.lib.scraperchain import ScraperChain

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

plugin = Plugin()
Config = ConfigHelper()
MLHelper = MoonlightHelper(Config)

addon_path = plugin.storage_path
addon_internal_path = xbmcaddon.Addon().getAddonInfo('path')


@plugin.route('/')
def index():
    items = [{
        'label': 'Games',
        'thumbnail': addon_internal_path + '/resources/icons/controller.png',
        'path': plugin.url_for(
                endpoint='show_games'
        )
    }, {
        'label': 'Settings',
        'thumbnail': addon_internal_path + '/resources/icons/cog.png',
        'path': plugin.url_for(
                endpoint='open_settings'
        )
    }]

    return plugin.finish(items)


@plugin.route('/settings')
def open_settings():
    # TODO: Check if there's a listener for closed settings. Use a file watcher if there's none?
    plugin.open_settings()


@plugin.route('/actions/create-mapping')
def create_mapping():
    log('Starting mapping')

    controllers = ['XBOX', 'PS3', 'Wii']
    ctrl_type = xbmcgui.Dialog().select(_('choose_ctrl_type'), controllers)
    map_name = xbmcgui.Dialog().input(_('enter_filename'))

    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(
            _('name'),
            _('starting_mapping')
    )

    log('Trying to call subprocess')
    map_file = '%s/%s-%s.map' % (os.path.expanduser('~'), controllers[ctrl_type], map_name)

    success = MLHelper.create_ctrl_map(progress_dialog, map_file)

    if success:
        confirmed = xbmcgui.Dialog().yesno(
                _('name'),
                _('mapping_success'),
                _('set_mapping_active')
        )

        log('Dialog Yes No Value: %s' % confirmed)

        if confirmed:
            plugin.set_setting('input_map', map_file)

    else:
        xbmcgui.Dialog().ok(
                _('name'),
                _('mapping_failure')
        )


@plugin.route('/actions/pair-host')
def pair_host():
    pair_dialog = xbmcgui.DialogProgress()
    pair_dialog.create(
            _('name'),
            'Starting Pairing'
    )

    success = MLHelper.pair_host(pair_dialog)

    if success:
        xbmcgui.Dialog().ok(
                _('name'),
                'Successfully paired'
        )
    else:
        confirmed = xbmcgui.Dialog().yesno(
                _('name'),
                'Pairing failed - do you want to try again?'
        )
        if confirmed:
            pair_host()


@plugin.route('/actions/reset-cache')
def reset_cache():
    confirmed = xbmcgui.Dialog().yesno(
            _('name'),
            _('reset_cache_warning')
    )
    # TODO: ScraperChain should be aware of this
    if confirmed:
        plugin.get_storage('game_storage').clear()
        if os.path.exists(addon_path + '/boxarts'):
            shutil.rmtree(addon_path + '/boxarts', ignore_errors=True)
            log('Deleted boxarts folder on user request')
        if os.path.exists(addon_path + '/api_cache'):
            shutil.rmtree(addon_path + '/api_cache', ignore_errors=True)
            log('Deleted api cache on user request')
        if os.path.exists(addon_path + 'art'):
            shutil.rmtree(addon_path + 'art', ignore_errors=True)
            log('Deleted new art folder on user request.')
        xbmcgui.Dialog().ok(
                _('name'),
                'Deleted cache.'
        )
    else:
        return


@plugin.route('/games')
def show_games():
    # TODO: This should be handled by some kind of game controller
    def context_menu():
        return [
            (
                _('addon_settings'),
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

    plugin.set_content('movies')
    games = plugin.get_storage('game_storage')

    if len(games.raw_dict()) == 0:
        get_games()

    items = []
    for i, game_name in enumerate(games):
        game = games.get(game_name)
        items.append({
            'label':     game.name,
            'icon':      game.thumb,
            'thumbnail': game.thumb,
            'info': {
                'year':  game.year,
                'plot':  game.plot,
                'genre': game.genre,
                'originaltitle': game.name,
            },
            'replace_context_menu': True,
            'context_menu': context_menu(),
            'path': plugin.url_for(
                    endpoint='launch_game',
                    game_id=game.name
            ),
            'properties': {
                'fanart_image': game.fanarts[0]
            }
        })

    return plugin.finish(items, sort_methods=['label'])


@plugin.route('/games/all/refresh')
def do_full_refresh():
    get_games()


@plugin.route('/games/launch/<game_id>')
def launch_game(game_id):
    # TODO: MLHelper
    log('Launching game %s' % game_id)
    Config.configure()
    log('Reconfigured helper and dumped conf to disk.')
    subprocess.call([addon_internal_path + '/resources/lib/launch-helper-osmc.sh',
                     addon_internal_path + '/resources/lib/launch.sh',
                     addon_internal_path + '/resources/lib/moonlight-heartbeat.sh',
                     game_id,
                     Config.get_config_path()])


def get_games():
    # TODO: This is an interaction between MLHelper and some kind of game controller
    game_list = []
    Config.configure()
    list_proc = subprocess.Popen([Config.get_binary(), 'list', Config.get_host()], stdout=subprocess.PIPE)

    while True:
        line = list_proc.stdout.readline()
        if line[3:] != '':
            log(line[3:])
            game_list.append(line[3:].strip())
        if not line:
            break

    log('Done getting games from moonlight')

    game_storage = plugin.get_storage('game_storage')
    cache = game_storage.raw_dict()
    game_storage.clear()

    for game_name in game_list:

        if plugin.get_setting('disable_scraper', bool):
            log('Scraper have been disabled, just adding game names to list.')
            game_storage[game_name] = Game(game_name, None)

        else:
            scraper = ScraperChain()

            if game_name in cache:
                if not game_storage.get(game_name):
                    game_storage[game_name] = cache.get(game_name)
            else:
                try:
                    game_storage[game_name] = scraper.query_game_information(game_name)
                except KeyError:
                    log('Key Error thrown while getting information for game {0}: {1}'.format(game_name,
                                                                                              KeyError.message))
                    game_storage[game_name] = Game(game_name, None)

    game_storage.sync()


def check_script_permissions():
    # TODO: Core functionality (static)
    st = os.stat(addon_internal_path + '/resources/lib/launch.sh')
    if not bool(st.st_mode & stat.S_IXUSR):
        os.chmod(addon_internal_path + '/resources/lib/launch.sh', st.st_mode | 0111)
        log('Changed file permissions for launch')

    st = os.stat(addon_internal_path + '/resources/lib/launch-helper-osmc.sh')
    if not bool(st.st_mode & stat.S_IXUSR):
        os.chmod(addon_internal_path + '/resources/lib/launch-helper-osmc.sh', st.st_mode | 0111)
        log('Changed file permissions for launch-helper-osmc')

    st = os.stat(addon_internal_path + '/resources/lib/moonlight-heartbeat.sh')
    if not bool(st.st_mode & stat.S_IXUSR):
        os.chmod(addon_internal_path + '/resources/lib/moonlight-heartbeat.sh', st.st_mode | 0111)
        log('Changed file permissions for moonlight-heartbeat')


def log(text):
    # TODO: Core functionality (static)
    plugin.log.info(text)


def _(string_id):
    # TODO: Core functionality (static)
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id]).encode('utf-8')
    else:
        log('String is missing: %s' % string_id)
        return string_id


if __name__ == '__main__':
    log('Launching Luna')
    check_script_permissions()
    if plugin.get_setting('host', unicode):
        Config.configure()
        plugin.run()
    else:
        xbmcgui.Dialog().ok(
                _('name'),
                _('configure_first')
        )
