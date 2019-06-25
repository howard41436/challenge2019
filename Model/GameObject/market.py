from pygame.math import Vector2 as Vec

import Model.const as model_const
import View.const as view_const
import Model.GameObject.item as Item
import random

class Market(object):
    def __init__(self, position):
        self.position = Vec(position)
        self.item = None

    def generate_item(self, player_list, oil_list, base_list, player_index):
        self.item = Item.MagnetAttract(player_list, oil_list, base_list, player_index)

    def sell(self):
        self.item = None 

    def update(self, player_list, oil_list, base_list, player_index):
        if self.item == None and random.random() < model_const.market_generate_item_probability:
            self.generate_item(player_list, oil_list, base_list, player_index)

