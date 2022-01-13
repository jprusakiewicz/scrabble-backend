import unittest

from app.game import Game, get_new_letters


class TestGame(unittest.TestCase):
    # def test_getting_new_letters(self):
    #     letters = get_new_letters()
    #     self.assertEqual(98, len(letters))
    #
    # def test_creating_game_object(self):
    #     # when
    #     game = Game(4)
    #     players = game.players
    #     # then
    #     self.assertEqual(7, len(players[0]))
    #     self.assertEqual(7, len(players[1]))
    #     self.assertEqual(7, len(players[2]))
    #     self.assertEqual(7, len(players[3]))
    #     self.assertEqual(70, len(game.bag))
    #     self.assertNotEqual(players[0], players[1])
    #     self.assertNotEqual(players[1], players[2])
    #     self.assertNotEqual(players[2], players[3])
    #     self.assertNotEqual(players[2], players[0])
    #     self.assertNotEqual(players[1], players[3])
    #
    # def test_getting_orientation(self):
    #     # given
    #     positive_tiles_1 = [{'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}]
    #     positive_tiles_2 = [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}, {'x': 3, 'y': 1}, {'x': 4, 'y': 1}]
    #     positive_tiles_3 = [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}]
    #
    #     nevative_tiles_1 = [{'x': 1, 'y': 2}, {'x': 2, 'y': 1}]
    #     nevative_tiles_2 = [{'x': 1, 'y': 2}, {'x': 2, 'y': 1}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}]
    #     nevative_tiles_3 = [{'x': 1, 'y': 2}]
    #     nevative_tiles_4 = [{'x': 1, 'y': 1}]
    #     nevative_tiles_5 = [{'x': 3, 'y': 7}, {'x': 4, 'y': 6}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}]
    #
    #     self.assertEqual(('y', 1), get_orientation(positive_tiles_1))
    #     self.assertEqual(('x', 1), get_orientation(positive_tiles_2))
    #     self.assertEqual(('x', 1), get_orientation(positive_tiles_3))
    #
    #     self.assertEqual(None, get_orientation(nevative_tiles_1))
    #     self.assertEqual(None, get_orientation(nevative_tiles_2))
    #     self.assertEqual(None, get_orientation(nevative_tiles_3))
    #     self.assertEqual(None, get_orientation(nevative_tiles_4))
    #     self.assertEqual(None, get_orientation(nevative_tiles_5))

    def test_game_one(self):
        game = Game(2, 'en')

        one = game.get_player_hand('1')
        two = game.get_player_hand('2')

        game.players['1'][:3] = ['G', 'I', 'F']
        game.players['2'][0] = 'T'

        game.handle_players_move('1', [{'x': 8, 'y': 8, 'letter': 'G'}, {'x': 8, 'y': 9, 'letter': 'I'},
                                       {'x': 8, 'y': 10, 'letter': 'F'}])
        self.assertEqual(game.board.number_of_fields_on_board(), 3)

        game.handle_players_move('2', [{'x': 8, 'y': 11, 'letter': 'T'}])

        self.assertEqual(game.board.number_of_fields_on_board(), 4)

        game.players['1'][0] = ["S"]

        game.handle_players_move('1', [{'x': 8, 'y': 12, 'letter': 'S'}])
        self.assertEqual(game.board.number_of_fields_on_board(), 5)

        game.players['2'][:4] = ['M', 'U', 'M', 'P']
        game.handle_players_move('2', [{'x': 4, 'y': 12, 'letter': 'M'}, {'x': 5, 'y': 12, 'letter': 'U'},
                                       {'x': 6, 'y': 12, 'letter': 'M'}, {'x': 7, 'y': 12, 'letter': 'P'}])

        self.assertEqual(game.board.number_of_fields_on_board(), 9)

    def test_game_pl_gwiazda(self):
        game = Game(2, 'pl')

        game.players['1'][:6] = ['G', 'W', 'I', 'A', 'Z', 'D']
        game.players['2'][0] = 'A'

        game.handle_players_move('1', [{'x': 8, 'y': 5, 'letter': 'G'}, {'x': 8, 'y': 6, 'letter': 'W'},
                                       {'x': 8, 'y': 7, 'letter': 'I'}, {'x': 8, 'y': 8, 'letter': 'A'},
                                       {'x': 8, 'y': 9, 'letter': 'Z'}, {'x': 8, 'y': 10, 'letter': 'D'}])
        self.assertEqual(game.board.number_of_fields_on_board(), 6)

        game.handle_players_move('2', [{'x': 8, 'y': 11, 'letter': 'A'}])

        self.assertEqual(game.board.number_of_fields_on_board(), 7)

    def test_game_pl_wada(self):
        game = Game(2, 'pl')

        game.players['1'][:4] = ['W', 'A', 'D', 'A']

        game.players['2'][:6] = ['G', 'W', 'I', 'A', 'Z', 'D']

        game.handle_players_move('1', [{'x': 8, 'y': 8, 'letter': 'W'}, {'x': 8, 'y': 9, 'letter': 'A'},
                                       {'x': 8, 'y': 10, 'letter': 'D'}])

        self.assertEqual(3, game.board.number_of_fields_on_board())

        game.handle_players_move('2', [{'x': 3, 'y': 10, 'letter': 'G'}, {'x': 4, 'y': 10, 'letter': 'W'},
                                       {'x': 5, 'y': 10, 'letter': 'I'}, {'x': 6, 'y': 10, 'letter': 'A'},
                                       {'x': 7, 'y': 10, 'letter': 'Z'}])
        self.assertEqual(8, game.board.number_of_fields_on_board())

        game.handle_players_move('1', [{'x': 9, 'y': 10, 'letter': 'A'}])

        self.assertEqual(9, game.board.number_of_fields_on_board())

        game.handle_players_move('1', [{'x': 8, 'y': 11, 'letter': 'A'}])

        self.assertEqual(10, game.board.number_of_fields_on_board())



if __name__ == '__main__':
    unittest.main()
