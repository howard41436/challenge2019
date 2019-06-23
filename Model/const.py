game_length = 60 * 60 * 5
#dir const
"""
DIR_U  = 1
DIR_RU = 2
DIR_R  = 3
DIR_RD = 4
DIR_D  = 5
DIR_LD = 6
DIR_L  = 7
DIR_LU = 8
"""
dir_mapping = [
    [0, 0],             #steady
    [0, -1],             #up
    [0.707, -0.707],     #up right
    [1, 0],             #right
    [0.707, 0.707],    #right down
    [0, 1],            #down
    [-0.707, 0.707],   #left down
    [-1, 0],	        #left
    [-0.707, -0.707],    #left up
]

# oil_const
oil_probability = 1 / 60
init_oil_number = 5
oil_radius = 8
price_max = 1000
price_min = 10
price_scale = 50

# player
player_number = 4
player_radius = 15
bag_capacity = 100**20
max_manual_player_num = 4
player_normal_speed = 3
init_insurance = 50
player_speed_decreasing_rate = player_normal_speed / price_max
player_speed_min = 1

# pet
pet_normal_speed = 1

# base

base_length = 100
base_center = [
    [ base_length / 2 , base_length / 2] ,
    [ view_const.game_size[0] - base_length / 2 , base_length / 2] ,
    [ base_length / 2 , view_const.game_size[0] - base_length / 2] ,
    [ view_const.game_size[0] - base_length / 2 , view_const.game_size[0] - base_length / 2]
]


# item
speed_up_idx = 0
oil_up_idx = 1
insurance_idx = 2

speed_multiplier = 1.2
oil_multiplier = 1.2
init_insurance = 50

default_equipments = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
