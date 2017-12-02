#!/usr/bin/env python
#-*- coding: utf-8 -*-

from stdafx import pygame
from load_path import *
#加载图片资源统一格式
def img_load(root_path): return pygame.image.load(root_path)

#图片处理操作
def img_process(img_size=(0, 0, 0, 0)):
    img = img_load(load_path("Ball_Collide/resource", "Airuddy_normal.jpg"))
    if cmp(img_size, (0, 0, 0, 0)) != 0:
        rect = pygame.Rect(img_size)
        img = img.subsurface(rect).convert_alpha()
    return img
