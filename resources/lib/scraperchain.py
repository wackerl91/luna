import os
import shutil

import core.corefunctions as core

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
        unique_paths = []
        for scraper in self.scraper_chain:
            unique_paths.append(scraper.return_paths())
        for path in set(unique_paths):
            self.plugin.get_storage('game_storage').clear()
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
                core.Logger.info('Deleted folder %s on user request' % path)

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
