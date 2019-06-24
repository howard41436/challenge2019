from AI.base import *

from pygame.math import Vector2 as Vec
import random
import math

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.skill = []
        self.last_dir = random.randint(1, 8)

<<<<<<< HEAD
    def get_best_oil_vec(self):
        my_pos = self.helper.get_player_position(self.helper.index)
        oils = self.helper.get_all_oil_data()
        best_pos = None
        best_cp = -1
        for pos, price in oils:
            cp = price / ((my_pos - pos).length() ** (3/2)) 
            if cp > best_cp:
                cp = best_cp
                best_pos = pos
        return (best_pos - my_pos)

    def get_best_player_to_comminism(self):
        myself = self.helper.get_my_data()
        other = self.helper.get_all_player_data()
        best_pos = None
        best_cp = -1

    def decide(self):
        AI_move_dir = 0
        vec_dot = 0
        best_oil_vec = Vec( self.get_best_oil_vec() )
        for dir_vec in AI_dir_mapping:
            if Vec(dir_vec).dot(best_oil_vec) > vec_dot:
                vec_dot = Vec(dir_vec).dot(best_oil_vec)
                AI_move_dir = AI_dir_mapping.index(dir_vec)
        return AI_move_dir

=======
    def get_best_oil_position(self):
        my_pos = self.helper.player_radius
        oil_poses = self.helper.get_oils()
        oil_prices = self.helper.get_oils_price()
        best_pos = None
        best_cp = -1
        for i in range(len(oil_poses)):
            cp = oil_prices[i] / (Vec(my_pos) - Vec(oil_poses[i])).length()
            if cp > best_cp:
                cp = best_cp
                best_pos = oil_poses[i]
        return best_pos, my_pos

    def decide(self):
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        best_pos, my_pos = self.get_best_oil_position()
        home = self.helper.get_base_center()
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
>>>>>>> a42a0b844b5fd320e2517e602a65947d8a991f21
