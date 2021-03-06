from pygame.math import Vector2 as Vec
from Events.Manager import EventBuyItem

import Model.const as model_const
import View.const as view_const
import Model.GameObject.item as Item
import numpy as np

class Market(object):
    __slots__ = ('position', 'item', 'item_list', 'p_distribution', 'timer', 'ev_manager')
    def __init__(self, position, ev_manager):
        self.position = Vec(position)
        self.item = None
        self.item_list, p = zip(*[(getattr(Item, item_name), model_const.item_weight[item_name]) for item_name, is_activate in model_const.priced_item_activate.items() if is_activate]) 
        self.p_distribution = p / np.sum(p)
        self.timer = 0
        self.ev_manager = ev_manager

    def generate_item(self, player_list, oil_list, base_list, player_index):
        self.item = np.random.choice(self.item_list, 1, p=self.p_distribution)[0](player_list, oil_list, base_list, player_index)

    def sell(self):
        self.timer = model_const.market_cd_time
        self.ev_manager.post(EventBuyItem(self.item))
        self.item = None

    def refresh(self):
        self.timer = model_const.market_cd_time
        self.item = None

    def update(self, player_list, oil_list, base_list, player_index):
        if self.timer == 0:
            self.refresh()
            self.generate_item(player_list, oil_list, base_list, player_list)
        self.timer -= 1

