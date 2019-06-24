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
        return best_pos, my_pos

    def decide(self):
        radius = self.helper.get_my_data().radius
        best_pos, my_pos = self.get_best_oil_position()
        home = self.helper.get_base_position()
        if 
        if best_pos[1] - my_pos[1] < -radius: return DIR_U
        if best_pos[0] - my_pos[0] > radius: return DIR_R
        if best_pos[0] - my_pos[0] < -radius: return DIR_L
        if best_pos[1] - my_pos[1] > radius: return DIR_D
"""
DIR_stop = 0
DIR_U    = 1
DIR_RU   = 2
DIR_R    = 3
DIR_RD   = 4
DIR_D    = 5
DIR_LD   = 6
DIR_L    = 7
DIR_LU   = 8
"""