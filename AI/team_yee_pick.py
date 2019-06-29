from AI.base import *
import View.const as view_const
import Model.const as model_const
import numpy as np
from scipy.stats import norm
from pygame.math import Vector2 as Vec
import random
from datetime import datetime

market_pos = Vec(view_const.game_size)/2
init_speed = [0] * 4
got_init_speed = False

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 0, 0, 0, 0]
        self.direct =  list(map(Vec, [
        [0, 0],             #steady
        [0, -1],             #up
        [0.707, -0.707],     #up right
        [1, 0],             #right
        [0.707, 0.707],    #right down
        [0, 1],            #down
        [-0.707, 0.707],   #left down
        [-1, 0],            #left
        [-0.707, -0.707],    #left up
        ]))
        self.radius = self.helper.player_radius
        self.half_game_size = self.helper.game_size[0] // 2
        self.id = self.helper.get_self_id()
    
    def get_init_speed(self):
        '''get the model_const.speed_multiplier ** self.equipments[model_const.speed_up_idx] for every players'''
        init_speed[self.id] = model_const.speed_multiplier ** self.equipments[model_const.speed_up_idx]
        for i, speed in enumerate(self.helper.get_players_speed()):
            init_speed[i] = max(init_speed[i], speed/model_const.player_normal_speed)
        if all(init_speed):
            got_init_speed = True

    def calc_expected_value_integral(self, mu, sd, high, low):
        return sd / np.sqrt(2 * np.pi) * (np.exp(-0.5 * low ** 2) - np.exp(-0.5 * high ** 2)) + mu * (norm.cdf(high, mu, sd) - norm.cdf(low, mu, sd))
    
    def get_oil_expected_value(self, pos, level):
        dist_from_center = (pos - market_pos).length() - model_const.market_radius
        mu = model_const.curve_a / (dist_from_center + model_const.curve_b)
        sd = model_const.price_scale
        level_range = [model_const.price_min, 400, 600, 800, model_const.price_max]

        E = 0.0
        if level == 1:
            E = model_const.price_min * norm.cdf(model_const.price_min, mu, sd)
        elif level == 4:
            E = model_const.price_max * (1 - norm.cdf(model_const.price_max, mu, sd))
        E = (E + self.calc_expected_value_integral(mu, sd, level_range[level], level_range[level - 1])) / (norm.cdf(level_range[level], mu, sd) - norm.cdf(level_range[level - 1], mu, sd))
        return E


    def get_best_oil_cp(self):
        oils = zip(list(map(Vec, self.helper.get_oils())), self.helper.get_oils_level())
        best_pos = None
        best_cp = -1
        for pos, oil_level in oils:
            cp = self.get_oil_expected_value(pos, oil_level) * (1 if (pos - self.home).length() <= self.half_game_size * 1.2 else (1 - 0.5 * (pos - self.home).length() / (self.helper.game_size[0] * 1.414))**2) \
                 / ((self.pos - pos).length_squared()/self.speed + 1e-5)
            if cp > best_cp:
                best_cp = cp
                best_pos = pos
        return best_pos, best_cp
    
    def get_speed_by_value(self, val, player_id=None):
        if player_id is None:
            player_id = self.id
        return init_speed[player_id] * max(model_const.player_speed_min, model_const.player_normal_speed - model_const.player_speed_decreasing_rate * val)

    def attack(self, players):
        #return None, -2
        best_pos, best_cp = Vec(0, 0), -1
        for i, item in enumerate(players):
            pos, v, val = item
            if i == self.id:
                continue
            if (val - self.carry) / 2 >= 1000: #rob it if it can gain enough money
                # it can catch up with the player
                dist = (self.pos - pos).length()
                t = dist / (self.speed - (pos - self.pos).normalize().dot(v) + 1e-5)
                player_home_dist = (Vec(self.helper.get_base_center(i)) - pos).length() - self.helper.base_length / 2
                if player_home_dist / (v.length()+1e-3) > t:
                    cp = (val - self.carry) * (player_home_dist / (dist+1e-5)) / dist / t * (1 if (pos - self.home).length() <= self.half_game_size * 1.2 else (1 - 0.5 * (pos - self.home).length() / (self.helper.game_size[0] * 1.414))**1.5)
                    if cp > best_cp:
                        best_pos, best_cp = pos, cp
        return best_pos, best_cp
                
    def get_dir(self, vec):
        maximum = 0
        record = 0
        for i, v in enumerate(self.direct):
            if maximum < vec.dot(v):
                maximum = vec.dot(v)
                record = i
        #print(record)
        return record
    
    def be_chased(self, players):
        thief_pos, loss = Vec(0,0), 0
        for i, item in enumerate(players):
            pos, v, val = item
            if i == self.id:
                continue
            if v.length() == 0:
                continue
            if (self.carry - val) / 2 > 1000 and (pos - self.pos).length() <= 15 * self.radius and (self.pos-pos).normalize().dot(v.normalize())>0.1:
                if (self.carry - val) / 2 > loss:
                    thief_pos, loss = pos, (self.carry - val) / 2
        return thief_pos, loss

    def eat_btw(self, dest, go_home):
        nearest_oil = self.helper.get_nearest_oil()
        ongoing_vec = dest - self.pos
        if nearest_oil is not None:
            nearest_oil = Vec(nearest_oil)
            nearest_vec = nearest_oil - self.pos
            if nearest_vec.length()/self.speed < 7 and nearest_vec.length()>0: #7 ticks
                if not go_home or ongoing_vec.normalize().dot(nearest_vec.normalize()) > 1e-3:
                    return self.get_dir(nearest_vec)
                else:
                    return self.get_dir(ongoing_vec)
        return self.get_dir(ongoing_vec)
    
    def get_other_threat(self, players):
        other_threat = 0
        for i, item in enumerate(players):
            pos, v, val = item
            if i == self.id:
                continue
            if self.carry > val:
                other_threat += (self.carry - val) / 2 / ((pos - self.pos).length_squared() / (abs(self.speed - v.length()) + 1e-5))
        return other_threat

    def get_home_cp(self, loss, players):
        to_home_dist = (self.pos - self.home).length()
        if self.carry <= 1000 or to_home_dist <= 1e-3:
            return 0
        carry_transform = (1 / 160 * (self.carry - 2500))** 3 + 1000
        
        other_threat = self.get_other_threat(players)
        if to_home_dist > self.half_game_size * 1.4:
            dist_cp = 5e-5 * (to_home_dist-self.half_game_size * 1.4) ** 0.8
        else:
            dist_cp = 1 / (to_home_dist * (to_home_dist / self.speed + 1))
        return other_threat + loss + carry_transform * dist_cp
    
    def get_pick_cp(self, players):
        name, price, _ = self.helper.get_market()
        if name is not None and name in ('IGoHome', 'RadiusNotMove') and self.carry >= price \
             and not self.item and not self.item_active:
            return 2000 / ((self.pos-market_pos).length_squared()/self.speed) - self.get_other_threat(players)
        else:
            return -1

    def pick_item(self):
        name, price, _ = self.helper.get_market()
        if name is not None and name in ('IGoHome', 'RadiusNotMove') and self.carry >= price:
            if (self.pos - market_pos).length() <= self.radius:
                return True
        return False


    def decide(self):
        if not got_init_speed:
            self.get_init_speed()

        self.carry = self.helper.get_player_value()
        self.home = Vec(self.helper.get_base_center())
        self.pos = Vec(self.helper.get_player_position())
        self.speed = self.helper.get_player_speed()
        self.item, self.item_active = self.helper.get_player_item_name(), self.helper.get_player_item_is_active()
        
        if not self.item and not self.item_active and self.pick_item():
            return 9
        
        players = list(zip(list(map(Vec, self.helper.get_players_position())),
            [i*j for i,j in zip(self.helper.get_players_speed(), list(map(Vec, self.helper.get_players_direction())))],
            self.helper.get_players_value()))

        oil_pos, oil_cp = self.get_best_oil_cp()
        attack_pos, attack_cp = self.attack(players)
        thief_pos, loss = self.be_chased(players)
        home_cp = self.get_home_cp(loss, players)
        pick_cp = self.get_pick_cp(players)

        if not self.item_active:
            if self.item == 'IGoHome':
                for i, item in enumerate(players):
                    pos, v, val = item
                    if i == self.id:
                        continue
                    if self.carry > 6000 or \
                        (self.pos - pos).length() <= 2*self.radius + self.speed + self.get_speed_by_value(val,i) and (self.carry-val)/2>500:
                        return 9
            elif self.item == 'RadiusNotMove':
                # sort by value and exclude myself
                valuable = np.argsort([player[2] for player in players])[::-1]
                valuable_pos, valuable_v, valuable_val = players[valuable[0] if valuable[0] != self.id else valuable[1]]
                
                if ((thief_pos - self.pos).length() < model_const.radius_not_move_radius and loss > 500) \
                    or ((valuable_pos - self.pos).length() < model_const.radius_not_move_radius and valuable_v.length()!=0):
                    return 9
        
        #print(best_cp, attack_cp)
        dest, best_cp = oil_pos, oil_cp
        action = 'oil'
        
        if pick_cp > best_cp:
            dest, best_cp = market_pos, pick_cp
            action = 'pick'

        if attack_cp > best_cp:
            #print('attack '+str(datetime.now().time())[:8],end=' ')
            dest, best_cp = attack_pos, attack_cp
            action = 'attack'

        go_home = go_straight = False
        if self.item != 'IGoHome' and (home_cp > best_cp or self.carry >= 5000):
            dest, best_cp = self.home, home_cp
            go_home = True
            go_straight = (loss >= 1000)
            # if go_home_now:
            #     print('go_home_now ' + str(datetime.now().time())[:8], end=' ')
            # else:
            #     print('go home', end=' ')
            action = 'home'
        
        # available_choice = np.array([[oil_pos, best_cp], [self.home,home_cp], [attack_pos, attack_cp]])
        # print(available_choice[:,1].ravel(),end=' ')
        # available_choice = available_choice[np.argsort(available_choice[:,1])[::-1]]

        if action == 'attack' or go_straight:
            return self.get_dir(dest - self.pos)
        else:
            return self.eat_btw(dest, go_home)
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
