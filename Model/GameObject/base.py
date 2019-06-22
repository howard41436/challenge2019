from pygame.math import Vector2 as Vec
from Model.const as modelconst

class Base(object) :
    def __init__(self, owner_index, center) :
        self.owner_index = owner_index
        self.value_sum = 0
        """
        Base is a square, given the center position and length of the square
        """
        self.center = center
        self.length = modelconst.base_length

    def put_oil(self, oil) :
        self.value_sum += oil.price

    def change_value_sum(self, delta) :
        self.value_sum += delta

    def get_value_sum(self) :
        return self.value_sum

    def get_position(self) :
        return (self.center, self.length)

