#!/usr/bin/env python
#-*- coding: utf-8 -*-

from stdafx import pygame
from pygame.locals import *

# 屏幕大小设置
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
SCREEN_DEFAULT_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

#屏幕处理操作
def screen_change(full_screen):
    if full_screen:
        screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE, FULLSCREEN)
        print '全屏模式!'
    else:
        screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE)
        print '默认窗口!'

# 运行环境初始化
def init_environment():
    global screen, full_screen
    full_screen = False
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("完全弹性碰撞演示")
    screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE, 0, 0)
    return screen, full_screen

#here add addtional function
