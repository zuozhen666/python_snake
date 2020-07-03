import pygame
import sys
import random
import time
from pygame.locals import *

#颜色变量
DimGray = (105,105,105)
SpringGreen = (0,255,127)
SkyBlue = (135,206,235)
FloralWhite = (255,250,240)
DarkOrange = (255,140,0)
DarkOrchid = (153,50,204)
white = (255,255,255)
red = (255,0,0)
Green = (0, 255, 0)

#开始界面   
def start_controller(screen):
    #游戏名称
    start_font = pygame.font.SysFont("MicrosoftYaHei", 100)     #字体格式
    start_colour = start_font.render('Snake', True, red)        #字体颜色
    start_location = start_colour.get_rect()                    #位置
    start_location.midtop = (400,150)               
    screen.blit(start_colour,start_location)                    #绑定到句柄
    #制作人
    producer_font = pygame.font.SysFont("MicrosoftYaHei", 66)
    producer_colour = producer_font.render('Producer: zuozhen666', True, Green)
    producer_location = producer_colour.get_rect()
    producer_location.midtop = (400,240)
    screen.blit(producer_colour,producer_location)
    #操作提示
    prompt_font = pygame.font.SysFont("MicrosoftYaHei", 66)
    prompt_colour = prompt_font.render('Press any key to continue', True, white)
    prompt_location = prompt_colour.get_rect()
    prompt_location.midtop = (400,300)
    screen.blit(prompt_colour,prompt_location)

    pygame.display.flip()

    while True:                                 #键盘监听事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):     #终止程序
                    pygame.quit()
                    sys.exit()
                else:
                    return                      #结束此函数, 开始游戏

#游戏结束
def GameOver(screen):
    pygame.mixer.music.load("die.mp3")
    pygame.mixer.music.play(1)                  #死亡音效播放一次
    #结束提示
    GameOver_font = pygame.font.SysFont("MicrosoftYaHei", 100)          
    GameOver_colour = GameOver_font.render('Game Over',True,SkyBlue)    
    GameOver_location = GameOver_colour.get_rect()                      
    GameOver_location.midtop = (400,250)
    screen.blit(GameOver_colour,GameOver_location)                      
    #操作提示
    restart_font = pygame.font.SysFont("MicrosoftYaHei", 38)
    restart_colour = restart_font.render('Press the ‘A’ key to restart the game or press the ‘B’ key to exit.', True, FloralWhite)
    restart_location = restart_colour.get_rect()
    restart_location.midtop = (400,320)
    screen.blit(restart_colour,restart_location)

    pygame.display.flip()
    
    while True:                             #键盘监听事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:     #重新开始
                if (event.key == K_a):
                    main()
                elif (event.key == K_b):    #退出程序
                    pygame.quit()
                    sys.exit()

#主函数
def main(): 
    pygame.init()                                       #初始化pygame
    pygame.time.Clock()
    ftpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((800,600))         #创建窗口
    pygame.display.set_caption('snake')                 #窗口标题
    start_controller(screen)                            #调用开始界面
    
    #背景音
    pygame.mixer.init()                                 #混音器初始化
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play(-1)                         #循环播放
    
    snakeposition = [100,100]                           #贪吃蛇初始位置
    snakelength = [[100,100],[80,100],[60,100]]         #初始长度
    square_purpose = [300,300]                          #果实初始位置
    square_position = 1                                 #标记变量，果实是否被吃
    derection = "right"                                 #初始方向
    change_derection = derection
    
    
    #游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:                      #退出程序
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:                 #判断键盘事件
                if event.key == K_RIGHT:
                    change_derection = "right"
                if event.key == K_LEFT:
                    change_derection = "left"
                if event.key == K_UP:
                    change_derection = "up"
                if event.key == K_DOWN:
                    change_derection = "down"
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                    
        #判断移动方向是否符合要求
        if change_derection =='left' and not derection =='right':
            derection = change_derection
        if change_derection =='right' and not derection =='left':
            derection = change_derection
        if change_derection == 'up' and not derection =='down':
            derection = change_derection
        if change_derection == 'down' and not derection == 'up':
            derection = change_derection
            
        #根据方向改变坐标
        if derection == 'left':
            snakeposition[0] -= 20
        if derection == 'right':
            snakeposition[0] += 20
        if derection == 'up':
            snakeposition[1] -= 20
        if derection == 'down':
            snakeposition[1] += 20
            
        #增加蛇的长度
        snakelength.insert(0,list(snakeposition))
        
        #判断是否吃掉目标方块
        if snakeposition[0] == square_purpose[0] and snakeposition[1] == square_purpose[1]:
            pygame.mixer.music.load("eat.mp3")
            pygame.mixer.music.play(1)                 #吃掉果实音效播放一次
            square_position = 0                        #标记置为0
        else:
            snakelength.pop()
            
        #重新生成目标方块
        if square_position == 0:
            x = random.randrange(1,40)                 #在界面范围内生产随机数
            y = random.randrange(1,30)
            square_purpose = [int(x*20), int(y*20)]    #转化为坐标
            square_position = 1                        #标记置为1
            
        #绘制pygame显示层
        screen.fill(DimGray)
        
        #绘制蛇身和果实
        for position in snakelength:
            pygame.draw.rect(screen,SpringGreen,Rect(position[0], position[1],20,20))
            pygame.draw.rect(screen,red,Rect(square_purpose[0], square_purpose[1],20,20))
        
        #分数提示
        score = (len(snakelength) - 3)
        score_font = pygame.font.SysFont("MicrosoftYaHei", 36)
        score_colour = score_font.render('score: %s' % score, True, DarkOrange)
        score_location = score_colour.get_rect()
        score_location.midtop = (700,10)
        screen.blit(score_colour, score_location)
        
        #判断是否死亡
        if snakeposition[0] < 0 or snakeposition[0] > 780:                              #判断是否到达边界
            GameOver(screen)
        if snakeposition[1] < 0 or snakeposition[1] > 580:
            GameOver(screen)
        for snakebody in snakelength[1:]:                                               #判断是否吃到蛇身                                               
            if snakeposition[0] == snakebody[0] and snakeposition[1] == snakebody[1]:
                GameOver(screen)
                
        #游戏速度设置
        i = int(score / 5) + 5  #基础速度为5，每得5分速度提升1
        ftpsClock.tick(i)
        
        #游戏速度提示
        speed_font = pygame.font.SysFont("MicrosoftYaHei", 36)
        speed_colour = speed_font.render('speed: %s' % i, True, DarkOrange)
        speed_location = speed_colour.get_rect()
        speed_location.midtop = (100, 10)
        screen.blit(speed_colour, speed_location)
        
        pygame.display.flip()   #刷新pygame显示界面
 
if __name__ == "__main__":
    main()

 

 

 

 

 

 

 

 
