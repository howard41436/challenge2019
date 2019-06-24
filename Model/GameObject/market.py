import Model.const as model_const
import View.const as view_const
import Model.GameObject.item as Item
from pygame.math import Vector2 as Vec
import random

class Market(object):
    def __init__(self, position):
        self.position = Vec(position)
        self.item = None

    def generate_item(self):
        self.item = Item.TheWorld()

    def sell(self):
        self.item = None 

    def update(self):
        if self.item == None and random.random() < view_const.market_generate_item_probability:
            self.generate_item()

