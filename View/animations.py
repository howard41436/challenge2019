import pygame as pg
import Model.main as model

'''
* How to use Animation:

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
    


* Hierarchy of classes:

Animation_Base
    Animation_vector
        Animation_equalize

    Animation_raster
'''

class Animation_Base():
    '''
    Base class of all animation.
    There will be a list (call it ANI) of all currently effective animations in main.py of view.
    To start an animation, you have to append the new Animation to ANI.
    Every animation in ANI should be drawn (if valid) or be discarded (if expired) in every tick.
    '''

    def __init__(self):
        self._timer = 0
        self.expired = False
    
    def update(self):
        pass

    def draw(self, screen):
        # draw first
        # update second
        pass


class Animation_vector(Animation_Base):
    pass


class Animation_raster(Animation_Base):
    frames = [] # should have .get_rect() method

    def __init__(self, **pos):
        self._timer = 0
        self.delay_of_frames = 1 # to be overwritten by descendant classes
        self.frame_index_to_draw = 0
        self.expired = False
        self.pos = pos

    def update(self):
        self._timer += 1

        if self._timer == (self.delay_of_frames * len(self.frames)):
            self.expired = True
        elif self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw += 1
            
    def draw(self, screen):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(),
        )

        self.update()
        


