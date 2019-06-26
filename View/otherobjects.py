import pygame as pg
import os.path
import math

import View.utils        as view_utils
import View.const        as view_const


'''
VERY IMPORTANT !!!
VERY IMPORTANT !!!
VERY IMPORTANT !!!

Once you add a new class in this module, you have to add CLASS.init_convert()
in the init_otherobjects() function!
'''


class __Object_base():
    images = tuple()

    @classmethod
    def init_convert(cls):
        cls.images = tuple( _image.convert_alpha() for _image in cls.images )


class View_players(__Object_base):
    images_player = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'player_{_color}.png')),
            0.2
        )
        for _color in ('blue', 'green', 'red', 'orange')
    )
    image_freeze = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'freeze.png')),0.5)

    @classmethod
    def init_convert(cls):
        cls.images_player = tuple( _image.convert_alpha() for _image in cls.images_player )
        cls.image_freeze = pg.Surface.convert_alpha( cls.image_freeze )

    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        players = self.model.player_list
        for _i in range(len(players)):
            angle = math.atan2(players[_i].direction.x, players[_i].direction.y) / math.pi * 180
            image = pg.transform.rotate(self.images_player[_i], angle)
            if players[_i].freeze: screen.blit(self.image_freeze, players[_i].position+[-15, -60])
            screen.blit(image, image.get_rect(center=players[_i].position))



def init_otherobjects():
    View_players.init_convert()
