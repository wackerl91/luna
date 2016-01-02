import os
import unittest

from resources.lib.model.game import Game
from resources.lib.scraper.scraperchain import ScraperChain


class TestScraperChain(unittest.TestCase):

    def setUp(self):
        chain = ScraperChain()
        self.chain = chain

    def testReturnType(self):
        game_name = 'Half-Life 2'
        game = self.chain.query_game_information(game_name)
        self.assertEqual(isinstance(game, Game), True)

    def testImageDump(self):
        game_name = 'Half-Life 2'
        game = self.chain.query_game_information(game_name)
        for img_path in game.fanarts:
            self.assertEqual(os.path.isfile(img_path), True)
        for img_path in game.posters:
            self.assertEqual(os.path.isfile(img_path), True)

    def tearDown(self):
        self.chain.reset_cache()
