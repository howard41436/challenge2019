import time, random

#from Events.Manager import *
#from Model.StateMachine import *
from GameObject.player import *
from GameObject.oil import *
from GameObject.base import *

import Model.const       as model_const
import View.const        as view_const
import Controller.const  as ctrl_const
import Interface.const   as ifa_const

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, ev_manager, AI_names):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
            running (bool): True while the engine is online. Changed via Event_Quit().
            state (StateMachine()): control state change, stack data structure.
            AIList (list.str): all AI name list.
            players (list.player()): all player object.
            TurnTo (int): current player
        """
        self.ev_manager = ev_manager
        #ev_manager.register_listener(self)

        self.running = False
        #self.state = StateMachine()
        self.AI_names = AI_names
        self.players = []
        self.oil_list = []
        self.base_list = []
        self.turn_to = 0

        self.init_oil()
        self.init_player()
        self.init_base()

        random.seed(time.time())
        

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, EventEveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                self.update_objects()
        elif isinstance(event, EventStateChange):
            # if event.state is None >> pop state.
            if event.state is None:
                # false if no more states are left
                if not self.state.pop():
                    self.ev_manager.post(EventQuit())
            elif event.state == STATE_RESTART:
                self.state.clear()
                self.state.push(STATE_MENU)
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, EventMove):
            self.set_player_direction(event.player_index, event.direction)
        elif isinstance(event, EventQuit):
            self.running = False
        elif isinstance(event, EventInitialize) or \
             isinstance(event, EventRestart):
            self.initialize()

    def init_player(self):
        # set AI Names List
        # "_" ==> default AI, "~" ==> manual player
        self.players, manual_player_num = [], 0
        for index in range(model_const.player_number):
            if len(self.AI_names) > index:
                PlayerName = self.AI_names[index]
                if PlayerName == "~":
                    if manual_player_num < model_const.max_manual_player_num:
                        manual_player_num += 1
                    else:
                        self.AI_names[index] = "_"
            else:
                if manual_player_num < model_const.max_manual_player_num:
                    manual_player_num += 1
                    self.AI_names.append("~")
                else:
                    self.AI_names.append("_")

        # init Player object
        for index in range(model_const.player_number):
            if self.AI_names[index] == "~":
                Tmp_P = player("manual", index)
            elif self.AI_names[index] == "_":
                Tmp_P = player("default", index)
            else:
                Tmp_P = Player(self.AI_names[index], index)
            self.players.append(Tmp_P)

    def set_player_direction(self, player_index, direction):
        if self.players[player_index] is not None:
            player = self.players[player_index]
            player.direction = direction


    def update_objects(self):
        # Update players
        for player in self.players:
            player.update(player.direction)
        for oil in self.oils :
            oil.update()

    def create_oil(self):
        #pos = random.randint(0, view_const.ScreenSize), random.randint(0, view_const.ScreenSize)
        pos = None
        price = random.randint(model_const.price_min, model_const.price_max)
        weight = random.randint(model_const.weight_min, model_const.weight_max)
        new_oil = Oil(pos, price, weight)
        self.oil_list.append(new_oil)

    def init_oil(self):
        for _ in range(model_const.init_oil_number):
            self.create_oil()

    def try_create_oil(self):
        if random.random() < model_const.oil_probability:
            create_oil()

    def init_base(self) :
        # todo
        for index in range(model_const.player_number) :
            self.base_list.append(Base(index, model_const.base_center[index]))
    
    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.ev_manager.post(EventInitialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = EventEveryTick()
            self.ev_manager.post(newTick)

def main():
    G = GameEngine()

if __name__ == '__main__':
    main()
