from pygame.math import Vector2 as Vec

class Oil(object):
    def __init__(self, pos, price, weight):
        self.pos = Vec(pos)
        self.price = price
        self.weight = weight

    def update(self):
        pass
