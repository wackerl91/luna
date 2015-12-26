from xbmcswift2 import Plugin

from resources.lib.model.game import Game
from scraper.abcscraper import AbstractScraper
from scraper.omdbscraper import OmdbScraper
from scraper.tgdbscraper import TgdbScraper


class ScraperChain:
    def __init__(self):
        self.scraper_chain = []
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

    def append_scraper(self, scraper):
        if isinstance(scraper, AbstractScraper):
            self.scraper_chain.append(scraper)
        else:
            raise AssertionError('Expected to receive an instance of AbstractScraper, got %s instead' % type(scraper))

    def _configure(self):
        plugin = Plugin(name='script.luna')
        if plugin.get_setting('enable_omdb', bool):
            self.append_scraper(OmdbScraper(plugin.storage_path))
        if plugin.get_setting('enable_tgdb', bool):
            self.append_scraper(TgdbScraper(plugin.storage_path))
