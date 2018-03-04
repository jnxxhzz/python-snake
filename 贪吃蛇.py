import pygame
import sys
import time
import random
from pygame.locals import *

#颜色 屏幕大小 方块大小
redColour = pygame.Color(220,220,220)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
buleColour = pygame.Color(0,192,252)
screenWidth = 500
screenHeight = 500
gameWidth = 550
gameHeight = 650
point_size = 20
screenlines = ( (0,0), (screenWidth,0), (screenWidth,screenHeight), (0,screenHeight))


def write_word(screen, word , posx , posy ,word_size, word_type):
    scoreFont = pygame.font.Font(None,word_size)
    scoreSurf = scoreFont.render(word, True, whiteColour)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (posx,posy)
    screen.blit(scoreSurf, scoreRect)
        

def gameOver(screen):
    gameOverFont = pygame.font.Font(None,48)
    gameOverSurf = gameOverFont.render('Game Over', True, redColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    screen.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()

def judge_food(newfood , snakeSegments):
    for pos in snakeSegments:
        if (newfood == pos):
            return True
    return False

def main():

    pygame.init()
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((gameWidth, gameHeight))
    pygame.display.set_caption('snakegame')
    snake_head = [100,100]
    snakeSegments = [[100,100],[80,100],[60,100]]
    
    foodPosition = [300,300]
    foodSpawned = 1
    
    moveup = 1
    movedown = -1
    moveleft = 2
    moveright = -2

    direction = -2
    changeDirection = -2
    score = 0
    #初始化  初始方向为right（-2）
    
    pygame.draw.rect(screen,redColour,Rect(snake_head[0],snake_head[1],point_size,point_size))
    pygame.draw.rect(screen,whiteColour,Rect(foodPosition[0], foodPosition[1],point_size,point_size))
    write_word(screen ,"Please press Space key to start the game" , int(screenWidth / 2), int(screenHeight / 2),35,None )
    write_word(screen,'Score: '+str(score), 60, screenHeight + 20, 25 , None)   
    write_word(screen,'By:jnxxhzz', screenWidth - 50 , screenHeight + 50 , 25 , "my_font.ttf")
    pygame.draw.lines(screen, buleColour, True , screenlines, 1)
    pygame.display.flip()
    
    
    gamestart = 1
    while gamestart == 1 :
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if (event.key == K_SPACE):
                    gamestart = 0

    while True:
        #检测键盘输入
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == K_RIGHT :
                    changeDirection = moveright
                if event.key == K_LEFT :
                    changeDirection = moveleft
                if event.key == K_UP :
                    changeDirection = moveup
                if event.key == K_DOWN :
                    changeDirection = movedown
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

        #反方向键入不进行步骤
        if (changeDirection+direction) != 0:
            direction = changeDirection
        
        # 移动
        if direction == moveright:
            snake_head[0] += point_size
        if direction == moveleft:
            snake_head[0] -= point_size
        if direction == moveup:
            snake_head[1] -= point_size
        if direction == movedown:
            snake_head[1] += point_size
        
        # 判断是否吃掉了食物
        if snake_head[0] == foodPosition[0] and snake_head[1] == foodPosition[1]:
            Height = (screenHeight-1) / point_size
            Width = (screenWidth-1) / point_size
            x = random.randrange(1,int(Height))
            y = random.randrange(1,int(Width))
            newfood = [int(x*point_size),int(y*point_size)]
            while judge_food(newfood,snakeSegments):
                x = random.randrange(1,int(Height))
                y = random.randrange(1,int(Width))
                newfood = [int(x*point_size),int(y*point_size)]
            foodPosition = newfood
            score = score + 1
            #吃到食物重新生成食物
        else:
            snakeSegments.pop()
            #删除尾巴 若吃到食物则蛇增加长度，不需要删除尾巴
    
        screen.fill(blackColour)
        for position in snakeSegments:
            pygame.draw.rect(screen,whiteColour,Rect(position[0],position[1],point_size,point_size))
        pygame.draw.rect(screen,whiteColour,Rect(foodPosition[0], foodPosition[1],point_size,point_size))

        #移动蛇头
        snakeSegments.insert(0,list(snake_head))
        pygame.draw.rect(screen,redColour,Rect(snake_head[0],snake_head[1],point_size,point_size))

        write_word(screen,'Score: '+str(score), 60, screenHeight + 20, 25 , None)
        write_word(screen,'By:jnxxhzz', screenWidth - 50 , screenHeight + 50 , 25 , "my_font.ttf")
        pygame.draw.lines(screen, buleColour, True , screenlines, 1)

        pygame.display.flip()
        
        # 判断是否死亡
        flagg = 0
        if snake_head[0] >= screenWidth or snake_head[0] <= 0:
            gameOver(screen)
            flagg = 1
        if snake_head[1] >= screenHeight or snake_head[1] <= 0:
            gameOver(screen)
            flagg = 1
        for snakeBody in snakeSegments[1:]:
            if snake_head[0] == snakeBody[0] and snake_head[1] == snakeBody[1]:
                gameOver(screen)
                flagg = 1
        if flagg == 1 :
            return 
        # 帧数    
        fpsClock.tick(10)

if __name__ == "__main__":
    flag = 1
    while flag:
        main()
        flag = 0
        while flag == 0:  
            event = pygame.event.poll()  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                exit(0)  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_r:  
                    flag = 1
                if event.key == pygame.K_n or event.key == pygame.K_ESCAPE:  
                    pygame.quit()
                    sys.exit() 
                    exit(0) 
        pygame.display.update()  