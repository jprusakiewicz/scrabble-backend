from starlette.websockets import WebSocket

from app.player import Player


class Connection:
    def __init__(self, ws: WebSocket, player: Player):
        self.ws = ws
        self.player = player