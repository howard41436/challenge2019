from AI.base import *

from pygame.math import Vector2 as Vec
import random

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.skill = []

        self.last_dir = random.randint(1, 8)

    def get_best_oil_position(self):
        my_pos = self.helper.get_player_position()
        oil_poses = self.helper.get_oils()
        oil_prices = self.helper.get_oils_distance_to_center()
        best_pos = None
        best_cp = -1
        for i in range(len(oil_poses)):
            cp = (400-oil_prices[i])/((Vec(my_pos) - Vec(oil_poses[i])).length()**2)
            if cp > best_cp:
                cp = best_cp
                best_pos = oil_poses[i]
        return best_pos, my_pos, best_cp

    def decide(self):
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        best_pos, my_pos, best_cp = self.get_best_oil_position()
        home = self.helper.get_base_center()
        dest = best_pos
        #home_cp = carry 
        if carry > 5000:
            dest = home
        togo = [DIR_U, DIR_RU, DIR_LU] if dest[1] - my_pos[1] < -radius else [DIR_D, DIR_RD, DIR_LD]
        if dest[0] - my_pos[0] > radius:
            togo = togo[1]
        if dest[0] - my_pos[0] < -radius:
            togo = togo[2]
        else:
            togo = togo[0]
        return togo
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