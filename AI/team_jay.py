rom AI.base import *

from pygame.math import Vector2 as Vec
import random

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.skill = []

        self.last_dir = random.randint(1, 😎

    def get_best_oil_position(self):
        my_pos = self.helper.get_player_position()
        oil_poses = self.helper.get_oils()
        oil_prices = self.helper.get_oils_distance_to_center()
        best_pos = None
        best_cp = -1
        for i in range(len(oil_poses)):
            cp = (400-oil_prices[i])/((Vec(my_pos) - Vec(oil_poses[i])).length()**2)
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

    def attack(self, carry, my_pos):
        players_value = self.helper.get_players_value()
        players_speed = self.helper.get_players_speed()
        players_position = self.helper.get_players_position()
        my_speed = self.helper.get_player_speed()
        maximum = 0
        target = -1
        for i in range(4):
            if self.helper.player_id == i:
                continue
            cp = 1e-3 * (players_value[i] - carry)/(((Vec(my_pos) - Vec(players_position[i])).length() / abs(players_speed[i] - my_speed + 1)))
            # print("{}th cp is {}".format(i, cp))
            if maximum <= cp:
                maximum = cp
                target = i
        return maximum, players_position[target]
    def decide(self):
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        best_pos, my_pos, best_cp = self.get_best_oil_position()
        home = self.helper.get_base_center()
        dest = best_pos
        home_cp = 5e-6 * carry if self.helper.get_distance(self.helper.get_base_center(), my_pos) \
                     <= self.helper.get_distance_to_center(self.helper.get_base_center()) \
                     else 3e-8 * carry * self.helper.get_distance(self.helper.get_base_center(), my_pos)

        if home_cp > best_cp:
            best_cp = home_cp
            dest = home
        attack_cp, target_pos = self.attack(carry, my_pos)
        # print("smooth")
        if attack_cp >= best_cp:
            dest = target_pos
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