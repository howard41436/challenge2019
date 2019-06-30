import pygame as pg
import os.path
import math

import Model.GameObject.item        as model_item
import View.utils        as view_utils
import View.const        as view_const
import Model.const       as model_const
import View.animations   as view_animation

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


class View_background(__Object_base):
    background = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'background.png')), 1)
    priced_market = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'market.png')), 0.3)
    
    @classmethod
    def init_convert(cls):
        cls.background = cls.background.convert()
        cls.priced_market = cls.priced_market.convert()
    
    def draw(self, screen): 
        screen.fill(view_const.COLOR_WHITE)
        screen.blit(self.background, [0, 0])
        screen.blit(self.priced_market, [322, 328])


class View_menu(__Object_base):
    menu = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'menu.png')), 1)
    base = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'base.png')), 0.5)

    @classmethod
    def init_convert(cls):
        cls.menu = cls.menu.convert()
        cls.base = cls.base.convert_alpha()

    def draw(self, screen):
        screen.blit(self.menu, [0, 0])
        screen.blit(self.base, [10, 645])


class View_characters(__Object_base):
    images = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'move_{_index}.png')),
            0.6
        )
        for _index in ('1', '2', '3', '4', '5', '6', '7')
    )
    image_oil = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'oil_black.png')),0.4)

    def __init__(self, model):
        self.model = model
        self.picture_switch = [0, 1, 2, 1, 2, 1, 2, 1, 2, 3, 4, 5, 4, 5, 4, 5, 4, 5, 6]
        self.position_switch = [130, 240, 350, 460, 570, 680, 790, 900, 1010,
                                1010, 900, 790, 680, 570, 460, 350, 240, 130, 120]
        self.index = 0
        self.counter = 0

    @classmethod
    def init_convert(cls):
        cls.images = tuple( _image.convert_alpha() for _image in cls.images )
        cls.image_oil = pg.Surface.convert_alpha( cls.image_oil )

    def draw(self, screen):
        image = self.images[self.picture_switch[self.index]]
        screen.blit(image, [self.position_switch[self.index], 520])
        if self.index < 10:
            screen.blit(self.image_oil, [1220, 700])
        if self.counter == 20:
            self.index += 1
            self.index %= 19
        self.counter %= 20
        self.counter += 1


class View_players(__Object_base):
    """images_color = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'player_color{_rainbow}.png')),
            0.2
        )
        for _rainbow in range(0,19,1)
    )"""
    image = view_utils.scaled_surface(pg.image.load( os.path.join(view_const.IMAGE_PATH, 'koreanfish.png') ), 0.2)

    def __init__(self, model):
        self.model = model
        self.color_switch = [0, 0, 0, 0]
        """self.images = tuple(
            view_utils.scaled_surface(
                view_utils.replace_color(os.path.join(view_const.IMAGE_PATH,'player_outfit.png'),
                                        view_const.COLOR_WHITE,
                                        player.color),
                0.2
            )
            for player in self.model.player_list
        )

    @classmethod
    def init_convert(cls):
        cls.images = tuple( _image.convert_alpha() for _image in cls.images )
        cls.images_color = tuple( _image.convert_alpha() for _image in cls.images_color)"""

    def draw(self, screen):
        players = self.model.player_list
        for _i in range(len(players)):
            angle = ((8 - players[_i].direction_no) % 8 - 3) * 45
            image = pg.transform.rotate(self.image, angle)
            if not players[_i].is_invincible: image = pg.transform.rotate(self.image, angle)
            else: 
                """image = pg.transform.rotate(self.images_color[self.color_switch[_i]%19], angle)"""
                self.color_switch[_i] += 1
            screen.blit(image, image.get_rect(center=players[_i].position))


class View_oils(__Object_base):
    images = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'oil_{_color}.png')), 0.16
        )
        for _color in ('purple', 'pink', 'gray', 'black')
    )
    
    def draw(self, screen):
        for _oil in self.model.oil_list:
            if _oil.price < 400          : image = self.images[0]
            elif 600 > _oil.price >= 400 : image = self.images[1]
            elif 800 > _oil.price >= 600 : image = self.images[2]
            elif 1200 > _oil.price >= 800: image = self.images[3]
            screen.blit(image, image.get_rect(center=_oil.position))



class View_bases(__Object_base):
    images = view_utils.scaled_surface(pg.image.load( os.path.join(view_const.IMAGE_PATH, 'base.png') ), 0.3)
    
    @classmethod
    def init_convert(cls):
        cls.images = cls.images.convert_alpha()

    def draw(self, screen):
        for _base in self.model.base_list:
            pg.draw.circle(screen, 
                          self.model.player_list[_base.owner_index].color, 
                          (round(int(_base.center[0]), -2), round(int(_base.center[1]), -2)), 
                          160)
            screen.blit(self.images, self.images.get_rect(center=_base.center))


class View_pets(__Object_base):
    def __init__(self, model):
        self.model = model
        self.images = tuple(
            view_utils.scaled_surface(
                view_utils.replace_color(os.path.join(view_const.IMAGE_PATH,'pet_robot_outfit.png'),
                                        view_const.COLOR_WHITE,
                                        player.color),
                0.08
            )
            for player in self.model.player_list
        )

    def draw(self, screen):
        pets = self.model.pet_list
        for _i in range(len(pets)):
            angle = math.atan2(pets[_i].direction.x, pets[_i].direction.y) / math.pi * 180
            image = pg.transform.rotate(self.images[_i], angle)
            screen.blit(image, image.get_rect(center=pets[_i].position))


class View_scoreboard(__Object_base):
    images = {
    'IGoHome'       :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'backbag.png')), 0.3),
    'MagnetAttract' :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'magnet.png')), 0.3),
    'Invincible'    :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'star.png')), 0.3),
    'TheWorld'      :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'clock.png')), 0.3),
    'OtherGoHome'   :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'hurricane.png')), 0.3),
    'RadiusNotMove' :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'staff.png')), 0.3),
    'RadiationOil'  :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'bomb.png')), 0.2),
    'ShuffleBases'  :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'shuffle.png')), 0.3),
    'FaDaCai'       :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'shuffle.png')), 0.3)
    }

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }
        cls.namefont = pg.font.Font(view_const.notosans_font, 55)
        cls.numfont = pg.font.Font(view_const.notosans_font, 25)


    def draw(self, screen):
        pg.draw.rect(screen, view_const.COLOR_WHITE, [800, 0, 480, 800])
        pg.draw.rect(screen, view_const.COLOR_KHAKI, [800, 0, 480, 160])
        pg.draw.rect(screen, view_const.COLOR_BLACK, ((800, 0),(480,160)), 5)
        for score in self.model.scoreboard.score_list:
            pg.draw.rect(screen, score.player.color, (score.position,(480,160)))
            pg.draw.rect(screen, view_const.COLOR_BLACK, (score.position,(480,160)), 5)
        for score in self.model.scoreboard.score_list:
            name = self.namefont.render(f'{score.player.name}', True, view_const.COLOR_BLACK)
            base_value = self.numfont.render(f'Base : {int(score.base.value_sum)}', True, view_const.COLOR_BLACK)
            player_value = self.numfont.render(f'Carried Value : {int(score.player.value)}', True, view_const.COLOR_BLACK)
            if score.player.item:
                item_image = self.images[score.player.item.name]
                screen.blit(item_image, score.position+[340, 5])
            screen.blit(name, score.position+[10,-5])
            screen.blit(base_value, score.position+[10,75])
            screen.blit(player_value, score.position+[10,115])
        for new_score in self.model.scoreboard.p_varition_list:
            if new_score.varition >= 0:
                carry_value = self.numfont.render(f'+{int(new_score.varition)}', True, view_const.COLOR_GOLD)
            else:
                carry_value = self.numfont.render(f'{int(new_score.varition)}', True, view_const.COLOR_GOLD)
            screen.blit(carry_value, new_score.get_position()+[300, 160])

        for new_base_score in self.model.scoreboard.b_varition_list:
            if new_base_score.varition >= 0:    
                base_value = self.numfont.render(f'+{int(new_base_score.varition)}', True, view_const.COLOR_GOLD)
            else:
                base_value = self.numfont.render(f'{int(new_base_score.varition)}', True, view_const.COLOR_GOLD)
            screen.blit(base_value, new_base_score.get_position()+[300, 120])
        
        




class View_items(__Object_base):
    images = {
    'IGoHome'       :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'backbag.png')), 0.2),
    'MagnetAttract' :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'magnet.png')), 0.2),
    'Invincible'    :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'star.png')), 0.2),
    'TheWorld'      :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'clock.png')), 0.2),
    'OtherGoHome'   :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'hurricane.png')), 0.2),
    'RadiusNotMove' :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'staff.png')), 0.2),
    'RadiationOil'  :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'bomb.png')), 0.15),
    'ShuffleBases'  :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'shuffle.png')), 0.2),
    'marketcenter'  :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'marketcenter.png')), 0.0001),
    'FaDaCai'       :view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'shuffle.png')), 0.2)
    }

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def draw(self, screen):
        image = self.images['marketcenter']
        for market in self.model.priced_market_list:
            if market.item:
                image = self.images[market.item.name]
            screen.blit(image, market.position+[5,5])




def init_staticobjects():
    View_background.init_convert()
    View_players.init_convert()
    View_oils.init_convert()
    View_bases.init_convert()
    View_pets.init_convert()
    View_items.init_convert()
    View_scoreboard.init_convert()
    View_menu.init_convert()
    View_characters.init_convert()
