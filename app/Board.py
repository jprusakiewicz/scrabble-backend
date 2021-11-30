from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ScoreOperation(Enum):
    DoubleLetter = "DoubleLetter"
    TripleLetter = "TripleLetter"
    DoubleWord = "DoubleWord"
    TripleWord = "TripleWord"


def setup_letter_scores():
    d = dict(A=1, E=1, I=1, N=1, O=1, R=1, S=1, W=1, Z=1,
             C=2, D=2, K=2, L=2, M=2, P=2, T=2, Y=2,
             B=3, G=3, H=3, J=3, Ł=3, U=3,
             Ą=5, Ę=5, F=5, Ó=5, Ś=5, Ż=5,
             Ć=6, Ń=7, Ź=9)
    return d


@dataclass
class Field:
    def __init__(self, x: int, y: int, letter: str, score_operation: Optional[ScoreOperation] = None):
        self.x = x
        self.y = y
        self.letter = letter
        self.ExtraScore: Optional[ScoreOperation] = score_operation


class Board:
    def __init__(self):
        self.fields: List[Field] = []
        self.scored_fields = self.get_scored_fields()
        self.letter_scores = setup_letter_scores()

    def get_scored_fields(self):
        scored_fields = [
            dict(x=1, y=1, score=ScoreOperation.TripleWord),
            dict(x=1, y=8, score=ScoreOperation.TripleWord),
            dict(x=1, y=15, score=ScoreOperation.TripleWord),
            dict(x=8, y=15, score=ScoreOperation.TripleWord),
            dict(x=15, y=15, score=ScoreOperation.TripleWord),
            dict(x=15, y=8, score=ScoreOperation.TripleWord),
            dict(x=15, y=1, score=ScoreOperation.TripleWord),
            dict(x=8, y=1, score=ScoreOperation.TripleWord),

            dict(x=2, y=2, score=ScoreOperation.DoubleWord),
            dict(x=3, y=3, score=ScoreOperation.DoubleWord),
            dict(x=4, y=4, score=ScoreOperation.DoubleWord),
            dict(x=5, y=5, score=ScoreOperation.DoubleWord),
            dict(x=14, y=2, score=ScoreOperation.DoubleWord),
            dict(x=13, y=3, score=ScoreOperation.DoubleWord),
            dict(x=12, y=4, score=ScoreOperation.DoubleWord),
            dict(x=11, y=5, score=ScoreOperation.DoubleWord),
            dict(x=5, y=11, score=ScoreOperation.DoubleWord),
            dict(x=4, y=12, score=ScoreOperation.DoubleWord),
            dict(x=3, y=13, score=ScoreOperation.DoubleWord),
            dict(x=2, y=14, score=ScoreOperation.DoubleWord),
            dict(x=14, y=14, score=ScoreOperation.DoubleWord),
            dict(x=13, y=13, score=ScoreOperation.DoubleWord),
            dict(x=12, y=12, score=ScoreOperation.DoubleWord),
            dict(x=11, y=11, score=ScoreOperation.DoubleWord),

            dict(x=4, y=1, score=ScoreOperation.DoubleLetter),
            dict(x=12, y=1, score=ScoreOperation.DoubleLetter),
            dict(x=7, y=3, score=ScoreOperation.DoubleLetter),
            dict(x=9, y=3, score=ScoreOperation.DoubleLetter),
            dict(x=1, y=4, score=ScoreOperation.DoubleLetter),
            dict(x=8, y=4, score=ScoreOperation.DoubleLetter),
            dict(x=15, y=4, score=ScoreOperation.DoubleLetter),
            dict(x=3, y=7, score=ScoreOperation.DoubleLetter),
            dict(x=7, y=7, score=ScoreOperation.DoubleLetter),
            dict(x=9, y=7, score=ScoreOperation.DoubleLetter),
            dict(x=13, y=7, score=ScoreOperation.DoubleLetter),
            dict(x=4, y=8, score=ScoreOperation.DoubleLetter),
            dict(x=12, y=8, score=ScoreOperation.DoubleLetter),
            dict(x=3, y=9, score=ScoreOperation.DoubleLetter),
            dict(x=7, y=9, score=ScoreOperation.DoubleLetter),
            dict(x=9, y=9, score=ScoreOperation.DoubleLetter),
            dict(x=13, y=9, score=ScoreOperation.DoubleLetter),
            dict(x=1, y=12, score=ScoreOperation.DoubleLetter),
            dict(x=8, y=12, score=ScoreOperation.DoubleLetter),
            dict(x=15, y=12, score=ScoreOperation.DoubleLetter),
            dict(x=7, y=13, score=ScoreOperation.DoubleLetter),
            dict(x=9, y=13, score=ScoreOperation.DoubleLetter),
            dict(x=4, y=15, score=ScoreOperation.DoubleLetter),
            dict(x=12, y=15, score=ScoreOperation.DoubleLetter),

            dict(x=6, y=2, score=ScoreOperation.TripleLetter),
            dict(x=10, y=2, score=ScoreOperation.TripleLetter),
            dict(x=2, y=6, score=ScoreOperation.TripleLetter),
            dict(x=6, y=6, score=ScoreOperation.TripleLetter),
            dict(x=10, y=6, score=ScoreOperation.TripleLetter),
            dict(x=14, y=6, score=ScoreOperation.TripleLetter),
            dict(x=2, y=10, score=ScoreOperation.TripleLetter),
            dict(x=6, y=10, score=ScoreOperation.TripleLetter),
            dict(x=10, y=10, score=ScoreOperation.TripleLetter),
            dict(x=14, y=10, score=ScoreOperation.TripleLetter),
            dict(x=6, y=14, score=ScoreOperation.TripleLetter),
            dict(x=10, y=14, score=ScoreOperation.TripleLetter),
        ]
        return scored_fields

    def add_tiles(self, player_tiles):
        for tile in player_tiles:
            self.fields.append(Field(tile["x"], tile["y"], tile["letter"]))

    def get_letter_score(self, letter: str):
        return self.letter_scores[letter]

    def get_score(self, player_move):
        score = 0
        word_operations = []
        for field in player_move:
            score_operation = self.get_score_operations(field["x"], field["y"])
            if score_operation is ScoreOperation.TripleWord or score_operation is ScoreOperation.DoubleWord:
                word_operations.append(score_operation)
                score += (self.get_letter_score(field["letter"]))
            elif score_operation is ScoreOperation.DoubleLetter:
                score += (self.get_letter_score(field["letter"]) * 2)
            elif score_operation is ScoreOperation.TripleLetter:
                score += (self.get_letter_score(field["letter"]) * 3)
            elif score_operation is None:
                score += (self.get_letter_score(field["letter"]))

        if ScoreOperation.DoubleWord in word_operations:
            score *= 2
        if ScoreOperation.TripleWord in word_operations:
            score *= 3
        return score

    def get_score_operations(self, x, y):
        for field in self.scored_fields:
            if field["x"] == x and field["y"] == y:
                return field["score"]

    def get_field(self, x, y) -> Field:
        for field in self.fields:
            if field.x == x and field.y == y:
                return field

    def get_letter(self, x, y) -> str:
        for field in self.fields:
            if field.x == x and field.y == y:
                return field.letter

    def is_in_board(self, tile):
        f = Field(tile['x'], tile['y'], tile['letter'])
        if f in self.fields:
            return True
        return False

    def is_empty(self):
        if len(self.fields) == 0:
            return True
        return False

    def number_of_fields_on_board(self) -> int:
        return len(self.fields)
