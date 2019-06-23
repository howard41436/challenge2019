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
    [0, 1],             #up
    [0.707, 0.707],     #up right
    [1, 0],             #right
    [0.707, -0.707],    #right down
    [0, -1],            #down
    [-0.707, -0.707],   #left down
    [-1, 0],	        #left
    [-0.707, 0.707],    #left up
]

# player
player_number = 4
bag_capacity = 100**20
max_manual_player_num = 4
player_normal_speed = 1
init_insurance = 50

# pet
pet_normal_speed = 1

# oil_const
oil_probability = 5e-3
init_oil_number = 5
oil_radius = 10
price_max = 1000
price_scale = 50

# base
base_length = 10
base_center = [
    [ 1 , 1] ,
    [ 87 , 1] ,
    [ 1 , 87] ,
    [ 87 , 87]
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
