import Model.const as model_const
from pygame.math import Vector2 as Vec

class Pet(object):
    def __init__(self, owner_index, position):
        self.owner_index = owner_index
        self.carry_max = model_const.pat_carry_max
        self.carry_now = 0
        self.position = Vec(position)
        self.radius = model_const.pet_radius
        self.color = [ random.randint(0, 255) for _ in range(3) ]
        """
        Pet is a circle
        """
        self.status = 0
        """
        0 for staying base
        1 for chasing the player
        2 for going base
        """
        self.speed = model_const.pat_normal_speed
    
    def check_collide_with_player(self, player):
        if Vec.magnitude(self.position - player.position) <= player.radius + self.radius:
            delta = min(carry_max - carry_now, player.value)
            self.carry_now += delta
            player.value -= delta
            self.status = 2
    
    def check_collide_with_base(self, base):
        if base.center[0] - base.length / 2 <= self.position[0] <= base.center[0] + base.length / 2 and
            base.center[1] - base.length / 2 <= self.position[1] <= base.center[1] + base.length / 2:
            self.status = 0
            base.value_sum += self.carry_now
            self.carry_now = 0
    
    def update(self, player_list, base_list):
        self.check_collide_with_player(player_list[self.owner_index])
        self.check_collide_with_base(base_list[self.owner_index])
        if self.stauts == 0:
            # do nothing
            pass
        else:
            target = (player_list[self.owner_index].position if status == 1 \
                      else base_list[self.owner_index].position)
            self.position += Vec.normalize(target - self.position) * self.speed

