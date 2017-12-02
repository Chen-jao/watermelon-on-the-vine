#!/usr/bin/env python
#-*- coding: utf-8 -*-


'''

title:
小球完全弹性碰撞

function:
小球绘制--finished
小球移动--finished
小球范围限定--finsihed
小球相互作用--finished

addtional function:
鼠标左右键控制小球增加删除--finished
小球碰撞音效--finished
背景音乐--finsihed
小求速度控制--finished             //这里需要注意的是小球运动中速度是改变的所以要判断速度？然后进行处理另外就是要改变所有的小球，

bug:
1.初始小球粘连问题 
debug: finsihed
solution: 增加检测小球初始位置函数

2.小球碰撞过程中贴边问题
debug: finished?
solution: 贴边检测
需要时间验证...........

3.数目变多的话会碰撞过程中会出现粘连卡顿现象         ----------------未处理---------------
debug: waiting
solution: 修改粘连

4.右键移除所有小球后自动退出
debug: finished
solution : 检测当前还有没有小球，没有则不再删除     

5.碰撞过多，碰撞音频处理不协调有延迟                 ----------------待优化---------------
debug: waiting
solution：暂无 

6.增减速度界限值控制                               -----------------未处理---------------
debug： waiting
solution： 暂无




个人感觉最好在碰撞检测时候不要直接使用所定义好的数值，这和数学上有点差异，最好在数值上稍微进行一下微调

optimize：                                       ----------------待处理---------------
分辨率问题 waiting
移动流畅度问题 waiting
函数优化，碰撞检测是该传递参数为坐标，放弃对象传递 waiting
代码结构未优化

区别version 1.0:
上一个版本中由于使用pygame中的group出现不能满足要求的情况，因此这个版本中自定义group实现


'''

'''
__author__ = {'name' : '葡萄藤上结西瓜', 
              'mail' : '785492682@qq.com', 
              'version' : '1.1'}
'''


import pygame
import math
import random
import os
import time
from pygame.locals import *

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 550


class Pong(pygame.sprite.Sprite):
    def __init__(self, color=(0, 0, 0), pos = [0, 0], vel = [0, 0]):
        pygame.sprite.Sprite.__init__(self)
        #初始化颜色、半径、位置和线条粗度等信息
        #这里完全采用列表进行形成二维数据进行操作判断exp: list[()]选取list[i][i]
        self.color = color
        self.vel = vel
        self.pos = pos
        self.width = 2
        self.radius = 30
    
    def moveBall(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        #边界碰撞检测与处理
        if self.pos[0] <= self.radius or self.pos[0] >= SCREEN_WIDTH - self.radius:
            self.vel[0] = -self.vel[0]
        if self.pos[1] <= self.radius or self.pos[1] >= SCREEN_HEIGHT - self.radius:
            self.vel[1] = -self.vel[1]

    #贴边检测的函数，解决碰撞过程中贴边问题
    def checkLimit(self):
        if self.pos[0] > SCREEN_WIDTH - self.radius:
            self.pos[0] = SCREEN_WIDTH - self.radius - 1
        elif self.pos[0] < self.radius:
            self.pos[0] = self.radius + 1
        elif self.pos[1] > SCREEN_HEIGHT - self.radius:
            self.pos[1] = SCREEN_HEIGHT - self.radius - 1
        elif self.pos[1] < self.radius:
            self.pos[1] = self.radius + 1
        return self.pos  # 返回矫正后的容器
    #速度加
    def addVel(self):
        if directionVelx(self) == True:
            self.vel[0] += 1
        else:
            self.vel[0] -= 1
        if directionVely(self) == True:
            self.vel[1] += 1
        else:
            self.vel[1] -= 1
    
    #速度减
    def reduceVel(self):
        if directionVelx(self) == True:
            self.vel[0] -= 1
        else:
            self.vel[0] += 1
        if directionVely(self) == True:
            self.vel[1] -= 1
        else:
            self.vel[1] += 1

#小球速度方向检测x
def directionVelx(ball):
    if ball.vel[0] > 0:
        return True
    return False
#小球速度方向检测y
def directionVely(ball):
    if ball.vel[1] > 0:
        return True
    return False

#判断小球是否碰撞
def BallCollideJudge(ball_first, ball_second):
    x = (ball_first.pos[0] - ball_second.pos[0])**2
    y = (ball_first.pos[1] - ball_second.pos[1])**2
    z = (ball_first.radius + ball_second.radius)**2
    if x + y <= z + 1:#判断时这里的加1是为了更好地拟合碰撞，防止出现小球碰撞时有粘连现象的发生
        return True
    return False

#进行速度交换
def BallCollideDo(ball_first, ball_second):
    return ball_second.vel[0], ball_second.vel[1], ball_first.vel[0], ball_first.vel[1]


#创建不同大小的字体
def createFont(size=10):
    return pygame.font.Font(None, size)
#文本信息输出函数吊调用


def textPrint(font, x, y, message, color=(0, 0, 0)):
    #文本信息处理
    text = font.render(message, True, color)
    #文本绘制
    screen.blit(text, (x, y))

def checkBallPos(temp_ball, ball_group):
    #检查生成小球的位置是否重叠
    if temp_ball.pos[0] > temp_ball.radius or temp_ball.pos[0] < SCREEN_WIDTH - temp_ball.radius:#pos.x限制在边界加减半径内
        if temp_ball.pos[1] > temp_ball.radius or temp_ball.pos[1] < SCREEN_HEIGHT - temp_ball.radius:#pos.y限制在边界加减半径内
            for i in range(len(ball_group)):#逐一进行对比
                if BallCollideJudge(temp_ball, ball_group[i]):#调用碰撞检测函数，这里只需要判定重合所以可以重用该函数
                    return False#重叠的话返回FAlse
    return True

#生成小球的函数
def createBall(ball_group):
    i = 1
    while True:
        #颜色随机生成
        ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #位置随机生成
        ball_pos = [random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)]
        #速度生成
        if i % 2 == 0:
            ball_vel = [3, 3]
        ball_vel = [-3, 3]

        temp_ball = Pong(ball_color, ball_pos, ball_vel)
        if checkBallPos(temp_ball, ball_group):  # 检查重叠
            ball_group.append(temp_ball)
            i += 1
            if i > 5:
                return


#音乐类
class Music():
    def __init__(self, sound):
        self.sound = sound
        self.channel = None
        
    def playSound(self):
        self.channel = pygame.mixer.Channel(True)
        self.channel.set_volume(0.1)
        self.channel.play(self.sound, -1, False, True)

    def playPause(self):
        #self.set_volume(0.0)
        self.channel.pause()
#加载初始音频
def auInit():
    global bg_au, hit_au
    pygame.mixer.init()
    bg_au = pygame.mixer.Sound("BallCollide/bg_au.ogg")
    #hit_au = pygame.mixer.music.load("BallCollide/hit.wav")
    hit_au = pygame.mixer.music
    hit_au.load("BallCollide/hit.ogg")
    hit_au.set_volume(0.3)

#循环播放背景音乐
def roundBgSound(bg_music_play):
    if not bg_music_play:
        bg_sound.playSound()
        bg_music_play = True
    if not bg_sound.channel.get_busy():
        bg_music_play = False
    return bg_music_play
#碰撞音乐播放
def hitSound(hit_music_play):
    if not hit_au.get_busy():
        hit_music_play = False
    if not hit_music_play:
        hit_au.play(0)
        hit_music_play = True
        #pygame.mixer.music.play(0)
    return hit_music_play

def addBall(ball_group):
    i = 1
    if len(ball_group) > 12:    #减少系统压力，过多可能会导致崩溃
        print "小球数目过多不在提供添加"
        return ball_group
    while True:
        #颜色随机生成
        ball_color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        #位置随机生成
        ball_pos = [random.randint(
            20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)]
        #速度生成
        if i % 2 == 0:
            ball_vel = [3, 3]
        ball_vel = [-3, 3]

        temp_ball = Pong(ball_color, ball_pos, ball_vel)
        if checkBallPos(temp_ball, ball_group):  # 检查重叠
            ball_group.append(temp_ball)
            i += 1
            if i > 1:
                return

#响应右键删除小球
def deleteBall(ball_group):
    if len(ball_group) <= 0:    #解决删除完毕后再删除的BUG问题
        print "无可删除的小球"
        return
    ball_group.pop()

#初始化库
pygame.init()
#初始化音频
auInit()
bg_sound = Music(bg_au)

#屏幕创建
SCREEN_DEFAULT_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE, 0, 0)
#标题
pygame.display.set_caption("小球碰撞演示")
#字体创建
font1 = createFont(22)
font2 = createFont(44)
#初始化背景
BG_IMG = "black.jpg"
bg_path = os.path.join("BallCollide", BG_IMG)   #这里只是突然想到了os模块想用一下，没啥特殊意义
if not os.path.exists(bg_path):
    print "无此图片"
background_img = pygame.image.load(bg_path)
background_rect = pygame.Rect(26, 12, 770, 550)
#截取所需要的图中位置匹配屏幕
background_ = background_img.subsurface(background_rect).convert_alpha()

#存放小球的容器，本来想用pygame自带的group 但是他不支持index所以后面判断会有问题，因此放弃了
#sprite的group用来绘制管理有较好的用途，不过还是自己重写方法更好
ball_group = []
#创建小球体
createBall(ball_group)
'''
for i in range(5):
    #颜色随机生成
    ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #位置随机生成
    ball_pos = [random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)]
    #速度生成
    if i % 2 == 0:
        ball_vel = [5, 5]
    ball_vel = [-5, 5]
    #测试用
    # if i == 1:
    #     ball_color = (0, 0, 0)
    #     ball_pos = [100, 300]
    #     ball_vel = [5, 0]
    # else:
    #     ball_color = (255, 255, 255)
    #     ball_pos = [600, 300]
    #     ball_vel = [-5, 0]
    temp_ball = Pong(ball_color, ball_pos, ball_vel)
    #生成ball
    if checkBallPos(temp_ball, ball_group):
        ball_group.append(temp_ball)
'''
#设置帧数
frame_time = pygame.time.Clock()

#背景音乐
bg_music_play = False #背景音乐播放标志
hit_music_play = False #撞击音乐播放标志
#bg_sound.playSound()
while True:
    #帧数50
    frame_time.tick(60)
    #事件捕捉
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.exit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_pressed_array = pygame.mouse.get_pressed()    #获取鼠标事件
            for index in range(len(mouse_pressed_array)):
                if mouse_pressed_array[index]:
                    if index == 0:
                        addBall(ball_group)
                        #print "left"
                    elif index == 1:
                        #print "wheel"
                        pass
                    elif index == 2:
                        #print "right"
                        deleteBall(ball_group)
        # if event.type == KEYDOWN:
        #     if event.key == K_f:
        #         full_screen = not full_screen
        #         if full_screen:
        #             print '全屏模式!'
        #         else:
        #             print '默认窗口!'
        #     if full_screen:
        #         screen = pygame.display.set_mode(
        #             SCREEN_DEFAULT_SIZE, FULLSCREEN)
        #     else:
        #         screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE)
    #键盘事件捕捉
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_UP] or keys[K_w]:#实现上和W加速度下S减速度
        for ball_vel_add in ball_group:
            ball_vel_add.addVel()
    elif keys[K_DOWN] or keys[K_s]:
        for ball_vel_reduce in ball_group:
            ball_vel_reduce.reduceVel()

    #绘制屏幕
    screen.blit(background_, (0, 0))
    #screen.fill((255, 255, 0))
    
    #绘制小球和移动小球
    for ball in ball_group:
        #贴边检测
        ball.pos = ball.checkLimit()
        #绘制小球
        pygame.draw.circle(screen, ball.color, ball.pos, ball.radius, ball.width)
        #移动
        ball.moveBall()

    for i in range(len(ball_group)):
        for j in range(len(ball_group)):
            if i < j:
                if BallCollideJudge(ball_group[i], ball_group[j]):#碰撞检测
                    hit_music_play = hitSound(hit_music_play)
                    ball_group[i].vel[0], ball_group[i].vel[1], ball_group[j].vel[0], ball_group[j].vel[1] = BallCollideDo(
                        ball_group[i], ball_group[j])#给两个小球的velx与vely交换

    bg_music_play = roundBgSound(bg_music_play)

    textPrint(font1, 500, 400, str("what do you want and want to be?"), (0, 120, 220))
    pygame.display.update()
