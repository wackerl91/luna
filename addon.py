import os
import sys
import resources.lib.config.bootstrap as bootstrapper

from xbmcswift2 import xbmc, xbmcaddon, xbmcgui, Plugin

import xbmcplugin
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.views.gameinfo import GameInfo

# plugin = bootstrapper.bootstrap()

addon = xbmcaddon.Addon()
addon_path = xbmc.translatePath(
            'special://profile/addon_data/%s/.storage/' % addon.getAddonInfo('id'))
addon_internal_path = addon.getAddonInfo('path')


def handle_request(path):
    if os.path.basename(path) == '':
        index()
    elif os.path.basename(path) == 'open_settings':
        open_settings()


def as_tuple(path, item):
    return path, item


def index():
    items = [
        {
            'label': 'Games',
            'thumbnail': addon_internal_path + '/resources/icons/controller.png',
            'path': 'plugin://script.luna/show_games'
        }, {
            'label': 'Settings',
            'thumbnail': addon_internal_path + '/resources/icons/cog.png',
            'path': 'plugin://script.luna/open_settings'
        }
    ]

    list_items = [
        ('plugin://script.luna/show_games',
         xbmcgui.ListItem(
                 label='Games',
                 thumbnailImage=addon_internal_path + '/resources/icons/controller.png',
                 path='plugin://script.luna/show_games'
         )
         ),
        ('plugin://script.luna/open_settings',
         xbmcgui.ListItem(
                 label='Settings',
                 thumbnailImage=addon_internal_path + '/resources/icons/cog.png',
                 path='plugin://script.luna/open_settings'
         )
         )
    ]

    print int(sys.argv[1])
    xbmcplugin.addDirectoryItems(int(sys.argv[1]), list_items)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    # return plugin.finish(items)


def open_settings():
    addon.openSettings()
    core_monitor = RequiredFeature('core-monitor').request()
    core_monitor.onSettingsChanged()
    del core_monitor


def create_mapping():
    config_controller = RequiredFeature('config-controller').request()
    config_controller.create_controller_mapping()
    del config_controller


def pair_host():
    config_controller = RequiredFeature('config-controller').request()
    config_controller.pair_host()
    del config_controller


def reset_cache():
    core = RequiredFeature('core').request()
    confirmed = xbmcgui.Dialog().yesno(
            core.string('name'),
            core.string('reset_cache_warning')
    )

    if confirmed:
        scraper_chain = RequiredFeature('scraper-chain').request()
        scraper_chain.reset_cache()
        del scraper_chain

    del core


def show_games():
    game_controller = RequiredFeature('game-controller').request()
    plugin.set_content('movies')
    return plugin.finish(game_controller.get_games_as_list(), sort_methods=['label'])


def do_full_refresh():
    game_controller = RequiredFeature('game-controller').request()
    game_controller.get_games()
    del game_controller


def show_game_info(game_id):
    core = RequiredFeature('core').request()
    game = core.get_storage().get(game_id)
    cache_fanart = game.get_selected_fanart()
    cache_poster = game.get_selected_poster()
    window = GameInfo(game, game.name)
    window.doModal()
    del window
    if cache_fanart != game.get_selected_fanart() or cache_poster != game.get_selected_poster():
        xbmc.executebuiltin('Container.Refresh')
    del core
    del game


def launch_game(game_id):
    core = RequiredFeature('core').request()
    game_controller = RequiredFeature('game-controller').request()
    core.logger.info('Launching game %s' % game_id)
    game_controller.launch_game(game_id)
    del core
    del game_controller


if __name__ == '__main__':
    # core = RequiredFeature('core').request()
    # game_controller = RequiredFeature('game-controller').request()
    # config_controller = RequiredFeature('config-controller').request()
    # updater = RequiredFeature('update-service').request()
    # core.check_script_permissions()
    # updater.check_for_update()
    print '------ Sys Argv Content ---------'
    print sys.argv
    print '------ Sys Argv Content End---------'

    plugin = bootstrapper.bootstrap()
    if addon.getSetting('host'):
        # config_helper = RequiredFeature('config-helper').request()
        # config_helper.configure()
        handle_request(sys.argv[0])
        del plugin
        # plugin.run()
    else:
        core = RequiredFeature('core').request()
        xbmcgui.Dialog().ok(
                core.string('name'),
                core.string('configure_first')
        )
        del core
