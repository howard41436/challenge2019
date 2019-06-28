import pygame as pg
import os.path
import math

import Model.GameObject.item        as model_item
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


class View_menu(__Object_base):
    menu = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'menu.png')), 1)

    def draw(self, screen):
        image = self.menu
        screen.blit(image, [0, 0])


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
        self.picture_switch = [0, 1, 2, 1, 2, 1, 2, 3, 4, 5, 4, 5, 4, 5, 6]
        self.position_switch = [200, 335, 470, 605, 740, 875, 1010, 1010, 875, 740, 605, 470, 335, 200, 200]
        self.index = 0
        self.counter = 0

    @classmethod
    def init_convert(cls):
        cls.images = tuple( _image.convert_alpha() for _image in cls.images )
        cls.image_oil = pg.Surface.convert_alpha( cls.image_oil )

    def draw(self, screen):
        image = self.images[self.picture_switch[self.index]]
        screen.blit(image, [self.position_switch[self.index], 520])
        if self.index < 8:
            screen.blit(self.image_oil, [1220, 700])
        if self.counter == 20:
            self.index += 1
            self.index %= 15
        self.counter %= 20
        self.counter += 1


class View_players(__Object_base):
    images = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'player_{_color}.png')),
            0.2
        )
        for _color in ('blue', 'green', 'red', 'orange')
    )
    image_freeze = view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, 'freeze.png')),0.5)
    images_color = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, f'player_color{_rainbow}.png')),
            0.2
        )
        for _rainbow in range(0,19,1)
    )
    def __init__(self, model):
        super(View_players, self).__init__(model)
        super(View_players, self).init_convert()
        self.color_switch = [0, 0, 0, 0]

    @classmethod
    def init_convert(cls):
        cls.images = tuple( _image.convert_alpha() for _image in cls.images )
        cls.image_freeze = pg.Surface.convert_alpha( cls.image_freeze )
    def draw(self, screen):
        players = self.model.player_list
        for _i in range(len(players)):
            angle = ((8 - players[_i].direction_no) % 8 - 3) * 45
            if not players[_i].is_invincible: image = pg.transform.rotate(self.images[_i], angle)
            else: 
                image = pg.transform.rotate(self.images_color[self.color_switch[_i]%19], angle)
                self.color_switch[_i] += 1
            if players[_i].freeze: screen.blit(self.image_freeze, players[_i].position+[-15, -60])
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
    images = ( view_utils.scaled_surface(pg.image.load( os.path.join(view_const.IMAGE_PATH, 'base.png') ), 0.3), )

    def draw(self, screen):
        for _base in self.model.base_list:
            if _base.owner_index == 0:
                if _base.center == [50, 50]:
                    pg.draw.circle(screen, view_const.COLOR_BLUE,[0, 0],  160, 160)
                elif _base.center == [750, 50]:
                    pg.draw.circle(screen, view_const.COLOR_BLUE,[800, 0],  160, 160)
                elif _base.center == [50, 750]:
                    pg.draw.circle(screen, view_const.COLOR_BLUE,[0, 800],  160, 160)
                elif _base.center == [750, 750]:
                    pg.draw.circle(screen, view_const.COLOR_BLUE,[800, 800],  160, 160)
            elif _base.owner_index == 1:
                if _base.center == [50, 50]:
                    pg.draw.circle(screen, view_const.COLOR_GREEN,[0, 0],  160, 160)
                elif _base.center == [750, 50]:
                    pg.draw.circle(screen, view_const.COLOR_GREEN,[800, 0],  160, 160)
                elif _base.center == [50, 750]:
                    pg.draw.circle(screen, view_const.COLOR_GREEN,[0, 800],  160, 160)
                elif _base.center == [750, 750]:
                    pg.draw.circle(screen, view_const.COLOR_GREEN,[800, 800],  160, 160)
            elif _base.owner_index == 2:
                if _base.center == [50, 50]:
                    pg.draw.circle(screen, view_const.COLOR_RED,[0, 0],  160, 160)
                elif _base.center == [750, 50]:
                    pg.draw.circle(screen, view_const.COLOR_RED,[800, 0],  160, 160)
                elif _base.center == [50, 750]:
                    pg.draw.circle(screen, view_const.COLOR_RED,[0, 800],  160, 160)
                elif _base.center == [750, 750]:
                    pg.draw.circle(screen, view_const.COLOR_RED,[800, 800],  160, 160)
            elif _base.owner_index == 3:
                if _base.center == [50, 50]:
                    pg.draw.circle(screen, view_const.COLOR_ORANGE,[0, 0],  160, 160)
                elif _base.center == [750, 50]:
                    pg.draw.circle(screen, view_const.COLOR_ORANGE,[800, 0],  160, 160)
                elif _base.center == [50, 750]:
                    pg.draw.circle(screen, view_const.COLOR_ORANGE,[0, 800],  160, 160)
                elif _base.center == [750, 750]:
                    pg.draw.circle(screen, view_const.COLOR_ORANGE,[800, 800],  160, 160)
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
        self.backbag = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'backbag.png')), 0.3)
        self.magnet = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'magnet.png')), 0.3)
        self.star = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'star.png')), 0.3)
        self.timer = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'clock.png')), 0.3)
        self.blackhole = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'blackhole.png')), 0.3)
        self.staff = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'staff.png')), 0.3)
        self.bomb = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'bomb.png')), 0.25)
        self.shuffle = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'shuffle.png')), 0.3)

    def draw(self, screen):
        namefont = pg.font.Font(view_const.board_name_font, 55)
        numfont = pg.font.Font(view_const.board_name_font, 25)
        for score in self.model.scoreboard.score_list:
            pg.draw.rect(screen, self.model.colors[score.get_id()], (score.position,(480,160)))
        for score in self.model.scoreboard.score_list:
            name = namefont.render(f'{score.get_rank_str()} {score.player.name}', True, view_const.COLOR_BLACK)
            base_value = numfont.render(f'Base : {int(score.base.value_sum)}', True, view_const.COLOR_BLACK)
            player_value = numfont.render(f'Carried Value : {int(score.player.value)}', True, view_const.COLOR_BLACK)
            item_image = None
            if isinstance(score.player.item, model_item.IGoHome):
                item_image = self.backbag
            elif isinstance(score.player.item, model_item.MagnetAttract):
                item_image = self.magnet
            elif isinstance(score.player.item, model_item.Invincible):
                item_image = self.star
            elif isinstance(score.player.item, model_item.TheWorld):
                item_image = self.timer
            elif isinstance(score.player.item, model_item.OtherGoHome):
                item_image = self.blackhole
            elif isinstance(score.player.item, model_item.RadiationOil):
                item_image = self.bomb
            elif isinstance(score.player.item, model_item.RadiusNotMove):
                item_image = self.staff
            elif isinstance(score.player.item, model_item.ShuffleBases):
                item_image = self.shuffle
            if item_image: screen.blit(item_image, score.position+[340,5])
            screen.blit(name, score.position+[10,-5])
            screen.blit(base_value, score.position+[10,75])
            screen.blit(player_value, score.position+[10,115])


class View_items(__Object_base):
    def __init__(self, model):
        self.model = model
        self.backbag = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'backbag.png')), 0.2)
        self.magnet = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'magnet.png')), 0.2)
        self.star = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'star.png')), 0.2)
        self.timer = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'clock.png')), 0.2)
        self.blackhole = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'blackhole.png')), 0.2)
        self.staff = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'staff.png')), 0.2)
        self.bomb = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'bomb.png')), 0.15)
        self.shuffle = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'shuffle.png')), 0.2)
        self.marketcenter = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'marketcenter.png')), 0.0001)

    def draw(self, screen):
        for market in self.model.priced_market_list:
            if isinstance(market.item, model_item.IGoHome):
                image = self.backbag           #pg.draw.rect(self.screen, view_const.COLOR_VIOLET, pg.Rect(market.position, [20, 20]))
            elif isinstance(market.item, model_item.MagnetAttract):
                image = self.magnet            #pg.draw.rect(self.screen, view_const.COLOR_BLACK, pg.Rect(market.position, [20, 20]))
            elif isinstance(market.item, model_item.Invincible):
                image = self.star              #pg.draw.rect(self.screen, view_const.COLOR_RED, pg.Rect(market.position, [20, 20]))
            elif isinstance(market.item, model_item.TheWorld):
                image = self.timer            #pg.draw.rect(self.screen, view_const.COLOR_GRAY, pg.Rect(market.position, [20, 20]))
            elif isinstance(market.item, model_item.OtherGoHome):
                image = self.blackhole        #pg.draw.rect(self.screen, view_const.COLOR_GRAY, pg.Rect(market.position, [20, 20]))
            elif isinstance(market.item, model_item.RadiationOil):
                image = self.bomb
            elif isinstance(market.item, model_item.RadiusNotMove):
                image = self.staff
            elif isinstance(market.item, model_item.ShuffleBases):
                image = self.shuffle
            else:
                image = self.marketcenter
            screen.blit(image, market.position+[5,5])

def init_staticobjects():
    View_players.init_convert()
    View_oils.init_convert()
    View_bases.init_convert()
    View_pets.init_convert()
    View_items.init_convert()
    View_menu.init_convert()
    View_characters.init_convert()
