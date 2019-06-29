import pygame as pg

DIR_U  = 1
DIR_RU = 2
DIR_R  = 3
DIR_RD = 4
DIR_D  = 5
DIR_LD = 6
DIR_L  = 7
DIR_LU = 8

#   [up,      right,      down,      left,      item1,    item2]
manual_player_keys = [
    [pg.K_w,  pg.K_d,     pg.K_s,    pg.K_a,    pg.K_q,   pg.K_e],
    [pg.K_t,  pg.K_h,     pg.K_g,    pg.K_f,    pg.K_r,   pg.K_y],
    [pg.K_i,  pg.K_l,     pg.K_k,    pg.K_j,    pg.K_u,   pg.K_o],
    [pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT, pg.K_RSHIFT, pg.K_RCTRL]
]

# up = 1, right = 2, down = 4, left = 8
# -> RU = 3, RD = 6, LU = 9, LD = 12
dir_hash = [
    0, DIR_U, DIR_R, DIR_RU, DIR_D,
    0, DIR_RD, 0, DIR_L, DIR_LU, 0, 0, DIR_LD, 0, 0, 0
]
