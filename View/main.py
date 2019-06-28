import pygame as pg
import Model.main as model
from Events.Manager import *
import os, math
import random

import Model.GameObject.item as model_item
import Model.const           as model_const
import View.const            as view_const
import View.animations       as view_Animation
import View.utils            as view_utils
import View.staticobjects    as view_staticobjects
import View.cutin            as view_cutin
import Controller.const      as ctrl_const
import Interface.const       as ifa_const
from pygame.math import Vector2 as Vec


class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, ev_manager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model

        self.is_initialized = False
        self.screen = None
        self.clock = None
        self.small_font = None

        self.last_update = 0
        pg.init(); pg.font.init()
        pg.display.set_caption(view_const.game_caption)
        self.screen = pg.display.set_mode(view_const.screen_size)

        view_staticobjects.init_staticobjects()
        view_Animation.init_animation()
        view_cutin.init_cutin()

        # animations
        self.animations = []
        self.post_animations = [] # animations such as the world need to be rendered lastly

        # about cutin
        self.cutin_manager = view_cutin.Cutin_manager(model)

        # static objects
        self.players = view_staticobjects.View_players(model)
        self.oils = view_staticobjects.View_oils(model)
        self.bases = view_staticobjects.View_bases(model)
        self.pets = view_staticobjects.View_pets(model)
        self.scoreboard = view_staticobjects.View_scoreboard(model)
        self.items = view_staticobjects.View_items(model)
        self.background = view_staticobjects.View_background(model)
        self.menu = view_staticobjects.View_menu(model)
        self.characters = view_staticobjects.View_characters(model)



    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, EventEveryTick) \
           and self.is_initialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            if cur_state == model.STATE_PLAY:
                self.render_play()
            if cur_state == model.STATE_CUTIN:
                self.cutin_manager.draw(self.screen)
            if cur_state == model.STATE_STOP:
                self.render_stop()
            if cur_state == model.STATE_ENDGAME:
                self.render_endgame()
            self.display_fps()
            self.clock.tick(view_const.frame_per_sec)
        elif isinstance(event, EventQuit):
            self.is_initialized = False
            pg.quit()
        elif isinstance(event, EventInitialize) or\
             isinstance(event, EventRestart):
            self.initialize()
        elif isinstance(event, EventEqualize):
            self.animations.append(view_Animation.Animation_equalize(center=event.position))
        elif isinstance(event, EventIGoHome):
            self.animations.append(view_Animation.Animation_gohome(center=event.position))
        elif isinstance(event, EventMagnetAttractStart):
            self.animations.append(view_Animation.Animation_magnetattract(event.player_index, self.model))
        elif isinstance(event, EventOtherGoHome):
            for player in self.model.player_list:
                if player.index != event.player_index:
                    self.animations.append(view_Animation.Animation_othergohome(center=player.position))
        elif isinstance(event, EventRadiationOil):
            self.animations.append(view_Animation.Animation_radiationOil(center=event.position))
        elif isinstance(event, EventShuffleBases):
            ani_pos = [(400, 20), (400, 780), (20, 400), (780, 400)]
            for pos in ani_pos:
                if pos[1] == 400: self.animations.append(view_Animation.Animation_shuffleBases_vertical(center=pos))
                else: self.animations.append(view_Animation.Animation_shuffleBases_horizontal(center=pos))
            self.animations.append(view_Animation.Animation_shuffleBases(self.model))
            self.bases.draw(self.screen)
            pg.display.flip()
        elif isinstance(event, EventCutInStart):
            self.cutin_manager.update_state(event.player_index, event.skill_name, self.screen)
        elif isinstance(event, EventTheWorldStart):
            self.post_animations.append(view_Animation.Animation_theworld(event.position))
        elif isinstance(event, EventRadiusNotMoveStart):
            self.animations.append(view_Animation.Animation_freeze(center=event.position))

    
    def render_menu(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU
            self.title_counter = 0

        # draw backround
        self.menu.draw(self.screen)
        self.characters.draw(self.screen)

        # word animation
        """titlefont = pg.font.Font(view_const.board_name_font, 90)
        title_loop_counter = self.title_counter % 80
        littlefont = pg.font.Font(view_const.board_name_font, 40)
        if not title_loop_counter:
            self.darken_time = [random.randint(25, 35), random.randint(55,65)]

        if self.title_counter <= 10:
            gray = (155 + int(self.title_counter / 10 * 100),) * 3
        elif self.darken_time[0] <= title_loop_counter <= self.darken_time[0] + 5:
            gray = ((155 + (title_loop_counter - self.darken_time[0]) / 5 * 100),) * 3
        elif self.darken_time[1] <= title_loop_counter <= self.darken_time[1] + 5:
            gray = ((155 + (title_loop_counter - self.darken_time[1]) / 5 * 100),) * 3
        else:
            gray = (255,) * 3

        self.title_counter += 1"""
        
        # update surface
        pg.display.flip()


    def render_endgame(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_ENDGAME:
            self.last_update = model.STATE_ENDGAME
            self.screen.fill(view_const.COLOR_WHITE)
            result = []
            for base in self.model.base_list:
                result.append([self.model.player_list[base.owner_index].name, 
                               base.value_sum,
                               self.model.player_list[base.owner_index].color])

            result.sort(key=(lambda item: item[1]), reverse=True)
            pos_x = 256
            prize = 1
            first = result[0][1]
            for player in result:
                self.animations.append(view_Animation.Animation_endboard(player[2], player[1]/first*500, (pos_x, 680), player[1], player[0]))
                pos_x += 256
                prize += 1


        if self.animations:
            self.screen.fill(view_const.COLOR_WHITE)
            titlefont = pg.font.Font(view_const.board_name_font, 60)
            title = titlefont.render('Scoreboard', True, view_const.COLOR_BLACK)
            self.screen.blit(title, title.get_rect(center=(645, 60)))
            for ani in self.animations:
                if ani.expired: self.animations.remove(ani)
                else          : ani.draw(self.screen)

        pg.display.flip()
 

    def render_play(self):
        """
        Render the game play.
        """
        if self.last_update != model.STATE_PLAY:
            self.last_update = model.STATE_PLAY
        
        # draw background
        self.background.draw(self.screen)
        self.bases.draw(self.screen)

        # draw animation
        for ani in self.animations:
            if ani.expired: self.animations.remove(ani)
            else          : ani.draw(self.screen)

        # draw static objects
        self.oils.draw(self.screen)
        self.items.draw(self.screen)
        self.pets.draw(self.screen)
        self.players.draw(self.screen)
        self.scoreboard.draw(self.screen)

        # draw time
        timefont = pg.font.Font(view_const.board_num_font, 60)
        time = timefont.render(str(round(self.model.timer/60, 1)), True, view_const.COLOR_BLACK)
        
        # draw post_animation
        for ani in self.post_animations:
            if ani.expired: self.post_animations.remove(ani)
            else          : ani.draw(self.screen)

        # update screen
        self.screen.blit(time, (950, 35))
        pg.display.flip()
        

    def render_stop(self):
        """
        Render the stop screen.
        """
        if self.last_update != model.STATE_STOP:
            self.last_update = model.STATE_STOP

            # draw backgound
            s = pg.Surface(view_const.screen_size, pg.SRCALPHA)
            s.fill((255, 255, 255, 128)); self.screen.blit(s, (0,0))
            
            # draw pause botton
            pg.draw.circle(s, view_const.COLOR_BLACK, (640,400), 300)
            pg.draw.rect(s, view_const.COLOR_WHITE, [690, 250, 60, 300])
            pg.draw.rect(s, view_const.COLOR_WHITE, [510, 250, 60, 300])
            self.screen.blit(s,(0,0))

            # update surface
            pg.display.flip()




    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(
            view_const.game_caption, self.clock.get_fps()
        )
        pg.display.set_caption(caption)
        
        
    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 40)
        self.is_initialized = True
