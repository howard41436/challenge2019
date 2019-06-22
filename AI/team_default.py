from AI.base import *

import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []

        self.last_dir = random.randint(1, 8)

    def decide( self ):
        if not random.randint(0, 9) % 10:
            self.last_dir = random.randint(1, 8)
        return self.last_dir
