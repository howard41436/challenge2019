'''
time span: 90 ticks

phase 1 (30 ticks): coming in
phase 2 (30 ticks): animation
phase 2 (30 ticks): faded
'''

import pygame as pg
import os
import View.const as view_const

from View.utils import scaled_surface


def load_and_scale(filename, scalar):
    return scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, filename)), scalar)


class Cutin_manager():
    images = {
        'background_red': load_and_scale('cutin_back_red.png', 1.51),
        'background_orange': load_and_scale('cutin_back_orange.png', 1.51),
        'background_green': load_and_scale('cutin_back_green.png', 1.51),
        'background_blue': load_and_scale('cutin_back_blue.png', 1.51),
    }

    color_of_player_index = ('blue', 'green', 'red', 'orange')

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def __init__(self, model):
        self.model = model

    def update_state(self, player_index, skill_name, prev_screen):
        print(player_index)
        self.player_index = player_index
        self.skill_name = skill_name
        self.background = prev_screen.copy()
        self.timer = 0

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        cutin_background = self.images[f'background_{self.color_of_player_index[self.player_index]}'].copy()

        if self.timer < 30:
            # phase 1
            screen.blit( cutin_background, ( -800 + (800/30*(self.timer+1)), 250) )

        elif 30 <= self.timer < 60:
            # phase 2
            screen.blit( cutin_background, (0, 250) )

        else:
            # phase 3
            cutin_background = cutin_background.convert()
            cutin_background.set_alpha(255/30*(90-self.timer))
            print('alpha:', cutin_background.get_alpha())
            screen.blit( cutin_background, (0, 250) )

        pg.display.flip()
        self.timer += 1


def init_cutin():
    Cutin_manager.init_convert()
