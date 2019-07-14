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
        my_pos = self.helper.get_player_position()
        oils = self.helper.get_oils()
        best_pos = None
        best_cp = -1
        for pos in oils:
            price = ( 1/self.helper.get_distance_to_center(pos) )
            cp = price / (self.helper.get_distance(pos, my_pos) ** (1/2)) 
            if cp > best_cp:
                cp = best_cp
                best_pos = pos 
        return Vec(best_pos) - Vec(my_pos)

    def go_home(self):
        my_pos = self.helper.get_player_position()
        if self.helper.get_distance(self.helper.get_nearest_oil(), my_pos) < 1/2*self.helper.player_radius():
            return self.direction(Vec(self.helper.get_nearest_oil.()) - Vec(my_pos))
        else:
            return self.direction(Vec(self.helper.get_base_center.()) - Vec(my_pos))

    def direction(self, pos_vec):
        vec_dot = 0
        for dir_vec in AI_dir_mapping:
            if Vec(dir_vec).dot(pos_vec) > vec_dot:
                vec_dot = Vec(dir_vec).dot(pos_vec)
                AI_move_dir = AI_dir_mapping.index(dir_vec)
        return AI_move_dir

    def decide(self):
        AI_move_dir = 0
        best_oil_vec = self.get_best_oil_vec()
        if self.helper.get_player_value() > 2000:
            return self.go_home()
        else:
            return self.direction(best_oil_vec)
    
    """
    def get_best_player_to_comminism(self):
        myself = self.helper.get_my_data()
        other = self.helper.get_all_player_data()
        best_pos = None
        best_cp = -1
    """

"""
const of AI code use.
"""
AI_DIR = [0, 1 ,2 ,3 ,4 ,5 ,6, 7, 8]
AI_dir_mapping = [
    [0, 0],             #steady
    [0, -1],             #up
    [0.707, -0.707],     #up right
    [1, 0],             #right
    [0.707, 0.707],    #right down
    [0, 1],            #down
    [-0.707, 0.707],   #left down
    [-1, 0],	        #left
    [-0.707, -0.707],    #left up
]