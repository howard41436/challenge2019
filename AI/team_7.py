from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 0, 0, 0, 0] # Set the number of your equipments.
        self.color = (245, 245, 10) # Set the color you like.


    def decide(self):
        #變數
        my_pos = self.helper.get_player_position()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        speed=self.helper.get_player_speed()
        nearest_player_id=self.helper.get_nearest_player()
        nearest_player_position=self.helper.get_player_position(nearest_player_id)
        distant_nearest_player=((nearest_player_position[0]-my_pos[0])**2+\
        (nearest_player_position[1]-my_pos[1])**2)**0.5
        nearest_player_speed=self.helper.get_player_speed(nearest_player_id)
        nearest_player_value=self.helper.get_player_value(nearest_player_id)
        nearest_player_Ivalue=self.helper.get_player_insurance_value(nearest_player_id)
        market_pos = self.helper.market_position
        best_oil_pos = self.helper.get_oils_by_distance_from_center()      
        best_oil_pos.reverse()
        destination = None
        item = self.helper.get_market()
        center = self.helper.get_distance_to_center(my_pos)
        oils = self.helper.get_oils()
        level = self.helper.get_oils_level()
        summ = 0
        myitem = self.helper.get_player_item_name()
        #搶石油
        if nearest_oil_pos is None:
            nearest_oil_dis = 1000000
        else:
            nearest_oil_dis = self.helper.get_distance(nearest_oil_pos, my_pos)
        my_home_dis_x = home[0] - my_pos[0]
        my_home_dis_y = home[1] - my_pos[1]
        destination = market_pos
        if nearest_oil_pos is not None:
            oil_home_dis_x = home[0] - nearest_oil_pos[0]
            oil_home_dis_y = home[1] - nearest_oil_pos[1]

        if carry > 3500:
            if nearest_oil_pos is not None and ((oil_home_dis_x <= my_home_dis_x and oil_home_dis_y <= my_home_dis_y and nearest_oil_dis < 200) or nearest_oil_dis < 50):
                destination = nearest_oil_pos
            else:
                destination = home
        else:
            for i, pos in enumerate(best_oil_pos):
                j = self.helper.get_distance(pos, my_pos)
                if j < 250:
                    destination = pos
                else:
                    if nearest_oil_pos is not None:
                        destination = nearest_oil_pos
                    else:
                        return AI_DIR_STOP
        #碰撞
        if  distant_nearest_player != 0 and \
            nearest_player_Ivalue/distant_nearest_player > 500 and nearest_player_value > carry:
            nearest_player_position=self.helper.get_player_position(nearest_player_id)
            direction = (nearest_player_position[0] - my_pos[0], nearest_player_position[1] - my_pos[1])
            return self.helper.get_direction(direction)
        #道具使用1
        destination = nearest_oil_pos if carry < 5000 else home
        for x in range(len(oils)):
            dis = self.helper.get_distance(oils[x],my_pos)
            if dis <= self.helper.radius_of_magnetic_attract:
                summ += level[x]            
        
        if summ > 5 and self.helper.get_player_item_name(self.helper.player_id) == 'MagnetAttract' and \
            self.helper.get_player_item_is_active(self.helper.player_id) == False:
            return AI_TRIGGER_ITEM
        if 689 < carry and item[0] == 'MagnetAttract':
            if self.helper.get_distance(my_pos, self.helper.market_position) < self.helper.market_radius + radius:
                return AI_TRIGGER_ITEM
            destination = self.helper.market_position
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1]) 
            return self.helper.get_direction(direction)         
        if 5000 < carry and self.helper.get_player_item_name(self.helper.player_id) == 'IGoHome' and \
            self.helper.get_player_item_is_active(self.helper.player_id) == False:
            return AI_TRIGGER_ITEM
        if 500 < carry and item[0] == 'IGoHome':
            if self.helper.get_distance(my_pos, self.helper.market_position) < self.helper.market_radius + radius:
                return AI_TRIGGER_ITEM
            destination = self.helper.market_position
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1]) 
            return self.helper.get_direction(direction)     
        elif destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)
        #道具使用2
        for x in range(len(oils)):
            dis = self.helper.get_distance(oils[x],my_pos)
            if dis < 160:
                summ += level[x]
        if  item[0] == 'Invincible' and myitem  == None:
            #go to market
            destination = self.helper.market_position
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            #return self.helper.get_direction(direction) 
            
            if self.helper.get_distance(my_pos, self.helper.market_position) < self.helper.market_radius + radius :
                return AI_TRIGGER_ITEM
            else:
                return self.helper.get_direction(direction)
        enemyid = self.helper.get_nearest_player()
        enemypos = self.helper.get_player_position(enemyid)
        enemydis = self.helper.get_distance(enemypos, my_pos)
        enemyoil = self.helper.get_player_value(enemyid)
        enemydirec = self.helper.get_player_direction(enemyid)
        
        direction = (enemypos[0] - my_pos[0], enemypos[1] - my_pos[1])
        
        if carry - enemyoil > 1000 and enemydis < 160 and myitem == 'Invincible' and self.helper.get_player_item_is_active() == False:
            return AI_TRIGGER_ITEM     
        if destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)

