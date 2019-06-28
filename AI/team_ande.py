from AI.base import *

from pygame.math import Vector2 as Vec
import random
import math

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.skill = []
        self.last_dir = random.randint(1, 8)

    def get_best_vec(self):
        my_speed = self.helper.get_player_speed()
        my_pos = self.helper.get_player_position()
        oils_pos = self.helper.get_oils()
        oils_value = self.helper.get_oils_level()
        players_speed = self.helper.get_players_speed()
        best_pos = None
        best_cp = 0
        attack_cp, victim_id, victim_pos = self.attack()
        home_cp = 1/10 * (self.helper.get_player_value()/200) ** 2 / (self.helper.get_distance(my_pos, self.helper.get_base_center()) + 1) ** 2
        for i in range(len(oils_pos)):
            level = oils_value[i]
            cp = level / (self.helper.get_distance(oils_pos[i], my_pos) ** 2 / my_speed) / (self.helper.get_distance(oils_pos[i], self.helper.get_base_center()) ** (1/2))
            players_pos = self.helper.get_players_position()
            """
            for i in range(len(players_pos)):
                if self.helper.player_id == i:
                    continue
                print (level / (self.helper.get_distance(players_pos[i], oils_pos[i]) ** 2 / abs(players_speed[i])) / (self.helper.get_distance(oils_pos[i], self.helper.get_base_center()) ** (1/2)))
                cp -= 1/10 * level / (self.helper.get_distance(players_pos[i], oils_pos[i]) ** 2 / abs(players_speed[i])) / (self.helper.get_distance(oils_pos[i], self.helper.get_base_center()) ** (1/2))
            """
            if cp > best_cp:
                best_cp = cp 
                best_pos = oils_pos[i] 
        #print ("attack cp = ", attack_cp)
        #print ("best_oil cp = ", best_cp)
        #print ("home_cp = ", home_cp)
        if max(attack_cp, best_cp, home_cp) == best_cp:
            #print ("attack")
            return Vec(best_pos) - Vec(my_pos)
        elif max(attack_cp, best_cp, home_cp) == attack_cp:
            #print ("get oil")
            return Vec(victim_pos) - Vec(my_pos)
        else:
            #print ("home")
            return self.go_home()
        
    def go_home(self):
        my_pos = self.helper.get_player_position()
        nearest_player_id = self.helper.get_nearest_player()
        nearest_player_pos = self.helper.get_player_position(nearest_player_id)
        if self.helper.get_distance(nearest_player_pos, my_pos) < 10*self.helper.player_radius and \
            self.helper.get_player_bag(nearest_player_id) < self.helper.get_player_bag():
            return (self.avoid(nearest_player_id))
        elif self.helper.get_nearest_oil() != None:
            if self.helper.get_distance(self.helper.get_nearest_oil(), my_pos) < 3*self.helper.player_radius:
                return (Vec(self.helper.get_nearest_oil()) - Vec(my_pos))
            else:
                return (Vec(self.helper.get_base_center()) - Vec(my_pos))
        else:
            return (Vec(self.helper.get_base_center()) - Vec(my_pos))

    def attack(self):
        my_pos = self.helper.get_player_position()
        players_pos = self.helper.get_players_position()
        players_value = self.helper.get_players_value()
        players_speed = self.helper.get_players_speed()
        my_speed = self.helper.get_player_speed()
        victim_id = None
        victim_pos = None
        best_cp = 0
        for i in range(len(players_pos)):
            if self.helper.player_id == i:
                continue
            if players_value[i] > self.helper.get_player_value() and players_speed[i] != my_speed:
                value_difference = (players_value[i] - self.helper.get_player_value()) / 2
                level = (value_difference - 400) / 200 + 1
                cp = level / (self.helper.get_distance(players_pos[i], my_pos)) / (self.helper.get_distance(players_pos[i], self.helper.get_base_center()) / abs(players_speed[i] - my_speed) )
                if self.helper.get_distance(players_pos[i], my_pos) / abs(players_speed[i] - my_speed) > 2/3*self.helper.get_distance(players_pos[i], self.helper.get_base_center(i)) / players_speed[i]:
                    cp = 0
                if cp > best_cp:
                    best_cp = cp
                    victim_id = i
                    victim_pos = players_pos[i]
        return (best_cp, victim_id, victim_pos)

    def avoid(self, player_id):
        my_pos = self.helper.get_player_position()
        player_pos = self.helper.get_player_position(player_id)
        vec1 = Vec(my_pos) - Vec(player_pos)
        vec2 = Vec(self.helper.get_base_center()) - Vec(my_pos)
        return (2*vec1 + vec2)

    def direction(self, pos_vec):
        if pos_vec == 9:
            return 9
        AI_move_dir = 0
        vec_dot = 0
        for dir_vec in AI_dir_mapping:
            if Vec(dir_vec).dot(pos_vec) > vec_dot:
                vec_dot = Vec(dir_vec).dot(pos_vec)
                AI_move_dir = AI_dir_mapping.index(dir_vec)
        return AI_move_dir

    def get_item(self):
        my_pos = self.helper.get_player_position()
        item_name, item_price, market_timer = self.helper.get_market()
        if item_name != None:
            if self.helper.get_player_item_name() == None and self.helper.get_player_value() >= item_price:
                if self.helper.player_in_market() is False:
                    return Vec(self.helper.get_market_center()) - Vec(my_pos)
                else:
                    return 9
            else:
                return None
        else:
            return None
            
    def decide(self):
        best_vec = self.get_best_vec()
        my_pos = self.helper.get_player_position()
        go_for_item = self.get_item()
        if go_for_item is not None:
            return self.direction(go_for_item)
        else:
            if self.helper.get_nearest_oil() != None:
                if self.helper.get_distance(self.helper.get_nearest_oil(), my_pos) < 2*self.helper.player_radius:
                    return self.direction(Vec(self.helper.get_nearest_oil()) - Vec(my_pos))
                else:
                    return self.direction(best_vec)
            else:
                return self.direction(best_vec)

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