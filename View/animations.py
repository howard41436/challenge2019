import pygame as pg
import numpy as np
import Model.main as model
import Model.const as model_const
import View.const as view_const
import View.utils as view_utils
import os.path
from math import *
import random

'''
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

    def draw(self, screen):
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
            
    def draw(self, screen):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(**self.pos),
        )

        self.update()
        

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
    images = view_utils.scaled_surface(pg.image.load( os.path.join(view_const.IMAGE_PATH, 'base.png') ), 0.3)
    
    def __init__(self, model):
        self.model = model
        self.expire_time = 90
        self.expired = False
        self.delay_of_frames = 10
        self._timer = 0

    def update(self):
        self._timer += 1
        if self._timer == self.expire_time:
            self.expired = True

    
    @classmethod
    def init_convert(cls):
        cls.images = cls.images.convert_alpha()
    
    def draw(self, screen):
        if self._timer % self.delay_of_frames:
            all_color = [player.color for player in self.model.player_list]
            random.shuffle(all_color)
            for _base in self.model.base_list:
                pg.draw.circle(screen, 
                              all_color[_base.owner_index], 
                              (round(int(_base.center[0]), -2), round(int(_base.center[1]), -2)), 
                              160)
                screen.blit(self.images, self.images.get_rect(center=_base.center))
        self.update()


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

    def draw(self, screen):
        col = pg.Rect(0,0,0,0)
        col.w = 200
        col.h = self.height
        col.midbottom = self.midbottom
        score_num = self.scorefont.render(f'{int(self.score)}', True, view_const.COLOR_BLACK)
        name = namefont.render(f'{self.name}', True, view_const.COLOR_BLACK)
        screen.blit(name, name.get_rect(midtop=(self.midbottom[0], 690)))
        screen.blit(score_num, score_num.get_rect(midbottom=(self.midbottom[0], 680-self.height)))
        pg.draw.rect(screen, self.color, col)
        self.update()


class Animation_theworld(Animation_raster):
    '''
    There are two phases in "the world" skill.
    phase 1: the circle grows larger from the starting position until the whole screen is covered
    phase 2: the circle shrinks
    '''

    image_inside = pg.image.load(os.path.join(view_const.IMAGE_PATH, 'theworld_inside.png'))
    inside_cache = dict()
    image_gray = tuple()
    t = 0
    max_radius = int(sqrt(view_const.screen_size[0]**2 + view_const.screen_size[1]**2)) # = 1509

    @classmethod
    def init_convert(cls):
        cls.image_inside = cls.image_inside.convert()
        for r in range(1, cls.max_radius+60+1, 60):
            cls.inside_cache[r] = pg.transform.scale(cls.image_inside, (2*r, 2*r))
        tmp = []
        for i in range(1, 180+180//27, 180//27):
            sur = pg.Surface(view_const.screen_size)
            sur.fill((22, 82, 117))
            sur = sur.convert()
            sur.set_alpha(i)
            tmp.append(sur)
        cls.image_gray = tuple(tmp)
    
    def __init__(self, center):
        '''
        Note that the argument "center" is not **kwarg, so just pass a tuple with length 2.
        '''
        self.tick_count = 0
        self.expired = False
        self.draw_twist = True
        self.gray_index = 0
        self.center = center
        self.radius = 1
        self.radius_vel = 60
        self.dt = 0.02
        self.radius_vel = 60

    def update(self):
        self.t += self.dt
        self.radius += self.radius_vel
        self.tick_count += 1
        if self.radius > self.max_radius: self.radius_vel = -self.radius_vel
        if self.radius == 1: self.draw_twist = False
        if self.tick_count == model_const.the_world_duration: self.expired = True
        if self.radius_vel < 0 and self.draw_twist: self.gray_index += 1

    def draw(self, screen):
        if self.draw_twist:
            mask_inside = self.inside_cache[self.radius].copy()

            # draw outside
            if self.radius_vel < 0:
                screen.blit(self.image_gray[self.gray_index], (0, 0))
            
            source = pg.surfarray.array2d(screen)

            # twist along y axis
            twisted = source[ np.clip(np.add(np.arange(view_const.screen_size[0]), 30*np.sin(np.arange(view_const.screen_size[0])/100 + self.t*7)).astype(int), 0, view_const.screen_size[0]-1) , : ]
            # twist along x axis
            twisted = twisted[ : , np.clip(np.add(np.arange(view_const.screen_size[1]), 30*np.cos(np.arange(view_const.screen_size[1])/100 + self.t*7)).astype(int), 0, view_const.screen_size[1]-1) ]

            # draw inside
            tmpsurf = pg.Surface((view_const.screen_size[0], view_const.screen_size[1]))
            pg.surfarray.blit_array(tmpsurf, twisted)
            mask_inside.blit(tmpsurf, tmpsurf.get_rect(topleft=(self.radius-self.center[0], self.radius-self.center[1])), None, pg.BLEND_RGBA_MULT)
            mask_inside.set_alpha(128)

            screen.blit(mask_inside, mask_inside.get_rect(center=self.center))
        
        else: screen.blit(self.image_gray[self.gray_index], (0, 0))

        self.update()


class Animation_freeze(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.transform.rotate(pg.image.load(os.path.join(view_const.IMAGE_PATH, f'ice.png')), i*4),
            1/60*i if i <= 30 else 1/2
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

