"""
define Application Programming Interface(API)
"""
from pygame.math import Vector2 as Vec

import Model.const as model_const
import Model.GameObject.item as Item
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
        self.market_position = tuple(model_const.priced_market_positions[0])
        self.market_radius = model_const.market_radius
        self.radius_not_move_radius = model_const.radius_not_move_radius
        self.radius_of_radiation_oil = model_const.radiation_oil_range
        self.radius_of_magnetic_attract = model_const.magnet_attract_radius

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

    def get_players_is_invincible(self):
        return [player.in_invincible for player in self.model.player_list]
    def get_player_is_invincible(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].is_invincible
    
    def get_players_insurance_value(self):
        return [player.insurance_value for player in self.model.player_list]
    def get_player_insurance_value(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].insurance_value


    # Get pet data

    # Get oil data
    def get_oils(self):
        return [tuple(oil.position) for oil in self.model.oil_list]
    def get_oils_level(self):
        return [oil.level for oil in self.model.oil_list]
    def get_oils_distance_to_center(self):
        return [self.get_distance_to_center(oil) for oil in self.get_oils()]
    def get_oils_by_distance_from_center(self):
        return sorted(self.get_oils(), key=lambda p: self.get_distance_to_center(p))

    # Get base data 
    def get_bases_center(self):
        return [tuple(base.center) for base in self.model.base_list]
    def get_base_center(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return tuple(self.model.base_list[player_id].center)
    def get_base_value(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.base_list[self.player_id].value_sum
    def get_bases_value(self):
        return [base.value_sum for base in self.model.base_list]

    # Get market data
    def get_market(self):
        market = self.model.priced_market_list[0]
        return (None, None, market.timer) if market.item is None else (market.item.name, market.item.price, 0)
    def player_in_market(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return True if self.model.player_list[player_id].check_market(self.model.priced_market_list) is not None else False
    def get_market_center(self):
        market = self.model.priced_market_list[0]
        return market.position

    # Get item data
    def get_player_item_name(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return None if self.model.player_list[player_id].item == None else self.model.player_list[player_id].item.name

    def get_player_item_is_active(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return False if self.model.player_list[player_id].item == None else self.model.player_list[player_id].item.active

    def get_player_item_duration(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return 0 if self.model.player_list[player_id].item == None else self.model.player_list[player_id].item.duration

    # Get game informations
    def get_timer(self):
        return self.model.timer

    # Extra functions
    def get_nearest_player(self, player_id = None):
        if player_id == None: player_id = self.player_id
        my_pos = self.get_player_position(player_id)
        players = self.get_players_position()
        min_distance = 800
        id = None
        for i in range(len(players)):
            if i == player_id:
                continue 
            if (Vec(players[i]) - Vec(my_pos)).length() < min_distance:
                min_distance = (Vec(players[i]) - Vec(my_pos)).length()
                id = i 
        return id

    def get_nearest_oil(self, player_id = None):
        if player_id == None: player_id = self.player_id
        my_pos = self.get_player_position(player_id)
        oils = self.get_oils()
        if len(oils) == 0:
            return None
        else:
            return min(oils, key=lambda oil: (Vec(oil) - Vec(my_pos)).length())

    def get_most_valuable_player(self):
        return max(range(4), key=lambda i: self.get_player_value(i))


    # Useful (?) functions
    def get_distance(self, p1, p2):
        return (Vec(p1) - Vec(p2)).length()
    def get_distance_to_center(self, p1):
        return self.get_distance(p1, Vec(self.game_size) / 2)
    def get_direction(self, vector_to_go):
        move_dir = 0 #default
        vec_dot = 0
        for dir_vec in model_const.dir_mapping:
            if Vec(dir_vec).dot(Vec(vector_to_go)) > vec_dot:
                vec_dot = Vec(dir_vec).dot(Vec(vector_to_go))
                move_dir = model_const.dir_mapping.index(dir_vec)
        return move_dir
