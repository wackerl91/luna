import os
import unittest
import resources.lib.config.bootstrap as bootstrapper

from resources.lib.di.requiredfeature import RequiredFeature

from resources.lib.model.game import Game


class TestScraperChain(unittest.TestCase):
    bootstrapper.bootstrap()

    def setUp(self):
        self.chain = RequiredFeature('scraper-chain').request()

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
