import Model.const as model_const
from pygame.math import Vector2 as Vec

class Item(object):
    '''
    Base Item
    '''
    def __init__(self):
        self.duration = 0
        self.position = None
        self.player_index = None

class GoHome(Item):
    '''
    Make all player move to their base
    '''
    def __init__(self):
        super().__init__()

    def trigger(self, player, ev_manager):
        ev_manager.post(EventGoHome(player))

class TheWorld(Item):
    '''
    Make all the other players not able to move for ? seconds
    '''
    def __init__(self):
        super().__init__()

    def trigger(self, player, ev_manager):
        ev_manager.post(EventTheWorldStart(player))
        self.duration = model_const.the_world_duration

    def update(self):
        self.duration -= 1
        if self.duration == 0:
            self.ev_manager.post(EventTheWorldStop(player))

class MagnetAttract(Item):
    '''
    Make all player attract to this player
    '''
    def __init__(self):
        super().__init__()

    def trigger(self, player, ev_manager):
        ev_manager.post(EventMagnetAttractStart(player))
        self.duration = model_const.magnet_attract_duration

    def update(self):
        self.duration -= 1
        if self.duration == 0:
            self.ev_manager.post(EventMagnetAttractStop(player))
