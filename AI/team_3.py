from AI.base import *

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [1, 0, 3, 1, 0] # Set the number of your equipments.
        self.color = (255, 0, 255) # Set the color you like.


    def decide(self):
        my_speed=self.helper.get_player_speed()
        my_pos = self.helper.get_player_position()
        radius = self.helper.player_radius
        carry = self.helper.get_player_value()
        nearest_oil_pos = self.helper.get_nearest_oil()
        home = self.helper.get_base_center()
        destination = nearest_oil_pos if carry < 2000 else home
        get_oil = self.helper.get_oils()
        my_speed = self.helper.get_player_speed()
        oil_level = self.helper.get_oils_level()

        #oil
        if destination is None:
            return AI_DIR_STOP
        elif destination == home: 
            direction = (home[0] - my_pos[0], home[1] - my_pos[1])
            return self.helper.get_direction(direction)
        else:
            cp = []
            i = 0
            for x, y in get_oil:
                temp = (((x - my_pos[0]) ** 2 + (y - my_pos[1]) ** 2) ** 0.5) / my_speed
                cp.append(oil_level[i] / temp)
                i += 1
        
            max_cp_index = cp.index(max(cp))
            X, Y = get_oil[max_cp_index]
            direction = (X - my_pos[0], Y - my_pos[1])
            return self.helper.get_direction(direction)

        #attack
        l = []
        for players_id in {0,1,2,3}-{self.helper.player_id}:
            oil =  self.helper.get_player_value(players_id)
            pos = self.helper.get_player_position(players_id)
            speed = self.helper.get_player_speed(players_id)
            distance = ((pos[0]-my_pos[0])**2+(pos[1]-my_pos[1])**2)**0.5
            if distance >=  150:
                continue
            if speed >= my_speed:
                continue
            time = distance/(my_speed-speed)
            cp = ((oil+carry)/2-carry)/time
            l.append((cp,players_id))
        l.sort(reverse=True)
        if len(l)>0:
            pos1=self.helper.get_player_position(l[0][1])
            direction = (pos1[0] - my_pos[0], pos1[1] - my_pos[1])
            return self.helper.get_direction(direction)
        else:#to do state transition?
            return AI_DIR_STOP

