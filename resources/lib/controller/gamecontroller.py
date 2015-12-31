from resources.lib.model.game import Game


class GameController:
    def __init__(self, container):
        """

        :type container: PluginContainer
        """
        self.container = container
        self.core = container.get_core()
        self.moonlight_helper = container.get_moonlight_helper()
        self.scraper_chain = container.get_scraper_chain()
        self.logger = self.core.logger

    def get_games(self):
        """
        Fills local game storage with scraper results (if enabled) or game names (if scrapers are disabled)
        """
        game_list = self.moonlight_helper.list_games()
        storage = self.core.get_storage()
        cache = storage.raw_dict()
        storage.clear()

        for game_name in game_list:
            if self.container.get_plugin().get_setting('disable_scraper', bool):
                self.logger.info('Scraper have been disabled, just adding game names to list.')
                storage[game_name] = Game(game_name, None)
            else:
                if game_name in cache:
                    if not storage.get(game_name):
                        storage[game_name] = cache.get(game_name)
                else:
                    try:
                        storage[game_name] = self.scraper_chain.query_game_information(game_name)
                    except KeyError:
                        self.logger.info(
                                'Key Error thrown while getting information for game {0}: {1}'
                                .format(game_name,
                                        KeyError.message))
                        storage[game_name] = Game(game_name, None)

        storage.sync()

    def get_games_as_list(self):
        """
        Parses contents of local game storage into a list that can be interpreted by Kodi
        :rtype: list
        """

        def context_menu(game_id):
            return [
                (
                    'Game Information',
                    'XBMC.RunPlugin(%s)' % self.container.get_plugin().url_for(
                            endpoint='show_game_info',
                            game_id=game_id
                    )
                ),
                (
                    self.core.string('addon_settings'),
                    'XBMC.RunPlugin(%s)' % self.container.get_plugin().url_for(
                            endpoint='open_settings'
                    )
                ),
                (
                    self.core.string('full_refresh'),
                    'XBMC.RunPlugin(%s)' % self.container.get_plugin().url_for(
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
                'path': self.container.get_plugin().url_for(
                        endpoint='launch_game',
                        game_id=game.name
                ),
                'properties': {
                    'fanart_image': game.get_selected_fanart()
                }
            })

        return items

    def launch_game(self, game_name):
        """
        Launches game with specified name
        :type game_name: str
        """
        self.moonlight_helper.launch_game(game_name)
