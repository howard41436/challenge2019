from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 1, 0, 0, 0] # Set the number of your equipments.
        self.color = (60,180,75) # Set the color you like.


    def decide(self):
        my_pos = self.helper.get_player_position()
        nearest_player = self.helper.get_nearest_player()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_player_value = self.helper.get_player_value(nearest_player)
        my_value = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        oils_pos = self.helper.get_oils()
        oils_level = self.helper.get_oils_level()
        game_len, game_wid = self.helper.game_size
        item = self.helper.get_market()
        my_item_name = self.helper.get_player_item_name()
        useful_item = ['IGoHome', 'OtherGoHome', 'TheWorld', 'MagnetAttract', 'Invincible', 'RadiusNotMove']
        destination = None
        if item[0] is not None and item[0] in useful_item and carry >= item[1] and self.helper.get_player_item_is_active() is False:
            destination = self.helper.market_position # Go to market
        if my_item_name is not None and self.helper.get_player_item_is_active() is False:
            i = 0
            if my_item_name == 'IGoHome':
                if nearest_player_value > my_value:
                    if self.helper.get_distance(my_pos, self.helper.get_player_position(nearest_player)) < 3 * radius:
                        return AI_TRIGGER_ITEM
                elif item[2] < 100:
                    return AI_TRIGGER_ITEM 
            elif my_item_name == 'OtherGoHome':
                players_pos = self.helper.get_players_position()
                othergohome_radius = self.helper.game_size[0] * 3 / 5
                num_players_inside = 0
                for i in range(4):
                    player_distance_to_center = self.helper.get_distance_to_center(players_pos[i])
                    if player_distance_to_center < othergohome_radius:
                        num_players_inside += 1
                if num_players_inside > 2:
                    return AI_TRIGGER_ITEM
            elif my_item_name == 'TheWorld':
                if my_value < 1000:
                    return AI_TRIGGER_ITEM
                else:
                    destination = home
                    direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
                    return self.helper.get_direction(direction)
            elif my_item_name == 'MagnetAttract':
                return AI_TRIGGER_ITEM
            elif my_item_name == 'Invincible':
                if nearest_player_value > my_value:
                    if self.helper.get_distance(my_pos, self.helper.get_player_position(nearest_player)) < 3 * radius:
                        return AI_TRIGGER_ITEM
                elif item[2] < 100:
                    return AI_TRIGGER_ITEM 
            elif my_item_name == 'RadiusNotMove':
                player_position = self.helper.get_players_position()
                player_oils = self.helper.get_bases_value()
                max_id = player_oils.index(max(player_oils))
                if max_id == self.helper.player_id:
                    max_id = player_oils.index(sorted(player_oils, reverse=True)[1])
                if self.helper.get_distance(player_position[max_id], my_pos) < self.helper.radius_not_move_radius:
                    return AI_TRIGGER_ITEM
            elif my_item_name == 'ShuffleBases':
                return AI_TRIGGER_ITEM
        if self.helper.get_distance(my_pos,self.helper.market_position) < self.helper.market_radius and item[0] is not None and item[0] in useful_item and self.helper.get_player_item_is_active() is False and carry > (item[1] if item[1] is not None else 100000):
            return AI_TRIGGER_ITEM # Buy item

        #if destination is None:
        #    return AI_DIR_STOP
        #else:
        #    direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
        #    return self.helper.get_direction(direction)

        
        #crash or not
        if nearest_player_value > my_value:
            if (nearest_player_value - my_value)/2 > 1000:
                destination = self.helper.get_player_position(nearest_player)
                direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
                return self.helper.get_direction(direction)
        

        """
        #TAKE OIL
        destination = nearest_oil_pos if carry < 5000 else home
        if destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)
        """

        #take oil 2.0
        distance = []
        cp = []
        for i in range(len(oils_pos)):
            distance.append(self.helper.get_distance(oils_pos[i], my_pos))
            cp.append(oils_level[i] / distance[i])
        if cp:
            max_cp = max(cp)
            max_cp_index = cp.index(max_cp)
            destination = oils_pos[max_cp_index] if carry < 3000 else home
        if destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)
