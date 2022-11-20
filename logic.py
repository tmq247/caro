from tabulate import tabulate
import numpy as np
import random
from dataclasses import dataclass
from itertools import cycle

win_conditions = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (1, 5, 9),
    (3, 5, 7)
)


@dataclass
class Players:
    id: int
    name: str
    sym: str
    score: list
    total_score: int
    player_list = []

    def __post_init__(self):
        self.player_list.append(self)


class Game:
    def __init__(self):
        self.init = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.spaces = self.init.copy()
        self.playerO = Players(id=1, name='playerO', sym='O', score=[], total_score=0)
        self.playerX = Players(id=2, name='playerX', sym='X', score=[], total_score=0)
        self.draw = Players(id=0, name='Draw', sym='', score=[], total_score=0)
        self.player = self.playerO
        self.mode = 1
        self.cycler = cycle(Players.player_list)

    def board(self):
        num = np.array(self.spaces)
        reshaped = num.reshape(3, 3)
        return tabulate(reshaped, tablefmt="plain")

    def ai_move(self):
        if self.predict_win(self.playerO):  # can AI win?
            return self.predict_win(self.playerO)
        elif self.predict_win(self.playerX):  # can player win?
            return self.predict_win(self.playerX)
        else:
            return random.choice([item for item in self.spaces if isinstance(item, int)])

    def predict_win(self, player):
        score = set(player.score)
        for i in win_conditions:
            i = set(i)
            if len(i.difference(score)) == 1:
                res = i.difference(score).pop()
                if res in self.spaces:
                    return res

    def move(self, play):
        self.spaces[play - 1] = self.player.sym
        return self.player.score.append(play)

    def win_check(self):
        draw = [s for s in self.spaces if isinstance(s, int)]
        if len(draw) == 0:
            self.draw.total_score += 1
            return self.draw

        score = set(self.player.score)
        for i in win_conditions:
            i = set(i)
            if len(i.intersection(score)) == 3:
                self.player.total_score += 1
                return self.player

    def reset(self):
        self.spaces.clear()
        self.playerO.score.clear()
        self.playerX.score.clear()
        self.spaces = self.init.copy()

    def full_reset(self):
        for i in Players.player_list:
            i.total_score = 0
        self.reset()
