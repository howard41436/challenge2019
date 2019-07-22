from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [2, 0, 1, 2, 0] # Set the number of your equipments.
        self.color = (255, 255, 0) # Set the color you like.

    def count_near(self,player,place):
        count = 0
        for tu in player:
            if distance(tu,place) < self.helper.radius_not_move_radius:
                count+=1
        return count

    def get_best_oil(self):
        oil_list = self.helper.get_oils()
        oil_level = self.helper.get_oils_level()
        player_speed = self.helper.get_player_speed()
        oil_cp = [0] * len(oil_list)
        for i in range(len(oil_list)):
            dis = distance(oil_list[i], self.helper.get_player_position())
            oil_cp[i] = oil_level[i] / (dis / player_speed)
            if dis > self.helper.market_radius:
                oil_cp[i] = 0
        max_oil = -1
        for x in range(len(oil_cp)):
            if oil_cp[x] > max_oil:
                max_oil = oil_cp[x]
                max_index = x
        return oil_list[max_index]
    
    def decide(self):
        strong = self.helper.get_player_item_is_active()
        player_list = self.helper.get_players_value()
        ene = self.helper.get_players_position()
        my_pos = self.helper.get_player_position()
        market_list = self.helper.get_market()
        if ((self.helper.get_player_item_name() == "TheWorld" or self.helper.get_player_item_name() == "MagnetAttract") and len(self.helper.get_oils()) >= 10 )and not strong:
            return 9
        if self.helper.get_player_item_name() == "RadiusNotMove" and (self.count_near(ene,my_pos) == 3 or market_list[0] == "TheWorld" and self.count_near(ene,my_pos) >= 2) and not strong:
            return 9
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        market_position = self.helper.market_position
        market_radius = self.helper.market_radius
        number_one_id = self.helper.get_most_valuable_player() ##獲得攜帶石油量一名的玩家id

        if carry < 2000:
            if distance(my_pos,ene[number_one_id])<self.helper.game_size[0]/4 and max(player_list)> max(500+carry,1000) - 500*self.equipments[2] :
                destination = ene[number_one_id] 
            elif self.helper.get_oils():
                destination = self.get_best_oil()
        else:
            destination =  home
        if market_list[0] == "TheWorld" and carry >= 1450 and not strong and self.helper.get_player_item_name() == None:
            if distance(my_pos,market_position) <= market_radius:
                return 9
            else:
                destination = market_position
        if market_list[0] == "RadiusNotMove" and carry >= 500 and not strong and self.helper.get_player_item_name() == None:
            if distance(my_pos,market_position)<=market_radius:
                return 9
            else:
                destination = market_position
        if market_list[0] == "MagnetAttract" and carry >= 689 and not strong and self.helper.get_player_item_name() == None:
            if distance(my_pos,market_position)<=market_radius:
                return 9
            else:
                destination = market_position
        if destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)

def distance(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5