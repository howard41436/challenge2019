import Model.const       as modelConst

import random

class Player(object):
    def __init__(self, name, index, is_AI):
        self.name = name
        self.is_AI = is_AI
        self.index = index
        self.ai = None
        self.color = [ random.randint(0,255) for _ in range(3) ]

        self.pos = [ random.randint(20,780), random.randint(20,780) ]
        self.direction = 1

    def update_pos(self):
        [add_x, add_y] = modelConst.dir_const[self.direction]
        Bounce = modelConst.dir_bounce
        if self.pos[0] + add_x < 20 \
            or self.pos[0] + add_x > 780 :
            self.direction = Bounce[0][self.direction]
        elif self.pos[1] + add_y < 20 \
            or self.pos[1] + add_y > 780 :
            self.direction = Bounce[1][self.direction]

        add_dir = modelConst.dir_const[self.direction]

        self.pos[0] += add_dir[0]
        self.pos[1] += add_dir[1]
