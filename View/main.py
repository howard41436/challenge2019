import pygame as pg

import Model.main as model
from Events.Manager import *

import Model.const       as model_const
import View.const        as view_const
import Controller.const  as ctrl_const
import Interface.const   as ifa_const

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
    
    def render_menu(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU

            # draw backgound
            self.screen.fill(view_const.Color_Black)
            # write some word
            somewords = self.smallfont.render(
                        'You are in the Menu', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (view_const.screen_size[0] - SurfaceX)/2
            pos_y = (view_const.screen_size[1] - SurfaceY)/2
            self.screen.blit(somewords, (pos_x, pos_y))
            # update surface
            pg.display.flip()
    
    def draw_player(self):
        for player in self.model.player_list:
            pos = player.position
            radius = player.radius
            color = player.color
            gfxdraw.filled_circle(self.gameSurface, *pos,
                                  int(radius), player.color)

    def draw_oil(self):
        for oil in self.model.oil_list:
            position = oil.position
            radius = oil.radius
            gfxdraw.filled_circle(self.gameSurface, *position,
                                  int(oil.radius), Color_Black)

    def draw_base(self):
        for base in self.model.base_list:
            center = base.center
            length = base.length
            pygame.draw.rect(self.gameSurface, Color_Gray, [center-length/2, center+length/2, length, length], 2)       

    def render_play(self):
        """
        Render the game play.
        """
        if self.last_update != model.STATE_PLAY:
            self.last_update = model.STATE_PLAY
        # draw backgound
        s = pg.Surface(view_const.ScreenSize, pg.SRCALPHA)
        self.screen.fill(view_const.Color_White)

        #draw player
        self.draw_player()
        self.draw_oil()
        self.draw_base()

        pg.draw.rect(s,view_const.Color_Black,[800,0,5,800])
        pg.draw.rect(s,view_const.Color_Black,[1275,0,5,800])
        pg.draw.rect(s,view_const.Color_Black,[800,197,480,5])
        pg.draw.rect(s,view_const.Color_Black,[800,397,480,5])
        pg.draw.rect(s,view_const.Color_Black,[800,597,480,5])
        self.screen.blit(s,(0,0))
        # update surface
        pg.display.flip()
        
    def render_stop(self):
        """
        Render the stop screen.
        """
        if self.last_update != model.STATE_STOP:
            self.last_update = model.STATE_STOP

            # draw backgound
            s = pg.Surface(view_const.screen_size, pg.SRCALPHA)
            s.fill((0, 0, 0, 128)); self.screen.blit(s, (0,0))

            # write some word
            somewords = self.smallfont.render(
                        'the game is paused. space, escape to return the game.', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (view_const.screen_size[0] - SurfaceX)/2
            pos_y = (view_const.screen_size[1] - SurfaceY)/2
            self.screen.blit(somewords, (pos_x, pos_y))

            # update surface
            pg.display.flip()

    def render_end(self):
        if self.last_update != model.STATE_END:
            self.last_update = model.STATE_END
            result = []
            boardfont = pg.font.SysFont("Ubuntu", 30)

            for player in seld.model.player_list:
                result.append((player.name, player.value_sum))
            result.sort(key=takeSecond)
            self.screen.fill(view_const.Color_White)
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
        pg.init(); pg.font.init()
        pg.display.set_caption(view_const.game_caption)
        self.screen = pg.display.set_mode(view_const.screen_size)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(view_const.titleFont, view_const.titleFontSize)
        self.is_initialized = True
