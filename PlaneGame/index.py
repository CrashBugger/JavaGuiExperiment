# coding:utf-8
import pygame
from pygame.locals import *
import time
import random
import sys
import os

canvas = pygame.display.set_mode((1200, 715))
# 初始化pygame环境
pygame.init()

# 创建一个长宽分别为480/650窗口
x = 80
y = 27

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

canvas.fill((255, 255, 255))

# 设置窗口标题
pygame.display.set_caption("飞机大战")

'''
#加载图片
enemy1=pygame.image.load("images/enemy1.png")
enemy2=pygame.image.load("images/enemy2.png")
enemy3=pygame.image.load("images/enemy3.png")
h=pygame.image.load("images/hero1.png")
bg=pygame.image.load("images/bg1.png")
#子弹图片
b=pygame.image.load("images/bullet1.png")
'''

# 敌飞机图片数组
e1 = []
e1.append(pygame.image.load("images/enemy1.png"))
e1.append(pygame.image.load("images/enemy1_down1.png"))
e1.append(pygame.image.load("images/enemy1_down2.png"))
e1.append(pygame.image.load("images/enemy1_down3.png"))
e1.append(pygame.image.load("images/enemy1_down4.png"))
e1.append(pygame.image.load("images/enemy1_down5.png"))
e2 = []
e2.append(pygame.image.load("images/enemy2.png"))
e2.append(pygame.image.load("images/enemy2_down1.png"))
e2.append(pygame.image.load("images/enemy2_down2.png"))
e2.append(pygame.image.load("images/enemy2_down3.png"))
e2.append(pygame.image.load("images/enemy2_down4.png"))
e2.append(pygame.image.load("images/enemy2_down5.png"))
e3 = []
e3.append(pygame.image.load("images/enemy3_1.png"))
e3.append(pygame.image.load("images/enemy3_2.png"))
e3.append(pygame.image.load("images/enemy3_down1.png"))
e3.append(pygame.image.load("images/enemy3_down2.png"))
e3.append(pygame.image.load("images/enemy3_down3.png"))
e3.append(pygame.image.load("images/enemy3_down4.png"))
e3.append(pygame.image.load("images/enemy3_down5.png"))
e3.append(pygame.image.load("images/enemy3_down6.png"))
e3.append(pygame.image.load("images/enemy3_down7.png"))
h = []
h.append(pygame.image.load("images/hero.png"))
h.append(pygame.image.load("images/hero_down1.png"))
h.append(pygame.image.load("images/hero_down2.png"))
h.append(pygame.image.load("images/hero_down3.png"))
h.append(pygame.image.load("images/hero_down4.png"))
# 背景图片
bg = pygame.image.load("images/bg4.png")
# 子弹图片
b = []
b.append(pygame.image.load("images/bullet1.png"))
# 开始游戏图片
startgame = pygame.image.load("images/startGame.png")
# logo图片
logo = pygame.image.load("images/LOGO.png")
# 暂停图片
pause = pygame.image.load("images/game_pause_nor.png")

score = pygame.image.load("images/score.png")

# 加载再来一局图片
again = pygame.image.load("images/again.png")

over = pygame.image.load("images/over.png")

bgg = pygame.image.load("images/bg235.jpg")
# 飞机的生命

E1 = 1
E2 = 3
E3 = 10

# 飞机的分数

S1 = 1
S2 = 5
S3 = 10


def handleEvent():
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        # 监听鼠标移动事件
        if event.type == pygame.MOUSEMOTION:
            # 根据鼠标的坐标修改英雄机的坐标
            # 使用get_width函数可以获取图片的宽度
            if GameVar.state == GameVar.STATES["RUNNING"]:
                GameVar.hero.x = event.pos[0] - GameVar.hero.width / 2
                GameVar.hero.y = event.pos[1] - GameVar.hero.height / 2
            # 鼠标移入移出事件切换状态
            if isMouseOut(event.pos[0], event.pos[1]):
                if GameVar.state == GameVar.STATES["RUNNING"]:
                    GameVar.state = GameVar.STATES["PAUSE"]
            if isMouseOver(event.pos[0], event.pos[1]):
                if GameVar.state == GameVar.STATES["PAUSE"]:
                    GameVar.state = GameVar.STATES["RUNNING"]

        # 点击左键切换为运行状态
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if GameVar.state == GameVar.STATES["START"]:
                GameVar.state = GameVar.STATES["RUNNING"]
        if event.type == KEYDOWN and event.key == K_r:
            if GameVar.state == GameVar.STATES["GAME_OVER"]:
                GameVar.score = 0
                GameVar.heroes = 3
                GameVar.state = GameVar.STATES["START"]
        # 这一处是判断鼠标是否点击再来一局，条件是gamestate为gameover且鼠标点下
        if event.type == MOUSEBUTTONDOWN and GameVar.state == GameVar.STATES["GAME_OVER"]:
            # 拿到矩形对象，pygame中万物皆矩形，用矩形去修改坐标，调整大小等等等等
            rect = again.get_rect()
            # 拿到鼠标坐标，注意返回的是元组
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 判断坐标是否落在矩形内
            if rect.collidepoint(mouse_x, mouse_y):
                # 开始重置gamevar属性
                GameVar.heroes = 3
                GameVar.state = GameVar.STATES["RUNNING"]
                # 判断是否要修改最高分文件，注意对文件操作权限符只能是w(写)或者（r）读其中的一个，
                with open("highest.txt", "r") as f:
                    read = int(f.read())
                f.close()
                with open("highest.txt", "w") as f:
                    if int(read) < int(GameVar.highestScore):
                        f.write(str(GameVar.highestScore))
                f.close()
                # 暂停一会让玩家来得及反应
                time.sleep(0.5)
                # 开始下一轮回合
                run()


def draw(img, x, y):
    canvas.blit(img, (x, y))


# 工具方法-判断时间间隔是否到了
def isActionTime(lastTime, interval):
    if lastTime == 0:
        return True
    currentTime = time.time()
    return currentTime - lastTime >= interval


# 工具方法-写文字方法
def renderText(text, position, view=canvas):
    # 设置字体样式和大小
    my_font = pygame.font.Font("my_font/font1.ttf", 30)
    # 渲染文字
    text = my_font.render(text, True, (255, 255, 255))
    view.blit(text, position)


# 工具方法-判断鼠标是否移出了游戏区域
def isMouseOut(x, y):
    if x >= 1190 or x <= 0 or y > 700 or y <= 0:
        return True
    else:
        return False


# 工具方法-判断鼠标是否移入了游戏区域
def isMouseOver(x, y):
    if x > 0 and x < 1150 and y > 1 and y < 648:
        return True
    else:
        return False


# 定义Sky类
class Sky(object):
    def __init__(self):
        self.width = 480
        self.height = 680
        self.img = bgg
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = -self.height

    def paint(self, view):
        # view.blit(bgg,(0,0))
        draw(self.img, self.x1, self.y1)
        draw(self.img, self.x2, self.y2)

    def step(self):
        self.y1 = self.y1 + 1
        self.y2 = self.y2 + 1
        if self.y1 > self.height:
            self.y1 = -self.height
        if self.y2 > self.height:
            self.y2 = -self.height


# 定义父类FlyingObject
class FlyingObject(object):
    def __init__(self, x, y, width, height, life, frames, baseFrameCount):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.life = life
        # self.img = img
        # 敌飞机移动的时间间隔
        self.lastTime = 0
        self.interval = 0.01
        # 添加掉落属性和删除属性
        self.down = False
        self.canDelete = False
        # 实现动画所需属性
        self.frames = frames
        self.frameIndex = 0
        self.img = self.frames[self.frameIndex]
        self.frameCount = baseFrameCount

    def paint(self, view):

        draw(self.img, self.x, self.y)

    def step(self):
        # 判断是否到了移动的时间间隔
        if not isActionTime(self.lastTime, self.interval):
            return
        self.lastTime = time.time()
        # 控制移动速度
        self.y = self.y + 5

    # 碰撞检测方法
    def hit(self, component):
        c = component
        return c.x > self.x - c.width and c.x < self.x + self.width and c.y > self.y - c.height and c.y < self.y + self.height

    # 处理碰撞发生后要做的事
    def bang(self):
        self.life -= 1
        if self.life == 0:
            # 生命值为0时将down置为True
            self.down = True
            # 将frameIndex切换为销毁动画的第一张
            self.frameIndex = self.frameCount

            # 因为现在没有销毁动画，所以死亡后立即删除
            # if self.down == True:
            # self.canDelete = True

            if hasattr(self, "score"):
                GameVar.score += self.score

    # 越界处理
    def outOfBounds(self):
        return self.y > 650

    # 实现动画
    def animation(self):
        if self.down:
            # 销毁动画播放完后将canDelete置为True
            if self.frameIndex == len(self.frames):
                self.canDelete = True
            else:
                self.img = self.frames[self.frameIndex]
                self.frameIndex += 1
        else:
            self.img = self.frames[self.frameIndex % self.frameCount]
            self.frameIndex += 1


# 定义Enemy类
class Enemy(FlyingObject):
    def __init__(self, x, y, width, height, type, life, score, frames, baseFrameCount):
        FlyingObject.__init__(self, x, y, width, height, life, frames, baseFrameCount)
        self.x = random.randint(0, 1300 - self.width)
        self.y = -self.height
        self.type = type
        self.score = score


# 定义Hero类
class Hero(FlyingObject):
    def __init__(self, x, y, width, height, life, frames, baseFrameCount):
        FlyingObject.__init__(self, x, y, width, height, life, frames, baseFrameCount)
        self.width = 60
        self.height = 75
        self.x = 450 + 480 / 2 - self.width / 2
        self.y = 650 - self.height - 30
        # 射击时间间隔
        self.shootLastTime = 0
        self.shootInterval = 0.1

    def paint(self, view):
        draw(self.img, self.x, self.y)

    def shoot(self):
        if not isActionTime(self.shootLastTime, self.shootInterval):
            return
        self.shootLastTime = time.time()
        GameVar.bullets.append(Bullet(self.x + self.width / 2, self.y, 9, 21, 1, b, 1))


# 定义Bullet类
class Bullet(FlyingObject):
    def __init__(self, x, y, width, height, life, frames, baseFrameCount):
        FlyingObject.__init__(self, x, y, width, height, life, frames, baseFrameCount)

    # 重写step方法
    def step(self):
        self.y = self.y - 10

    # 重写判断是否越界的方法
    def outOfBounds(self):
        return self.y < -self.height


def componentEnter():
    # 判断是否到了产生敌飞机的时间
    if not isActionTime(GameVar.lastTime, GameVar.interval):
        return
    GameVar.lastTime = time.time()

    # 随机生成坐标
    x = random.randint(0, 1300 - 57)
    x1 = random.randint(0, 1300 - 50)
    x2 = random.randint(0, 1300 - 169)
    # 根据随机整数的值生成不同的敌飞机
    n = random.randint(0, 9)
    if n <= 7:
        # 因为列表初始值为空，所以这里可以使用append或insert进行添加元素，append会将新增的追加到末尾，但insert会将新增的插入到指定位置
        GameVar.enemies.append \
            (Enemy(x, 0, 57, 45, 1, E1, S1, e1, 1))
    elif n == 8:
        GameVar.enemies.append \
            (Enemy(x1, 0, 50, 68, 2, E2, S2, e2, 1))
    elif n == 9:
        # 将打飞机放在列表中索引为0的位置
        if len(GameVar.enemies) == 0 or GameVar.enemies[0].type != 3:
            GameVar.enemies.insert \
                (0, Enemy(x2, 0, 169, 258, 3, E3, S3, e3, 2))


# 画组件方法
def paintComponent(view):
    # 判断是否到了飞行物重绘的时间
    if not isActionTime(GameVar.paintLastTime, GameVar.paintInterval):
        return
    GameVar.paintLastTime = time.time()

    # 调用sky对象的paint方法
    GameVar.sky.paint(view)
    # 画敌飞机并实现敌飞机移动
    for enemy in GameVar.enemies:
        enemy.paint(view)
    # 画英雄机
    GameVar.hero.paint(view)
    # 画子弹
    for bullet in GameVar.bullets:
        bullet.paint(view)
    # 写分数和生命值
    draw(score, 720 + 210, 10)
    renderText(str(GameVar.score), (780 + 305, 25))
    renderText(str(GameVar.heroes), (780 + 305, 58))

    # 因为需要时刻显示最高分变化，所以将他加入在paintComponent方法中，这样可以每次while循环都能调用到
    # 这一处是时刻显示最高分的代码，如果当前分数大于最高分，则覆盖gamevar.highscore的值
    if GameVar.score > GameVar.highestScore:
        GameVar.highestScore = GameVar.score
    renderText("HighestScore", (780 + 100, 650))
    # 注意renderText的参数是str类型
    renderText(str(GameVar.highestScore), ((780 + 350, 650)))


# 组件移动方法
def componentStep():
    # 调用sky对象的step方法
    GameVar.sky.step()
    for enemy in GameVar.enemies:
        enemy.step()
    # 子弹移动
    for bullet in GameVar.bullets:
        bullet.step()


# 检测组件碰撞
def checkHit():
    # 判断敌飞机是否和英雄机相撞
    for enemy in GameVar.enemies:
        # 如果当前飞机已经死亡则换下一架飞机
        if enemy.down == True:
            continue

        if GameVar.hero.hit(enemy):
            enemy.bang()
            GameVar.hero.bang()
        for bullet in GameVar.bullets:
            # 如果当前子弹是无效的子弹则换下一颗子弹
            if bullet.down == True:
                continue

            if enemy.hit(bullet):
                enemy.bang()
                bullet.bang()


# 删除无效组件
def deleteComponent():
    # 删除无效的敌飞机
    for i in range(len(GameVar.enemies) - 1, -1, -1):
        x = GameVar.enemies[i]
        if x.canDelete or x.outOfBounds():
            GameVar.enemies.remove(x)
    # 删除无效子弹
    for i in range(len(GameVar.bullets) - 1, -1, -1):
        x = GameVar.bullets[i]
        if x.canDelete or x.outOfBounds():
            GameVar.bullets.remove(x)
    # 删除无效的英雄机
    if GameVar.hero.canDelete == True:
        GameVar.heroes -= 1
        if GameVar.heroes == 0:
            # renderText("游戏结束",(100, 200))
            # print("游戏结束")
            GameVar.state = GameVar.STATES["GAME_OVER"]
        else:
            GameVar.hero = Hero(0, 0, 60, 75, 1, h, 1)


# 组件的动画
def componentAnimation():
    # 敌飞机播放动画
    for enemy in GameVar.enemies:
        enemy.animation()
    # 子弹播放动画
    for bullet in GameVar.bullets:
        bullet.animation()
    # 英雄机播放动画
    GameVar.hero.animation()


# 使用类属性存储游戏中的变量，以减少全局变量的数量
class GameVar(object):
    # 每次初始化该类时（游戏启动时才会初始化，并且仅初始化一次），读取highest文件最高分（所以每次启动前需要
    # 将最高分txt文件写为0，或者给定的值），注意关闭文件流，否则会发生多个流读写一个文件，windows下容易报奇怪的错
    highestScore = 0
    with open("highest.txt", "r", encoding="utf-8") as f:
        highestScore = int(f.read())
        f.close()
    # --------------------------------------------------------
    sky = None
    # 英雄机对象
    hero = None
    enemies = []
    # 存放子弹的列表
    bullets = []

    # 产生敌飞机的时间间隔
    lastTime = 0
    interval = 0.5  # 单位为秒
    # 重绘飞行物的时间间隔
    paintLastTime = 0
    paintInterval = 0.01
    # 分数和生命值
    score = 0

    # heroes = int(h)
    # 控制飞机有几条性命
    heroes = 3
    # 控制游戏状态
    STATES = {"START": 1, "RUNNING": 2, "PAUSE": 3, "GAME_OVER": 4}
    state = STATES["START"]


# 游戏状态控制
def contralState():
    if GameVar.state == GameVar.STATES["START"]:
        GameVar.sky.paint(canvas)
        GameVar.sky.step()
        draw(logo, 200, 200)
        draw(startgame, 460, 450)
    elif GameVar.state == GameVar.STATES["RUNNING"]:
        componentEnter()
        # 画组件
        paintComponent(canvas)
        # 组件移动
        componentStep()
        # 播放组件动画
        componentAnimation()
        # 英雄机发射子弹
        GameVar.hero.shoot()
        # 碰撞检测
        checkHit()
        # 删除无效组件
        deleteComponent()
    elif GameVar.state == GameVar.STATES["PAUSE"]:
        paintComponent(canvas)
        GameVar.sky.step()
        draw(pause, 500, 250)
    elif GameVar.state == GameVar.STATES["GAME_OVER"]:
        paintComponent(canvas)
        GameVar.sky.step()
        draw(over, 230, 250)
        # 这一处是显示得到最高分时的话，需要将其加到gamevar.state的属性为gameover是的代码下
        # 判断：当前得分与最高分相同时（当前得分超过最高分的一刻，最高分与当前得分同步变化），输出此句话
        # renderText()方法封装的是显示文字方法，第一个参数是显示文本，第二个是坐标（x,y）
        if GameVar.highestScore == GameVar.score:
            with open("highest.txt", "w") as f:
                f.write(str(GameVar.highestScore))
            renderText("%s! You got the highest score!" % str(GameVar.highestScore), (0, 60))
        # 显示再来一局
        draw(again, 0, 0)


# 将原本的执行的关键代码统一封装在run()方法中,这样再来一次时可以直接调用run()方法从而开始
# 再一次游戏,但再来一局时需要对GameVar类中的heroes参数进行初始化，防止生命值出现负数从而游戏无法停止
# run方法中的代码就是原本的代码，无需过多讲解
def run():
    # 创建sky对象
    GameVar.sky = Sky()
    # 创建英雄机对象
    GameVar.hero = Hero(0, 0, 60, 75, 1, h, 1)
    while True:
        # 游戏状态控制
        contralState()
        # 更新屏幕内容
        pygame.display.update()
        # 监听有没有按下退出按钮
        handleEvent()
        # 等待0.01秒后再进行下一次循环
        pygame.time.delay(15)


if __name__ == '__main__':
    # 新加功能的注释的行号
    # 79,128，518，510,380,449,128
    run()
