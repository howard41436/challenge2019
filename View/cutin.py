import pygame as pg

import View.const as view_const


class Cutin_manager():
    images = dict()

    @classmethod
    def init_convert(cls):
        cls.images = { _name: _image.convert_alpha() for _name, _image in cls.images }

    def __init__(self, model):
        self.model = model

    def update_state(self, player_index, skill_name, prev_screen):
        self.player_index = player_index
        self.skill_name = skill_name
        self.background = prev_screen

    def draw(self, screen):
        screen.fill((255, 255, 255))

        pg.display.flip()


def init_cutin():
    Cutin_manager.init_convert()
