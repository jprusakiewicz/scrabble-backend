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


if __name__ == '__main__':
    unittest.main()
