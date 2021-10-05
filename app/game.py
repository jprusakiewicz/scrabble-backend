from random import Random
from typing import List

r = Random()


class Game:
    def __init__(self, taken_ids: List[str]):
        self.person_turn = 1
        self.board: []

    def handle_players_move(self, player_color, player_move: dict):
        try:
            if player_move['other']:
                return True

        except KeyError:
            pass

    def get_current_state(self):
        return {
            "idle": [],
            "finnish": [],
            "regular": []
        }
