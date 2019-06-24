DIR_stop = 0
DIR_U    = 1
DIR_RU   = 2
DIR_R    = 3
DIR_RD   = 4
DIR_D    = 5
DIR_LD   = 6
DIR_L    = 7
DIR_LU   = 8


"""
a base of AI.
"""
class BaseAI:
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper

    def decide( self ):
        pass