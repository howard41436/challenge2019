import View.const      as view_const
import Model.const     as model_const

from pygame.math import Vector2 as Vec
import random

class Player(object):
    def __init__(self, name, index, equipments = [0, 0, 0], is_AI = False):
        self.index = index
        self.name = name
        self.radius = model_const.player_radius
        self.position = Vec(model_const.base_center[self.index])
        self.color = [ random.randint(0, 255) for _ in range(3) ]
        self.value = 0
        self.is_AI = is_AI
        self.direction = Vec(0, 0)
        self.direction_no = model_const.player_initial_direction_no[index]
        self.oil_multiplier = 1  # the oil player gains will be multiplied with this value
        self.insurance_value = model_const.init_insurance  # when collide, the player can keep at least this oil
        self.speed = model_const.player_normal_speed
        self.pet = pet_list[index]
        self.init_equipments(equipments)
        self.item = None
        self.is_invincible = False
        self.magnet_attract = False #Use Magnet Attract to make it true
        self.freeze = False   # If one of the other players is use 'The World', then self is freeze

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_item(self):
        return self.item

    def init_equipments(self, equipments):
        self.speed_multiplier = model_const.speed_multiplier ** equipments[model_const.speed_up_idx]
        self.speed *= self.speed_multiplier
        self.oil_multiplier = model_const.oil_multiplier ** equipments[model_const.oil_up_idx]
        self.insurance_value = model_const.init_insurance * equipments[model_const.insurance_idx]
        self.pet.carry_max *= model_const.pet_carry_max_up_multiplier ** equipments[model_const.pet_carry_max_up_idx]
        self.pet.speed *= model_const.pet_speed_multiplier ** equipments[model_const.pet_speed_up_idx]

    def use_item(self, ev_manager):
        if self.item is not None and not self.item.active:
            self.item.trigger(ev_manager)

    def pick_oil(self, oils):
        for i, oil in reversed(list(enumerate(oils))):
            if (oil.position - self.position).length_squared() <= (oil.radius + self.radius)**2:
                if self.value + oil.price * self.oil_multiplier <= model_const.bag_capacity:
                    self.value += oil.price * self.oil_multiplier
                    oils.remove(oil)

    def store_price(self, bases):
        if self.position[0] <= bases[self.index].center[0] + bases[self.index].length/2 \
            and self.position[0] >= bases[self.index].center[0] - bases[self.index].length/2 \
            and self.position[1] <= bases[self.index].center[1] + bases[self.index].length/2 \
            and self.position[1] >= bases[self.index].center[1] - bases[self.index].length/2:
            bases[self.index].change_value_sum(self.value)
            self.value = 0

    def check_collide(self, player_list):
        collide = []
        sum_of_all = 0
        for player in player_list:
            if player.is_invincible:
                continue
            if (player.position - self.position).length() <= self.radius + player.radius:
                collide.append(player)
                sum_of_all += max(player.value - player.insurance_value, 0)
        for player in collide:
            player.value = min(player.value, player.insurance_value)
            player.value += sum_of_all / len(collide)
            player.bag = sum_of_all / len(collide)

    def check_market(self, market_list):
        for market in market_list:
            if (market.position - self.position).length() <= self.radius + model_const.market_radius:
                return market
        return None

    def buy(self, market_list):
        market = self.check_market(market_list)
        if market and market.item is not None and self.value >= market.item.price:
            self.value -= market.item.price
            self.item = market.item
            self.item.player_index = self.index
            market.sell()

    def update_speed(self):
        self.speed = self.speed_multiplier * max(model_const.player_speed_min, model_const.player_normal_speed - model_const.player_speed_decreasing_rate * self.value)

    def update(self, oils, bases, players, ev_manager):
        if self.item is not None and self.item.active:
            self.item.update(ev_manager)
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
        if not self.is_invincible:
            self.check_collide(players)
