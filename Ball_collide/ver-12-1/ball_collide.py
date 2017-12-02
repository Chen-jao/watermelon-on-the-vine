#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
此处为程序主逻辑区域，负责脚本的调用

function 说明：基本完成
1.生成小球
2.移动控制
3.碰撞检测及处理
4.音效控制
5.ball速度控制
6.屏幕大小控制
7.....

bug 说明:     待解决
1.贴边问题
2.粘连问题 
3.屏幕分辨率
4......

优化说明：   待处理
1.代码进一步重构
2.逻辑运算进一步优化
3.模块化进一步优化
4.命名规范优化
5.高级语法技巧引入
6.新功能添加
7.可维护性检测



后记：
    说实话我觉得事件处理这一块写的很不好，虽然还没有对这一块代码进行整理，但是给人感觉太长了，
    不好看，难受.....
    我觉得完全可以单独建立一个事件处理模块，以后慢慢试试，最近一段时间不会再进行大的改动了
'''


'''
__author__ = {'name' : '葡萄藤上结西瓜', 
              'mail' : '785492682@qq.com', 
              'version' : '1.3'}
'''


from stdafx import *  # 加载预设模块or库
from load_image import *    # 加载图片管理模块
from pygame.locals import * # 加载pygame库的一些方法
from load_audio import MusicBgm, MusicEffect    # 加载音频管理模块
from init_run_environment import init_environment, screen_change   # 加载预设环境模块
from ball_manager import * # 加载小球管理模块

screen, full_screen = init_environment()  # 屏幕创建
bg_img = img_process()  # 背景图片生成and处理

bg_sound = MusicBgm()  # bgm加载
bg_sound.init_music(load_path('Ball_collide/audio', 'bg_au.ogg'))

hit_sound = MusicEffect() # hit音效加载
hit_sound.init_music(load_path('Ball_collide/audio', 'hit.ogg'))

#创建存放小球的容器
ball_group = []
#生成小球
createBall(ball_group)

frame_time = pygame.time.Clock()  # 设置帧数
while True:
    frame_time.tick(60)  # 设置帧数60

    for event in pygame.event.get(): # 事件捕捉            
        if event.type == QUIT:
            pygame.display.QUIT()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_f:  # 屏幕模式切换
                full_screen = not full_screen
                screen_change(full_screen)
        if event.type == MOUSEBUTTONDOWN:
            mouse_pressed_array = pygame.mouse.get_pressed()  # 获取鼠标事件
            for index in range(len(mouse_pressed_array)):
                if mouse_pressed_array[index]:
                    if index == 0:
                        createBall(ball_group, 1)  # 1表示添加1个小球
                        #print "left"
                    elif index == 1:
                        #print "wheel"
                        pass
                    elif index == 2:
                        #print "right"
                        deleteBall(ball_group)

    keys = pygame.key.get_pressed()  # 键盘事件捕捉及处理
    if keys[K_ESCAPE]:
        exit()
    elif keys[K_UP] or keys[K_w]:  # 实现上和W加速度
        for ball_vel in ball_group:
            ball_vel.velAdd()
    elif keys[K_DOWN] or keys[K_s]:  # 下S减速度
        for ball_vel in ball_group:
            ball_vel.velReduce()
    
    screen.blit(bg_img, (0, 0))  # 屏幕绘制

    for ball in ball_group:
        #绘制小球
        pygame.draw.circle(screen, ball.color, ball.pos,
                           ball.radius, ball.width)
        #移动小球
        ball.ballMove()

    #碰撞的检测和处理
    if ballCollide(ball_group):
        hit_sound.play_sound()  # 播放碰撞音效

    #bg_sound.play_sound()   # 播放背景音乐

    pygame.display.update() # 更新屏幕

