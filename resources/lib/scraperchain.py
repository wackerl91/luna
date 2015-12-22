from scraper.abcscraper import AbstractScraper


class ScraperChain:
    def __init__(self):
        self.scraper_chain = []

    def query_game_information(self, game_name):
        game_info = []
        for scraper in self.scraper_chain:
            game_info.append(scraper.get_game_information(game_name))

        return game_info

    def append_scraper(self, scraper):
        if isinstance(scraper, AbstractScraper):
            self.scraper_chain.append(scraper)
        else:
            raise AssertionError('Expected to receive an instance of AbstractScraper, got %s instead' % type(scraper))
