import os
import shutil
import stat
import subprocess
import threading

from xbmcswift2 import Plugin, xbmcgui, xbmc, xbmcaddon

from resources.lib.confighelper import ConfigHelper
from resources.lib.scraper import ScraperCollection
from resources.lib.game import Game

STRINGS = {
    'name': 30000,
    'addon_settings': 30100,
    'full_refresh': 30101,
    'choose_ctrl_type': 30200,
    'enter_filename': 30201,
    'starting_mapping': 30202,
    'mapping_success': 30203,
    'set_mapping_active': 30204,
    'mapping_failure': 30205,
    'pair_failure_paired': 30206,
    'configure_first': 30207
}

plugin = Plugin()
Config = ConfigHelper()

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
    plugin.open_settings()


@plugin.route('/actions/create-mapping')
def create_mapping():
    log('Starting mapping')

    controllers = ['XBOX', 'PS3', 'Wii']
    ctrl_type = xbmcgui.Dialog().select(_('choose_ctrl_type'), controllers)
    map_name = xbmcgui.Dialog().input(_('enter_filename'))

    if map_name == '':
        return

    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(
            _('name'),
            _('starting_mapping')
    )

    log('Trying to call subprocess')
    map_file = '%s/%s-%s.map' % (os.path.expanduser('~'), controllers[ctrl_type], map_name)

    mapping = subprocess.Popen(['stdbuf', '-oL', Config.get_binary(), 'map', map_file, '-input',
                                plugin.get_setting('input_device', unicode)], stdout=subprocess.PIPE)

    lines_iterator = iter(mapping.stdout.readline, b"")

    thread = threading.Thread(target=loop_lines, args=(progress_dialog, lines_iterator))
    thread.start()

    success = 'false'

    while True:
        xbmc.sleep(1000)
        if not thread.isAlive():
            progress_dialog.close()
            success = 'true'
            log('Done, created mapping file in: %s' % map_file)
            break
        if progress_dialog.iscanceled():
            mapping.kill()
            progress_dialog.close()
            success = 'canceled'
            log('Mapping canceled')
            break

    if os.path.isfile(map_file) and success == 'true':
        confirmed = xbmcgui.Dialog().yesno(
                _('name'),
                _('mapping_success'),
                _('set_mapping_active')
        )
        log('Dialog Yes No Value: %s' % confirmed)
        if confirmed:
            plugin.set_setting('input_map', map_file)
            return
        else:
            return

    else:
        if success == 'false':
            xbmcgui.Dialog().ok(
                    _('name'),
                    _('mapping_failure')
            )
        else:
            return


@plugin.route('/actions/pair-host')
def pair_host():
    pair_dialog = xbmcgui.DialogProgress()
    pair_dialog.create(
            _('name'),
            'Starting Pairing'
    )

    pairing = subprocess.Popen(['stdbuf', '-oL', Config.get_binary(), 'pair', Config.get_host()],
                               stdout=subprocess.PIPE)

    lines_iterator = iter(pairing.stdout.readline, b"")

    thread = threading.Thread(target=loop_lines, args=(pair_dialog, lines_iterator))
    thread.start()

    success = False

    while True:
        xbmc.sleep(1000)
        if not thread.isAlive():
            success = True
            break
        if pair_dialog.iscanceled():
            pairing.kill()
            pair_dialog.close()
            success = False
            log('Pairing canceled')
            break

    if success:
        pair_dialog.update(0, 'Checking if pairing has been successful.')
        xbmc.sleep(1000)
        pairing_check = subprocess.Popen([Config.get_binary(), 'list', Config.get_host()],
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        last_line = ''
        while True:
            line = pairing_check.stdout.readline()
            err = pairing_check.stderr.readline()
            if line != '':
                last_line = line
            if err != '':
                last_line = err
            if not line and not err:
                break

        pair_dialog.close()
        if last_line.lower().strip() != 'You must pair with the PC first'.lower().strip():
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
            else:
                return
    else:
        return


@plugin.route('/actions/reset-cache')
def reset_cache():
    confirmed = xbmcgui.Dialog().yesno(
            _('name'),
            'This will remove all cached game information and clear the game storage. Next time you\'re going to ' +
            'visit the game view it will take some time until all information is available again. ' +
            'Are you sure you want to do this?'
    )
    if confirmed:
        plugin.get_storage('game_storage').clear()
        if os.path.exists(addon_path + '/boxarts'):
            shutil.rmtree(addon_path + '/boxarts', ignore_errors=True)
            log('Deleted boxarts folder on user request')
        if os.path.exists(addon_path + '/api_cache'):
            shutil.rmtree(addon_path + '/api_cache', ignore_errors=True)
            log('Deleted api cache on user request')
        xbmcgui.Dialog().ok(
                _('name'),
                'Deleted cache.'
        )
    else:
        return


@plugin.route('/games')
def show_games():
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

    games = plugin.get_storage('game_storage')

    if len(games.raw_dict()) == 0:
        get_games()

    items = []
    for i, game_name in enumerate(games):
        game = games.get(game_name)
        items.append({
            'label': game.name,
            'icon': game.thumb,
            'thumbnail': game.thumb,
            'info': {
                'originaltitle': game.name,
                'year': game.year,
                'plot': game.plot,
                'genre': game.genre,
            },
            'replace_context_menu': True,
            'context_menu': context_menu(),
            'path': plugin.url_for(
                    endpoint='launch_game',
                    game_id=game.name
            )
        })
    return plugin.finish(items)


@plugin.route('/games/all/refresh')
def do_full_refresh():
    get_games()


@plugin.route('/games/launch/<game_id>')
def launch_game(game_id):
    log('Launching game %s' % game_id)
    configure_helper(Config, Config.get_binary())
    log('Reconfigured helper and dumped conf to disk.')
    subprocess.call([addon_internal_path + '/resources/lib/launch-helper-osmc.sh',
                     addon_internal_path + '/resources/lib/launch.sh',
                     addon_internal_path + '/resources/lib/moonlight-heartbeat.sh',
                     game_id,
                     Config.get_config_path()])


def loop_lines(dialog, iterator):
    for line in iterator:
        log(line)
        dialog.update(0, line)


def get_games():
    game_list = []
    configure_helper(Config, Config.get_binary())
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

    scraper = ScraperCollection(addon_path)

    for game_name in game_list:
        if plugin.get_setting('disable_scraper', bool):
            log('Scraper have been disabled, just adding game names to list.')
            game_storage[game_name] = Game(game_name, None)
        else:
            if cache.has_key(game_name):
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


def get_binary():
    binary_locations = [
        '/usr/bin/moonlight',
        '/usr/local/bin/moonlight'
    ]

    for f in binary_locations:
        if os.path.isfile(f):
            return f

    return None


def configure_helper(config, binary_path):
    """

    :param config: ConfigHelper
    :param binary_path: string
    """
    config.configure(
            addon_path,
            binary_path,
            plugin.get_setting('host', unicode),
            plugin.get_setting('enable_custom_resolution', bool),
            plugin.get_setting('resolution_width', str),
            plugin.get_setting('resolution_height', str),
            plugin.get_setting('resolution', str),
            plugin.get_setting('framerate', str),
            plugin.get_setting('graphic_optimizations', bool),
            plugin.get_setting('remote_optimizations', bool),
            plugin.get_setting('local_audio', bool),
            plugin.get_setting('enable_custom_bitrate', bool),
            plugin.get_setting('bitrate', int),
            plugin.get_setting('packetsize', int),
            plugin.get_setting('enable_custom_input', bool),
            plugin.get_setting('input_map', str),
            plugin.get_setting('input_device', str),
            plugin.get_setting('override_default_resolution', bool)
    )

    config.dump_conf()

    return True


def check_script_permissions():
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
    plugin.log.info(text)


def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id]).encode('utf-8')
    else:
        log('String is missing: %s' % string_id)
        return string_id


if __name__ == '__main__':
    log('Launching Luna')
    check_script_permissions()
    if plugin.get_setting('host', unicode) and get_binary():
        if configure_helper(Config, get_binary()):
            plugin.run()
    else:
        xbmcgui.Dialog().ok(
                _('name'),
                _('configure_first')
        )
