import pygame as pg
import os.path
import math

import View.utils        as view_utils
import View.const        as view_const


'''
* "Static" object means that it is rendered every tick!
* The term "static" is designed compared to "animation", which is dynamic.

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
    
    def __init__(self, model):
        self.model = model


class View_players(__Object_base):
    images = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'player_{_color}.png')),
            0.2
        )
        for _color in ('blue', 'green', 'red', 'orange')
    )
    image_freeze = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'freeze.png')),0.5)

    @classmethod
    def init_convert(cls):
        cls.images = tuple( _image.convert_alpha() for _image in cls.images )
        cls.image_freeze = pg.Surface.convert_alpha( cls.image_freeze )

    def draw(self, screen):
        players = self.model.player_list
        for _i in range(len(players)):
            angle = ((8 - players[_i].direction_no) % 8 - 3) * 45
            image = pg.transform.rotate(self.images[_i], angle)
            if players[_i].freeze: screen.blit(self.image_freeze, players[_i].position+[-15, -60])
            screen.blit(image, image.get_rect(center=players[_i].position))


class View_oils(__Object_base):
    images = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'oil_{_color}.png')), 0.16
        )
        for _color in ('black', 'gray', 'pink', 'purple')
    )
    
    def draw(self, screen):
        for _oil in self.model.oil_list:
            if _oil.price < 400          : image = self.images[0]
            elif 600 > _oil.price >= 400 : image = self.images[1]
            elif 800 > _oil.price >= 600 : image = self.images[2]
            elif 1200 > _oil.price >= 800: image = self.images[3]
            screen.blit(image, image.get_rect(center=_oil.position))



class View_bases(__Object_base):
    images = ( view_utils.scaled_surface(pg.image.load( os.path.join(view_const.IMAGE_PATH, 'base.png') ), 0.3), )

    def draw(self, screen):
        for _base in self.model.base_list:
            screen.blit(self.images[0], self.images[0].get_rect(center=_base.center))


class View_pets(__Object_base):
    images = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'pet_robot_{_color}.png')),
            0.08
        )
        for _color in ('blue', 'green', 'red', 'orange')
    )

    def draw(self, screen):
        pets = self.model.pet_list
        for _i in range(len(pets)):
            angle = math.atan2(pets[_i].direction.x, pets[_i].direction.y) / math.pi * 180
            image = pg.transform.rotate(self.images[_i], angle)
            screen.blit(image, image.get_rect(center=pets[_i].position))

class View_scoreboard(__Object_base):
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        namefont = pg.font.Font(view_const.board_name_font, 55)
        numfont = pg.font.Font(view_const.board_name_font, 25)
        for score in self.model.scoreboard.score_list:
            pg.draw.rect(screen, self.model.colors[score.get_id()], (score.position,(480,160)))
        for score in self.model.scoreboard.score_list:
            name = namefont.render(f'{score.get_rank_str()} {score.player.name}', True, view_const.COLOR_BLACK)
            base_value = numfont.render(f'Base : {int(score.base.value_sum)}', True, view_const.COLOR_BLACK)
            player_value = numfont.render(f'Carried Value : {int(score.player.value)}', True, view_const.COLOR_BLACK)
            screen.blit(name, score.position+[10,-5])
            screen.blit(base_value, score.position+[10,75])
            screen.blit(player_value, score.position+[10,115])

def init_staticobjects():
    View_players.init_convert()
    View_oils.init_convert()
    View_bases.init_convert()
    View_pets.init_convert()
