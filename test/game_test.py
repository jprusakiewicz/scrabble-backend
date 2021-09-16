import unittest

from app.card import Color
from app.game import Game


class TestGame(unittest.TestCase):
    def test_calling_collor(self):
        # given
        game = Game(2)
        collor_call = "Hearts"
        # when
        game.handle_ace(collor_call)
        # then
        self.assertEqual(Color.Hearts, game.color_call)  # add assertion here

    def test_getting_call(self):
        # given
        game = Game(2)
        collor_call = "Hearts"
        game.color_call = collor_call
        # when
        call = game.get_call()
        # then
        self.assertEqual(collor_call, call)  # add assertion here


if __name__ == '__main__':
    unittest.main()
