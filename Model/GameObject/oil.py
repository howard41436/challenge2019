import Model.const as model_const
import View.const as view_const
import numpy as np
import math
import random
from pygame.math import Vector2 as Vec

class Oil(object):
    def __init__(self, pos, price):
        self.position = pos
        self.price = price
        self.radius = model_const.oil_radius
        self.level = None

    def update(self):
        pass

def calc_price(pos):
    game_center = Vec(
        view_const.game_size[0] / 2,
        view_const.game_size[1] / 2
        )
    dist_from_center = (pos - game_center).length()
    mean = model_const.curve_a / (dist_from_center + model_const.curve_b)
    price = max(
        min(
        model_const.price_max,
        np.random.normal(mean, model_const.price_scale)
        ),
        model_const.price_min
        )
    return price

def level_determined(price):
    if price <= 400:
        self.level = 1
    elif price <= 600:
        self.level = 2
    elif price <= 800:
        self.level = 3
    else:
        self.level = 4

def new_oil(): 
    R = random.random() * (view_const.game_size[0] / 2)
    theta = random.random() * 2 * np.pi
    pos = Vec(
	R * math.cos(theta) + view_const.game_size[0] / 2,
	R * math.sin(theta) + view_const.game_size[0] / 2
        )
    price = calc_price(pos)
    level_determined(price)
    return Oil(pos, price) 
