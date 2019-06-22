import pygame as pg

import Model.main as model
from Events.Manager import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrl_const
import Interface.const   as IfaConst

class Control(object):
    """
    Handles control input.
    """
    def __init__(self, ev_manager, model):
        """
        ev_manager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.RegisterListener(self)
        self.model = model

        self.control_keys = {}

        self.sec_event_type = pg.USEREVENT

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            # Called for each game tick. We check our keyboard presses here.
            for event in pg.event.get():
                # handle window manager closing our window
                if event.type == pg.QUIT:
                    self.ev_manager.Post(Event_Quit())
                else:
                    cur_state = self.model.state.peek()
                    if cur_state == model.STATE_MENU:
                        self.ctrl_menu(event)
                    if cur_state == model.STATE_PLAY:
                        self.ctrl_play(event)
                    if cur_state == model.STATE_STOP:
                        self.ctrl_stop(event)
        elif isinstance(event, Event_Initialize):
            self.initialize()

    def ctrl_menu(self, event):
        """
        Handles menu events.
        """
        if event.type == pg.KEYDOWN:
            # escape pops the menu
            if event.key == pg.K_ESCAPE:
                self.ev_manager.Post(Event_StateChange(None))
            # space plays the game
            if event.key == pg.K_SPACE:
                self.ev_manager.Post(Event_StateChange(model.STATE_PLAY))

    def ctrl_stop(self, event):
        """
        Handles help events.
        """
        if event.type == pg.KEYDOWN:
            # space, enter or escape pops help
            if event.key in [pg.K_ESCAPE, pg.K_SPACE ]:
                self.ev_manager.Post(Event_StateChange(None))

    def ctrl_play(self, event):
        """
        Handles play events.
        """
        if event.type == pg.KEYDOWN:
            # escape pops the menu
            if event.key == pg.K_ESCAPE:
                self.ev_manager.Post(Event_StateChange(None))
                self.ev_manager.Post(Event_Restart())
            # space to stop the game
            elif event.key == pg.K_SPACE:    
                self.ev_manager.Post(Event_StateChange(model.STATE_STOP))

        # player controler
        for player in self.model.players:
            if player.is_AI:
                continue
            dir_keys = self.control_keys[player.index][0:4]
            now_pressing = self.get_key_pressing(dir_keys)
            dir_hash_value = self.get_dir_hash_value(now_pressing, dir_keys)
            self.ev_manager.Post(Event_Move(player.index, ctrl_const.dir_hash[dir_hash_value]))
        
    def get_key_pressing(self, keylist):
        return [key for key, value in enumerate(pg.key.get_pressed()) if value == 1 and key in keylist]

    def get_dir_hash_value(self, press_list, dir_key_list):
        hash_value = 0
        for index, key in enumerate(dir_key_list):
            if key in press_list:
                hash_value += 2 ** index
        return hash_value

    def initialize(self):
        """
        # init pygame event and set timer
        # # Document
        # pg.event.Event(event_id)
        # pg.time.set_timer(event_id, TimerDelay)
        """
        pg.time.set_timer(self.sec_event_type, 1000)

        now_manual_index = 0
        for index, AI_name in enumerate(self.model.AINames):
            if AI_name == "~":
                self.control_keys[index] = ctrl_const.manual_player_keys[now_manual_index]
                now_manual_index += 1
