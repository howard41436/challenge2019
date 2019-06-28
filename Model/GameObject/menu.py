from pygame.math import Vector2 as Vec
import View.const      as view_const
import Model.const     as model_const
from Events.Manager import *

class Menu_robot(object):
    def __init__(self, radius):
        self.radius = radius
        self.position = Vec(200 + radius, -view_const.screen_size[0] + radius)
        self.direction = Vec(1, 0)
        self.speed = player_normal_speed = 7
    def pick(self, oil_list):
        if (self.position - oil_list[0].position).length() > self.radius + oil_list[0].radius:
            self.position += self.direction * self.speed
        else:
            oil_list = []
    def go_home(self):
        home = 200 + self.radius
        if self.position[0] > home:
            self.position -= self.direction * self.speed
class Menu_oil(object):
    def __init__(self, radius):
        self.radius = radius
        self.position = Vec(view_const.screen_size[0] - radius, -view_const.screen_size[0] + radius)