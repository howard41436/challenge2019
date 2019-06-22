PlayerNum = 4
MaxManualPlayerNum = 1

#dir const
dirConst = [
    [0,0],              # can't movw
    [0,-1],             # Up
    [0.707,-0.707],     # Right up
    [1,0],              # Roght
    [0.707,0.707],      # Right down
    [0,1],              # Down
    [-0.707,0.707],     # Left down
    [-1,0],             # Left
    [-0.707,-0.707]     # Left up
]
dirBounce = [
    [0, 1, 8, 7, 6, 5, 4, 3, 2], # x bouce
    [0, 5, 4, 3, 2, 1, 8, 7, 6], # y bouce
]

# player
player_number = 4

# oil_const
oil_probability = 5e-3
price_min = 10
price_max = 1000
weight_min = 20
weight_max = 100

