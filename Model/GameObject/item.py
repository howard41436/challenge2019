import Model.const as model_const
from pygame.math import Vector2 as Vec

class Item(object):
    '''
    Base Item
    '''
    def __init__(self, player):
        self.duration = 0
        self.position = Vec(player.position)

class Communism(Item):
    '''
    Evenly distribute the sum of all the values in all the players' bases
    '''
    def __init__(self):
        pass

    def trigger(self, player_list):
        total = sum(player.value for player in player_list)
        for player in player_list:
            player.value = total / len(player_list)


class GoHome(Item):
    '''
    Make all player move to their base
    '''
    def __init__(self, player):
        super().__init__(player)

    def trigger(self, player_list, base_list):
        for player in player_list:
            player.position.x = base_list[player.index].position.x
            player.position.y = base_list[player.index].position.y

class TheWorld(Item):
    '''
    Make all the other players not able to move for ? seconds
    '''
    def __init__(self, player, ev_manager):
        super().__init__(player)
        self.duration = model_const.the_world_duration
        self.ev_manager = ev_manager

    def trigger(self):
        self.ev_manager.post(EventTheWorldStart(self))

    def update(self):
        self.duration -= 1
        if self.duration == 0:
            self.ev_manager.post(EventTheWorldStop(self))

