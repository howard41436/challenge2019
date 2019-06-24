import pygame as pg

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
