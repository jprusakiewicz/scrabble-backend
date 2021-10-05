from typing import Optional


class Player:
    def __init__(self, player_id: str, nick: str, is_playing: bool):
        self.in_game = is_playing
        self.id = player_id
        self.game_id = None
        self.nick: str = nick
