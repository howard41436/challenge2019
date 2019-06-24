"""
define Application Programming Interface(API) 
"""
import Model.const as model_const
import View.const as view_const
from pygame.math import Vector2 as Vec

class Player_data(object):
    def __init__(self, player):
        # TODO: Get player score
        self.value = player.value
        self.speed = player.speed
        self.radius = player.radius
        self.position = player.position

class Helper(object):

    def __init__(self, model, index):
        self.model = model
        self.index = index

    def get_all_oil_data(self):
        return [ (tuple(oil.position), oil.price) for oil in self.model.oil_list ]

    # my info
    def get_my_data(self):
        return Player_data(self.model.player_list[self.index])
    
    def get_base_position(self):
        return self.model.base_list[self.index]

    def get_all_player_data(self):
        return [ Player_data(player) for player in self.model.player_list ]
