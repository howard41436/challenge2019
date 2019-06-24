"""
define Application Programming Interface(API) 
"""
from pygame.math import Vector2 as Vec

import Model.const as model_const
import View.const as view_const

class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index
        self.oil_radius = model_const.oil_radius
        self.player_radius = model_const.player_radius
        self.bag_capacity = model_const.bag_capacity
        self.player_normal_speed = model_const.player_normal_speed
        self.base_length = model_const.base_length
        self.game_size = view_const.game_size
        

    # Get player data
    def get_self_id(self):
        return self.player_id

    def get_players_position(self):
        return [tuple(player.position) for player in self.model.player_list]
    def get_player_position(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return tuple(self.model.player_list[player_id].position)

    def get_players_direction(self):
        return [tuple(player.direction) for player in self.model.player_list]
    def get_player_direction(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return tuple(self.model.player_list[player_id].direction)

    def get_players_value(self):
        return [player.value for player in self.model.player_list]
    def get_player_value(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].value

    def get_players_bag(self):
        return [player.bag for player in self.model.player_list]
    def get_player_bag(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].bag

    def get_players_is_AI(self):
        return [player.is_AI for player in self.model.player_list]
    def get_player_is_AI(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].is_AI

    def get_players_speed(self):
        return [player.speed for player in self.model.player_list]
    def get_player_speed(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].speed

    # Get pet data

    # Get oil data
    def get_oils(self):
        return [tuple(oil.position) for oil in self.model.oil_list]

    # Get base data
    def get_bases_center(self):
        return [tuple(base.center) for base in self.model.base_list]
    def get_base_center(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return tuple(self.model.base_list[player_id])
        
    # Get game informations
    def get_timer(self):
        return self.model.timer

    # Extra functions
    def get_nearest_player(self, player_id = None):
        if player_id == None: player_id = self.player_id
        my_pos = self.get_player_position(player_id)
        players = self.get_players_position()
        return min(players.remove(my_pos), key=lambda player: (player - my_pos).magnitude())

    def get_nearest_oil(self, player_id = None):
        if player_id == None: player_id = self.player_id
        my_pos = self.get_player_position(player_id)
        oils = self.get_oils()
        return min(oils, key=lambda oil: (oil - my_pos).magnitude())
    
    def get_most_valuable_player(self):
        return max(range(4), key=lambda i: self.get_player_value(i))


