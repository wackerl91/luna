import os

from abcscraper import AbstractScraper


class TgdbScraper(AbstractScraper):
    def __init__(self, addon_path):
        AbstractScraper.__init__(self, addon_path)
        self.api_url = 'http://thegamesdb.net/api/GetGame.php?name=%s'
        self.art_cache = os.path.join(self.base_path, 'art/poster/')
        self.api_cache = os.path.join(self.base_path, 'api_cache/')
        self._set_up_paths()

    def _set_up_paths(self):
        if not os.path.exists(self.art_cache):
            os.makedirs(self.art_cache)
        if not os.path.exists(self.api_cache):
            os.makedirs(self.api_cache)

    def get_game_information(self, game_name):
        AbstractScraper.get_game_information(self, game_name)
