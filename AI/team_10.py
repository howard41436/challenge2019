from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 0, 0, 0, 0] # Set the number of your equipments.
        self.color = (255, 79, 174) # Set the color you like.
        self.hanFen = False




    def decide(self):
        my_pos = self.helper.get_player_position()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        oil_pos =self.helper.get_oils()
        oilslevel=self.helper.get_oils_level()
        market_item = self.helper.get_market()[0]
        distance_to_market = self.helper.get_distance(my_pos, self.helper.market_position)
        amount_oils=len(self.helper.get_oils())
        index=(0,225,500,700,1000)
        destination = None

        #我和所有玩家的距離
        players_distance_below_150 = 0
        players_array = []
        for i in range(4):
            if i == self.helper.player_id:
                continue
            if self.helper.get_distance(my_pos, self.helper.get_player_position(i)) < 150:
            #我和所有玩家距離有幾個比150小
                players_distance_below_150 += 1
                players_array.append((i, self.helper.get_player_value(i)))

        # Begin of Merge
        # The world
        if self.helper.get_market()[0] == "TheWorld" and carry >= 1450:
            destination = self.helper.market_position
            dist = self.helper.get_distance(my_pos, destination)
            if dist < self.helper.player_radius + self.helper.market_radius:
                return AI_TRIGGER_ITEM


        if not self.helper.get_player_item_is_active() and self.helper.get_player_item_name() == "TheWorld":
            return AI_TRIGGER_ITEM
        # End of Merge

        #I go home
        #購買
        if market_item == "IGoHome" and self.helper.get_player_item_name() == None:
            if carry > 500:
                destination = self.helper.market_position
                if distance_to_market < self.helper.market_radius:
                    return AI_TRIGGER_ITEM
                direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
                return self.helper.get_direction(direction)
        #使用:
        #看他們的原本設定(最大負載量)
        if self.helper.get_distance(my_pos, home) > 150 and \
        carry > 2000 and \
        self.helper.get_player_item_name() == "IGoHome":
            return AI_TRIGGER_ITEM

        #韓粉
        #購買(搶得到?)
        
        if market_item == "RadiusNotMove" and self.helper.get_player_item_name() == None:
            if carry > 500:
                destination = self.helper.market_position
                if distance_to_market < self.helper.market_radius:
                    self.hanFen = True
                    return AI_TRIGGER_ITEM
                direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
                return self.helper.get_direction(direction)
        #使用: 如果範圍內有兩個敵人或有超過多少錢的敵人
        if self.helper.get_player_item_name() == "RadiusNotMove" and self.hanFen:
            if players_distance_below_150 >= 2:
                self.hanFen = False
                return AI_TRIGGER_ITEM
            else :
                for i in range(len(players_array)) :
                    if players_array[i][1] - carry > 1000:
                        self.hanFen = False
                        return AI_TRIGGER_ITEM

        best = (1,5,-1)
        for i in range(4):
            if i == self.helper.player_id:
                continue
            delta = self.helper.get_player_value(i) - carry
            if delta > 2000:
                cp = delta /  self.helper.get_distance( my_pos,self.helper.get_player_position(i) ) / 2
                if cp > best[2]:
                    best = (0,i,cp) 
        for i in range(amount_oils):
            if (index[oilslevel[i]] / self.helper.get_distance(my_pos,oil_pos[i])) > best[2]:
            	best = (1,i,index[oilslevel[i]] / self.helper.get_distance(my_pos,oil_pos[i]))
        if best[0] is 0:
        	destination = self.helper.get_player_position(best[1]) if carry < 1500 else home
        else:
        	if best[2] != -1:
        		destination = oil_pos[best[1]] if carry < 2000 else home
        if destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)