import View.const      as view_const
import Model.const     as model_const

from pygame.math import Vector2 as Vec
import random

class Player(object):
    def __init__(self, name, index, equipments = [0, 0, 0], is_AI = False):
        self.index = index
        self.name = name
        self.bag = 0
        self.radius = model_const.player_radius
        self.position = Vec(model_const.base_center[self.index])
        self.color = [ random.randint(0, 255) for _ in range(3) ]
        self.value = 0
        self.is_AI = is_AI
        self.direction = Vec(0, 0)
        self.oil_multiplier = 1  # the oil player gains will be multiplied with this value
        self.insurance_value = model_const.init_insurance  # when collide, the player can keep at least this oil
        self.speed = model_const.player_normal_speed
        self.pet = None
        self.init_equipments(equipments)

    def init_equipments(self, equipments):
        self.speed_multiplier = model_const.speed_multiplier ** equipments[model_const.speed_up_idx]
        self.speed *= self.speed_multiplier
        self.oil_multiplier = model_const.oil_multiplier ** equipments[model_const.oil_up_idx]
        self.insurance_value = model_const.init_insurance * equipments[model_const.insurance_idx]

    def pick_oil(self, oils):
        for i, oil in reversed(list(enumerate(oils))):
            if (oil.position - self.position).length_squared() <= (oil.radius + self.radius)**2:
                if self.bag + oil.price <= model_const.bag_capacity:
                    self.bag += oil.price
                    self.value += oil.price
                    oils.remove(oil)

    def store_price(self, bases):
        if self.position[0] <= bases[self.index].center[0] + bases[self.index].length/2 \
            and self.position[0] >= bases[self.index].center[0] - bases[self.index].length/2 \
            and self.position[1] <= bases[self.index].center[1] + bases[self.index].length/2 \
            and self.position[1] >= bases[self.index].center[1] - bases[self.index].length/2:
            bases[self.index].change_value_sum(self.value)
            self.value = 0
            self.bag = 0

    def check_collide(self, player_list):
        collide = []
        sum_of_all = 0
        for player in player_list:
            if (player.position - self.position).length() <= self.radius + player.radius:
                collide.append(player)
                sum_of_all += max(player.value - player.insurance_value, 0)
        for player in collide:
            player.value = min(player.value, player.insurance_value)
            player.value += sum_of_all / len(collide)
            player.bag = sum_of_all / len(collide)

    def update_speed(self):
        self.speed = self.speed_multiplier * max(model_const.player_speed_min, model_const.player_normal_speed - model_const.player_speed_decreasing_rate * self.bag)

    def update(self, oils, bases, players):
        self.update_speed()
        new_x = self.position[0] + self.direction[0] * self.speed
        new_y = self.position[1] + self.direction[1] * self.speed
        if new_x < self.radius or new_x > view_const.game_size[0] - self.radius:
            self.direction[0] = 0
        if new_y < self.radius or new_y > view_const.game_size[1] - self.radius:
            self.direction[1] = 0
        self.position += Vec(self.direction) * self.speed
        self.pick_oil(oils)
        self.store_price(bases)
        self.check_collide(players)

