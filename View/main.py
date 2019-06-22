import pygame as pg

import Model.main as model
from Events.Manager import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.is_initialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

        self.last_update = 0
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick) \
           and self.is_initialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            if cur_state == model.STATE_PLAY:
                self.render_play()
            if cur_state == model.STATE_STOP:
                self.render_stop()
#			if cur_state == model.STATE_END:
#				self.render_end()

            self.display_fps()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(viewConst.FramePerSec)
        elif isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.is_initialized = False
            pg.quit()
        elif isinstance(event, Event_Initialize) or\
             isinstance(event, Event_Restart):
            self.initialize()
    
    def render_menu(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU

            # draw backgound
            self.screen.fill(viewConst.Color_Black)
            # write some word
            somewords = self.smallfont.render(
                        'You are in the Menu', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (viewConst.ScreenSize[0] - SurfaceX)/2
            pos_y = (viewConst.ScreenSize[1] - SurfaceY)/2
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


    def render_play(self):
        """
        Render the game play.
        """
        if self.last_update != model.STATE_PLAY:
            self.last_update = model.STATE_PLAY
        # draw backgound
        s = pg.Surface(viewConst.ScreenSize, pg.SRCALPHA)
        self.screen.fill(viewConst.Color_White)

        #draw player
        self.draw_player()



        pg.draw.rect(s,viewConst.Color_Black,[800,0,5,800])
        pg.draw.rect(s,viewConst.Color_Black,[1275,0,5,800])
        pg.draw.rect(s,viewConst.Color_Black,[800,197,480,5])
        pg.draw.rect(s,viewConst.Color_Black,[800,397,480,5])
        pg.draw.rect(s,viewConst.Color_Black,[800,597,480,5])
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
            s = pg.Surface(viewConst.ScreenSize, pg.SRCALPHA)
            s.fill((0, 0, 0, 128)); self.screen.blit(s, (0,0))

            # write some word
            somewords = self.smallfont.render(
                        'the game is paused. space, escape to return the game.', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (viewConst.ScreenSize[0] - SurfaceX)/2
            pos_y = (viewConst.ScreenSize[1] - SurfaceY)/2
            self.screen.blit(somewords, (pos_x, pos_y))

            # update surface
            pg.display.flip()

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(
            viewConst.GameCaption, self.clock.get_fps()
        )
        pg.display.set_caption(caption)
        
    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        pg.init(); pg.font.init()
        pg.display.set_caption(viewConst.GameCaption)
        self.screen = pg.display.set_mode(viewConst.ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(viewConst.titleFont, viewConst.titleFontSize)
        self.is_initialized = True
"""
	def render_end(self):
		if self.last_update != model.STATE_END:
			self.last_update = model.STATE_END

			#draw background
			s - pg.Surface(viewConst.ScreenSize, pg.SRCALPHA)
			s.fill((0, 0, 0, 128)); self.screen.blit(s, (0,0))

			#end 
			somewords = self.smallfont.renter(
					'The game is end',True, (0, 255, 0))
			(SurfaceX, SurfaceY) = spmewords.get_size();
			pos_x = (viewConst.ScreenSize[0] - SurfaceX)/2
			pos_y = (viewConst.ScreenSize[1] - SurfaceY)/2
			self.screem.blit(somewords. (pos_x, pos_y))

			#score table
			

			#the winner
			

			#update surface
			pg.display.flip();
"""

