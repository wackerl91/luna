import resources.lib.config.bootstrap as bootstrapper

from xbmcswift2 import xbmc, xbmcgui

from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.model.game import Game
from resources.lib.views.gameinfo import GameInfo

plugin = bootstrapper.bootstrap()

addon_path = plugin.storage_path
addon_internal_path = plugin.addon.getAddonInfo('path')


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
        }, {
            'label': 'Check For Update',
            'thumbnail': addon_internal_path + '/resources/icons/update.png',
            'path': plugin.url_for(
                        endpoint='check_update'
                    )
        }
    ]

    return plugin.finish(items)


@plugin.route('/settings')
def open_settings():
    plugin.open_settings()
    core_monitor = RequiredFeature('core-monitor').request()
    core_monitor.onSettingsChanged()
    del core_monitor


@plugin.route('/update')
def check_update():
    updater = RequiredFeature('update-service').request()
    if updater.check_for_update(True):
        updater.initiate_update()


@plugin.route('/actions/create-mapping')
def create_mapping():
    config_controller = RequiredFeature('config-controller').request()
    config_controller.create_controller_mapping()
    del config_controller


@plugin.route('/actions/pair-host')
def pair_host():
    config_controller = RequiredFeature('config-controller').request()
    config_controller.pair_host()
    del config_controller


@plugin.route('/actions/reset-cache')
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


@plugin.route('/games')
def show_games():
    game_controller = RequiredFeature('game-controller').request()
    plugin.set_content('movies')
    return plugin.finish(game_controller.get_games_as_list(), sort_methods=['label'])


@plugin.route('/games/refresh')
def do_full_refresh():
    game_controller = RequiredFeature('game-controller').request()
    game_controller.get_games()
    del game_controller


@plugin.route('/games/info/<game_id>')
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


@plugin.route('/games/launch/<game_id>')
def launch_game(game_id):
    core = RequiredFeature('core').request()
    game_controller = RequiredFeature('game-controller').request()
    core.logger.info('Launching game %s' % game_id)
    game_controller.launch_game(game_id)
    del core
    del game_controller


if __name__ == '__main__':
    core = RequiredFeature('core').request()
    updater = RequiredFeature('update-service').request()
    core.check_script_permissions()
    updater.check_for_update()
    del updater

    if plugin.get_setting('host', str):
        config_helper = RequiredFeature('config-helper').request()
        config_helper.configure()

        game_refresh_required = False

        try:
            if plugin.get_storage('game_version')['version'] != Game.version:
                game_refresh_required = True
        except KeyError:
            game_refresh_required = True

        if game_refresh_required:
            game_controller = RequiredFeature('game-controller').request()
            game_controller.get_games()

        plugin.run()
        del plugin
        del core
    else:
        core = RequiredFeature('core').request()
        xbmcgui.Dialog().ok(
                core.string('name'),
                core.string('configure_first')
        )
        del core
