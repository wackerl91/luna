import os
import shutil


from xbmcswift2 import Plugin

from model.game import Game

from scraper.abcscraper import AbstractScraper
from scraper.omdbscraper import OmdbScraper
from scraper.tgdbscraper import TgdbScraper


class ScraperChain:
    def __init__(self):
        self.scraper_chain = []
        self.plugin = Plugin(name='script.luna')
        self._configure()

    def query_game_information(self, game_name):
        """
        :type game_name: str
        :rtype game: Game
        """
        game_info = []
        for scraper in self.scraper_chain:
            game_info.append(Game.from_dict(**scraper.get_game_information(game_name)))

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
