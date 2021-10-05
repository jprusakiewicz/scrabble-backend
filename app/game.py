from random import Random, shuffle
from typing import List, Union

from app.Board import Board

r = Random()


def get_new_letters():
    letters = []
    letters.extend(['A'] * 9)
    letters.extend(['I'] * 8)
    letters.extend(['E'] * 7)
    letters.extend(['N'] * 5)
    letters.extend(['O'] * 6)
    letters.extend(['R'] * 4)
    letters.extend(['S'] * 4)
    letters.extend(['W'] * 4)
    letters.extend(['Z'] * 5)
    letters.extend(['C'] * 3)
    letters.extend(['D'] * 3)
    letters.extend(['K'] * 3)
    letters.extend(['L'] * 3)
    letters.extend(['M'] * 3)
    letters.extend(['P'] * 3)
    letters.extend(['T'] * 3)
    letters.extend(['Y'] * 4)
    letters.extend(['B'] * 2)
    letters.extend(['G'] * 2)
    letters.extend(['H'] * 2)
    letters.extend(['J'] * 2)
    letters.extend(['Ł'] * 2)
    letters.extend(['U'] * 2)
    letters.extend(['Ą'] * 1)
    letters.extend(['Ę'] * 1)
    letters.extend(['F'] * 1)
    letters.extend(['Ó'] * 1)
    letters.extend(['Ś'] * 1)
    letters.extend(['Ż'] * 1)
    letters.extend(['Ć'] * 1)
    letters.extend(['Ń'] * 1)
    letters.extend(['Ź'] * 1)
    shuffle(letters)

    return letters


class Game:
    def __init__(self, number_of_players: int):
        self.board: Board = Board()
        self.bag: List[str] = get_new_letters()
        self.players: dict = self.get_new_game_tiles(number_of_players)
        self.score = self.setup_score(number_of_players)

    def get_new_game_tiles(self, number_of_players: int):
        players = {}
        for n in range(number_of_players):
            players[str(n + 1)] = self.bag[-7:]
            self.bag = self.bag[:-7]
        return players

    def handle_players_move(self, game_id, player_move: Union[dict, List[dict]]) -> bool:
        if 'other' in player_move:
            print("other")
        else:
            self.handle_player_tiles(game_id, player_move)
            return True

    def get_board(self):
        return [f.__dict__ for f in self.board.fields]

    def get_player_hand(self, game_id):
        return self.players[game_id]

    def handle_player_tiles(self, game_id, player_move):
        self.board.add_tiles(player_move)
        self.score[game_id] += self.board.get_score(player_move)
        self.handle_players_hand(game_id, player_move)

    def setup_score(self, number_of_players: int):
        return {str(n + 1): 0 for n in range(number_of_players)}

    def get_score(self, game_id):
        return self.score[game_id]

    def handle_players_hand(self, game_id, player_move):
        for tile in player_move:
            self.players[game_id].remove(tile["letter"])
        tiles_in_hand_number = len(self.players[game_id])
        if tiles_in_hand_number < 7:
            tiles_to_get_number = 7 - tiles_in_hand_number
            self.players[game_id].extend(self.get_new_cards(tiles_to_get_number))

    def get_new_cards(self, tiles_to_get_number):
        tiles_to_get = self.bag[-tiles_to_get_number:]
        self.bag = self.bag[:-tiles_to_get_number]
        return tiles_to_get
