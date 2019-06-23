import Model.const as model_const
import View.const as view_const

from pygame.math import Vector2 as Vec

class Oil(object):
    def __init__(self, pos, price, weight):
        self.position = Vec(pos)
        self.price = price
        self.weight = weight
        self.radius = model_const.oil_radius

    def update(self):
        pass
