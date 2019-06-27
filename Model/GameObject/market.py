from pygame.math import Vector2 as Vec

import Model.const as model_const
import View.const as view_const
import Model.GameObject.item as Item
import random

class Market(object):
    def __init__(self, position, is_free=False):
        self.position = Vec(position)
        self.item = None
        if is_free:
            self.item_list = [getattr(Item, item_name) for item_name, is_activate in model_const.free_item_activate.items() if is_activate == True]
        else:
            self.item_list = [getattr(Item, item_name) for item_name, is_activate in model_const.priced_item_activate.items() if is_activate == True]
        self.timer = 0


    def generate_item(self, player_list, oil_list, base_list, player_index):
        self.item = random.choice(self.item_list)(player_list, oil_list, base_list, player_index)

    def sell(self):
        self.item = None
        self.timer = model_const.market_cd_time

    def update(self, player_list, oil_list, base_list, player_index):
        if self.timer == 0:
            if self.item is None:
                self.generate_item(player_list, oil_list, base_list, player_index)
            elif self.item is not None and random.random() < model_const.market_refresh_item_probability:
                self.generate_item(player_list, oil_list, base_list, player_index)
        else:
            self.timer -= 1
                

