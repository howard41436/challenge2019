from pygame.math import Vector2 as Vec
import const as model_const
import view.const as view_const

class Oil(object):
    def __init__(self, pos, price, weight):
        self.position = Vec(pos)
        self.price = price
        self.weight = weight
        self.radius = model_const.oil_radius

    def update(self):
        pass
