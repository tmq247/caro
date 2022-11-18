from tabulate import tabulate
from termcolor import colored
import numpy as np
import random
from dataclasses import dataclass, field
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
        self.playerO = Players(name='playerO', sym=colored("O", "blue", attrs=["bold"]), score=[], total_score=0)
        self.playerX = Players(name='playerX', sym=colored("X", "red", attrs=["bold"]), score=[], total_score=0)
        self.draw = Players(name='Draw', sym='', score=[], total_score=0)
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
        score_ = set(player.score)
        for i in win_conditions:
            i = set(i)
            if len(i.difference(score_)) == 1:
                res = i.difference(score_).pop()
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

    def draw_check(self):
        draw = [s for s in self.spaces if isinstance(s, int)]
        if len(draw) == 0:
            self.draw.total_score += 1
            return True

    def reset(self):
        self.spaces.clear()
        self.playerO.score.clear()
        self.playerX.score.clear()
        self.spaces = self.init.copy()
