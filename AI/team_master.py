from AI.base import *
from pygame.math import Vector2 as Vec

PICK = 9
direct = [
[0, 0],             #steady
[0, -1],             #up
[0.707, -0.707],     #up right
[1, 0],             #right
[0.707, 0.707],    #right down
[0, 1],            #down
[-0.707, 0.707],   #left down
[-1, 0],            #left
[-0.707, -0.707],    #left up
]

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 0, 0, 0, 0]
        self.color = (163, 193, 173)
        self.want_to_buy = {'RadiusNotMove' : 100, 'TheWorld' : 100, 'IGoHome' : 100, 'ShuffleBases': 1, 'Invincible': 1}
        self.FaDaCai1 = True

    def get_best_oil_position(self):
        my_pos = self.helper.get_player_position()
        oil_poses = self.helper.get_oils()
        best_pos = None
        best_cp = -1
        for oil_pos in oil_poses:
            cp = (400 - self.helper.get_distance_to_center(oil_pos)) / (((Vec(my_pos) - Vec(oil_pos)).length())**2)
            if cp > best_cp:
                best_cp = cp
                best_pos = oil_pos
        return best_pos, my_pos, best_cp

    def get_dir(self, dest, my_pos):
        new = Vec(dest) - Vec(my_pos)
        maximum = 0
        record = 0
        for i in range(9):
            if maximum < (new).dot(Vec(direct[i])):
                maximum = (new).dot(Vec(direct[i]))
                record = i
        return record

    def attack(self, carry, my_pos):
        if self.helper.get_player_item_is_active() and self.helper.get_player_item_name() == 'Invincible':
            return 0, 0, 0
        players_value = self.helper.get_players_value()
        players_speed = self.helper.get_players_speed()
        players_position = self.helper.get_players_position()
        my_speed = self.helper.get_player_speed()
        maximum = 0
        target = -1
        for i in range(4):
            if self.helper.player_id == i:
                continue
            #bug
            speed_relative = abs(players_speed[i] - my_speed) if abs(players_speed[i] - my_speed) != 0 else 0.1
            length_relative = (Vec(my_pos) - Vec(players_position[i])).length() if (Vec(my_pos) - Vec(players_position[i])).length() != 0 else 10000
            cp = 0.9e-3 * (players_value[i] - self.helper.get_player_insurance_value(i) - carry) / (length_relative / speed_relative)
            # print("{}th cp is {}".format(i, cp))
            if maximum <= cp and players_speed[i] < my_speed:
                maximum = cp
                target = i
        #print(maximum, players_position[target], target)
        return maximum, players_position[target], target

    def pick_item(self, dest, my_pos, carry):
        if self.helper.get_player_item_name() or self.helper.get_player_item_is_active():
            return dest
        item = self.helper.get_market()
        if ((item[0] == 'RadiationOil' and self.helper.get_timer() <= 85 * 60) or item[0] in self.want_to_buy and self.want_to_buy[item[0]] > 0) \
            and carry > item[1] \
            and not self.helper.get_player_item_name():
            if (Vec(my_pos) - Vec(self.helper.get_market_center())).length() < self.helper.market_radius:
                if item[0] in self.want_to_buy:
                    self.want_to_buy[item[0]] -= 1
                return PICK
            return self.helper.get_market_center()
        return dest

    def use_radiation(self, my_pos):
        bases_value = self.helper.get_bases_value()
        target = bases_value.index(max(bases_value))
        dest = self.helper.get_base_center(player_id=target)
        if self.helper.get_distance(dest, my_pos) < self.helper.radius_of_radiation_oil:
            return 9
        return self.get_dir(dest, my_pos)

    def use(self, my_pos):
        bases_value = self.helper.get_bases_value()
        if not self.helper.get_player_item_is_active() and self.helper.get_player_item_name():
            use_directly = ['TheWorld', 'ShuffleBases', 'Invincible', 'ShuffleBases']
            if self.helper.get_player_item_name() in use_directly:
                return True
            elif self.helper.get_player_item_name() == 'RadiusNotMove':
                tmp = 0
                best_idx = 0
                for idx in range(4):
                    if idx == self.helper.player_id:
                        continue
                    value = self.helper.get_base_value(idx)
                    if value > tmp:
                        tmp = value
                        best_idx = idx
                if self.helper.get_distance(self.helper.get_player_position(best_idx), my_pos) < self.helper.radius_not_move_radius:
                    return True
            elif self.helper.get_player_item_name() == 'RadiationOil' \
                and self.helper.player_id != bases_value.index(max(bases_value)) \
                and self.helper.get_timer() <= 80 * 60:
                return True
        return False

    def decide(self):
        if self.helper.get_timer() == 179 * 60 and self.FaDaCai1:
            self.FaDaCai1 = False
            return 10
        carry = self.helper.get_player_value()
        best_pos, my_pos, best_cp = self.get_best_oil_position()
        bases = self.helper.get_bases_value()
        home = self.helper.get_base_center()
        dest = best_pos
        if self.helper.get_timer() <= 3 * 60 and bases.index(max(bases)) == self.helper.player_id:
            return self.get_dir(home, my_pos)
        if self.use(my_pos) == True:
            if self.helper.get_player_item_name() == 'RadiationOil':
                return self.use_radiation(my_pos)
            else:
                return 9
        home_cp =  5e-6 * carry if self.helper.get_player_item_name() == 'IGoHome' else 7.5e-6 * carry
        t = self.attack(carry, my_pos)
        attack_cp, target_pos, target = t

        if attack_cp >= best_cp and self.helper.get_player_item_name(target) != 'Invincible':
            best_cp = attack_cp
            dest = target_pos
        
        if home_cp > best_cp:
            if not self.helper.get_player_item_is_active() and self.helper.get_player_item_name() == 'IGoHome':
                return 9
            dest = home
        dest = self.pick_item(dest, my_pos, carry)
        if dest == PICK:
            return PICK
        return self.get_dir(dest, my_pos)
"""
DIR_stop = 0
DIR_U    = 1
DIR_RU   = 2
DIR_R    = 3
DIR_RD   = 4
DIR_D    = 5
DIR_LD   = 6
DIR_L    = 7
DIR_LU   = 8
"""
