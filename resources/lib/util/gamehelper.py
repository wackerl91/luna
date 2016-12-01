import xbmcgui
from resources.lib.model.game import Game


class GameHelper(object):
    def __init__(self, plugin, core, game_manager, moonlight_helper, scraper_chain, logger):
        self.plugin = plugin
        self.core = core
        self.game_manager = game_manager
        self.moonlight_helper = moonlight_helper
        self.scraper_chain = scraper_chain
        self.logger = logger

    def get_games(self, host, silent=False):
        """
        Fills local game storage with scraper results (if enabled) or game names (if scrapers are disabled)
        """
        game_list = self.moonlight_helper.list_games()

        if game_list is None or len(game_list) == 0:
            xbmcgui.Dialog().notification(
                self.core.string('name'),
                'Getting game list failed. ' +
                'This usually means your host wasn\'t paired properly.',
                '',
                20000
            )
            return

        if not silent:
            progress_dialog = xbmcgui.DialogProgress()
            progress_dialog.create(
                self.core.string('name'),
                'Refreshing Game List'
            )

        if not silent:
            if game_list is None or len(game_list) == 0:
                xbmcgui.Dialog().notification(
                    self.core.string('name'),
                    self.core.string('empty_game_list')
                )
                return

        bar_movement = int(1.0 / len(game_list) * 100)

        # TODO: storage should be closed after access -> need to build a list(!!) of games and add them all together
        games = self.game_manager.get_games(host)
        game_version_storage = self.plugin.get_storage('game_version')

        cache = {}
        if game_version_storage.get('version') == Game.version:
            cache = games.copy()

        games.clear()

        self.game_manager.remove_games(host)

        i = 1
        for nvapp in game_list:
            if not silent:
                progress_dialog.update(bar_movement * i, 'Processing: %s' % nvapp.title, '')
            game = Game(nvapp.title, host.uuid)
            self.logger.info("Processing: %s" % nvapp.title)

            if nvapp.id in cache:
                if not games.get(nvapp.id):
                    if not silent:
                        progress_dialog.update(bar_movement * i, line2='Restoring information from cache')
                    games[nvapp.id] = cache.get(nvapp.id)
                    self.logger.info("Restored information from cache")
            else:
                try:
                    if not silent:
                        progress_dialog.update(bar_movement * i, line2='Getting Information from Online Sources')
                    games[nvapp.id] = self.scraper_chain.query_game_information(nvapp)
                    self.logger.info("Loaded information from online sources")
                except KeyError:
                    self.logger.info(
                        'Key Error thrown while getting information for game {0}: {1}'
                        .format(nvapp.title,
                                KeyError.message))
                    games[nvapp.id] = game
            i += 1

        game_version_storage.clear()
        game_version_storage['version'] = Game.version

        for id, game in games.iteritems():
            self.game_manager.add_game(host, game)
        game_version_storage.sync()

        return games

    def get_games_as_list(self, host, force_refresh=False):
        """
        Parses contents of local game storage into a list that can be interpreted by Kodi
        :rtype: list
        """
        games = self.game_manager.get_games(host)

        if len(games) == 0:
            games = self.get_games(host)
        if force_refresh:
            games = self.get_games(host, silent=True)

        items = []
        for i, game_name in enumerate(games):
            game = games.get(game_name)
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
                # 'context_menu': context_menu(game_name),
                # 'path': self.plugin.url_for(
                #     endpoint='launch_game',
                #     game_id=game.name
                # ),
                'properties': {
                    'fanart_image': game.get_selected_fanart().get_original(),
                    'id': game.id
                }
            })

        return items
