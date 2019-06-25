import Model.const as model_const
from pygame.math import Vector2 as Vec

class Item(object):
    '''
    Base Item
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        self.active = False  # taking effect or not
        self.duration = 0
        self.position = None
        self.player_index = player_index
        self.player_list = player_list
        self.oil_list = oil_list
        self.base_list = base_list

class IGoHome(Item):
    '''
    Make one player move to his/her base
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)

    def trigger(self,  ev_manager):
        ev_manager.post(EventIGoHome(player))
        for player in self.player_list:
            if self.player_index == player.index:
                player.position = self.base_list[ player.index ].position

class OtherGoHome(Item):
    '''
    Make other players move to their base
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)

    def trigger(self,  ev_manager):
        ev_manager.post(EventIGoHome(player))
        for player in self.player_list:
            if self.player_index != player.index:
                player.position = self.base_list[ player.index ].position

class TheWorld(Item):
    '''
    Make all the other players not able to move for ? seconds
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)

    def trigger(self, ev_manager):
        ev_manager.post(EventTheWorldStart(self.player_list[self.player_index]))
        self.duration = model_const.the_world_duration
        self.active = True
        for player in self.player_list:
            if player.index != self.player_index:
                player.freeze = True

    def update(self, player, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            self.close(ev_manager)

    def close(self, ev_manager):
        ev_manager.post(EventTheWorldStop(player))
        self.active = False
        player[self.player_index].item = None
        for player in self.player_list:
            player.freeze = False

class MagnetAttract(Item):
    '''
    Make all player attract to this player
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)

    def trigger(self, ev_manager):
        ev_manager.post(EventMagnetAttract(player_list[player_index]))
        self.duration = model_const.the_world_duration
        self.active = True
        for player in player_list:
            if player.index != player_index:
                player.freeze = True

    def update(self, player, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            self.close()

    def close(self, ev_manager, player_list):
        ev_manager.post(EventTheWorldStop(player))
        self.active = False
        player[self.player_index].item = None
        for player in player_list:
            player.freeze = False

class Invincible(Item):
    '''
    Make the player itself immune to collision
    '''
    def __init__(self):
        super().__init__()
    def trigger(self, player, ev_manager):
        ev_manager.post(EventInvincibleStart(player))
        player.is_invisible = True
        self.duration = model_const.invincible_duration
    def update(self, player, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            # TODO: overlap
            player.is_invisible = False
            ev_manager.post(EventInvincibleStop(player))
