"""
define Application Programming Interface(API) 
"""
from pygame.math import Vector2 as Vec

import Model.const as model_const
import View.const as view_const

class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.index = index

    # Get constants
    def get_oil_radius(self):
        return model_const.oil_radius
    def get_player_radius(self):
        return model_const.player_radius
    def get_bag_capacity(self):
        return model_const.bag_capacity
    def get_player_normal_speed(self):
        return model_const.player_normal_speed
    def get_base_length(self):
        return model_const.base_length
    
    def get_game_size(self):
        return view_const.game_size

    # Get player data
    def get_players_position(self):
        return [Vec(player.position) for player in self.model.player_list]
    def get_player_position(self, player_id):
        return Vec(self.model.player_list[player_id].position)

    def get_players_direction(self):
        return [Vec(player.direction) for player in self.model.player_list]
    def get_player_direction(self, player_id):
        return Vec(self.model.player_list[player_id].direction)

    def get_players_value(self):
        return [player.value for player in self.model.player_list]
    def get_player_value(self, player_id):
        return self.model.player_list[player_id].value

    def get_players_bag(self):
        return [player.bag for player in self.model.player_list]
    def get_player_bag(self, player_id):
        return self.model.player_list[player_id].bag

    def get_players_is_AI(self):
        return [player.is_AI for player in self.model.player_list]
    def get_player_is_AI(self, player_id):
        return self.model.player_list[player_id].is_AI

    def get_players_speed(self):
        return [player.speed for player in self.model.player_list]
    def get_player_speed(self, player_id):
        return self.model.player_list[player_id].speed

    # Get pet data

    # Get oil data
    def get_oils(self):
        return [Vec(oil.position) for oil in self.model.oil_list]

    # Get base data
    def get_bases_center(self):
        return [Vec(base.center) for base in self.model.base_list]
    def get_base_center(self, player_id):
        return Vec(self.model.base_list[player_id])
        
    # Get game informations
    def get_timer(self):
        return self.model.timer

    # Extra functions
    def get_nearest_oil(self, player_id):
        my_pos = self.get_player_position(player_id)
        oils = self.get_oils()
        return min(oils, key=lambda oil: (oil - my_pos).magnitude())
    
    def get_most_valuable_player(self):
        return max(range(4), key=lambda i: self.get_player_value(i))

