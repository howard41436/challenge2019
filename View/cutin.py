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
        'front_blue': load_and_scale('cutin_front_blue.png', 0.9),
        'front_theworld': load_and_scale('cutin_front_theworld.png', 0.93),
    }

    color_of_player_index = ('blue', 'green', 'red', 'orange')

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def __init__(self, model):
        self.model = model

    def update_state(self, player_index, skill_name, prev_screen):
        self.player_index = player_index
        self.skill_name = skill_name
        self.background = prev_screen.copy()
        self.timer = 0

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        cutin_background = self.images[f'background_{self.color_of_player_index[self.player_index]}'].copy()
        cutin_front_player = self.images[f'front_blue']
        #cutin_front_skill = self.images[f'front_{self.skill_name}']
        cutin_front_skill = self.images[f'front_theworld']

        if self.timer < 30:
            # phase 1
            screen.blit( cutin_background, view_const.CUTIN_BACKGROUND_PHASE1_TOPLEFT + (800/30*(self.timer+1), 0) )
            screen.blit( cutin_front_skill, view_const.CUTIN_FRONT_SKILL_PHASE1_TOPLEFT + ((800/30*(self.timer+1)), 0) )
            screen.blit( cutin_front_player, view_const.CUTIN_FRONT_PLAYER_PHASE1_TOPLEFT + ((800/30*(self.timer+1)), 0) )

        elif 30 <= self.timer < 60:
            # phase 2
            screen.blit( cutin_background, view_const.CUTIN_BACKGROUND_PHASE2_TOPLEFT )
            screen.blit( cutin_front_skill, view_const.CUTIN_FRONT_SKILL_PHASE2_TOPLEFT + ((view_const.CUTIN_PHASE2_SHIFT/30*(self.timer-29)), 0) )
            screen.blit( cutin_front_player, view_const.CUTIN_FRONT_PLAYER_PHASE2_TOPLEFT + ((view_const.CUTIN_PHASE2_SHIFT/30*(self.timer-29)), 0) )

        else:
            # phase 3
            cutin_background.blit(cutin_front_skill, (view_const.CUTIN_FRONT_SKILL_PHASE3_TOPLEFT[0], view_const.CUTIN_FRONT_SKILL_PHASE3_TOPLEFT[1] - view_const.CUTIN_BACKGROUND_PHASE2_TOPLEFT[1]))
            cutin_background.blit(cutin_front_player, (view_const.CUTIN_FRONT_PLAYER_PHASE3_TOPLEFT[0], view_const.CUTIN_FRONT_PLAYER_PHASE3_TOPLEFT[1] - view_const.CUTIN_BACKGROUND_PHASE2_TOPLEFT[1]))
            cutin_background = cutin_background.convert()
            cutin_background.set_alpha(255/30*(90-self.timer))
            screen.blit( cutin_background, view_const.CUTIN_BACKGROUND_PHASE2_TOPLEFT )

        pg.display.flip()
        self.timer += 1


def init_cutin():
    Cutin_manager.init_convert()
