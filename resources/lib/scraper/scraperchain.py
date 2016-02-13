import os
import shutil

from resources.lib.di.component import Component
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.model.fanart import Fanart
from resources.lib.model.game import Game
from resources.lib.scraper.abcscraper import AbstractScraper


class ScraperChain(Component):
    plugin = RequiredFeature('plugin')
    logger = RequiredFeature('logger')

    def __init__(self):
        self.scraper_chain = []
        self.game_blacklist = ['Steam', 'Steam Client Bootstrapper']

    def query_game_information(self, game_name):
        """
        :type game_name: str
        :rtype game: Game
        """
        game_info = []
        self.logger.info("Trying to get information for game: %s" % game_name)
        if game_name not in self.game_blacklist:
            for scraper in self.scraper_chain:
                if scraper.is_enabled():
                    game_info.append(Game.from_api_response(scraper.get_game_information(game_name)))

        else:
            game = Game(game_name, None)

            if game_name == 'Steam':
                game.fanarts = []
                fanart = Fanart('resources/statics/steam_wallpaper___globe_by_diglididudeng-d7kq9v9.jpg',
                                'resources/statics/steam_wallpaper___globe_by_diglididudeng-d7kq9v9.jpg')
                game.fanarts.append(fanart)

            game_info.append(game)

        game = game_info[0]
        while len(game_info) > 1:
            next_game = game_info.pop()
            game.merge(next_game)

        return game

    def reset_cache(self):
        self.plugin.get_storage('game_storage').clear()

        paths = []
        for scraper in self.scraper_chain:
            for path in scraper.return_paths():
                paths.append(path)
        unique_paths = set(paths)

        for path in unique_paths:
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)

    def append(self, scrapers):
        for scraper in scrapers:
            obj = RequiredFeature(scraper).request()
            self._append_scraper(obj)

    def _append_scraper(self, scraper):
        if isinstance(scraper, AbstractScraper):
            self.scraper_chain.append(scraper)
        else:
            raise AssertionError('Expected to receive an instance of AbstractScraper, got %s instead' % type(scraper))
