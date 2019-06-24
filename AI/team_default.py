from AI.base import *

from pygame.math import Vector2 as Vec
import random

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.skill = []

        self.last_dir = random.randint(1, 8)

    def get_best_oil_position(self):
        my_pos = self.helper.get_player_position(3)
        oils = self.helper.get_oils_item()
        best_pos = None
        best_cp = -1
        for oil in oils:
            cp = oil.price / (Vec(my_pos) - Vec(oil.position)).length()
            if cp > best_cp:
                cp = best_cp
                best_pos = oil.position
        return best_pos, my_pos

    def decide(self):
        radius = self.helper.get_player_radius()
        carry = self.helper.get_player_value(3)
        best_pos, my_pos = self.get_best_oil_position()
        home = self.helper.get_base_center(3)
        if carry > 2000:
            if home[1] - my_pos[1] < -radius: return DIR_U
            if home[0] - my_pos[0] > radius: return DIR_R
            if home[0] - my_pos[0] < -radius: return DIR_L
            if home[1] - my_pos[1] > radius: return DIR_D
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