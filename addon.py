import os
import subprocess

import resources.lib.core.corefunctions as core

from xbmcswift2 import Plugin, xbmcgui, xbmcaddon

from resources.lib.model.game import Game
from resources.lib.moonlighthelper import MoonlightHelper

from resources.lib.confighelper import ConfigHelper
from resources.lib.scraperchain import ScraperChain


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
    core.Logger.info('Starting mapping')

    controllers = ['XBOX', 'PS3', 'Wii']
    ctrl_type = xbmcgui.Dialog().select(core.string('choose_ctrl_type'), controllers)
    map_name = xbmcgui.Dialog().input(core.string('enter_filename'))

    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(
            core.string('name'),
            core.string('starting_mapping')
    )

    core.Logger.info('Trying to call subprocess')
    map_file = '%s/%s-%s.map' % (os.path.expanduser('~'), controllers[ctrl_type], map_name)

    success = MLHelper.create_ctrl_map(progress_dialog, map_file)

    if success:
        confirmed = xbmcgui.Dialog().yesno(
                core.string('name'),
                core.string('mapping_success'),
                core.string('set_mapping_active')
        )

        core.Logger.info('Dialog Yes No Value: %s' % confirmed)

        if confirmed:
            plugin.set_setting('input_map', map_file)

    else:
        xbmcgui.Dialog().ok(
                core.string('name'),
                core.string('mapping_failure')
        )


@plugin.route('/actions/pair-host')
def pair_host():
    pair_dialog = xbmcgui.DialogProgress()
    pair_dialog.create(
            core.string('name'),
            'Starting Pairing'
    )

    success = MLHelper.pair_host(pair_dialog)

    if success:
        xbmcgui.Dialog().ok(
                core.string('name'),
                'Successfully paired'
        )
    else:
        confirmed = xbmcgui.Dialog().yesno(
                core.string('name'),
                'Pairing failed - do you want to try again?'
        )
        if confirmed:
            pair_host()


@plugin.route('/actions/reset-cache')
def reset_cache():
    confirmed = xbmcgui.Dialog().yesno(
            core.string('name'),
            core.string('reset_cache_warning')
    )

    if confirmed:
        ScraperChain().reset_cache()
    else:
        return


@plugin.route('/games')
def show_games():
    # TODO: This should be handled by some kind of game controller
    def context_menu():
        return [
            (
                core.string('addon_settings'),
                'XBMC.RunPlugin(%s)' % plugin.url_for(
                        endpoint='open_settings'
                )
            ),
            (
                core.string('full_refresh'),
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
    core.Logger.info('Launching game %s' % game_id)
    MLHelper.launch_game(game_id)


def get_games():
    # TODO: This is an interaction between MLHelper and some kind of game controller
    game_list = []
    Config.configure()
    list_proc = subprocess.Popen([Config.get_binary(), 'list', Config.get_host()], stdout=subprocess.PIPE)

    while True:
        line = list_proc.stdout.readline()
        if line[3:] != '':
            core.Logger.info(line[3:])
            game_list.append(line[3:].strip())
        if not line:
            break

    core.Logger.info('Done getting games from moonlight')

    game_storage = plugin.get_storage('game_storage')
    cache = game_storage.raw_dict()
    game_storage.clear()

    for game_name in game_list:

        if plugin.get_setting('disable_scraper', bool):
            core.Logger.info('Scraper have been disabled, just adding game names to list.')
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
                    core.Logger.info('Key Error thrown while getting information for game {0}: {1}'.format(game_name,
                                                                                              KeyError.message))
                    game_storage[game_name] = Game(game_name, None)

    game_storage.sync()


if __name__ == '__main__':
    core.Logger.info('Launching Luna')
    core.check_script_permissions()
    if plugin.get_setting('host', unicode):
        Config.configure()
        plugin.run()
    else:
        xbmcgui.Dialog().ok(
                core.string('name'),
                core.string('configure_first')
        )
