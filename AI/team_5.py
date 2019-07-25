from AI.base import *

class TeamAI(BaseAI):

    def vector_sub(self, u, v):
                return (u[0] - v[0], u[1] - v[1])

    def is_in_market(self):
        my_pos = self.helper.get_player_position()
        market_radius = self.helper.market_radius
        return self.helper.get_distance(my_pos, self.helper.market_position) < market_radius

    def __init__(self, helper):
        self.helper = helper
        self.equipments = [1, 3, 0, 4, 0] # Set the number of your equipments.
        self.color = (123, 235, 235) # Set the color you like.


    def decide(self):
        my_pos = self.helper.get_player_position()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()# 最近的石油位址
        home = self.helper.get_base_center()# 半圓形基地
        
        my_id = self.helper.player_id
        myspeed = self.helper.get_player_speed(my_id)
        mymoney = self.helper.get_player_value(my_id)
        richman_id = self.helper.get_most_valuable_player()
        richman_pos = self.helper.get_player_position(richman_id)
        richman_money = self.helper.get_player_value(richman_id)
        richmanspeed = self.helper.get_player_speed(richman_id)
        attack_cp = 0
        poormanmoney = -1000000
        poorman_id = 0

        market_pos = self.helper.get_market_center()
        radius = self.helper.player_radius #半徑
        market_radius = self.helper.market_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        get_distance = self.helper.get_distance 

        if self.helper.get_player_item_name(my_id) != None:
            if self.helper.get_player_item_is_active(my_id) == False:
                #f self.helper.get_player_item_name(my_id) == 'IGoHome' and mymoney > 000:
                #   return AI_TRIGGER_ITEM
                if self.helper.get_player_item_name(my_id) == 'TheWorld':
                    return AI_TRIGGER_ITEM
                if self.helper.get_player_item_name(my_id) == 'MagnetAttract':
                    return AI_TRIGGER_ITEM


        if mymoney > 3000 :
            direction = (home[0] - my_pos[0], home[1] - my_pos[1])
            return self.helper.get_direction(direction)

        if self.helper.get_market()[0] == 'TheWorld':
            if mymoney > 2000 :
                if get_distance(my_pos, market_pos) <= market_radius:
                    return AI_TRIGGER_ITEM
                else:
                    destination = market_pos 
                direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
                return self.helper.get_direction(direction)
        if self.helper.get_market()[0] == 'MagnetAttract':
            if mymoney > 700 :
                if get_distance(my_pos, market_pos) < market_radius:
                    return AI_TRIGGER_ITEM
                else:
                    destination = market_pos
                direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
                return self.helper.get_direction(direction)
        #  self.helper.get_market()[0] == 'IGoHome':
        #  if mymoney > self.helper.get_market()[1]:
        #      if not self.is_in_market():
        #           return self.helper.get_direction(self.vector_sub(self.helper.market_position, self.helper.get_player_position(my_id)))
        #        else:
        #            return AI_TRIGGER_ITEM
        if richman_id != my_id: 
            dist = self.helper.get_distance(richman_pos, my_pos)
            base = self.helper.get_base_center(richman_id)
            basedist = self.helper.get_distance(richman_pos,base)
            if basedist / richmanspeed -35 > dist / myspeed:
                attack_cp = (richman_money - mymoney) / 2 / dist 
            else:
                attack_cp = 0
        #####
        oils = self.helper.get_oils()
        level = self.helper.get_oils_level()
        max_cp = 0
        max_number = -1
        length = len(oils)
        for i in range(length) :
            if(level[i] == 1):
                cp = 225*1.331/self.helper.get_distance(oils[i], my_pos)
                if(max_cp < cp):
                    max_cp = cp
                    max_number = i
            if(level[i] == 2):
                cp = 500*1.331/self.helper.get_distance(oils[i], my_pos)
                if(max_cp < cp):
                    max_cp = cp
                    max_number = i
            if(level[i] == 3):
                cp = 700*1.331/self.helper.get_distance(oils[i], my_pos)
                if(max_cp < cp):
                    max_cp = cp
                    max_number = i
            if(level[i] == 4):
                cp = 1000*1.331/self.helper.get_distance(oils[i], my_pos)
                if(max_cp < cp):
                    max_cp = cp
                    max_number = i
        if(attack_cp > max_cp):
            direction = (richman_pos[0] - my_pos[0], richman_pos[1] - my_pos[1])
        else:
            direction = (oils[max_number][0] - my_pos[0], oils[max_number][1] - my_pos[1])
        for i in range(0, 4):
            if i != my_id and (poormanmoney < self.helper.get_player_value(i)):
                poormanmoney = self.helper.get_player_value(i)
                poorman_id = i
        poorman_pos = self.helper.get_player_position(poorman_id)
        radius = self.helper.player_radius #半徑
        if (mymoney - poormanmoney >= 1000):
                if ((my_pos[0] - poorman_pos[0])**2 + (my_pos[1] - poorman_pos[1])**2)**0.5 < 200 :
                    direction = (home[0] - my_pos[0], home[1] - my_pos[1])
        return self.helper.get_direction(direction)

        

#道具
#oil 
#avoid attack
#attack others AI when self oil < others
#purple 339 #pink 634 #gray 865 #blaack 1331 
#分數越高，
#distance 接近別人家的時候，原路折返，
#otherwise distance 別人接近家的時候，，
#範圍