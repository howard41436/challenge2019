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

    def update_target(self, rank):
        self.rank = rank
        self.target = Vec(model_const.score_position[rank])

    def update(self):
        pass

    def get_rank_str(self):
        return model_const.rank_str[self.rank]

class ScoreBoard(object):

    def __init__(self, player_list, base_list):
        """
        self.player_list = player_list
        self.base_list = base_list
        """ 
        self.index_list = [ i for i in range(model_const.player_number) ]
        self.score_list = [ Score(player_list[i], base_list[i], i) for i in range(model_const.player_number) ]

    def get_score(self, index):
        return self.score_list[index].base.get_value_sum()

    def update(self):
        new_list = sorted(self.index_list, key=self.get_score, reverse=True)
        for i in range(model_const.player_number):
            if self.index_list[i] != new_list[i]:
                self.score_list[i].update_target(new_list[i])

    def __str__(self):
        return str(self.index_list)
