#!/usr/bin/env python
#-*- coding: utf-8 -*-

from stdafx import pygame
from pygame.locals import *

# 建议使用mixer.music来播放背景音乐，channel来播放音效,这里方便子类重写
class Music(object):
    def __init__(self):
        self.music = None
        self.music_play = False

    #预处理音频，进入待机状态
    def init_music(self, au_path): 
        pass
    #播放音频，负责一些逻辑控制
    def play_sound(self):
        pass
    
    #add addtional function and you can add in children class.

#继承实现音效处理
class MusicEffect(Music):
    def __init__(self):
        Music.__init__(self)

    def init_music(self, au_path):
        self.music = pygame.mixer.Channel(True)
        self.music.set_volume(0.1)
        self.sound = pygame.mixer.Sound(au_path)

    def play_sound(self):
        if not self.music.get_busy():
            self.music_play = False
        if not self.music_play:
            self.music.play(self.sound, 0, False, True)
            self.music_play = True
            
#继承实现bgm处理
class MusicBgm(Music):
    def __init__(self):
        Music.__init__(self)
    #bgm加载与播放状体初始化

    def init_music(self, au_path):  # 建议使用mixer.music来播放背景音乐，channel来播放音效
        self.music = pygame.mixer.music
        self.music.load(au_path)
        self.music.set_volume(0.1)
    #播放
    def play_sound(self):
        if not self.music_play:
            self.music.play(-1)
            self.music_play = True
        if not self.music.get_busy():
            self.music_play = False
