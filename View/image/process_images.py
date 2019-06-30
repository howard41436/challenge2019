import pygame as pg
import os
import sys
from itertools import product

screen = pg.display.set_mode((1280, 800))

default_bg_color = (128, 140, 126)
converted = open('converted.txt', 'r').read()
converted_file = open('converted.txt', 'a')

for filename in os.listdir():
    if not 'png' in filename: continue
    if filename in converted: continue
    print(filename)
    
    img = pg.image.load(filename)
    size = img.get_size()
    bg = pg.Surface(size)
    
    for x, y in product(range(size[0]), range(size[1])):
        if img.get_at((x, y)) == default_bg_color:
            print()
            print(f'background color is used in this image: {filename}', file=sys.stderr)
            converted_file.close()
            exit(1)
        
    bg.fill(default_bg_color)
    bg.blit(img, (0, 0))
    pg.image.save(bg, filename)
    print(filename, file=converted_file)

converted_file.close()
    



