from AI.base import *

from pygame.math import Vector2 as Vec
import random
import math

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.skill = []
        self.last_dir = random.randint(1, 8)

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

