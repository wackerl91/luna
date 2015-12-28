import os
import xbmcgui

from xbmcswift2 import Plugin, xbmcaddon

from resources.lib.plugincontainer import PluginContainer

plugin = Plugin()
container = PluginContainer(plugin)
core = container.get_core()

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

    # TODO: Routing shouldn't know about the existence of the moonlight helper; should be handled by config controller
    success = container.get_moonlight_helper().create_ctrl_map(progress_dialog, map_file)

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

    # TODO: Routing shouldn't know about the existence of the moonlight helper; should be handled by config controller
    success = container.get_moonlight_helper().pair_host(pair_dialog)

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
        container.get_scraper_chain().reset_cache()
    else:
        return


@plugin.route('/games')
def show_games():
    import resources.lib.controller.gamecontroller as game_controller
    plugin.set_content('movies')
    return plugin.finish(game_controller.get_games_as_list(), sort_methods=['label'])


@plugin.route('/games/refresh')
def do_full_refresh():
    import resources.lib.controller.gamecontroller as game_controller
    game_controller.get_games()


@plugin.route('/games/launch/<game_id>')
def launch_game(game_id):
    core.Logger.info('Launching game %s' % game_id)
    # TODO: Routing shouldn't know about the existence of the moonlight helper; should be handled by game controller
    container.get_moonlight_helper().launch_game(game_id)


if __name__ == '__main__':
    core.Logger.info('Launching Luna')
    core.check_script_permissions()
    if plugin.get_setting('host', unicode):
        container.get_config_helper().configure()
        plugin.run()
    else:
        xbmcgui.Dialog().ok(
                core.string('name'),
                core.string('configure_first')
        )
