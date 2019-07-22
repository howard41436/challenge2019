from AI.base import *






class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [1, 1, 0, 1, 3] # Set the number of your equipments.
        self.color = (240, 50, 230) # Set the color you like.

    def get_near_oil_level(self):
        value = 0
        oil_list = self.helper.get_oils()
        oil_level = self.helper.get_oils_level()
        my_pos = self.helper.get_player_position()
        oil_pos = self.helper.get_oils_distance_to_center()
        for i, pos in enumerate(oil_list):
            if self.helper.get_distance(my_pos, pos) < self.helper.base_length*2:
                value += oil_level[i]
        return value

    def decide(self):
        my_pos = self.helper.get_player_position()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        base_length = self.helper.base_length
        my_id = self.helper.player_id
        my_speed = self.helper.get_player_speed(my_id)
        preys_id = self.helper.get_nearest_player(my_id)
        preys_pos = self.helper.get_player_position(preys_id)
        preys_speed = self.helper.get_player_speed(preys_id)
        preys_dis = self.helper.get_distance(my_pos , preys_pos) 
        thedirection = self.helper.get_direction((preys_pos[0] - my_pos[0], preys_pos[1] - my_pos[1]))
        item = self.helper.get_player_item_name(my_id)
        mrk_pos = self.helper.market_position
        oil_list = self.helper.get_oils()
        oil_level = self.helper.get_oils_level()
        oil_pos = self.helper.get_oils_distance_to_center()
        richest_id = self.helper.get_most_valuable_player()
        richest_pos = self.helper.get_player_position(richest_id)
        richest_dis = self.helper.get_distance(my_pos , richest_pos)
        richest_val = self.helper.get_player_value(richest_id)
        preys_val = self.helper.get_player_value(preys_id)
        shop_item = self.helper.get_market() #tupple 名稱、價錢，下一個倒數計時
        my_money = self.helper.get_player_value(my_id)
        market_pos = self.helper.market_position
        shop_direction = self.helper.get_direction((market_pos[0]-my_pos[0],market_pos[1]-my_pos[1]))
        destination = None
        market_r=self.helper.market_radius
        distance = self.helper.get_distance(my_pos , market_pos)

         


        if (market_r + radius) < distance < 60:
            
            return shop_direction

        if distance < market_r + radius < 75:
            
            if shop_item[0] != None:   #商城有東西
                if item == None:   #你身上沒東西
                    if shop_item[0] == 'IGoHome' :
                        if my_money >= 500:
                            return AI_TRIGGER_ITEM
                    elif shop_item[0] == 'MagnetAttract':
                        if my_money >= 689:
                            return AI_TRIGGER_ITEM
                    elif shop_item[0] == 'RadiusNotMove':    
                        if my_money >= 500:
                            return AI_TRIGGER_ITEM
                    

        #道具使用時機(購買後)
        if item == 'IGoHome' and self.helper.get_player_item_is_active(my_id) == False:#傳送
            if preys_dis < base_length/2 and my_speed < preys_speed and carry - preys_val > 1000:
                return 9
        elif item == 'MagnetAttract' and self.helper.get_player_item_is_active(my_id) == False:#磁鐵
            value = self.get_near_oil_level()
            if value > 15:
                return 9
        elif item == 'RadiusNotMove' and self.helper.get_player_item_is_active(my_id) == False:#範圍內不能移動
            if preys_dis < self.helper.radius_not_move_radius:
                return 9

        players_pos = self.helper.get_players_position()
        va = self.helper.get_players_speed()
        v2 = self.helper.get_player_speed()
        oa = self.helper.get_players_value()
        os = self.helper.get_player_value()
        
        for i in range(4):
            d = self.helper.get_distance(my_pos, players_pos[i])
            if d > 0:
                oa[i] = (oa[i] - os) / 2 * (v2-va[i]) / d
            else :
                oa[i] = 0
        max_robv = max(oa)
        oil_pos = self.helper.get_oils()
        v = self.helper.get_oils_level()
        for i in range(len(v)):
            if v[i] ==1:
                v[i] = 225
            elif v[i] == 2:
                v[i] = 500
            elif v[i] == 3:
                v[i] = 700
            else:
                v[i] = 1000
        count = 0
        if len(v) != 0 :
            for i in oil_pos:
                d = self.helper.get_distance(i , my_pos)
                v[count] /= (d / v2)
                count += 1
            maxoil = max(v)
            max_oil_num = v.index(max(v))
            if max_robv > maxoil:
                destination = players_pos[oa.index(max_robv)]
            else:
                destination = oil_pos[max_oil_num]
        else:
            destination = players_pos[oa.index(max_robv)]
        if carry > 3000:
            destination = home

        if destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)