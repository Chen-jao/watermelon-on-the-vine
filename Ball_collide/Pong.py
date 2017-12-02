#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''

title:
小球完全弹性碰撞

process:
小球绘制--finished
小球移动--finished
小球范围限定--finsihed
小球相互作用--waiting

addtional:
小球增加删除--waitong
小球碰撞音效--waiting
背景音乐--waiting
小求速度控制--waiting

此方案作罢，group虽然便于管理但group不能像list那样获取特定值，故因此group在执行循环判断会出现致命BUG
导致交换两次值从而变为本身，重开文档

'''

'''
__author__ = {'name' : '葡萄藤上结西瓜', 
              'mail' : '785492682@qq.com', 
              'version' : '1.0'}
'''

import pygame
import math
import random
import sys
from sys import exit
from pygame.locals import *

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 550

class Pong(pygame.sprite.Sprite):
    def __init__(self, color = (0, 0, 0), x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        #初始化颜色、半径、位置和线条粗度等信息
        self.color = color
        self.radius = 50
        self.pos_x = x
        self.pos_y = y
        self.width = 2
    
    #速度处理
    def vel(self, x, y):
        self.vel_x = x
        self.vel_y = y

    #绘制小球移动轨迹
    def moveBall(self):
        
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        #边界碰撞检测与处理
        if self.pos_x <= self.radius or self.pos_x >= SCREEN_WIDTH - self.radius:
            self.vel_x = -self.vel_x
        if self.pos_y <= self.radius or self.pos_y >= SCREEN_HEIGHT - self.radius:
            self.vel_y = -self.vel_y

    def BallCollideDo(self, ball_second):
        #小球之间的碰撞进行速度交换
        textPrint(font2, 0, 350, str("ball_first_x_pre: ") +
                  str(self.vel_x), (0, 120, 220))
        textPrint(font2, 0, 400, str("ball_secon_x_pre: ") +
                  str(ball_second.vel_x), (0, 120, 220))
        # temp_vel_x = self.vel_x
        # temp_vel_y = self.vel_y
        # self.vel_x = ball_second.vel_x
        # self.vel_y = ball_second.vel_y
        # ball_second.vel_x = temp_vel_x
        # ball_second.vel_y = temp_vel_y
        textPrint(font2, 0, 450, str("ball_first_x: ") + str(self.vel_x), (0, 120, 220))
        textPrint(font2, 0, 500, str("ball_secon_x: ") + str(ball_second.vel_x), (0, 120, 220))
        return ball_second.vel_x, ball_second.vel_y, self.vel_x, self.vel_y
    #小球间碰撞检测
    def BallCollideJudge(self, ball_second):
        x = (self.pos_x - ball_second.pos_x)**2
        y = (self.pos_y - ball_second.pos_y)**2
        z = (self.radius + ball_second.radius)**2
        textPrint(font2, 0, 200, str("x: ") +
                  str(x) + str(" ") + str("y: ") + str(y) + str(" ") + str("z: ") + str(z), (0, 120, 220))
        if x + y <= z:
            return True
#创建不同大小的字体
def createFont(size = 10):
    return pygame.font.Font(None, size)
#文本信息输出函数吊调用
def textPrint(font, x, y, message, color = (0, 0, 0)):
    #文本信息处理
    text = font.render(message, True, color)
    #文本绘制
    screen.blit(text, (x, y))

#初始化库
pygame.init()
#屏幕创建
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0)
#标题
pygame.display.set_caption("小球碰撞演示")
#字体创建
font1 = createFont(22)
font2 = createFont(44)
#初始化背景
background_img = pygame.image.load('BallCollide/black.jpg')
background_rect = pygame.Rect(26, 12, 770, 550)
#截取所需要的图中位置匹配屏幕
background_ = background_img.subsurface(background_rect).convert_alpha()
#创建小球的精灵组
ball_group = pygame.sprite.Group()

#创建小球体
for i in range(2):
    #颜色随机生成
    #ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if i == 1:
        ball_color = (0, 0, 0)
    else:
        ball_color = (255, 255, 255)
    #位置随机生成
    #ball_x = random.randint(20, SCREEN_WIDTH - 20)
    # ball_y = random.randint(20, SCREEN_HEIGHT - 20)
    if i == 0:
        ball_x = 100
    else:
        ball_x = 600
    ball_y = 300
    #生成ball
    ball = Pong(ball_color, ball_x, ball_y)
    #速度设置
    if i == 0:
        ball.vel(5, 0)
    else:
        ball.vel(-5, 0)
    #分配组便于管理
    ball_group.add(ball)

#ball_test1 = Pong((255, 0, 0), (100, 100))
#设置帧数
time = pygame.time.Clock()
while True:
    #帧数50
    time.tick(10)
    #事件捕捉
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.exit()
            sys.exit()
    #键盘事件捕捉
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    #绘制屏幕
    #screen.blit(background_, (0, 0))
    screen.fill((255, 255, 0))
    #绘制小球和移动小球
    for ball in ball_group:
         pygame.draw.circle(screen, ball.color, (ball.pos_x, ball.pos_y), ball.radius, ball.width)
         ball.moveBall()
    # for ball_first in ball_group:
    #     pygame.draw.circle(screen, ball_first.color, (ball_first.pos_x, ball_first.pos_y), ball_first.radius, ball_first.width)
    #     ball_first.moveBall()
    #     for ball_second in ball_group:
    #         #if ball_first != ball_second:
    #         if BallCollideJudge(ball_first, ball_second):
    #             BallCollideDo(ball_first, ball_second)
    #             pass
    for ball_first in ball_group:
        for ball_second in ball_group:
            if ball_first != ball_second:
                if ball_first.BallCollideJudge(ball_second):
                    ball_first.velx, ball_first.vel_y, ball_second.vel_x, ball_second.vel_y = ball_first.BallCollideDo(ball_second)
                    textPrint(font2, 0, 50, str("ball_first_x: ") + str(ball_first.vel_x), (0, 120, 220))
                    textPrint(font2, 0, 100, str("ball_secon_x: ") + str(ball_second.vel_x), (0, 120, 220))
    
    textPrint(font2, 300, 50, str("ball_first_x: ") + str(ball_first.vel_x), (0, 120, 220))
    textPrint(font2, 300, 100, str("ball_secon_x: ") + str(ball_second.vel_x), (0, 120, 220))
    # for i in range(len(ball_group)):
    #     for j in range(len(ball_group)):
    #         if i != j:
    #             if ball_group[i].BallCollideJudge(ball_group[j]):
    #                 ball_group[i].BallCollideDo(ball_group[j])

    textPrint(font1, 500, 400, str("what do you want and want to be?"), (0, 120, 220))
    pygame.display.update()

