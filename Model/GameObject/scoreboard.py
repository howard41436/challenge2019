import Model.const as model_const
import View.const as view_const
from pygame.math import Vector2 as Vec

class Score(object):
    def __init__(self, player, base, rank):
        self.player = player
        self.base = base
        self.rank = rank
        self.position = Vec(model_const.score_position[rank])
        self.target = Vec(model_const.score_position[rank])
        self.velocity = Vec((0, 0))
        self.acceleration = Vec((0, 0)) 

        self.p_value = player.value
        self.b_value = base.value_sum
        self.timer = 0

    def get_id(self):
        return self.player.index

    def get_position(self):
        return self.position

    def update_target(self, rank):
        self.rank = rank
        self.target = Vec(model_const.score_position[rank])
        displacement = self.target - self.position
        self.acceleration = -2 * displacement / model_const.swap_duration ** 2
        self.velocity = 2 * displacement / model_const.swap_duration
        self.timer = model_const.swap_duration

    def update(self): 
        self.p_value = self.player.value
        self.b_value = self.base.value_sum
        if self.timer > 0:
            self.timer -= 1
            self.position += self.velocity
            self.velocity += self.acceleration
        else:
            self.position = self.target

    def get_rank_str(self):
        return model_const.rank_str[self.rank]

class Score_varition(object):
    def __init__(self, score, varition):
        self.score = score
        self.varition = varition
        self.position = Vec((0, 0)) # relative to Score
        self.velocity = Vec(model_const.varition_vel)
        self.timer = model_const.varition_duration

    def update(self):
        self.position += self.velocity
        self.timer -= 1

    def get_position(self):
        return self.position + self.score.position

def update_varition_list(score, varition, varition_list):
    if varition != 0:
        varition_list.append(Score_varition(score, varition))
    for v in varition_list:
        v.update()
    for i in reversed(range(len(varition_list))):
        if varition_list[i].timer == 0:
            varition_list.pop(i)

class Scoreboard(object): 
    def __init__(self, player_list, base_list):
        self.index_list = [i for i in range(model_const.player_number)]
        self.score_list = [Score(player_list[i], base_list[i], i) for i in range(model_const.player_number)]
        self.p_varition_list = []
        self.b_varition_list = []

    def get_score(self, index):
        return self.score_list[index].base.get_value_sum()

    def update(self):
        self.update_rank()
        self.update_varition()

    def update_rank(self):
        new_list = sorted(self.index_list, key=self.get_score, reverse=True)
        for i in range(model_const.player_number):
            if self.index_list[i] != new_list[i]:
                self.score_list[new_list[i]].update_target(i)
        self.index_list = new_list

    def update_varition(self):
        for score in self.score_list:
            update_varition_list(score, score.player.value - score.p_value, self.p_varition_list)
            update_varition_list(score, score.base.value_sum - score.b_value, self.b_varition_list) 
            score.update()

    def __str__(self):
        return str(self.index_list)
