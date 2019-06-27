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
            cp = 1/(Vec(my_pos) - Vec(oil_poses[i])).length()
            if cp > best_cp:
                best_cp = cp
                best_pos = oil_poses[i]
        return best_pos, my_pos, best_cp
    def get_dir(self, dest, my_pos):
        direct = [
        [0, 0],             #steady
        [0, -1],             #up
        [0.707, -0.707],     #up right
        [1, 0],             #right
        [0.707, 0.707],    #right down
        [0, 1],            #down
        [-0.707, 0.707],   #left down
        [-1, 0],            #left
        [-0.707, -0.707],    #left up
        ]
        new = Vec(dest) - Vec(my_pos)
        maximum = 0
        record = 0
        for i in range(9):
            if maximum < (new).dot(Vec(direct[i])):
                maximum = (new).dot(Vec(direct[i]))
                record = i
        return record

    def decide(self):
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        best_pos, my_pos, best_cp = self.get_best_oil_position()
        home = self.helper.get_base_center()
        dest = best_pos
        if dest is None:
            return 0
        if carry > 5000:
            dest = home
        return self.get_dir(dest, my_pos)
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