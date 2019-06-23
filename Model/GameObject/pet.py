import Model.const as model_const
from pygame.math import Vector2 as Vec

class Pet(object) :
    def __init__(self, owner_index, position) :
        self.owner_index = owner_index
        self.carry_max = model_const.pat_carry_max
        self.carry_now = 0
        self.position = Vec(position)
        self.status = 0
        """
        0 for staying base
        1 for chasing the player
        2 for going base
        """
        self.speed = model_const.pat_normal_speed

    def update(self, player_list, base_list) :
        if self.stauts == 0 :
            # do nothing
            pass
        else :
            target = (player_list[self.owner_index].position if status == 1 \
                      else base_list[self.owner_index].position)
            self.position += Vec.normalize(target - self.position) * self.speed

