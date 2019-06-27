import pygame as pg
import numpy as np
import PIL.Image
from View.transforms import RGBTransform


class PureText():
    def __init__(self, text, size, font, color, **pos):
        '''
        pos: refer to the attributes of pg.Rect
        '''
        self.font = pg.font.Font(font, size)
        self.text_surface = self.font.render(text, True, pg.Color(color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)

def scaled_surface(surface, scale):
    '''
    example:
    image = scaled_surface(image, 0.3)
    '''
    return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))

def uni_color(im_path, color, transparency):
    im = PIL.Image.open(im_path)
    im = im.convert()
    im = RGBTransform().mix_with(color, factor=transparency).applied_to(im)
    mode = im.mode
    size = im.size
    data = im.tobytes()
    im = pg.image.fromstring(data, size, mode)
    return im


