from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 1, 1, 0, 1] # Set the number of your equipments.
        self.color = (245, 130, 48) # Set the color you like.
        self.destination = None

    def decide(self):
        my_pos = self.helper.get_player_position()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        nearplayer=self.helper.get_nearest_player()
        nearplayerpos = self.helper.get_player_position(nearplayer)
        dist = self.helper.get_distance(my_pos,nearplayerpos)
        base_pos = self.helper.get_base_center()
        oil_pos = self.helper.get_oils()
        oil_price = self.helper.get_oils_distance_to_center()
        me_oil_distance = list(self.helper.get_distance(self.helper.get_player_position(), oil_pos[i]) for i in range(len(oil_pos)))
        max_cp = -1
        max_i = 0
        best_cp = -1
        str_item = self.helper.get_player_item_name()
        item = self.helper.get_market()
        market = self.helper.get_market_center()
        best_destination = None

        if str_item and not self.helper.get_player_item_is_active():
            return AI_TRIGGER_ITEM


        elif item[0] == 'IGoHome':
            if not self.helper.get_player_item_name(self.helper.player_id) and (self.helper.get_distance(market,my_pos) < 15) and item[0]:
                return AI_TRIGGER_ITEM
            if carry >= item[1]:
                market = self.helper.get_market_center()
                m_direct = (market[0]-my_pos[0],market[1]-my_pos[1])
                return self.helper.get_direction(m_direct)
        elif item[0] == 'TheWorld':
            if not self.helper.get_player_item_name(self.helper.player_id) and (self.helper.get_distance(market,my_pos) < 15) and item[0]:
                return AI_TRIGGER_ITEM
            if carry >= item[1]:
                market = self.helper.get_market_center()
                m_direct = (market[0]-my_pos[0],market[1]-my_pos[1])
                return self.helper.get_direction(m_direct)
        elif item[0] == 'MagnetAttract':
            if not self.helper.get_player_item_name(self.helper.player_id) and (self.helper.get_distance(market,my_pos) < 15) and item[0]:
                return AI_TRIGGER_ITEM
            if carry >= item[1]:
                market = self.helper.get_market_center()
                m_direct = (market[0]-my_pos[0],market[1]-my_pos[1])
                return self.helper.get_direction(m_direct)
        elif item[0] == 'RadiationOil':
            if not self.helper.get_player_item_name(self.helper.player_id) and (self.helper.get_distance(market,my_pos) < 15) and item[0]:
                return AI_TRIGGER_ITEM
            if carry >= item[1]:
                market = self.helper.get_market_center()
                m_direct = (market[0]-my_pos[0],market[1]-my_pos[1])
                return self.helper.get_direction(m_direct)

        #attack
        if(dist < 40 and self.helper.get_player_value(nearplayer)-self.helper.get_player_value()>1000):
            if(self.helper.get_player_speed(nearplayer)<self.helper.get_player_speed()):   
                attack_cp = 1/(((self.helper.get_player_value(nearplayer)-self.helper.get_player_value())/2)*dist)
                # print(attack_cp)
                if attack_cp > best_cp:
                    best_cp=attack_cp
                    best_destination=nearplayerpos
        #defense
        elif(dist < 40 and self.helper.get_player_value(nearplayer)<=self.helper.get_player_value()):
            #  print("defense emerge")
            direction = (my_pos[0]-nearplayerpos[0], my_pos[1]-nearplayerpos[1]) 
            return self.helper.get_direction(direction)
        #oil
        for i in range(len(oil_pos)):
            oil_cp = 1 / (oil_price[i] * me_oil_distance[i])
            if max_cp < oil_cp:
                max_cp = oil_cp
                max_i = i
                max_oil_pos = oil_pos[i]
        home = self.helper.get_base_center()
        if(max_cp>best_cp):
            best_cp = max_cp
            best_destination = max_oil_pos

        if(best_destination == nearplayerpos):
            pass
            # print("attack emerge")

        if len(oil_pos) == 0:
            best_destination = None

        if best_destination is None:
            return AI_DIR_STOP
        else :
            if(carry < 2500):    
                self.destination=best_destination
                direction = (self.destination[0] - my_pos[0], self.destination[1] - my_pos[1])
                return self.helper.get_direction(direction)
            else :
                direction = (home[0] - my_pos[0], home[1] - my_pos[1])
                return self.helper.get_direction(direction)
