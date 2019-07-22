from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 0, 0, 0, 0] # Set the number of your equipments.
        self.color = (0, 130, 200) # Set the color you like.


    def decide(self):
        my_pos = self.helper.get_player_position() #位置
        radius = self.helper.player_radius
        carry = self.helper.get_player_value() #負重
        #nearest_oil_pos = self.helper.get_nearest_oil(my_id) #最近的石油位置
        home = self.helper.get_base_center() #家的位置
        nearest_player_id = self.helper.get_nearest_player()
        nearest_id_carry = self.helper.get_player_value(nearest_player_id)
        valuable_player = self.helper.get_most_valuable_player()#油水最多玩家id
        most_valueable_player_position = self.helper.get_player_position(valuable_player)

        
        #todo 計算max_cp值
        max_cp=-1
        all_carry_list= self.helper.get_players_value() #全員負重
        all_pos_list= self.helper.get_players_position() #位置
        my_id=self.helper.player_id
        nearest_oil_pos = self.helper.get_nearest_oil(my_id) 
        #my_position=self.helper.get_player_position(my_id)
        best_direction=self.helper.get_player_position(my_id)
        for oil in range(len(all_carry_list)):
            #my_position=#todo
            dis_xy=all_pos_list[oil]
            if dis_xy==my_pos:
                continue
            value=all_carry_list[oil]
            dis=(((my_pos[0]-dis_xy[0])**2)+((my_pos[1]-dis_xy[1])**2))**0.5
            cp=value*(1/dis) #if dis!=0 else 100000 #dis為0無法執行else數字先隨意打
            if cp>max_cp:
                max_cp=cp
                best_direction=dis_xy
            else:
                max_cp=max_cp
                best_direction=best_direction
        
            

            
        destination=None
        all_oils_pos = self.helper.get_oils()#位置
        all_oils_level = self.helper.get_oils_level()#價值
        cp_max = 0
        bestOil_place=None
        if carry>=2000:
            destination=home
            if (self.helper.get_distance(my_pos,nearest_oil_pos) < 10):
                destination=nearest_oil_pos
                return self.helper.get_direction((destination[0]-my_pos[0],destination[1]-my_pos[1]))
            else:
                return self.helper.get_direction((destination[0]-my_pos[0],destination[1]-my_pos[1]))

        elif carry < 1500 and max_cp > 1 : #max_cp > 某數
            destination = best_direction #到最有價值玩家的地方

            return self.helper.get_direction((destination[0]-my_pos[0],destination[1]-my_pos[1]))
        else:
            destination = nearest_oil_pos   
            if destination is None:
                return AI_DIR_STOP
            else:
                print(destination, my_pos)

                for i in range(len(all_oils_pos)):
                    dist=self.helper.get_distance(all_oils_pos[i],my_pos)
                    if all_oils_level[i] == 1:
                        price = 225
                    elif all_oils_level[i] == 2:
                        price = 500
                    elif all_oils_level[i] == 3:
                        price = 700
                    elif all_oils_level[i] == 4:
                        price = 1000
            #if all_oils_pos[i] == self.helper.get_nearest_oil():
            #   price+=1000
                    cp_now = price/dist
    #all_oils_cp.append(cp_now)
                    if cp_now > cp_max:
                        cp_max = cp_now
                        bestOil_place=all_oils_pos[i]
                    else:
                        cp_max=cp_max
                        bestOil_place=bestOil_place
                destination=bestOil_place
                return self.helper.get_direction((destination[0]-my_pos[0],destination[1]-my_pos[1]))