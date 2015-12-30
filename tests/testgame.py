import unittest

from resources.lib.model.game import Game


class TestGame(unittest.TestCase):
    def testGameMergeSelfNone(self):
        game1 = Game('Name')

        game2 = Game('Name')
        game2.genre = ['Action', 'Adventure']
        game2.poster = '/path/to/poster'
        game2.fanarts = ['path/to/art/1', 'path/to/art/2', 'path/to/art/3']

        game1.merge(game2)

        self.assertEqual(game1.genre, ['Action', 'Adventure'])
        self.assertEqual(game1.poster, '/path/to/poster')
        self.assertEqual(game1.fanarts, ['path/to/art/1', 'path/to/art/2', 'path/to/art/3'])
        self.assertEqual(game1.get_selected_fanart(), 'path/to/art/1')

    def testGameMergeSelfFilled(self):
        game1 = Game('Name')
        game1.genre = ['Shooter', 'Adventure']
        game1.poster = '/path/to/poster/original'
        game1.fanarts = ['path/to/art/1-1', 'path/to/art/1-2', 'path/to/art/1-3']

        game2 = Game('Name')
        game2.genre = ['Action', 'Adventure']
        game2.poster = '/path/to/poster'
        game2.fanarts = ['path/to/art/1', 'path/to/art/2', 'path/to/art/1-3']

        game1.merge(game2)

        self.assertEqual(game1.genre, ['Action', 'Adventure', 'Shooter'])
        self.assertEqual(game1.poster, '/path/to/poster/original')
        self.assertEqual('path/to/art/1' in game1.fanarts, True)
        self.assertEqual('path/to/art/2' in game1.fanarts, True)
        self.assertEqual('path/to/art/1-1' in game1.fanarts, True)
        self.assertEqual('path/to/art/1-2' in game1.fanarts, True)
        self.assertEqual('path/to/art/1-3' in game1.fanarts, True)
