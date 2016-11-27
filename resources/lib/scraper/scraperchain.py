import os
import shutil

from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.model.fanart import Fanart
from resources.lib.model.game import Game
from resources.lib.scraper.abcscraper import AbstractScraper


class ScraperChain:
    def __init__(self, plugin, game_manager, logger):
        self.plugin = plugin
        self.game_manager = game_manager
        self.logger = logger
        self.scraper_chain = []
        self.game_blacklist = ['Steam', 'Steam Client Bootstrapper']

    def query_game_information(self, nvapp):
        game_info = []
        self.logger.info("Trying to get information for game: %s" % nvapp.title)
        if nvapp.title not in self.game_blacklist:
            for scraper in self.scraper_chain:
                if scraper.is_enabled():
                    api_response = scraper.get_game_information(nvapp)
                    game = Game.from_api_response(api_response)
                    game.id = nvapp.id
                    game_info.append(game)

        else:
            game = Game(nvapp.title, None, nvapp.id)

            if nvapp.title == 'Steam':
                fanart_path = os.path.join(self.plugin.addon.getAddonInfo('path'),
                                           'resources/statics/steam_wallpaper___globe_by_diglididudeng-d7kq9v9.jpg')
                fanart = Fanart(fanart_path, fanart_path)
                game.fanarts[os.path.basename(fanart_path)] = fanart
                for scraper in self.scraper_chain:
                    if scraper.name() == 'NvHTTP':
                        game.posters = scraper.get_game_information(nvapp).posters
                        self.logger.info("Appending steam posters: %s" % game.posters)

            game_info.append(game)

        game = game_info[0]
        while len(game_info) > 1:
            next_game = game_info.pop()
            game.merge(next_game)

        return game

    def reset_cache(self):
        self.logger.info("Reset cache requested ...")
        self.game_manager.clear()

        paths = []
        for scraper in self.scraper_chain:
            self.logger.info("Getting paths from scraper: %s" % scraper.name())
            for path in scraper.return_paths():
                paths.append(path)
        unique_paths = set(paths)

        for path in unique_paths:
            self.logger.info("Attempting to clear path: %s" % path)
            if os.path.exists(path):
                self.logger.info("Clearing path: %s" % path)
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
