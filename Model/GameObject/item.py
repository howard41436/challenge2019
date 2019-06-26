import random

from pygame.math import Vector2 as Vec

import Model.const as model_const
from Events.Manager import *

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
        self.name = None

    def trigger(self, ev_manager):
        ev_manager.post(EventCutInStart(self.player_index, self.name))

class IGoHome(Item):
    '''
    Make one player move to his/her base
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.name = 'IGoHome'
        self.price = model_const.item_price[self.name]


    def trigger(self, ev_manager):
        ev_manager.post(EventIGoHome(self.player_list[self.player_index]))
        for player in self.player_list:
            if self.player_index == player.index:
                player.position = Vec(self.base_list[player.index].center)
        self.player_list[self.player_index].item = None

class OtherGoHome(Item):
    '''
    Make other players move to their base
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.name = 'OtherGoHome'
        self.price = model_const.item_price[self.name]

    def trigger(self, ev_manager):
        ev_manager.post(EventOtherGoHome(self.player_list[self.player_index]))
        for player in self.player_list:
            if self.player_index != player.index:
                player.position = Vec(self.base_list[player.index].center)
        self.player_list[self.player_index].item = None

class TheWorld(Item):
    '''
    Za Warudo!
    Only the player who triggered this item is able to move, pick up oil and item, and use other items,
    like the whole game is the player's own world.
    This effect will last ? seconds.
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.freeze_list = []
        self.name = 'TheWorld'
        self.price = model_const.item_price[self.name]

    def trigger(self, ev_manager):
        super().trigger(ev_manager)
        ev_manager.post(EventTheWorldStart(self.player_list[self.player_index]))
        self.duration = model_const.the_world_duration
        self.active = True
        for player in self.player_list:
            if player.index != self.player_index:
                player.freeze = True
                self.freeze_list.append(player)

    def update(self, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            self.close(ev_manager)

    def close(self, ev_manager):
        # ev_manager.post(EventTheWorldStop(self.player_list[self.player_index]))
        self.active = False
        self.player_list[self.player_index].item = None
        for player in self.freeze_list:
            player.freeze = False

class MagnetAttract(Item):
    '''
    Make all oils attract to this player
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.name = 'MagnetAttract'
        self.price = model_const.item_price[self.name]

    def trigger(self, ev_manager):
        ev_manager.post(EventMagnetAttractStart(self.player_list[self.player_index]))
        self.duration = model_const.magnet_attract_duration
        self.active = True
        for player in self.player_list:
            if player.index == self.player_index:
                player.magnet_attract = True

    def update(self, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            self.close(ev_manager)

    def close(self, ev_manager):
        # ev_manager.post(EventMagnetAttractStop(self.player_list[self.player_index]))
        self.active = False
        self.player_list[self.player_index].item = None
        for player in self.player_list:
            if player.index == self.player_index:
                player.magnet_attract = False

class RadiationOil(Item):
    '''
    Make some's bases balue * multiplier (< 1 constant)
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.name = 'RadiationOil'
        self.price = model_const.item_price[self.name]

    def trigger(self, ev_manager):
        ev_manager.post(EventRadiationOil(self.player_list[self.player_index]))
        position = self.player_list[self.player_index].position
        for base in self.base_list:
            if base.center.x - base.length/2 <= position.x <= base.center.x + base.length/2 and \
               base.center.y - base.length/2 <= position.y <= base.center.y + base.length/2:
                base.value_sum *= model_const.radius_oil_multiplier
        self.player_list[self.player_index].item = None
               
class Invincible(Item):
    '''
    Make the player itself immune to collision
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.name = 'Invincible'
        self.price = model_const.item_price[self.name]

    def trigger(self, ev_manager):
        ev_manager.post(EventInvincibleStart(self.player_list[self.player_index]))
        self.duration = model_const.invincible_duration
        self.active = True
        self.player_list[self.player_index].is_invincible = True

    def update(self, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            self.close(ev_manager)

    def close(self, ev_manager):
        # ev_manager.post(EventInvincibleStop(self.player_list[self.player_index]))
        self.active = False
        self.player_list[self.player_index].is_invincible = False
        self.player_list[self.player_index].item = None


class RadiusNotMove(Item):
    '''
    Make all the other players in the range of ? that can not move for ? seconds
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.freeze_list = []
        self.name = 'RadiusNotMove'
        self.price = model_const.item_price[self.name]

    def trigger(self, ev_manager):
        ev_manager.post(EventRadiusNotMoveStart(self.player_list[self.player_index]))
        self.duration = model_const.radius_not_move_duration
        self.active = True
        position = self.player_list[ self.player_index ].position
        for player in self.player_list:
            if player.index != self.player_index and \
               Vec.magnitude(position - player.position) <= model_const.radius_not_move_radius + player.radius:
                player.freeze = True
                self.freeze_list.append(player)

    def update(self, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            self.close(ev_manager)

    def close(self, ev_manager):
        # ev_manager.post(EventRadiusNotMoveStop(self.player_list[self.player_index]))
        self.active = False
        self.player_list[self.player_index].item = None
        for player in self.freeze_list:
            player.freeze = False

def get_disarrangement(n):
    ls = [i for i in range(n)]
    while True:
        random.shuffle(ls)
        flag = True
        for i in range(n):
            if i == ls[i]: 
                flag = False
                break
        if flag:
            break
    return ls

class ShuffleBases(Item):
    '''
    Make other players move to their base
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.name = 'ShuffleBases'
        self.price = model_const.item_price[self.name]

    def trigger(self, ev_manager):
        ev_manager.post(EventShuffleBases(self.player_list[self.player_index]))
        disarrangement = get_disarrangement(model_const.player_number)
        for index in range(model_const.player_number):
            self.base_list[index].center.x = model_const.base_center[disarrangement[index]][0]
            self.base_list[index].center.y = model_const.base_center[disarrangement[index]][1]
        self.player_list[self.player_index].item = None

class FaDaCai(Item):
    '''
    發大財(Only MasterAI can use this item)
    '''
    def __init__(self, player_list, oil_list, base_list, player_index):
        super().__init__(player_list, oil_list, base_list, player_index)
        self.name = 'FaDaCai'
        self.price = model_const.item_price[self.name]

    def trigger(self, ev_manager):
        ev_manager.post(EventFaDaCaiStart(self.player_list[self.player_index]))
        self.duration = model_const.fadacai_duration
        self.active = True

    def update(self, ev_manager):
        self.duration -= 1
        if self.duration == 0:
            self.close(ev_manager)

    def close(self, ev_manager):
        # ev_manager.post(EventFaDaCaiStop(self.player_list[self.player_index]))
        self.active = False
        self.player_list[self.player_index].item = None

