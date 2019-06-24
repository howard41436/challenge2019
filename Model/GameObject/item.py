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

    def trigger(self, player_index, ev_manager, player_list):
        ev_manager.post(EventTheWorldStart(player_list[player_index]))
        self.duration = model_const.the_world_duration
        for player in player_list:
            if player.index != player_index:
                player.freeze = True

    def update(self, player, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            self.close()

    def close(self, ev_manager, player_list):
        ev_manager.post(EventTheWorldStop(player))
        for player in player_list:
            player.freeze = False

class MagnetAttract(Item):
    '''
    Make all player attract to this player
    '''
    def __init__(self):
        super().__init__()

    def trigger(self, player, ev_manager):
        ev_manager.post(EventMagnetAttractStart(player))
        self.duration = model_const.magnet_attract_duration

    def update(self, player, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            ev_manager.post(EventMagnetAttractStop(player))

class Invincible(Item):
    '''
    Make the player itself immune to collision
    '''
    def __init__(self):
        super().__init__()
    
    def trigger(self, player, ev_manager):
        ev.manager.post(EventInvincibleStart(player))
        self.duration = model_const.invincible_duration
    def update(self, player, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            ev_manager.post(EventInvincibleStop(player))
