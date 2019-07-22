from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [1, 0, 2, 1, 1] # Set the number of your equipments.
        self.color = (230, 190, 255) # Set the color you like.


    def decide(self):
        
        my_pos = self.helper.get_player_position()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        center = (self.helper.game_size[0]/2 , self.helper.game_size[1]/2)
        most_valuable_player_id = self.helper.get_most_valuable_player()
        most_valuable_player_pos = self.helper.get_player_position(most_valuable_player_id)
        distance_to_most_valuable_player=((most_valuable_player_pos[0] - my_pos[0])**2 + (most_valuable_player_pos[1] - my_pos[1])**2)**0.5
        most_valuable_player_value=self.helper.get_player_value(most_valuable_player_id)
        most_valuable_player_insurance_value = self.helper.get_player_insurance_value(most_valuable_player_id)
        my_insurance_value = self.helper.get_player_insurance_value()
        most_valuable_player_speed = self.helper.get_player_speed(most_valuable_player_id)
        my_speed = self.helper.get_player_speed()
        most_valuable_player_is_invincible = self.helper.get_player_is_invincible(most_valuable_player_id)
        x = carry - my_insurance_value
        y = most_valuable_player_value - most_valuable_player_insurance_value        
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        income = (x+y)/2 + my_insurance_value - carry        
        maxValue = 0
        for i in range(4):
            if self.helper.get_players_value()[i] > maxValue and i!=most_valuable_player_id :
                maxValue = self.helper.get_players_value()[i]
                second_most_valuable_player_id = i

        second_most_valuable_player_id = self.helper.get_most_valuable_player()
        second_most_valuable_player_pos = self.helper.get_player_position(second_most_valuable_player_id)
        distance_to_second_most_valuable_player=((second_most_valuable_player_pos[0] - my_pos[0])**2 + (second_most_valuable_player_pos[1] - my_pos[1])**2)**0.5
        second_most_valuable_player_value=self.helper.get_player_value(second_most_valuable_player_id)
        second_most_valuable_player_insurance_value = self.helper.get_player_insurance_value(second_most_valuable_player_id)
        second_most_valuable_player_speed = self.helper.get_player_speed(second_most_valuable_player_id)
        second_most_valuable_player_is_invincible = self.helper.get_player_is_invincible(second_most_valuable_player_id)

        second_x = carry - my_insurance_value
        second_y = second_most_valuable_player_value - second_most_valuable_player_insurance_value        
        if second_x < 0:
            second_x = 0
        if second_y < 0:
            second_y = 0
        second_income = (x+y)/2 + my_insurance_value - carry 
        
        market_position = self.helper.market_position
        item = self.helper.get_market()
        my_item_duration = self.helper.get_player_item_duration()
        my_item_name = self.helper.get_player_item_name()
        market_radius = self.helper.market_radius

        if item[0] == 'MagnetAttract' and carry > 689:
            if self.helper.get_distance(my_pos,market_position) < radius + market_radius:
                return AI_TRIGGER_ITEM
            else :
                destination = market_position
                direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
                return self.helper.get_direction(direction)

        if my_item_name == 'MagnetAttract' and self.helper.get_player_item_is_active() == False:
            return AI_TRIGGER_ITEM










        if carry>1450 and item[0] == 'TheWorld' and my_item_name is None:
            if self.helper.get_distance(my_pos, market_position) < radius + market_radius:
                return AI_TRIGGER_ITEM
            else :
                destination = market_position
                direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
                return self.helper.get_direction(direction)    

        if self.helper.get_player_item_name() == 'TheWorld' and self.helper.get_player_item_is_active() == False:
            if sum(sorted(self.helper.get_players_value())[-2:])>5000 and sum(sorted(self.helper.get_oils_level())[-3:])>6:
                return  AI_TRIGGER_ITEM


        if self.helper.get_player_item_duration() > 0 and my_item_name == 'TheWorld':

            
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            income = (x+y)/2 + my_insurance_value - carry        
            maxValue = 0

            if income > 1000:
                destination = most_valuable_player_pos
            elif carry > 1500:
                destination = home
            else:
                destination = nearest_oil_pos



















        if carry > 2500:
            destination = home
            if nearest_oil_pos is not None:
                if self.helper.get_distance(nearest_oil_pos,my_pos) <= 100:
                    homex = home[0]
                    homey = home[1]
                    me_to_home_x = homex - my_pos[0]
                    me_to_home_y = homey - my_pos[1]
                    me_to_oil_x = nearest_oil_pos[0] - my_pos[0]
                    me_to_oil_y = nearest_oil_pos[1] - my_pos[1]

                    if(me_to_home_x * me_to_oil_x >= 0 and me_to_home_y * me_to_oil_y >= 0):
                        destination = nearest_oil_pos
            

        elif income > 1000 and distance_to_most_valuable_player < (self.helper.game_size[0]/2) \
        and not most_valuable_player_is_invincible \
        and ((self.helper.get_distance(home,most_valuable_player_pos) <= self.helper.game_size[0]) \
        or (my_speed > most_valuable_player_speed*1.2)):
            destination = most_valuable_player_pos
        elif second_income > 1000 and distance_to_second_most_valuable_player < (self.helper.game_size[0]/2) \
        and not second_most_valuable_player_is_invincible \
        and ((self.helper.get_distance(home,second_most_valuable_player_pos) <= self.helper.game_size[0]) \
        or (my_speed > second_most_valuable_player_speed*1.2)):
            destination = second_most_valuable_player_pos

        else:
            destination = nearest_oil_pos

        if destination is None:
            return AI_DIR_STOP
        else:
            direction = (destination[0] - my_pos[0], destination[1] - my_pos[1])
            return self.helper.get_direction(direction)
