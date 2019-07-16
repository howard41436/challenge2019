"""
const of AI code use.
"""
AI_DIR_STOP     = 0
AI_DIR_U        = 1
AI_DIR_RU       = 2
AI_DIR_R        = 3
AI_DIR_RD       = 4
AI_DIR_D        = 5
AI_DIR_LD       = 6
AI_DIR_L        = 7
AI_DIR_LU       = 8
AI_TRIGGER_ITEM = 9
AI_dir_mapping = [
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
"""
a base of AI.
"""
class BaseAI:
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper

    def decide(self):
    	pass