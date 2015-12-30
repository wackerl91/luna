import xbmc
import xbmcgui

from xbmcswift2 import Plugin, xbmcaddon

from resources.lib.controller.configcontroller import ConfigController
from resources.lib.controller.gamecontroller import GameController
from resources.lib.plugincontainer import PluginContainer

from resources.lib.views.gameinfo import GameInfo

plugin = Plugin()
container = PluginContainer(plugin)
core = container.get_core()

game_controller = GameController(container)
config_controller = ConfigController(container)

addon_path = plugin.storage_path
addon_internal_path = xbmcaddon.Addon().getAddonInfo('path')


@plugin.route('/')
def index():
    items = [
        {
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
        }
    ]

    return plugin.finish(items)


@plugin.route('/settings')
def open_settings():
    # TODO: Check if there's a listener for closed settings. Use a file watcher if there's none?
    plugin.open_settings()


@plugin.route('/actions/create-mapping')
def create_mapping():
    config_controller.create_controller_mapping()


@plugin.route('/actions/pair-host')
def pair_host():
    config_controller.pair_host()


@plugin.route('/actions/reset-cache')
def reset_cache():
    confirmed = xbmcgui.Dialog().yesno(
            core.string('name'),
            core.string('reset_cache_warning')
    )

    if confirmed:
        container.get_scraper_chain().reset_cache()
    else:
        return


@plugin.route('/games')
def show_games():
    plugin.set_content('movies')
    return plugin.finish(game_controller.get_games_as_list(), sort_methods=['label'])


@plugin.route('/games/refresh')
def do_full_refresh():
    game_controller.get_games()


@plugin.route('/games/info/<game_id>')
def show_game_info(game_id):
    game = core.get_storage().get(game_id)
    window = GameInfo(container, game, game.name)
    window.doModal()
    del window
    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/games/launch/<game_id>')
def launch_game(game_id):
    core.logger.info('Launching game %s' % game_id)
    # TODO: Routing shouldn't know about the existence of the moonlight helper; should be handled by game controller
    container.get_moonlight_helper().launch_game(game_id)


if __name__ == '__main__':
    core.logger.info('Launching Luna')
    core.check_script_permissions()
    if plugin.get_setting('host', unicode):
        container.get_config_helper().configure()
        plugin.run()
    else:
        xbmcgui.Dialog().ok(
                core.string('name'),
                core.string('configure_first')
        )
