from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 0, 0, 0, 0] # Set the number of your equipments.
        self.color = (0, 255, 255) # Set the color you like.
    def decide(self):
        my_pos = self.helper.get_player_position()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        destination = nearest_oil_pos if carry < 2000 else home
        item = self.helper.get_market()
        my_item_name = self.helper.get_player_item_name()
        useful_item = ['IGoHome', 'OtherGoHome', 'TheWorld', 'MagnetAttract', 'Invincible', 'RadiusNotMove']
        if item[0] is not None and item[0] in useful_item and carry >= item[1] and self.helper.get_player_item_is_active() is False:
            destination = self.helper.market_position # Go to market
        if my_item_name is not None and self.helper.get_player_item_is_active() is False:
            if my_item_name == 'IGoHome':
                if carry > 2500:
                    return AI_TRIGGER_ITEM
            elif my_item_name == 'OtherGoHome':
                if carry > 3000:
                    return AI_TRIGGER_ITEM
            elif my_item_name == 'TheWorld':
                return AI_TRIGGER_ITEM
            elif my_item_name == 'MagnetAttract':
                return AI_TRIGGER_ITEM
            elif my_item_name == 'Invincible': 
                if carry >3000:
                    return AI_TRIGGER_ITEM
            elif my_item_name == 'RadiusNotMove':
                player_position = self.helper.get_players_position()
                for i in range(4):
                    distance = my_pos-player_position[i] < self.helper.radius_not_move_radius
                    return AI_TRIGGER_ITEM
            elif my_item_name == 'ShuffleBases':
                return AI_TRIGGER_ITEM
        if self.helper.get_distance(my_pos,self.helper.market_position) < self.helper.market_radius and item[0] is not None and item[0] in useful_item and self.helper.get_player_item_is_active() is False and carry > (item[1] if item[1] is not None else 100000):
            return AI_TRIGGER_ITEM # Buy item

        if destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)