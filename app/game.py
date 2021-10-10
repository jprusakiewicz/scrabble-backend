from random import Random, shuffle
from typing import List, Union

from app.Board import Board
from words import words_manager

r = Random()


def get_new_letters(locale):
    letters = []

    if locale == 'pl':
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

    elif locale == 'en':
        letters.extend(['A'] * 9)
        letters.extend(['I'] * 9)
        letters.extend(['E'] * 12)
        letters.extend(['N'] * 6)
        letters.extend(['O'] * 8)
        letters.extend(['R'] * 6)
        letters.extend(['S'] * 4)
        letters.extend(['W'] * 2)
        letters.extend(['Z'] * 1)
        letters.extend(['C'] * 2)
        letters.extend(['D'] * 4)
        letters.extend(['K'] * 1)
        letters.extend(['L'] * 4)
        letters.extend(['M'] * 2)
        letters.extend(['P'] * 2)
        letters.extend(['T'] * 6)
        letters.extend(['Y'] * 2)
        letters.extend(['B'] * 2)
        letters.extend(['G'] * 3)
        letters.extend(['H'] * 2)
        letters.extend(['J'] * 1)
        letters.extend(['U'] * 4)
        letters.extend(['V'] * 2)
        letters.extend(['F'] * 2)
        letters.extend(['X'] * 1)
        letters.extend(['Q'] * 1)

    shuffle(letters)
    return letters


def read_words(locale: str):
    path = ""
    try:
        if locale == 'pl':
            path = 'words/slowa.txt'
        elif locale == 'en':
            path = "words/words.txt"
        with open(path) as f:
            words = f.read().split('\n')
    except FileNotFoundError as e:
        print("File not found!")
    return words


class Game:
    def __init__(self, number_of_players: int, locale: str):
        self.board: Board = Board()
        self.bag: List[str] = get_new_letters(locale)
        self.players: dict = self.get_new_game_tiles(number_of_players)
        self.score = self.setup_score(number_of_players)
        self.locale = locale

    def get_new_game_tiles(self, number_of_players: int):
        players = {}
        for n in range(number_of_players):
            players[str(n + 1)] = self.bag[-7:]
            self.bag = self.bag[:-7]
        return players

    def handle_players_move(self, game_id, player_move: Union[dict, List[dict]]) -> bool:
        if 'other' in player_move:
            if player_move['other'] == "refresh":
                pass
            elif player_move['other'] == "skip":
                letter = player_move['letter']
                self.replace_letter(game_id, letter)
                return True
            return False
        else:
            next_player = self.handle_player_tiles(game_id, player_move)
            return next_player

    def get_board(self):
        return [f.__dict__ for f in self.board.fields]

    def get_player_hand(self, game_id):
        return self.players[game_id]

    def handle_player_tiles(self, game_id, player_move):
        if self.validate_move(game_id, player_move):
            self.board.add_tiles(player_move)
            self.score[game_id] += self.board.get_score(player_move)
            self.handle_players_hand(game_id, player_move)
            return True
        return False

    def setup_score(self, number_of_players: int):
        return {str(n + 1): 0 for n in range(number_of_players)}

    def get_score(self, game_id):
        return self.score[game_id]

    def handle_players_hand(self, game_id, player_move):
        for tile in player_move:
            try:
                self.players[game_id].remove(tile["letter"])
            except ValueError:
                pass
        tiles_in_hand_number = len(self.players[game_id])
        if tiles_in_hand_number < 7:
            tiles_to_get_number = 7 - tiles_in_hand_number
            self.players[game_id].extend(self.get_new_tiles(tiles_to_get_number))

    def get_new_tiles(self, tiles_to_get_number):
        if len(self.bag) < tiles_to_get_number:
            tiles_to_get = self.bag
            self.bag = []
        else:
            tiles_to_get = self.bag[-tiles_to_get_number:]
            self.bag = self.bag[:-tiles_to_get_number]
        return tiles_to_get

    def get_orientation(self, player_move):
        if len(player_move) == 1:
            surroundings = self.get_surroundings(player_move['x'], player_move['y'])
            if len(surroundings) == 1:
                player_move.extend(surroundings)
            else:
                return None

        xs = [tile["x"] for tile in player_move]
        ys = [tile["y"] for tile in player_move]

        if len(xs) > 1 and len(set(xs)) == 1:
            return 'y'
        elif len(ys) > 1 and len(set(ys)) == 1:
            return 'x'
        else:
            return None

    def validate_move(self, game_id, player_move):
        try:
            if self.board.is_empty():
                if not self.is_first_or_last_on_center(player_move):
                    return False

            orientation = self.get_orientation(player_move)
            if orientation is not None:
                if self.validate_continuum(player_move, orientation):
                    self.append_extreme_tiles(player_move, orientation)
                    if self.validate_tiles_position(player_move, orientation):
                        if self.validate_word(player_move):
                            return True
            return False

        except Exception as e:
            print(e.__class__.__name__)
            return False

    def validate_continuum(self, player_move, orientation):
        indices = [tile[orientation] for tile in player_move]
        start_idx = min(indices)
        end_idx = max(indices)
        for i in range(start_idx, end_idx):
            if i not in indices:
                if orientation == 'x':
                    field = self.board.get_field(i, player_move[0]["y"])
                    if field is not None:
                        player_move.append({"x": field.x, "y": field.y, "letter": field.letter})
                    else:
                        return False
                elif orientation == 'y':
                    field = self.board.get_field(player_move[0]["x"], i)
                    if field is not None:
                        player_move.append({"x": field.x, "y": field.y, "letter": field.letter})
                    else:
                        return False
        return True

    def validate_tiles_position(self, players_move, orientation):
        if orientation == 'x':
            opposite_orientation = 'y'
        else:
            opposite_orientation = 'x'
        for tile in players_move:
            if not self.board.is_in_board(tile):
                new_word = [tile]
                self.append_extreme_tiles(new_word, opposite_orientation)
                if len(new_word) > 1:
                    print("new word: ", new_word)
                    if self.validate_word(new_word) is not True:
                        return False
        return True

    def get_surroundings(self, x, y):
        surroundings = []

        surroundings.append(self.board.get_field(x - 1, y))
        surroundings.append(self.board.get_field(x + 1, y))
        surroundings.append(self.board.get_field(x, y - 1))
        surroundings.append(self.board.get_field(x, y + 1))

        surroundings = list(filter(None, surroundings))
        surroundings = [s.__dict__ for s in surroundings]
        return surroundings

    def get_oriented_surrounding(self, x, y, orientation: str):
        surroundings = []
        if orientation == 'x':
            surroundings.append(self.board.get_field(x - 1, y))
            surroundings.append(self.board.get_field(x + 1, y))
        elif orientation == 'y':
            surroundings.append(self.board.get_field(x, y - 1))
            surroundings.append(self.board.get_field(x, y + 1))

        surroundings = list(filter(None, surroundings))
        if any(surroundings):
            return surroundings[0]

    def append_extreme_top_tiles(self, player_move, orientation):
        player_move.sort(key=lambda l: l[orientation])
        first_tile = player_move[0]

        new = self.get_oriented_surrounding(first_tile['x'], first_tile['y'], orientation)
        if new is not None and {"x": new.x, "y": new.y, "letter": new.letter} not in player_move:
            player_move.append({"x": new.x, "y": new.y, "letter": new.letter})
            player_move.sort(key=lambda l: l[orientation])
            self.append_extreme_top_tiles(player_move, orientation)

    def append_extreme_bottom_tiles(self, player_move, orientation):
        player_move.sort(key=lambda l: l[orientation])
        last = player_move[-1]

        new = self.get_oriented_surrounding(last['x'], last['y'], orientation)
        if new is not None and {"x": new.x, "y": new.y, "letter": new.letter} not in player_move:
            player_move.append({"x": new.x, "y": new.y, "letter": new.letter})
            player_move.sort(key=lambda l: l[orientation])
            self.append_extreme_top_tiles(player_move, orientation)

    def append_extreme_tiles(self, player_move, orientation):
        self.append_extreme_top_tiles(player_move, orientation)
        self.append_extreme_bottom_tiles(player_move, orientation)

    def validate_word(self, player_move):
        word = "".join([w["letter"] for w in player_move]).lower()
        return words_manager.check_word(word, self.locale)

    def is_first_or_last_on_center(self, player_move):
        for tile in player_move:
            if tile['x'] == 8 and tile['y'] == 8:
                return True
        return False

    def replace_letter(self, game_id, letter):
        idx = self.players[game_id].index(letter)
        self.players[game_id][idx] = self.bag[-1]
        self.bag[-1] = letter
