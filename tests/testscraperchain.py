import os
import shutil
import unittest

from resources.lib.model.game import Game
from resources.lib.scraperchain import ScraperChain


class TestScraperChain(unittest.TestCase):

    def setUp(self):
        path = os.path.join(os.path.expanduser('~'), 'LunaTestTemp')
        if not os.path.exists(path):
            os.makedirs(path)
        chain = ScraperChain()
        self.chain = chain

    def testReturnType(self):
        game_name = 'Half-Life 2'
        game = self.chain.query_game_information(game_name)
        self.assertEqual(isinstance(game, Game), True)

    def testImageDump(self):
        game_name = 'Half-Life 2'
        game = self.chain.query_game_information(game_name)
        for img_path in game.fanart:
            self.assertEqual(os.path.isfile(img_path), True)
        self.assertEqual(os.path.isfile(game.poster), True)

    def tearDown(self):
        path = os.path.join(os.path.expanduser('~'), 'LunaTestTemp')
        shutil.rmtree(path, ignore_errors=True)
