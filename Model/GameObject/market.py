import Model.const as model_const
import View.const as view_const
import Model.GameObject.item as 
import random

class Market(object):
    def __init__(self, position):
        self.position = position
        self.state = 0
        self.item = None

    def generate_item(self):
        pass

    def update(self):
        if random.random() < view_const.market_generate_item_probability:
            self.generate_item()

