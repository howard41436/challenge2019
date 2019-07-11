import pygame as pg
from pygame.math import Vector2 as Vec
import os, math, random

from Events.Manager import *
import Model.main            as model
import Model.GameObject.item as model_item
import Model.const           as model_const
import View.const            as view_const
import View.animations       as view_Animation
import View.utils            as view_utils
import View.staticobjects    as view_staticobjects
import View.cutin            as view_cutin
import Controller.const      as ctrl_const
import Interface.const       as ifa_const


class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, ev_manager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        ev_manager.register_listener(self)

        self.ev_manager = ev_manager
        self.model = model
        self.is_initialized = False
        self.screen = None
        self.clock = None
        self.small_font = None
        self.last_update = 0
        self.theworld_background = pg.Surface(view_const.screen_size)


    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, EventEveryTick) and self.is_initialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            if cur_state == model.STATE_PLAY:
                if self.play_fadacai_cutin_video:
                    self.video_manager.play_fadacai()
                    self.play_fadacai_cutin_video = False
                theworld = False
                for ani in self.post_animations:
                    if isinstance(ani, view_Animation.Animation_theworld):
                        theworld = True
                self.render_play(theworld)
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
        elif isinstance(event, EventInitialize) or isinstance(event, EventRestart):
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
            self.animations.append(view_Animation.Animation_shuffleBases_horizontal(center=ani_pos[0]))
            self.animations.append(view_Animation.Animation_shuffleBases_horizontal(center=ani_pos[1]))
            self.animations.append(view_Animation.Animation_shuffleBases_vertical(center=ani_pos[2]))
            self.animations.append(view_Animation.Animation_shuffleBases_vertical(center=ani_pos[3]))
            self.animations.append(view_Animation.Animation_shuffleBases(self.model))
        elif isinstance(event, EventCutInStart):
            self.cutin_manager.update_state(event.player_index, event.skill_name, self.screen)
            self.players.set_theworld_player(event.player_index)
        elif isinstance(event, EventTheWorldStart):
            self.post_animations.append(view_Animation.Animation_theworld(event.position, self.ev_manager))
        elif isinstance(event, EventRadiusNotMoveStart):
            self.animations.append(view_Animation.Animation_freeze(center=event.position))
        elif isinstance(event, EventFaDaCaiStart):
            self.play_fadacai_cutin_video = True


    def render_menu(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU

        self.menu.draw(self.screen)
        self.characters.draw(self.screen)
        pg.display.flip()


    def render_endgame(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_ENDGAME:
            self.last_update = model.STATE_ENDGAME
            self.animations = []
            self.post_animations = []
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
            title = self.titlefont.render('Scoreboard', True, view_const.COLOR_BLACK)
            self.screen.blit(title, title.get_rect(center=(645, 60)))
            for ani in self.animations:
                if ani.expired: self.animations.remove(ani)
                else          : ani.draw(self.screen)

        pg.display.flip()


    def render_play(self, theworld=False):
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
            else          : ani.draw(self.screen, (not theworld))

        # draw static objects
        self.oils.draw(self.screen)
        self.items.draw(self.screen)
        self.pets.draw(self.screen)
        self.players.draw(self.screen)
        self.scoreboard.draw(self.screen)

        # draw time
        time = self.timefont.render(str(round(self.model.timer/60, 1)), True, view_const.COLOR_BLACK)
        self.screen.blit(time, (950, 35))
        
        # draw post_animation
        for ani in self.post_animations:
            if ani.expired: self.post_animations.remove(ani)
            elif isinstance(ani, view_Animation.Animation_theworld): ani.draw(self.screen, self.video_manager)
            else: ani.draw(self.screen, (not theworld))

        # the world specific
        if theworld: self.players.draw(self.screen, True)

        # update screen
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
        pg.init()
        pg.font.init()
        pg.display.set_caption(view_const.game_caption)
        self.screen = pg.display.set_mode(view_const.screen_size)

        self.clock = pg.time.Clock()
        self.small = pg.font.Font(None, 40)
        self.is_initialized = True

        # convert images
        view_staticobjects.init_staticobjects()
        view_Animation.init_animation()
        view_cutin.init_cutin()

        # animations
        self.animations = []
        self.post_animations = [] # animations such as "the world" need to be rendered lastly

        # about cutin
        self.cutin_manager = view_cutin.Cutin_manager(self.model)
        self.video_manager = view_cutin.Video_manager(self.ev_manager)
        self.play_fadacai_cutin_video = False

        # static objects
        self.players = view_staticobjects.View_players(self.model)
        self.oils = view_staticobjects.View_oils(self.model)
        self.bases = view_staticobjects.View_bases(self.model)
        self.pets = view_staticobjects.View_pets(self.model)
        self.scoreboard = view_staticobjects.View_scoreboard(self.model)
        self.items = view_staticobjects.View_items(self.model)
        self.background = view_staticobjects.View_background(self.model)
        self.menu = view_staticobjects.View_menu(self.model)
        self.characters = view_staticobjects.View_characters(self.model)

        # fonts
        self.titlefont = pg.font.Font(view_const.notosans_font, 60)
        self.timefont = pg.font.Font(view_const.notosans_font, 60)


pg.mixer.init(22050, -16, 2, 64)
class Sound(object):
    '''
    Manages the background music and skill sounds.
    '''
    # reusable sounds
    sounds = {
        'equalize': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'equalize.ogg')),
        'theworld_cutin': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'ZaWarudoCutIn.ogg')),
        'theworld_resume': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'ZaWarudoTimeResume.ogg')),
        'eat_oil_low': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'eatoil_low.ogg')),
        'eat_oil_mid': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'eatoil_mid.ogg')),
        'eat_oil_high': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'eatoil_high.ogg')),
        'buy_item': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'buy.ogg')),
        'igohome': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'igohome.ogg')),
        'othergohome': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'othergohome.ogg')),
        'money_collected': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'money_collected.ogg')),
        'star': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'star.ogg')),
        'boom': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'boom.ogg')),
        'freeze': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'freeze.ogg')),
        'electric': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'electric.ogg')),
        'magnet': pg.mixer.Sound(os.path.join(view_const.SOUND_PATH, 'magnet.ogg')),
        #'fadacai_cutin': None,
    }
    pg.mixer.music.load(os.path.join(view_const.SOUND_PATH, 'bgm_test.ogg'))


    def __init__(self, ev_manager):
        ev_manager.register_listener(self)
        self.ev_manager = ev_manager
        self.theworld_countdown = -1
        self.cutin_countdown = -1
        self.play_equalize_after_theworld = False


    def notify(self, event):
        if isinstance(event, EventEveryTick):
            if self.theworld_countdown == 70:
                self.sounds['theworld_resume'].play()
            if self.theworld_countdown > 0:
                self.theworld_countdown -= 1
            elif self.theworld_countdown == 0:
                if self.play_equalize_after_theworld:
                    self.sounds['equalize'].play()
                self.ev_manager.post(EventResumeSound())
                self.play_equalize_after_theworld = False
                self.theworld_countdown -= 1
            if self.cutin_countdown > 0:
                self.cutin_countdown -= 1
            elif self.cutin_countdown == 0:
                self.ev_manager.post(EventResumeSound())
                self.cutin_countdown -= 1
        elif isinstance(event, EventInitialize):
            pg.mixer.music.play(-1)
        elif isinstance(event, EventEatOil):
            max_price = model_const.price_max
            if                    event.oil_value < max_price/3  : level = 'low'
            elif max_price/3   <= event.oil_value < max_price/3*2: level = 'mid'
            elif max_price/3*2 <= event.oil_value                : level = 'high'
            self.sounds[f'eat_oil_{level}'].play()
        elif isinstance(event, EventEqualize):
            if self.theworld_countdown == -1: self.sounds['equalize'].play()
            else                            : self.play_equalize_after_theworld = True
        elif isinstance(event, EventTheWorldStart):
            self.theworld_countdown = model_const.the_world_duration + model_const.cutin_time
        elif isinstance(event, EventBuyItem):
            self.sounds['buy_item'].play()
        elif isinstance(event, EventCutInStart):
            self.cutin_countdown = model_const.cutin_time - 1
            self.ev_manager.post(EventPauseSound())
            if event.skill_name == 'TheWorld': self.sounds['theworld_cutin'].play()
            # elif event.skill_name == 'FaDaCai': self.sounds['fadacai_cutin'].play()
        elif isinstance(event, EventIGoHome):
            self.sounds['igohome'].play()
        elif isinstance(event, EventOtherGoHome):
            self.sounds['othergohome'].play()
        elif isinstance(event, EventStorePrice):
            self.sounds['money_collected'].play()
        elif isinstance(event, EventInvincibleStart):
            self.sounds['star'].play()
        elif isinstance(event, EventRadiationOil):
            self.sounds['boom'].play()
        elif isinstance(event, EventRadiusNotMoveStart):
            self.sounds['freeze'].play()
        elif isinstance(event, EventShuffleBases):
            self.sounds['electric'].play()
        elif isinstance(event, EventMagnetAttractStart):
            self.sounds['magnet'].play()
        elif isinstance(event, EventPauseSound):
            pg.mixer.pause()
        elif isinstance(event, EventPauseMusic):
            pg.mixer.music.pause()
        elif isinstance(event, EventResumeSound):
            pg.mixer.unpause()
        elif isinstance(event, EventResumeMusic):
            pg.mixer.music.unpause()
