'''
time span: 90 ticks

phase 1 (30 ticks): coming in
phase 2 (30 ticks): animation
phase 2 (30 ticks): faded
'''

import pygame as pg

import os.path
import View.const as view_const
import View.utils as view_utils
from View.utils import scaled_surface
from Events.Manager import EventPauseSound, EventPauseMusic, EventResumeMusic, EventResumeSound

import moviepy.editor
from View.customized_video_preview import preview as video_preview
moviepy.video.io.VideoFileClip.VideoFileClip.preview = video_preview
from View.customized_audio_preview import preview as audio_preview
moviepy.audio.io.AudioFileClip.AudioFileClip.preview = audio_preview


def load_and_scale(filename, scalar):
    return scaled_surface(pg.image.load(os.path.join(view_const.IMAGE_PATH, filename)), scalar)


class Video_manager():
    videos = {
        'theworld': moviepy.editor.VideoFileClip(os.path.join(view_const.VIDEO_PATH, 'zawarudo_cutin_video.mp4'), target_resolution=view_const.screen_size[::-1]),
        'fadacai': moviepy.editor.VideoFileClip(os.path.join(view_const.VIDEO_PATH, 'fadacai_cutin_video.wmv'), target_resolution=view_const.screen_size[::-1])
    }

    def __init__(self, ev_manager):
        self.ev_manager = ev_manager

    def play_theworld(self):
        self.ev_manager.post(EventPauseMusic())
        self.ev_manager.post(EventPauseSound())
        self.videos['theworld'].preview()
        self.ev_manager.post(EventResumeMusic())

    def play_fadacai(self):
        self.ev_manager.post(EventPauseMusic())
        self.ev_manager.post(EventPauseSound())
        self.videos['fadacai'].preview()
        self.ev_manager.post(EventResumeMusic())
        self.ev_manager.post(EventResumeSound())


class Cutin_manager():
    '''
    Handles everything about cut-in animation.
    "update_state(...)" to setup for next cut-in animation.
    "draw(...)" to draw cut-in animation.
    '''

    images = {
        'front_TheWorld': load_and_scale('cutin_front_theworld.png', 0.93),
        'front_ShuffleBases': load_and_scale('cutin_front_shufflebases.png', 0.65),
        'front_RadiusNotMove': load_and_scale('cutin_front_radiusnotmove.png', 0.52),
        'front_FaDaCai': load_and_scale('cutin_front_fadacai.png', 0.9),
        'front_team_0': load_and_scale('cutin_front_team_0.png', 0.8), # default
        **{f'front_team_1_{_i}': load_and_scale(f'cutin_front_team_1_{_i}.png', 1.5) for _i in range(20)},
        'front_team_2': load_and_scale('cutin_front_team_2.png', 2.45),
        'front_team_3': load_and_scale('cutin_front_team_3.png', 1.95),
        'front_team_4': load_and_scale('cutin_front_team_4.png', 0.65),
        'front_team_5': load_and_scale('cutin_front_team_5.png', 0.32),
        'front_team_6': load_and_scale('cutin_front_team_6.png', 0.71),
        'front_team_7': load_and_scale('cutin_front_team_7.png', 0.61),
        'front_team_8': load_and_scale('cutin_front_team_8.png', 1.),
        'front_team_9': load_and_scale('cutin_front_team_9.png', 1.5),
        'front_team_10': load_and_scale('cutin_front_team_10.png', 0.6),
        'front_team_11': load_and_scale('cutin_front_team_11.png', 0.9), # master
    }

    # background moving lines for the speed visual effect
    # there are two layers
    line_color = (160, 160, 160)
    mid_lines = {
        'size': (300, 8),
        'velocity': 30,
    }
    back_lines = {
        'size': (200, 5),
        'velocity': 20,
    }

    # format: (time, y_position)
    # size of cutin_background: (798, 376)
    # the last element (99, 0) is here to prevent out-of-bound indexing
    mid_lines['time_pos'] = (
        ( 1, 150), ( 2,  40), ( 7, 300), (15, 120), (19, 220), (23,  70), (28, 280),
        (30,  90), (35, 150), (36, 340), (43,  50), (50, 170), (58,  70), (59, 200),
        (60, 330), (62, 160), (67, 120), (73,  70), (80, 270), (84, 300), (99,   0),
    )
    back_lines['time_pos'] = (
        ( 1,  60), ( 4, 200), ( 6, 100), (13,  70), (16, 300), (22,  30), (28, 120),
        (32, 200), (34, 150), (35,  50), (42, 300), (47, 170), (57,  70), (59, 120),
        (60, 180), (64, 130), (65, 200), (74,  80), (78, 120), (84, 110), (99,   0),
    )

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def __init__(self, model):
        self.model = model
        for player in self.model.player_list:
            self.images[f'{player.index}'] = (
                view_utils.overlay_color(
                    os.path.join(view_const.IMAGE_PATH,'cutin_back_outfit.png'),
                    player.color,
                    1.504,
                    0.7
                ).convert()
            )
        self.background_width = 800

    def update_state(self, player_index, team_index, skill_name, prev_screen):
        self.player_index = player_index
        self.team_index = team_index
        self.skill_name = skill_name
        self.background = prev_screen.copy()
        self.timer = 0
        self.mid_lines_index = 0
        self.back_lines_index = 0
        self.mid_lines_to_draw = []
        self.back_lines_to_draw = []

    def update_lines_to_draw(self):
        # append new lines
        if self.timer == self.mid_lines['time_pos'][self.mid_lines_index][0]:
            ypos = self.mid_lines['time_pos'][self.mid_lines_index][1]
            self.mid_lines_to_draw.append(pg.Rect((-self.mid_lines['size'][0], ypos), self.mid_lines['size']))
            self.mid_lines_index += 1
        if self.timer == self.back_lines['time_pos'][self.back_lines_index][0]:
            ypos = self.back_lines['time_pos'][self.back_lines_index][1]
            self.back_lines_to_draw.append(pg.Rect((-self.back_lines['size'][0], ypos), self.back_lines['size']))
            self.back_lines_index += 1
        
        # update position
        for _mid_line in self.mid_lines_to_draw:
            _mid_line.move_ip(self.mid_lines['velocity'], 0)
        for _back_line in self.back_lines_to_draw:
            _back_line.move_ip(self.back_lines['velocity'], 0)

        # remove expired lines
        if (self.mid_lines_to_draw) and (self.mid_lines_to_draw[0].left > self.background_width):
            self.mid_lines_to_draw.remove(self.mid_lines_to_draw[0])
        if (self.back_lines_to_draw) and (self.back_lines_to_draw[0].left > self.background_width):
            self.back_lines_to_draw.remove(self.back_lines_to_draw[0])

    def draw_lines(self, cutin_background):
        for _mid_line in self.mid_lines_to_draw:
            pg.draw.rect(cutin_background, self.line_color, _mid_line)
        for _back_line in self.back_lines_to_draw:
            pg.draw.rect(cutin_background, self.line_color, _back_line)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        cutin_background = self.images[f'{self.player_index}'].copy()
        if self.team_index == 1:
            cutin_front_player = self.images[f'front_team_{self.team_index}_{(self.timer//2)%20}']
        else:
            cutin_front_player = self.images[f'front_team_{self.team_index}']
        cutin_front_skill = self.images[f'front_{self.skill_name}']
        self.update_lines_to_draw()
        self.draw_lines(cutin_background)

        if self.timer < 30:
            # phase 1
            screen.blit( cutin_background, view_const.CUTIN_BACKGROUND_PHASE1_TOPLEFT + (800/30*(self.timer+1), 0) )
            screen.blit( cutin_front_skill, view_const.CUTIN_FRONT_SKILL_PHASE1_TOPLEFT + view_const.CUTIN_SKILL_OFFSET[self.skill_name] + ((800/30*(self.timer+1)), 0) )
            screen.blit( cutin_front_player, view_const.CUTIN_FRONT_PLAYER_PHASE1_TOPLEFT + view_const.CUTIN_PLAYER_OFFSET[self.team_index] + ((800/30*(self.timer+1)), 0) )

        elif 30 <= self.timer < 60:
            # phase 2
            screen.blit( cutin_background, view_const.CUTIN_BACKGROUND_PHASE2_TOPLEFT )
            screen.blit( cutin_front_skill, view_const.CUTIN_FRONT_SKILL_PHASE2_TOPLEFT + view_const.CUTIN_SKILL_OFFSET[self.skill_name] + ((view_const.CUTIN_PHASE2_SHIFT/30*(self.timer-29)), 0) )
            screen.blit( cutin_front_player, view_const.CUTIN_FRONT_PLAYER_PHASE2_TOPLEFT + view_const.CUTIN_PLAYER_OFFSET[self.team_index] + ((view_const.CUTIN_PHASE2_SHIFT/30*(self.timer-29)), 0) )

        else:
            # phase 3
            cutin_background.blit(cutin_front_skill, view_const.CUTIN_SKILL_OFFSET[self.skill_name] + (view_const.CUTIN_FRONT_SKILL_PHASE3_TOPLEFT[0], view_const.CUTIN_FRONT_SKILL_PHASE3_TOPLEFT[1] - view_const.CUTIN_BACKGROUND_PHASE2_TOPLEFT[1]))
            cutin_background.blit(cutin_front_player, view_const.CUTIN_PLAYER_OFFSET[self.team_index] + (view_const.CUTIN_FRONT_PLAYER_PHASE3_TOPLEFT[0], view_const.CUTIN_FRONT_PLAYER_PHASE3_TOPLEFT[1] - view_const.CUTIN_BACKGROUND_PHASE2_TOPLEFT[1]))
            cutin_background = cutin_background.convert()
            cutin_background.set_alpha(255/30*(90-self.timer))
            screen.blit( cutin_background, view_const.CUTIN_BACKGROUND_PHASE2_TOPLEFT )

        pg.display.flip()
        self.timer += 1


def init_cutin():
    Cutin_manager.init_convert()
