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

        self.animations = []

        self.players = view_staticobjects.View_players(model)
        self.oils = view_staticobjects.View_oils(model)
        self.bases = view_staticobjects.View_bases(model)
        self.pets = view_staticobjects.View_pets(model)
        self.scoreboard = view_staticobjects.View_scoreboard(model)
        self.items = view_staticobjects.View_items(model)

        self.priced_market = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'market.png')), 0.3)
        self.background_image = view_utils.scaled_surface(pg.image.load(os.path.join('View', 'image', 'background.png')).convert(), 1)

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
            if cur_state == model.STATE_STOP:
                self.render_stop()
            if cur_state == model.STATE_ENDGAME:
                self.render_endgame()

            self.display_fps()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(view_const.frame_per_sec)
        elif isinstance(event, EventQuit):
            # shut down the pygame graphics
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
            base_pos = self.model.base_list
            for i in range(0, model_const.player_number):
                for j in range(i+1, model_const.player_number):
                    if base_pos[i].center[0] == base_pos[j].center[0]:
                        self.animations.append(view_Animation.Animation_shuffleBases_vertical(center=\
                            (base_pos[i].center+base_pos[j].center)/2))
                    if base_pos[i].center[1] == base_pos[j].center[1]:
                        self.animations.append(view_Animation.Animation_shuffleBases_horizontal(center=\
                            (base_pos[i].center+base_pos[j].center)/2))

            






    
    def render_menu(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU
            self.title_counter = 0;

        # draw backround
        self.screen.fill(view_const.COLOR_BLACK)

        # word animation
        titlefont = pg.font.Font(view_const.board_name_font, 90)
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
       
        words_1 = titlefont.render("Fa", True, gray)
        words_2 = titlefont.render("Da", True, gray)
        words_3 = titlefont.render("Cai!", True, gray)
        words_4 = littlefont.render("presented by 2019 NTU CSIE CAMP", True, gray)

        self.screen.blit(words_1, (595,150))
        self.screen.blit(words_2, (595,300))
        self.screen.blit(words_3, (570,450))
        self.screen.blit(words_4, (320,600))

        self.title_counter += 1
        
        # update surface
        pg.display.flip()
    
    def render_endgame(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU

            # draw background
            self.screen.fill(view_const.COLOR_WHITE)
            # write some word
            result = []
            
            titlefont = pg.font.Font(view_const.board_name_font, 70)
            title = titlefont.render("Score Board", True, view_const.COLOR_BLACK)
            self.screen.blit(title, (400, 15))
            numfont = pg.font.Font(view_const.board_name_font, 30)
            for base in self.model.base_list:
                result.append([self.model.player_list[base.owner_index].name, base.value_sum])
            def takeSecond(item): return item[1]
            result.sort(key=takeSecond, reverse=True)
            pos_x = 0
            prize = 1
            for player in result:
                line = numfont.render(str(prize)+". "+(player[0] + ":" + str(int(player[1]))), True, view_const.COLOR_BLACK)
                self.screen.blit(line, (400, 200 + pos_x))
                pg.display.flip()
                pos_x += 100
                prize += 1
            # update surface
            pg.display.flip()
    

    def render_play(self):
        """
        Render the game play.
        """
        if self.last_update != model.STATE_PLAY:
            self.last_update = model.STATE_PLAY
        # draw background
        self.screen.fill(view_const.COLOR_WHITE)
        self.screen.blit(self.background_image, [0, 0])
        self.screen.blit(self.priced_market, [322, 328])

        # draw animation
        for ani in self.animations:
            if ani.expired: self.animations.remove(ani)
            else          : ani.draw(self.screen)

        # draw static objects
        self.oils.draw(self.screen)
        self.bases.draw(self.screen)
        self.items.draw(self.screen)
        self.pets.draw(self.screen)
        self.players.draw(self.screen)
        self.scoreboard.draw(self.screen)


        timefont = pg.font.Font(view_const.board_name_font, 60)


        time = timefont.render(str(round(self.model.timer/60, 1)), True, view_const.COLOR_BLACK)
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
            """
            #write some word
            somewords = self.smallfont.render(
                        'the game is paused. space, escape to return the game.', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (view_const.screen_size[0] - SurfaceX)/2
            pos_y = (view_const.screen_size[1] - SurfaceY)/2
            self.screen.blit(somewords, (pos_x, pos_y))
            """

            # update surface
            pg.display.flip()

    def render_end(self):
        if self.last_update != model.STATE_END:
            self.last_update = model.STATE_END
            result = []
            numfont = pg.font.Font(view_const.board_name_font, 30)

            for player in self.model.player_list:
                result.append((player.name, player.value_sum))
            result.sort(key=takeSecond)
            self.screen.fill(view_const.COLOR_WHITE)
            pos_x = 0
            for player in result:
                line = boardfont.render((player[0] + ":" + str(player[1])), True, (0, 128, 0))
                self.screen.blit(line, (50, 50 + pos_x))
                pg.display.flip()
                pos_x += 50


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
