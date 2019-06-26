from pygame.math import Vector2 as Vec

import Model.const as model_const
import View.const as view_const
import Model.GameObject.item as Item
import random

class Market(object):
    item_list = [getattr(Item, item_name) for item_name, is_activate in model_const.item_activate.items() if is_activate == True]
    def __init__(self, position):
        self.position = Vec(position)
        self.item = None

    def generate_item(self, player_list, oil_list, base_list, player_index):
        self.item = random.choice(self.item_list)(player_list, oil_list, base_list, player_index)

    def sell(self):
        print(self.item.price)
        self.item = None 

    def update(self, player_list, oil_list, base_list, player_index):
        if self.item is None and random.random() < model_const.market_generate_item_probability:
            self.generate_item(player_list, oil_list, base_list, player_index)
        elif self.item is not None and random.random() < model_const.market_refresh_item_probability:
            self.generate_item(player_list, oil_list, base_list, player_index)
                

