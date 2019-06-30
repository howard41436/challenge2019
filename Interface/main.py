import imp, traceback

import Model.main as model
from Events.Manager import *

from Interface.helper import Helper

import Model.const       as model_const
import View.const        as view_const
import Controller.const  as ctrl_const
import Interface.const   as ifa_const

class Interface(object):
    def __init__(self, ev_manager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model

        self.player_AI = {}

        self.is_init_AI = False
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, EventEveryTick):
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_PLAY:
                self.API_play()
        elif isinstance(event, EventQuit):
            pass
        elif isinstance(event, EventInitialize):
            self.initialize()
    
    def API_play(self):
        for player in self.model.player_list:
            if player.is_AI:
                AI_dir = self.player_AI[player.index].decide()
                if AI_dir in range(9):
                    self.ev_manager.post(EventMove(player.index, AI_dir))
                elif AI_dir == 9:
                    self.ev_manager.post(EventMove(player.index, 0))
                    self.ev_manager.post(EventTriggerItem(player.index))
                else:
                    self.ev_manager.post(EventMove(player.index, 0))
        
    def initialize(self):
        if self.is_init_AI: return

        self.is_init_AI = True
        for index, player in enumerate(self.model.player_list):
            if player.name == "manual":
                continue
            # load TeamAI .py file
            try:
                loadtmp = imp.load_source('', f"./AI/team_{player.name}.py")
            except:
                self.load_msg(str(index), player.name, "AI can't load")
                print(player.name)
                player.name, player.is_AI, player.ai = "Error", False, None
                continue
            self.load_msg(str(index), player.name, "Loading")
            # init TeamAI class
            try:
                self.player_AI[player.index] = loadtmp.TeamAI(Helper(self.model, index))
            except:
                self.load_msg(str(index), player.name, "AI init crashed")
                traceback.print_exc()
                player.name, player.is_AI, player.ai = "Error", False, None
                continue
            self.load_msg(str(index), player.name, "Successful to Load")
            #if self.player_AI[player.index].equipments and len(self.player_AI[player.index].equipments) == model_const.equipment_num:
            try: 
                player.equip_equipments(self.player_AI[player.index].equipments)
            except:
                pass
            try:
                player.color = self.player_AI[player.index].color
            except:
                pass

    def load_msg(self, index, name ,msg):
        print(f"[{str(index)}] team_{name}.py: {msg}")
    
