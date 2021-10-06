import unittest

from app.game import Game, get_new_letters


class TestGame(unittest.TestCase):
    def test_getting_new_letters(self):
        letters = get_new_letters()
        self.assertEqual(98, len(letters))

    def test_creating_game_object(self):
        # when
        game = Game(4)
        players = game.players
        # then
        self.assertEqual(7, len(players[0]))
        self.assertEqual(7, len(players[1]))
        self.assertEqual(7, len(players[2]))
        self.assertEqual(7, len(players[3]))
        self.assertEqual(70, len(game.bag))
        self.assertNotEqual(players[0], players[1])
        self.assertNotEqual(players[1], players[2])
        self.assertNotEqual(players[2], players[3])
        self.assertNotEqual(players[2], players[0])
        self.assertNotEqual(players[1], players[3])

    def test_getting_orientation(self):
        # given
        positive_tiles_1 = [{'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}]
        positive_tiles_2 = [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}, {'x': 3, 'y': 1}, {'x': 4, 'y': 1}]
        positive_tiles_3 = [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}]

        nevative_tiles_1 = [{'x': 1, 'y': 2}, {'x': 2, 'y': 1}]
        nevative_tiles_2 = [{'x': 1, 'y': 2}, {'x': 2, 'y': 1}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}]
        nevative_tiles_3 = [{'x': 1, 'y': 2}]
        nevative_tiles_4 = [{'x': 1, 'y': 1}]
        nevative_tiles_5 = [{'x': 3, 'y': 7}, {'x': 4, 'y': 6}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}]

        self.assertEqual(('y', 1), get_orientation(positive_tiles_1))
        self.assertEqual(('x', 1), get_orientation(positive_tiles_2))
        self.assertEqual(('x', 1), get_orientation(positive_tiles_3))

        self.assertEqual(None, get_orientation(nevative_tiles_1))
        self.assertEqual(None, get_orientation(nevative_tiles_2))
        self.assertEqual(None, get_orientation(nevative_tiles_3))
        self.assertEqual(None, get_orientation(nevative_tiles_4))
        self.assertEqual(None, get_orientation(nevative_tiles_5))


if __name__ == '__main__':
    unittest.main()
