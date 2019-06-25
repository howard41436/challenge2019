import Model.const as model_const
from pygame.math import Vector2 as Vec
import random

class Pet(object):
    def __init__(self, owner_index, position):
        self.owner_index = owner_index
        self.carry_max = model_const.pet_carry_max
        self.carry_now = 0
        self.position = Vec(position)
        self.radius = model_const.pet_radius
        self.color = [ random.randint(0, 255) for _ in range(3) ]
        self.direction = Vec(0, 0)
        """
        Pet is a circle
        """
        self.status = 0
        """
        0 for staying base
        1 for chasing the player
        2 for going base
        """
        self.speed = model_const.pet_normal_speed
    
    def check_collide_with_player(self, player):
        if Vec.magnitude(self.position - player.position) <= player.radius + self.radius:
            delta = min(self.carry_max - self.carry_now, player.value)
            self.carry_now += delta
            player.value -= delta
            self.status = 2
    
    def change_status(self, new_status):
        self.status = new_status
    
    def check_collide_with_base(self, base):
        if self.status == 2 and Vec.magnitude(self.position - base.center) <= self.radius:
            self.status = 0
            base.value_sum += self.carry_now
            self.carry_now = 0
    
    def update(self, player_list, base_list):
        self.check_collide_with_player(player_list[self.owner_index])
        self.check_collide_with_base(base_list[self.owner_index])
        if self.status == 0:
            # do nothing
            self.direction = Vec(0, 0)
            pass
        else:
            target = (player_list[self.owner_index].position if self.status == 1 \
                      else base_list[self.owner_index].center)
            self.direction = Vec.normalize(target - self.position)
            self.position += self.direction * self.speed

