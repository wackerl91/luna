from resources.lib.di.requiredfeature import RequiredFeature

plugin = RequiredFeature('plugin').request()

addon_path = plugin.storage_path
addon_internal_path = plugin.addon.getAddonInfo('path')


@plugin.route('/')
def index():
    default_fanart_path = addon_internal_path + '/fanart.jpg'

    items = [
        {
            'label': 'Games',
            'thumbnail': addon_internal_path + '/resources/icons/controller.png',
            'properties': {
                    'fanart_image': default_fanart_path
            },
            'path': plugin.url_for(
                        endpoint='show_games'
                    )
        }, {
            'label': 'Settings',
            'thumbnail': addon_internal_path + '/resources/icons/cog.png',
            'properties': {
                    'fanart_image': default_fanart_path
            },
            'path': plugin.url_for(
                        endpoint='open_settings'
                    )
        }, {
            'label': 'Check For Update',
            'thumbnail': addon_internal_path + '/resources/icons/update.png',
            'properties': {
                    'fanart_image': default_fanart_path
            },
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


@plugin.route('/settings/select-input')
def select_input_devices():
    from resources.lib.views.selectinput import SelectInput
    window = SelectInput('Select Input Devices')
    window.doModal()
    del window


@plugin.route('/settings/select-audio')
def select_audio_device():
    audio_controller = RequiredFeature('audio-controller').request()
    audio_controller.select_audio_device()


@plugin.route('/update')
def check_update():
    updater = RequiredFeature('update-service').request()
    update = updater.check_for_update(True)
    if update is not None:
        updater.initiate_update(update)


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
    import xbmcgui
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


@plugin.route('/actions/patch-osmc')
def patch_osmc_skin():
    skinpatcher = RequiredFeature('skin-patcher').request()
    skinpatcher.patch()
    del skinpatcher
    import xbmc
    xbmc.executebuiltin('ReloadSkin')


@plugin.route('/actions/rollback-osmc')
def rollback_osmc_skin():
    import xbmc
    skinpatcher = RequiredFeature('skin-patcher').request()
    skinpatcher.rollback()
    del skinpatcher
    xbmc.executebuiltin('ReloadSkin')


@plugin.route('/games')
def show_games():
    game_controller = RequiredFeature('game-controller').request()
    plugin.set_content('movies')
    return plugin.finish(game_controller.get_games_as_list(), sort_methods=['label'])


@plugin.route('/games/refresh')
def do_full_refresh():
    import xbmc
    game_controller = RequiredFeature('game-controller').request()
    game_controller.get_games()
    del game_controller
    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/games/info/<game_id>')
def show_game_info(game_id):
    from resources.lib.views.gameinfo import GameInfo
    core = RequiredFeature('core').request()
    game = core.get_storage().get(game_id)
    cache_fanart = game.get_selected_fanart()
    cache_poster = game.get_selected_poster()
    window = GameInfo(game, game.name)
    window.doModal()
    del window
    if cache_fanart != game.get_selected_fanart() or cache_poster != game.get_selected_poster():
        import xbmc
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


@plugin.route('/games/launch-from-widget/<xml_id>')
def launch_game_from_widget(xml_id):
    core = RequiredFeature('core').request()
    game_id = int(xml_id)
    internal_game_id = plugin.get_storage('sorted_game_storage').get(game_id)

    game_controller = RequiredFeature('game-controller').request()
    core.logger.info('Launching game %s' % internal_game_id)
    game_controller.launch_game(internal_game_id)

    del core
    del game_controller

if __name__ == '__main__':
    core = RequiredFeature('core').request()
    update_storage = plugin.get_storage('update', TTL=24*60)
    if not update_storage.get('checked'):
        updater = RequiredFeature('update-service').request()
        updater.check_for_update()
        del updater
    core.check_script_permissions()

    if plugin.get_setting('host', str):
        game_refresh_required = False

        try:
            from resources.lib.model.game import Game
            if plugin.get_storage('game_version')['version'] != Game.version:
                game_refresh_required = True
        except KeyError:
            game_refresh_required = True

        if game_refresh_required:
            game_controller = RequiredFeature('game-controller').request()
            game_controller.get_games()
            del game_controller

        plugin.run()
        del plugin
        del core
    else:
        import xbmcgui
        core = RequiredFeature('core').request()
        xbmcgui.Dialog().ok(
                core.string('name'),
                core.string('configure_first')
        )
        del core
