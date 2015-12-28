import os
import shutil


from model.game import Game

from xbmcswift2 import Plugin

from scraper.abcscraper import AbstractScraper
from scraper.omdbscraper import OmdbScraper
from scraper.tgdbscraper import TgdbScraper


class ScraperChain:
    def __init__(self):
        self.plugin = Plugin('script.luna')
        self.scraper_chain = []
        self.game_blacklist = ['Steam', 'Steam Client Bootstrapper']
        self._configure()

    def query_game_information(self, game_name):
        """
        :type game_name: str
        :rtype game: Game
        """
        game_info = []
        if not game_name in self.game_blacklist:
            for scraper in self.scraper_chain:
                game_info.append(Game.from_dict(**scraper.get_game_information(game_name)))
        else:
            game_info.append(Game(game_name, None))

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

    def _append_scraper(self, scraper):
        if isinstance(scraper, AbstractScraper):
            self.scraper_chain.append(scraper)
        else:
            raise AssertionError('Expected to receive an instance of AbstractScraper, got %s instead' % type(scraper))

    def _configure(self):
        if self.plugin.get_setting('enable_omdb', bool):
            self._append_scraper(OmdbScraper(self.plugin.storage_path))
        if self.plugin.get_setting('enable_tgdb', bool):
            self._append_scraper(TgdbScraper(self.plugin.storage_path))
