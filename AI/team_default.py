from AI.base import *

from pygame.math import Vector2 as Vec
import random

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.skill = []

        self.last_dir = random.randint(1, 8)

    def get_best_oil_position(self):
        my_pos = self.helper.get_my_data().position
        oils = self.helper.get_all_oil_data()
        best_pos = None
        best_cp = -1
        for pos, price in oils:
            cp = price / (my_pos - pos).length()
            if cp > best_cp:
                cp = best_cp
                best_pos = pos
        return best_pos

    def decide(self):
        if not random.randint(0, 9) % 10:
            self.last_dir = random.randint(1, 8)
        return self.last_dir
