import time, random

from Events.Manager import *
from Model.StateMachine import *
from Model.GameObject.Player import *

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
        ev_manager.register_listener(self)

        self.running = False
        self.state = StateMachine()
        self.AI_names = AI_names
        self.players = []
        self.turn_to = 0

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

    def initialize(self):
        self.set_player()

    def set_player(self):
        # set AI Names List
        # "_" ==> default AI, "~" ==> manual player
        self.players, manual_player_num = [], 0
        for index in range(model_const.player_num):
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
        for index in range(model_const.player_num):
            if self.AI_names[index] == "~":
                Tmp_P = Player("manual", index, False)
            elif self.AI_names[index] == "_":
                Tmp_P = Player("default", index, True)
            else:
                Tmp_P = Player(self.AI_names[index], index, True)
            self.players.append(Tmp_P)

    def set_player_direction(self, player_index, direction):
        if self.players[player_index] is not None:
            player = self.players[player_index]
            player.direction = direction


    def update_objects(self):
        # Update players
        for player in self.players:
            player.update_pos()


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
