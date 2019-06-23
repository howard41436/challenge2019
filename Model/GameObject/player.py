import View.const      as view_const
import Model.const     as model_const

from pygame.math import Vector2 as Vec
import random

class Player(object):
    def __init__(self, name, index):
        self.index = index
        self.name = name
        self.bag = 0
        self.radius = 10
        self.position = Vec(1, 1)#TODO add position in view_const Vec(view_const.position[index])
        self.color = [ random.randint(0,255) for _ in range(3) ]
        self.value = 0
        self.is_AI = False
        self.direction = Vec(0, 0)

    def pick_oil(self, oils):
        for i, e in reversed(list(enumerate(oils))):
            if Vec.magnitude(e.position - self.position) <= e.radius + self.radius:
                if self.bag + e.weight <= model_const.bag_capacity:
                    self.bag += e.weight
                    self.value += e.price
                    oils.remove(i)

    def store_price(self, bases):
        if self.position[0] <= bases[self.index].center[0] + bases[self.index].length/2 \
            and self.position[0] >= bases[self.index].center[0] - bases[self.index].length/2 \
            or self.position[1] <= bases[self.index].center[1] + bases[self.index].length/2 \
            and self.position[1] >= bases[self.index].center[1] - bases[self.index].length/2:
            bases[self.index].change_value_sum(self.price)
            self.price = 0

    def check_collide(self, players):
        collide = []
        sum_of_all = 0
        for player in players:
            if player is self:
                continue
            if Vec.magnitude(player.position - self.position) <= self.radius + player.radius:
                collide.append(player.index)
                sum_of_all += player.price
        sum_of_all += self.price
        self.price = sum_of_all / (len(collide) + 1)
        for player in collide :
            player.price = sum_of_all / (len(collide) + 1)
        
    def update(self, oils, bases, players):
        if self.position[0] + self.direction[0] < model_const.size \
            or self.position[0] + self.direction[0] > view_const.size - model_const.size:
            self.direction[0] = 0
        if self.position[1] + self.direction[1] < model_const.size \
            or self.position[1] + self.direction[1] > view_const.size - model_const.size:
            self.direction[1] = 0
        self.position += Vec(self.direction)
        self.pick_oil(oils)
        self.store_price(bases)
        self.check_collide(players)

