#!/usr/bin/env python
#-*- coding: utf-8 -*-

from stdafx import random
from init_run_environment import SCREEN_WIDTH, SCREEN_HEIGHT

class Ball(object):
    def __init__(self, color=(0, 0, 0), pos=[0, 0], vel=[0, 0]):
        #初始化颜色、半径、位置、速度和线条粗度等信息
        #这里完全采用列表进行形成二维数据进行操作判断exp: list[()]选取list[i][i]
        self.color = color
        self.vel = vel
        self.pos = pos
        self.width = 2
        self.radius = 30

    #控制小球移动
    def ballMove(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        #边界碰撞检测与处理,这里原本打算和边界限定合并，经过研究发现没有多大意义，而且功能会冲突，所以还是这样写吧，注意多减少的1是为了避免出现沾边现象
        if self.pos[0] <= self.radius - 1 or self.pos[0] >= SCREEN_WIDTH - self.radius - 1:
            self.vel[0] = -self.vel[0]
        if self.pos[1] <= self.radius - 1 or self.pos[1] >= SCREEN_HEIGHT - self.radius - 1:
            self.vel[1] = -self.vel[1]

    #限定小球于屏幕范围内，这里整合上个版本的贴边问题代码和控制小球生成在屏幕内的代码，可重复调用
    def ballInScreen(self):
        if self.pos[0] > SCREEN_WIDTH - self.radius:
            self.pos[0] = SCREEN_WIDTH - self.radius - 1
        elif self.pos[0] < self.radius:
            self.pos[0] = self.radius + 1
        elif self.pos[1] > SCREEN_HEIGHT - self.radius:
            self.pos[1] = SCREEN_HEIGHT - self.radius - 1
        elif self.pos[1] < self.radius:
            self.pos[1] = self.radius + 1
        return self.pos  # 返回矫正后的pos

    #速度加
    def velAdd(self):
        if directionVelx(self): # 判断速度方向
            self.vel[0] += 1
        else:
            self.vel[0] -= 1
        if directionVely(self):
            self.vel[1] += 1
        else:
            self.vel[1] -= 1

    #速度减
    def velReduce(self):
        if directionVelx(self):
            self.vel[0] -= 1
        else:
            self.vel[0] += 1
        if directionVely(self):
            self.vel[1] -= 1
        else:
            self.vel[1] += 1
# # 速度值限定
# def vel_limit(vel):
#     if vel == 0 or abs(vel) >= 10:
#         return True
#     return False


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


#限制小球重叠，可以将其视为小球间碰撞检测
def ballCollideJudge(ball_first, ball_second):
    x = (ball_first.pos[0] - ball_second.pos[0])**2
    y = (ball_first.pos[1] - ball_second.pos[1])**2
    z = (ball_first.radius + ball_second.radius)**2
    if x + y <= z + 1:  # 判断时这里的加1是为了更好地拟合碰撞，防止出现小球碰撞时有粘连现象的发生
        return True
    return False

#进行速度交换
def ballCollideDo(ball_first, ball_second):
    return ball_second.vel[0], ball_second.vel[1], ball_first.vel[0], ball_first.vel[1]

#处理小球碰撞
def ballCollide(ball_group):
    mark = False
    for i in range(len(ball_group)):
        for j in range(len(ball_group)):
            if i < j:
                if ballCollideJudge(ball_group[i], ball_group[j]):  # 碰撞检测

                    ball_group[i].vel[0], ball_group[i].vel[1], ball_group[j].vel[0], ball_group[j].vel[1] = ballCollideDo(
                        ball_group[i], ball_group[j])  # 给两个小球的velx与vely交换
                    mark = True
    return mark

# 生成位置随机需要对位置进行检测防止出现重叠现象
def checkBallPos(temp_ball, ball_group):
    # 检查生成小球的位置是否重叠
    temp_ball.ballInScreen()  # 限定范围在屏幕内
    for i in range(len(ball_group)):  # 逐一进行对比
        # 调用碰撞检测函数，这里只需要判定重合所以可以重用该函数
        if ballCollideJudge(temp_ball, ball_group[i]):
            return False  # 重叠的话返回FAlse
    return True

#随机生成属性
def ballPropertyInit(i):
    #颜色随机生成
    ball_color = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))
    #位置随机生成
    ball_pos = [random.randint(20, SCREEN_WIDTH - 20),
                random.randint(20, SCREEN_HEIGHT - 20)]
    #速度生成
    if i % 2 == 0:
        ball_vel = [3, 3]
    else:
        ball_vel = [-3, 3]
    return ball_color, ball_pos, ball_vel

#生成小球体,mark控制小球生成数目，可以和add重用
def createBall(ball_group, mark=5):
    i = 1
    if len(ball_group) > 12:  # 减少系统压力，过多可能会导致崩溃
        print "小球数目过多不在提供添加"
        return ball_group
    while True:
        #小球初始化
        ball_color, ball_pos, ball_vel = ballPropertyInit(i)
        temp_ball = Ball(ball_color, ball_pos, ball_vel)
        if checkBallPos(temp_ball, ball_group):  # 检查重叠
            ball_group.append(temp_ball)  # 放入容器内
            i += 1
            if i > mark:  # 数量控制
                return ball_group

#响应右键删除小球
def deleteBall(ball_group):
    if len(ball_group) <= 0:  # 解决删除完毕后再删除的BUG问题
        print "无可删除的小球"
        return
    ball_group.pop()
