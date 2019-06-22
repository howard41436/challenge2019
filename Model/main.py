import time, random

from Events.Manager import *
from Model.StateMachine import *
from Model.GameObject.Player import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AINames):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
            running (bool): True while the engine is online. Changed via Event_Quit().
            state (StateMachine()): control state change, stack data structure.
            AIList (list.str): all AI name list.
            players (list.player()): all player object.
            TurnTo (int): current player
        """
        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AINames = AINames
        self.players = []
        self.TurnTo = 0

<<<<<<< HEAD
        self.init_oil()
        self.setPlayer()
=======
        self.oil_list = []
        self.base_list = []
>>>>>>> 23fced82afb4ad6115e575dd7edc8ca720f1b4d8

        random.seed(time.time())
        

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                self.updateObjects()
        elif isinstance(event, Event_StateChange):
            # if event.state is None >> pop state.
            if event.state == None:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            elif event.state == STATE_RESTART:
                self.state.clear()
                self.state.push(STATE_MENU)
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, Event_Move):
            self.setPlayerDirection(event.PlayerIndex, event.Direction)
        elif isinstance(event, Event_Quit):
            self.running = False
        elif isinstance(event, Event_Initialize) or \
             isinstance(event, Event_Restart):
            self.Initialize()

    def setPlayer(self):
        # set AI Names List
        # "_" ==> default AI, "~" ==> manual player
        self.players, ManualPlayerNum = [], 0
        for index in range(modelConst.PlayerNum):
            if len(self.AINames) > index:
                PlayerName = self.AINames[index]
                if PlayerName == "~":
                    if ManualPlayerNum < modelConst.MaxManualPlayerNum:
                        ManualPlayerNum += 1
                    else:
                        self.AINames[index] = "_"
            else:
                if ManualPlayerNum < modelConst.MaxManualPlayerNum:
                    ManualPlayerNum += 1
                    self.AINames.append("~")
                else:
                    self.AINames.append("_")

        # init Player object
        for index in range(modelConst.PlayerNum):
            if self.AINames[index] == "~":
                Tmp_P = player("manual", index, False)
            elif self.AINames[index] == "_":
                Tmp_P = player("default", index, True)
            else:
                Tmp_P = player(self.AINames[index], index, True)
            self.players.append(Tmp_P)

    def setPlayerDirection(self, playerIndex, direction):
        if self.players[playerIndex] != None:
            player = self.players[playerIndex]
            player.direction = direction;


    def updateObjects(self):
        # Update players
        for player in self.players:
            player.updatePos()

    def init_oil(self):
        self.oil_list = []
        for _ in range(modelConst.init_oil_number):
            create_oil()

    def create_oil(self):
        pos = random.randint(0, viewConst.ScreenSize), random.randint(0, viewConst.ScreenSize)
        price = random.randint(modelConst.price_min, modelConst.price_max)
        weight = random.randint(modelConst.weight_min, modelConst.weight_max)
        new_oil = Oil(pos, price, weight)
        self.oil_list.append(new_oil)

    def try_create_oil(self):
        if random.random() < modelConst.oil_probability:
            create_oil()

    def set_base(self) :
        # todo
        for index in range(modelConst.player_number) :
            self.base_list.append(Base(index, modelConst.base_center[index]))
    
    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(Event_Initialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = Event_EveryTick()
            self.evManager.Post(newTick)
