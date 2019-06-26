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


class View_oils(__Object_base):
    images_oil = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'oil_{_color}.png')), 0.16
        )
        for _color in ('black', 'gray', 'pink', 'purple')
    )

    @classmethod
    def init_convert(cls):
        cls.images_oil = tuple( _image.convert_alpha() for _image in cls.images_oil )
    
    def __init__(self, model):
        self.model = model
    
    def draw(self, screen):
        for _oil in self.model.oil_list:
            if _oil.price < 400          : image = self.images_oil[0]
            elif 600 > _oil.price >= 400 : image = self.images_oil[1]
            elif 800 > _oil.price >= 600 : image = self.images_oil[2]
            elif 1200 > _oil.price >= 800: image = self.images_oil[3]
            screen.blit(image, image.get_rect(center=_oil.position))


class View_bases(__Object_base):
    images = ( view_utils.scaled_surface(pg.image.load( os.path.join(view_const.IMAGE_PATH, 'base.png') ), 0.3), )
    
    def __init__(self, model):
        self.model = model
    
    def draw(self, screen):
        for _base in self.model.base_list:
            screen.blit(self.images[0], self.images[0].get_rect(center=_base.center))


def init_staticobjects():
    View_players.init_convert()
    View_oils.init_convert()
    View_bases.init_convert()
