import View.const as view_const

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
curve_a = 100000
curve_b = 100
oil_probability = 1 / 20
init_oil_number = 20
oil_radius = 8
price_max = 1200
price_min = 50
price_scale = 50

# player
player_number = 4
player_radius = 15
bag_capacity = 100**20
max_manual_player_num = 4
player_normal_speed = 9
init_insurance = 50
player_speed_decreasing_rate = player_normal_speed / price_max / 10
player_speed_min = player_normal_speed / 3
player_initial_direction_no = [4, 6, 2, 8]

# pet
pet_normal_speed = 3
pet_radius = 4
pet_carry_max = 1000

# base

base_length = 100
base_center = [
    [ base_length / 2 , base_length / 2] ,
    [ view_const.game_size[0] - base_length / 2 , base_length / 2] ,
    [ base_length / 2 , view_const.game_size[0] - base_length / 2] ,
    [ view_const.game_size[0] - base_length / 2 , view_const.game_size[0] - base_length / 2]
]


# equipments
speed_up_idx = 0
oil_up_idx = 1
insurance_idx = 2

speed_multiplier = 1.2
oil_multiplier = 1.2
init_insurance = 50

default_equipments = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# items
the_world_duration = 60 * 5

