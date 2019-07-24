import Model.const as model_const

from pygame.math import Vector2 as Vec

class Base(object) :
    __slots__ = ('owner_index', 'value_sum', 'center', 'length')

    def __init__(self, owner_index, center) :
        self.owner_index = owner_index
        self.value_sum = 0
        """
        Base is a square, given the center position and length of the square
        """
        self.center = Vec(center)
        self.length = model_const.base_length

    def put_oil(self, oil) :
        self.value_sum += oil.price

    def change_value_sum(self, delta) :
        self.value_sum += delta

    def get_value_sum(self) :
        return self.value_sum

    def get_position(self) :
        return (self.center, self.length)

