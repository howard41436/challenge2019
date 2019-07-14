import pygame as pg
import numpy as np
import os.path, threading, random
from math import *

import Model.main as model
import Model.const as model_const
import View.const as view_const
import View.utils as view_utils
import View.sound as snd_manager
from Events.Manager import EventPauseSound, EventPauseMusic, EventResumeSound, EventResumeMusic


'''
VERY IMPORTANT !!!
VERY IMPORTANT !!!
VERY IMPORTANT !!!

Once you add a new class in this module, you have to add CLASS.init_convert()
in the init_otherobjects() function!


* How Animation works:

tick = 0
animations = []
while True:
    for ani in animations:
        if ani.expired:
            animations.remove(ani)

    animations.append(new_animation)

    for ani in animations:
        ani.draw(screen)
    
    tick += 1
'''


class Animation_base():
    '''
    Base class of all animation.
    There will be a list (call it ANI) of all currently effective animations in main.py of view.
    To start an animation, you have to append the new Animation to ANI.
    Every animation in ANI should be drawn (if valid) or be discarded (if expired) in every tick.
    '''

    def __init__(self, delay_of_frames, **pos):
        self._timer = 0
        self.expired = False
    
    def update(self):
        pass

    # the "update" argument is for the purpose of GraphicalView.theworld_background in View/main.py
    def draw(self, screen, update=True):
        # draw first
        # update second
        pass


class Animation_vector(Animation_base):
    pass


class Animation_raster(Animation_base):
    frames = tuple()

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames )
    
    def __init__(self, delay_of_frames, expire_time, **pos):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
        self.expire_time = expire_time
        self.expired = False
        pos[next(iter(pos))] = pg.math.Vector2(pos[next(iter(pos))]) # turn tuple into vec2
        self.pos = pos

    def update(self):
        self._timer += 1

        if self._timer == self.expire_time:
            self.expired = True
        elif self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % len(self.frames)

        # update self.pos if needed
        # self.pos[ next(iter(self.pos)) ] = pg.math.Vector2(next_pos)
        # or
        # self.pos[ next(iter(self.pos)) ] += pg.math.Vector2(dx, dy)
            
    # the "update" argument is for the purpose of GraphicalView.theworld_background in View/main.py
    def draw(self, screen, update=True):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(**self.pos),
        )

        if update: self.update()
        

class Animation_equalize(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'equalize_background.png')),
            1 / 20 * i
        )
        for i in range(1, 21)
    )

    def __init__(self, **pos):
        super().__init__(2, 2*len(self.frames), **pos)


class Animation_gohome(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'gohome.png')),
            1/20 * i
        )
        for i in range(1, 20)
    )

    def __init__(self, **pos):
        super().__init__(1, 2*len(self.frames), **pos)


class Animation_magnetattract(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'mag.png')),
            1 / 20 * i
        )
        for i in range(1, 11)
    )

    def __init__(self, player_index, model):
        super().__init__(2, model_const.magnet_attract_duration, center=model.player_list[player_index].position)
        self.player_index = player_index
        self.model = model
    
    def update(self):
        super().update()
        self.pos[ next(iter(self.pos)) ] = self.model.player_list[self.player_index].position + (10, 0)


class Animation_othergohome(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'othergohome.png')),
            1/20 * i
        )
        for i in range(1, 20)
    )

    def __init__(self, **pos):
        super().__init__(1, 2*len(self.frames), **pos)


class Animation_radiationOil(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'radiation.png')),
            1/30 * i
        )
        for i in range(1, 30)
    )

    def __init__(self, **pos):
        super().__init__(1, 2*len(self.frames), **pos)


# the countdown animation
class Animation_start():
    pass


class Animation_shuffleBases_vertical(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'ver.png')),
            1/30 * i
        )
        for i in range(1, 45)
    )

    def __init__(self, **pos):
        super().__init__(1, 90, **pos)


class Animation_shuffleBases_horizontal(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'hor.png')),
            1/30 * i
        )
        for i in range(1, 45)
    )

    def __init__(self, **pos):
        super().__init__(1, 90, **pos)

class Animation_shuffleBases(Animation_raster):
    image = view_utils.scaled_surface(pg.image.load( os.path.join(view_const.IMAGE_PATH, 'base.png') ), 0.3)
    
    def __init__(self, model):
        self.model = model
        self.expire_time = 90
        self.expired = False
        self.delay_of_frames = 10
        self._timer = 0

    @classmethod
    def init_convert(cls):
        cls.image = cls.image.convert_alpha()

    def update(self):
        self._timer += 1
        if self._timer == self.expire_time:
            self.expired = True

    def draw(self, screen, update=True):
        if self._timer % self.delay_of_frames:
            all_color = [player.color for player in self.model.player_list]
            random.shuffle(all_color)
            for _base in self.model.base_list:
                pg.draw.circle(
                    screen, 
                    all_color[_base.owner_index], 
                    (round(int(_base.center[0]), -2), round(int(_base.center[1]), -2)), 
                    160
                )
                screen.blit(self.image, self.image.get_rect(center=_base.center))
        if update: self.update()


class Animation_endboard(Animation_raster):
    def __init__(self, color, max_height, midbottom, score, name):
        super().__init__(1, 120, midbottom=midbottom)
        self.midbottom = midbottom
        self.height = 1
        self.max_height = max_height
        self.score = 0
        self.max_score = score
        self.vel = max_height / self.expire_time
        self.color = color
        self.name = name
        self.scorefont = pg.font.Font(view_const.notosans_font, 25)
        self.namefont = pg.font.Font(view_const.notosans_font, 30)

    def update(self):
        if self.height + self.vel < self.max_height:
            self.height += self.vel
            self.score += self.max_score / self.expire_time
        else:
            self.height = self.max_height
            self.score = self.max_score

    def draw(self, screen, update=True):
        col = pg.Rect(0,0,0,0)
        col.w = 200
        col.h = self.height
        col.midbottom = self.midbottom
        score_num = self.scorefont.render(f'{int(self.score)}', True, view_const.COLOR_BLACK)
        name = self.namefont.render(f'{self.name}', True, view_const.COLOR_BLACK)
        screen.blit(name, name.get_rect(midtop=(self.midbottom[0], 690)))
        screen.blit(score_num, score_num.get_rect(midbottom=(self.midbottom[0], 680-self.height)))
        pg.draw.rect(screen, self.color, col)
        if update: self.update()


class Animation_theworld(Animation_raster):
    '''
    There are two phases in "the world" skill.
    phase 1: the circle grows larger from the starting position until the whole screen is covered
    phase 2: the circle shrinks
    '''

    image_inside = pg.image.load(os.path.join(view_const.IMAGE_PATH, 'theworld_inside.png'))
    inside_cache = dict()
    t = 0
    dt = 0.02
    max_radius = int(sqrt(view_const.screen_size[0]**2 + view_const.screen_size[1]**2)) # = 1509
    radius_vel = 60

    @classmethod
    def init_convert(cls):
        cls.image_inside = cls.image_inside.convert()
        for r in range(1, cls.max_radius+60+1, 60):
            cls.inside_cache[r] = pg.transform.scale(cls.image_inside, (2*r, 2*r))
        cls.gray_mask = pg.Surface(view_const.screen_size)
        cls.gray_mask.fill((22, 82, 117))
        cls.gray_mask.set_colorkey((255, 255, 255))
        cls.gray_mask.set_alpha(128)

    def __init__(self, center, ev_manager):
        '''
        Note that the argument "center" is not **kwarg, so just pass a tuple with length 2.
        '''
        self.tick_count = 0
        self.expired = False
        self.draw_twist = True
        self.center = center
        self.radius = 1
        self.has_played_video = False
        self.ev_manager = ev_manager
        
    def update(self):
        self.t += self.dt
        self.radius += self.radius_vel
        self.tick_count += 1
        if self.radius > self.max_radius: self.radius_vel = -self.radius_vel
        if self.radius == 1: self.draw_twist = False
        if self.tick_count == model_const.the_world_duration: self.expired = True

    def draw(self, screen, video_manager, update=True):
        if not self.has_played_video:
            video_manager.play_theworld()
            self.has_played_video = True

        if self.draw_twist:
            mask_inside = self.inside_cache[self.radius].copy()
            source = pg.surfarray.array2d(screen)

            # twist along y axis
            twisted = source[ np.clip(np.add(np.arange(view_const.screen_size[0]), 25*np.sin(np.arange(view_const.screen_size[0])/65 + self.t*7)).astype(int), 0, view_const.screen_size[0]-1) , : ]
            # twist along x axis
            twisted = twisted[ : , np.clip(np.add(np.arange(view_const.screen_size[1]), 25*np.cos(np.arange(view_const.screen_size[1])/65 + self.t*7)).astype(int), 0, view_const.screen_size[1]-1) ]

            # draw inside
            tmpsurf = pg.Surface((view_const.screen_size[0], view_const.screen_size[1]))
            pg.surfarray.blit_array(tmpsurf, twisted)
            mask_inside.blit(tmpsurf, tmpsurf.get_rect(topleft=(self.radius-self.center[0], self.radius-self.center[1])), None, pg.BLEND_RGBA_MULT)
            mask_inside.set_alpha(128)

            screen.blit(mask_inside, mask_inside.get_rect(center=self.center))

            # draw outside
            if self.radius_vel < 0:
                out_mask = self.gray_mask.copy()
                out_mask.fill((22, 82, 117))
                pg.draw.circle(out_mask, (255, 255, 255), tuple(map(int, self.center)), self.radius)
                screen.blit(out_mask, (0, 0))

        else: screen.blit(self.gray_mask, (0, 0))

        if update: self.update()


class Animation_freeze(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.transform.rotate(view_utils.scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, f'ice.png') ), 1.1), i*4),
            0.6/30*i if i <= 30 else 0.6
        )
        for i in range(1, 300)
    )

    def __init__(self, **pos):
        super().__init__(1, len(self.frames), **pos)


def init_animation():
    Animation_equalize.init_convert()
    Animation_gohome.init_convert()
    Animation_magnetattract.init_convert()
    Animation_othergohome.init_convert()
    Animation_radiationOil.init_convert()
    Animation_theworld.init_convert()
    Animation_freeze.init_convert()
    Animation_shuffleBases.init_convert()
    Animation_shuffleBases_vertical.init_convert()
    Animation_shuffleBases_horizontal.init_convert()

