import os
import unittest

from resources.lib.di.requiredfeature import RequiredFeature

from resources.lib.model.game import Game


class TestScraperChain(unittest.TestCase):
    def setUp(self):
        self.chain = RequiredFeature('scraper-chain').request()

    def testReturnType(self):
        game_name = 'Half-Life 2'
        game = self.chain.query_game_information(game_name)
        self.assertEqual(isinstance(game, Game), True)

    def testImageDump(self):
        game_name = 'Half-Life 2'
        game = self.chain.query_game_information(game_name)

        for img_id in game.fanarts:
            art = game.fanarts.get(img_id)
            self.assertEqual(os.path.isfile(art.get_thumb()), True)
            if art != game.get_selected_fanart():
                self.assertEqual(os.path.isfile(art.get_original()), False)
            else:
                self.assertEqual(os.path.isfile(art.get_original()), True)

        for img_path in game.posters:
            self.assertEqual(os.path.isfile(img_path), True)

        self.assertEqual(os.path.isfile(game.get_selected_fanart().get_original()), True)

    def tearDown(self):
        self.chain.reset_cache()
