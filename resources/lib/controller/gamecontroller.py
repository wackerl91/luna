import xbmcgui
from resources.lib.model.game import Game


class GameController:
    def __init__(self, plugin, core, moonlight_helper, scraper_chain, logger):
        self.plugin = plugin
        self.core = core
        self.moonlight_helper = moonlight_helper
        self.scraper_chain = scraper_chain
        self.logger = logger

    def get_games(self):
        """
        Fills local game storage with scraper results (if enabled) or game names (if scrapers are disabled)
        """
        game_list = self.moonlight_helper.list_games()

        progress_dialog = xbmcgui.DialogProgress()
        progress_dialog.create(
            self.core.string('name'),
            'Refreshing Game List'
        )

        if game_list is None or len(game_list) == 0:
            xbmcgui.Dialog().notification(
                self.core.string('name'),
                self.core.string('empty_game_list')
            )
            return

        bar_movement = int(1.0 / len(game_list) * 100)

        storage = self.core.get_storage()
        game_version_storage = self.plugin.get_storage('game_version')

        cache = {}
        if game_version_storage.get('version') == Game.version:
            cache = storage.raw_dict().copy()

        storage.clear()

        i = 1
        for game_name in game_list:
            progress_dialog.update(bar_movement * i, 'Processing: %s' % game_name, '')
            if self.plugin.get_setting('disable_scraper', bool):
                self.logger.info('Scraper have been disabled, just adding game names to list.')
                progress_dialog.update(bar_movement * i, line2='Scrapers have been disabled, just adding game names to list.')
                storage[game_name] = Game(game_name, None)
            else:
                if game_name in cache:
                    if not storage.get(game_name):
                        progress_dialog.update(bar_movement * i, line2='Restoring information from cache')
                        storage[game_name] = cache.get(game_name)[0]
                else:
                    try:
                        progress_dialog.update(bar_movement * i, line2='Getting Information from Online Sources')
                        storage[game_name] = self.scraper_chain.query_game_information(game_name)
                    except KeyError:
                        self.logger.info(
                                'Key Error thrown while getting information for game {0}: {1}'
                                .format(game_name,
                                        KeyError.message))
                        storage[game_name] = Game(game_name, None)
            i += 1

        game_version_storage.clear()
        game_version_storage['version'] = Game.version

        storage.sync()
        game_version_storage.sync()

    def get_games_as_list(self):
        """
        Parses contents of local game storage into a list that can be interpreted by Kodi
        :rtype: list
        """

        def context_menu(game_id):
            return [
                (
                    'Game Information',
                    'XBMC.RunPlugin(%s)' % self.plugin.url_for(
                            endpoint='show_game_info',
                            game_id=game_id
                    )
                ),
                (
                    self.core.string('addon_settings'),
                    'XBMC.RunPlugin(%s)' % self.plugin.url_for(
                            endpoint='open_settings'
                    )
                ),
                (
                    self.core.string('full_refresh'),
                    'XBMC.RunPlugin(%s)' % self.plugin.url_for(
                            endpoint='do_full_refresh'
                    )
                )
            ]

        storage = self.core.get_storage()

        if len(storage.raw_dict()) == 0:
            self.get_games()

        items = []
        for i, game_name in enumerate(storage):
            game = storage.get(game_name)
            items.append({
                'label': game.name,
                'icon': game.get_selected_poster(),
                'thumbnail': game.get_selected_poster(),
                'info': {
                    'year': game.year,
                    'plot': game.plot,
                    'genre': game.get_genre_as_string(),
                    'originaltitle': game.name,
                },
                'replace_context_menu': True,
                'context_menu': context_menu(game_name),
                'path': self.plugin.url_for(
                        endpoint='launch_game',
                        game_id=game.name
                ),
                'properties': {
                    'fanart_image': game.get_selected_fanart().get_original()
                }
            })

        return items

    def launch_game(self, game_name):
        """
        Launches game with specified name
        :type game_name: str
        """
        self.moonlight_helper.launch_game(game_name)
