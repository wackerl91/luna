from resources.lib.model.game import Game
from scraper.abcscraper import AbstractScraper


class ScraperChain:
    def __init__(self):
        self.scraper_chain = []

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
