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

5.碰撞过多，碰撞音频处理不协调有延迟                ----------------待优化---------------
debug: waiting
solution：暂无 多线程的话可能会解决这个问题

6.增减速度界限值控制                               -----------------未处理---------------
debug： waiting
solution： 


optimize：                                       ----------------待处理---------------
分辨率问题 waiting
移动流畅度问题 waiting
函数优化，碰撞检测是该传递参数为坐标，放弃对象传递 waiting
代码结构未优化

区别version 1.0:
上一个版本中由于使用pygame中的group出现不能满足要求的情况，因此这个版本中自定义group实现


新版本修改如下：
    进行了部分的代码重构
待改进：
    模块化
    代码进一步重构，关于音频的处理统一模式
    命名规范

'''

'''
__author__ = {'name' : '葡萄藤上结西瓜', 
              'mail' : '785492682@qq.com', 
              'version' : '1.2'}
'''


from stdafx import *

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 550
SCREEN_DEFAULT_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

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
        if directionVelx(self):
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

class Music:
    def __init__(self, sound):
        self.sound = sound
        self.channel = None
    
    def init_channel(self):
        self.channel = pygame.mixer.Channel(True)
        self.channel.set_volume(0.1)
        self.channel.play(self.sound, -1, False, True)

    def play_bg_sound(self, bg_music_play):
        if not bg_music_play:
            self.init_channel()
            bg_music_play =  True
        if not self.channel.get_busy():
            bg_music_play =  False
        return bg_music_play

    # def play_hit_sound(slef, hit_music_play):
    #     if not self.get_busy():
    #         hit_music_play = False
    #     if not hit_music_play:
    #         self.init_music()
    #         hit_music_play =  True
            #pygame.mixer.music.play(0)


def load_bg_audio(root, name):
    au_path = os.path.join(root, name)
    if not au_path:
        print 'no exists audio.'
    else:
        return pygame.mixer.Sound(au_path)

def load_hit_audio(root, name):
    au_path = os.path.join(root, name)
    if not au_path:
        print 'no exists audio.'
    else:
        hit_au = pygame.mixer.music
        hit_au.load(au_path)
        hit_au.set_volume(0.3)
    return hit_au

def play_hit_sound(hit_music_play):
    if not hit_sound.get_busy():
        hit_music_play = False
    if not hit_music_play:
        hit_sound.play(0)
        hit_music_play = True
    return hit_music_play

# #加载初始音频
# def auInit():
#     global bg_au, hit_au
#     pygame.mixer.init()
#     bg_au = pygame.mixer.Sound("BallCollide/bg_au.ogg")
#     #hit_au = pygame.mixer.music.load("BallCollide/hit.wav")
#     hit_au = pygame.mixer.music
#     hit_au.load("BallCollide/hit.ogg")
#     hit_au.set_volume(0.3)

#速度大小控制
def velNunLimit(vel):
    pass

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

#运行环境初始化
def initRunEnvironment():
    global screen, full_screen
    full_screen = False
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("完全弹性碰撞演示")
    screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE, 0, 0)

#屏幕处理操作
def screenChange(full_screen):
    if full_screen:
        screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE, FULLSCREEN)
        print '全屏模式!'
    else:
        screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE)
        print '默认窗口!'

#创建不同大小的字体
def createFont(size=10):
    return pygame.font.Font(None, size)

#文本信息输出函数吊调用
def textPrint(font, x, y, message, color=(0, 0, 0)):
    #文本信息处理
    text = font.render(message, True, color)
    #文本绘制
    screen.blit(text, (x, y))

#加载图片资源
def loadImg(root, name):
    img_path = os.path.join(root, name)
    if not img_path:
        print "no exists picture."
    else:
        return pygame.image.load(img_path)



#限制小球重叠，科将其视为小球间碰撞检测
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
def ballCollide():
    mark = False
    for i in range(len(ball_group)):
        for j in range(len(ball_group)):
            if i < j:
                if ballCollideJudge(ball_group[i], ball_group[j]):  # 碰撞检测
                    
                    ball_group[i].vel[0], ball_group[i].vel[1], ball_group[j].vel[0], ball_group[j].vel[1] = ballCollideDo(ball_group[i], ball_group[j])  # 给两个小球的velx与vely交换
                    mark = True
    return mark
'''
#原本打算采用这种方法，但发现调用太麻烦而且代码冗余大就舍弃了，不过可以借鉴
# #小球出现范围限定在屏幕内,这里使用矫正的话效果会更好，故改用矫正方法
# def ballInScreen(temp_ball):
#     if temp_ball.pos[0] > temp_ball.radius or temp_ball.pos[0] < SCREEN_WIDTH - temp_ball.radius:  # pos.x限制在边界加减半径内
#         if temp_ball.pos[1] > temp_ball.radius or temp_ball.pos[1] < SCREEN_HEIGHT - temp_ball.radius:  # pos.y限制在边界加减半径内
#             return True
'''

#生成位置随机需要对位置进行检测防止出现重叠现象
def checkBallPos(temp_ball, ball_group):
    #检查生成小球的位置是否重叠
    temp_ball.ballInScreen()#限定范围在屏幕内
    for i in range(len(ball_group)):  # 逐一进行对比
        # 调用碰撞检测函数，这里只需要判定重合所以可以重用该函数
        if ballCollideJudge(temp_ball, ball_group[i]):
            return False  # 重叠的话返回FAlse
    return True

#随机生成属性
def ballPropertyInit(i):
    #颜色随机生成
    ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #位置随机生成
    ball_pos = [random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)]
    #速度生成
    if i % 2 == 0:
        ball_vel = [3, 3]
    else:
        ball_vel = [-3, 3]
    return ball_color, ball_pos, ball_vel

#生成小球体
def createBall(ball_group, mark = 5):
    i = 1
    if len(ball_group) > 12:  # 减少系统压力，过多可能会导致崩溃
        print "小球数目过多不在提供添加"
        return ball_group

    while True:
        #小球初始化
        ball_color, ball_pos, ball_vel = ballPropertyInit(i)
        temp_ball = Ball(ball_color, ball_pos, ball_vel)
        if checkBallPos(temp_ball, ball_group):  # 检查重叠
            ball_group.append(temp_ball)#放入容器内
            i += 1
            if i > mark:#数量控制
                return ball_group
'''
#将小球的create与add代码合并，故舍弃这里
# def addBall(ball_group):
#     if len(ball_group) > 12:  # 减少系统压力，过多可能会导致崩溃
#         print "小球数目过多不在提供添加"
#         return ball_group
#     i = 1
#     while True:
#         #小球初始化
#         ball_color, ball_pos, ball_vel = ballPropertyInit(i)
#         temp_ball = Ball(ball_color, ball_pos, ball_vel)
#         if checkBallPos(temp_ball, ball_group):  # 检查重叠
#             ball_group.append(temp_ball)  # 放入容器内
#             i += 1
#             if i > 1:  # 数量控制
#                 return ball_group
'''
#响应右键删除小球
def deleteBall(ball_group):
    if len(ball_group) <= 0:  # 解决删除完毕后再删除的BUG问题
        print "无可删除的小球"
        return
    ball_group.pop()

#init runenvironment
initRunEnvironment()
bg_img = loadImg("Ball_Collide/resource", "black.jpg")
bg_rect = pygame.Rect(26, 12, 770, 550)
bg_img = bg_img.subsurface(bg_rect).convert_alpha()

bg_sound = Music(load_bg_audio('Ball_collide/resource', 'bg_au.ogg'))
hit_sound = load_hit_audio('Ball_collide/resource', 'hit.ogg')
#背景音乐
bg_music_play = False  # 背景音乐播放标志
hit_music_play = False  # 撞击音乐播放标志



#字体生成
font1 = createFont(22)
#创建存放小球的容器
ball_group = []
#生成小球
createBall(ball_group)
#设置帧数
frame_time = pygame.time.Clock()

while True:

    frame_time.tick(60)#设置帧数60

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.exit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_f:    #屏幕模式切换
                full_screen = not full_screen
                screenChange(full_screen)
        if event.type == MOUSEBUTTONDOWN:
            mouse_pressed_array = pygame.mouse.get_pressed()  # 获取鼠标事件
            for index in range(len(mouse_pressed_array)):
                if mouse_pressed_array[index]:
                    if index == 0:
                        createBall(ball_group, 1)#1表示添加1个小球
                        #print "left"
                    elif index == 1:
                        #print "wheel"
                        pass
                    elif index == 2:
                        #print "right"
                        deleteBall(ball_group)

    #键盘事件捕捉及处理
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_UP] or keys[K_w]:  # 实现上和W加速度下S减速度
        for ball_vel_add in ball_group:
            ball_vel_add.velAdd()
    elif keys[K_DOWN] or keys[K_s]:
        for ball_vel_reduce in ball_group:
            ball_vel_reduce.velReduce()
    
    #绘制屏幕
    screen.blit(bg_img, (0, 0))

    for ball in ball_group:
        #绘制小球
        pygame.draw.circle(screen, ball.color, ball.pos, ball.radius, ball.width)
        #移动小球
        ball.ballMove()
    
    #碰撞的检测和处理
    if ballCollide():
        hit_music_play = play_hit_sound(hit_music_play)
        pass

    #bg_music_play = bg_sound.play_bg_sound(bg_music_play)
    bg_music_play = bg_sound.play_bg_sound(bg_music_play)

    textPrint(font1, 500, 400, str(
        "what do you want and want to be?"), (0, 120, 220))
    pygame.display.update()
