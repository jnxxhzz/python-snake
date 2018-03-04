import pygame
import sys
import time
import random
from pygame.locals import *

#颜色 屏幕大小 方块大小
huiColour = pygame.Color(220,220,220)
redColour = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
buleColour = pygame.Color(0,192,252)
screenWidth = 200
screenHeight = 200
gameWidth = 350
gameHeight = 450
point_size = 20
listsizeW = int(screenWidth / point_size)
listsizeH = int(screenHeight / point_size)
winscore = int(listsizeH * listsizeW)
UNDEFIND = 250000
SNAKE = UNDEFIND * 2

screenlines = ( (0,0), (screenWidth,0), (screenWidth,screenHeight), (0,screenHeight))

pygame.init()   
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption('snakegame')

snake_head = [60,60]
snakeSegments = [[60,60],[40,60],[20,60]]

foodPosition = [100,100]

direction = -2
changeDirection = -2
score = 0

moveup = 1
movedown = -1
moveleft = 2
moveright = -2
mov = [1,-1,2,-2]

board = [0] * (listsizeW * listsizeH + 100) 
inqueue = [0] * (listsizeW * listsizeH + 100) 
pboard = [0] * (listsizeW * listsizeH + 100) 
tmpsnake = [0] * (listsizeW * listsizeH + 100) 
tmpboard = [0] * (listsizeW * listsizeH + 100) 

ERR = -1111  #错误码



def write_word(screen, word , posx , posy ,word_size, word_type):
    scoreFont = pygame.font.Font(None,word_size)
    scoreSurf = scoreFont.render(word, True, whiteColour)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (posx,posy)
    screen.blit(scoreSurf, scoreRect)
        

def gameOver(screen):
    gameOverFont = pygame.font.Font(None,48)
    gameOverSurf = gameOverFont.render('Game Over', True, huiColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    screen.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()


def goto_where(idx , direction,steeplen):
    #rint(idx)
    if direction == moveright:
        idx[0] += int(point_size / steeplen)
    if direction == moveleft:
        idx[0] -= int(point_size / steeplen)
    if direction == moveup: 
        idx[1] -= int(point_size / steeplen)
    if direction == movedown:
        idx[1] += int(point_size / steeplen)
    return idx

def possible_go(idx):
    if (idx[0]<0):
        return False
    if (idx[0]>=screenWidth):
        return False
    if (idx[1]<0):
        return False
    if (idx[1]>=screenHeight):
        return False
    return True

#bfs找food到其他非蛇身点的最短路长度
def board_refresh(snake_head,food,snakeSegments):
    global board
    queue = []
    queue.append(food)
    inqueue = [0] * (listsizeW * listsizeH + 100) 
    pboard = [UNDEFIND] * (listsizeW * listsizeH + 100) 
    for pos in snakeSegments:
        idx = int((pos[0]/point_size) + (pos[1]/point_size)*listsizeW)
        pboard[idx] = SNAKE
    
    found = False
    idx = int((food[0]/point_size) + (food[1]/point_size)*listsizeW)
    pboard[idx] = 0

    while len(queue)!=0: 
        nidx = queue.pop(0)
        idx = int((nidx[1]/point_size)*listsizeW + (nidx[0]/point_size))
        if inqueue[idx] == 1: 
            continue
        inqueue[idx] = 1
        for i in mov:
            goidx = []
            goidx = nidx[:]
            goidx = goto_where(goidx,i,1)
            idxx = int((goidx[1]/point_size)*listsizeW + (goidx[0]/point_size))
            if possible_go(goidx) :
                if goidx == snake_head :
                    found = True
                if pboard[idxx] < SNAKE :
                    if (pboard[idxx] > pboard[idx] + 1):
                        pboard[idxx] = pboard[idx] + 1
                    if inqueue[idxx] == 0:
                        queue.append(goidx)
    #print(pboard)
    board = []
    board = pboard[:]
    return found

# 从蛇头开始，根据board中元素值，
# 从蛇头周围4个领域点中选择最短路径
def choose_shortest_safe_move(snake_head, pboard,snake):
    best_move = ERR
    min = SNAKE
    for i in mov:
        goidx = []
        goidx = snake_head[:]
        goidx = goto_where(goidx, i, 1)
        idxx = int((goidx[1]/point_size)*listsizeW + (goidx[0]/point_size))
        if possible_go(goidx) and pboard[idxx] < min and pboard[idxx] <UNDEFIND : 
            min = pboard[idxx]
            best_move = i
    return best_move

# 从蛇头开始，根据board中元素值，
# 从蛇头周围4个领域点中选择最远路径
def choose_longest_safe_move(snake_head, pboard,snake):
    best_move = ERR
    max = -1 
    for i in mov:
        goidx = []
        goidx = snake_head[:]
        goidx = goto_where(goidx, i, 1)
        idxx = int((goidx[1]/point_size)*listsizeW + (goidx[0]/point_size))
        if possible_go(goidx) and pboard[idxx]<UNDEFIND and pboard[idxx] > max: 
            max = pboard[idxx]
            best_move = i
    return best_move


def find_anyway(snake_head, pboard,snake):
    #board_refresh(snake_head,foodPosition,snake)
    #print('find_anyway')
    best_move = ERR
    min = -1
    for i in mov:
        goidx = []
        goidx = snake_head[:]
        goidx = goto_where(goidx, i, 1)
        idxx = int((goidx[1]/point_size)*listsizeW + (goidx[0]/point_size))
        if possible_go(goidx) and pboard[idxx]<UNDEFIND and pboard[idxx] > min: 
            min = pboard[idxx]
            best_move = i
    return best_move



# 虚拟运行吃到食物后，得到虚拟下蛇在board的位置
def virtual_shortest_move(snake_head):
    global board,foodPosition,snakeSegments
    tmpsnake = []
    tmpsnake = snakeSegments[:]
    new_head = snake_head[:]
    food_eated = False
    while not food_eated:
        eatfood = board_refresh(new_head,foodPosition,tmpsnake)
        tmpboard = []
        tmpboard = board[:]
        #print(tmpboard)
        movedirection = choose_shortest_safe_move(new_head, tmpboard,tmpsnake)
        #print(movedirection)
        new_head = goto_where(new_head , movedirection , 1)
        #print(movedirection)
        if new_head == foodPosition:
            food_eated = True
        else:
            tmpsnake.pop()
        tmpsnake.insert(0, list(new_head))
        
    #虚拟运行完后头和尾能否连通
    new_food = tmpsnake.pop()
    result = board_refresh(new_head,new_food,tmpsnake)
    for i in mov:
        goidx = []
        goidx = new_head[:]
        goidx = goto_where(goidx, i, 1)
        if possible_go(goidx) and goidx == tmpsnake[0] : 
            result = False 
    return result
    
def find_tail(snake_head):
    global snakeSegments,foodPosition
    print('find_tail')
    tmpsnake = []
    tmpsnake = snakeSegments[:]

    change = tmpsnake.pop()
    tmpsnake.append(foodPosition)
    touch_head = board_refresh(snake_head,change,tmpsnake) # 求得各个位置到达蛇尾的路径长度
    
    tmpboard = []
    tmpboard = board[:]
    idxx = int((change[1]/point_size)*listsizeW + (change[0]/point_size))
    
    tmpsnake.pop()
    tmpsnake.append(change)
    tmpboard[idxx] = SNAKE

    return choose_longest_safe_move(snake_head, tmpboard,tmpsnake) 



# 如果蛇与食物间有路径，则调用本函数
def find_safeway(snake_head,mainboard,snakeSegments):
    #虚拟运行
    safe_move = ERR
    #print(snakeSegments)
    if virtual_shortest_move(snake_head):
        return choose_shortest_safe_move(snake_head, mainboard,snakeSegments)
    safe_move = find_tail(snake_head)  
    return safe_move


def main():
    global foodPosition,score,direction,snake_head,snakeSegments

    screen = pygame.display.set_mode((gameWidth, gameHeight))
    pygame.display.set_caption('snakegame')
    
    #snake_head = [100,100]
    #snakeSegments = [[100,100],[80,100],[60,100]]
    #foodPosition = [300,300]
    
    snake_head = [60,60]
    snakeSegments = [[60,60],[40,60],[20,60]]

    foodPosition = [100,100]

    #print(snake_head)

    direction = -2
    changeDirection = -2
    score = 0
    #初始化  初始方向为right（-2）
    
    pygame.draw.rect(screen,huiColour,Rect(snake_head[0],snake_head[1],point_size,point_size))
    pygame.draw.rect(screen,redColour,Rect(foodPosition[0], foodPosition[1],point_size,point_size))
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
        
        caneat = board_refresh(snake_head,foodPosition,snakeSegments)

        mainboard = []
        mainboard = board[:]
        if caneat:
            direction = find_safeway(snake_head,mainboard,snakeSegments)
        else:
            direction = find_tail(snake_head)
        if direction == ERR :
            direction = find_anyway(snake_head,mainboard,snakeSegments)

        #print(snakeSegments)
        # 移动
        snake_head = goto_where(snake_head,direction,1)
        # 判断是否吃掉了食物
        #if snake_head[0] == foodPosition[0] and snake_head[1] == foodPosition[1]:
        if (snake_head==foodPosition): 
            snakeSegments.insert(0,list(snake_head))
            Height = (screenHeight-1) / point_size
            Width = (screenWidth-1) / point_size
            x = random.randrange(1,int(Height))
            y = random.randrange(1,int(Width))
            newfood = [int(x*point_size),int(y*point_size)]
            while newfood in snakeSegments:
                x = random.randrange(1,int(Height))
                y = random.randrange(1,int(Width))
                newfood = [int(x*point_size),int(y*point_size)]
            foodPosition = newfood
            score = score + 1
            #吃到食物重新生成食物
        else:
            snakeSegments.pop()
            snakeSegments.insert(0,list(snake_head))
            #删除尾巴 若吃到食物则蛇增加长度，不需要删除尾巴
    
        screen.fill(blackColour)
        for position in snakeSegments:
            pygame.draw.rect(screen,whiteColour,Rect(position[0]-3,position[1]-3,point_size-6,point_size-6))
        pygame.draw.rect(screen,redColour,Rect(foodPosition[0]-3, foodPosition[1]-3,point_size-6,point_size-6))

        #移动蛇头
        
        pygame.draw.rect(screen,huiColour,Rect(snake_head[0]-3,snake_head[1]-3,point_size-6,point_size-6))

        write_word(screen,'Score: '+str(score), 60, screenHeight + 20, 25 , None)
        #write_word(screen,'By:jnxxhzz', screenWidth - 50 , screenHeight + 50 , 25 , "my_font.ttf")
        pygame.draw.lines(screen, buleColour, True , screenlines, 1)

        pygame.display.flip()
        #print('Score:',score)
        if (score == winscore):
            gamewin(screen)
            flagg = 1
            return 

        # 判断是否死亡
        flagg = 0
        if snake_head[0] >= screenWidth or snake_head[0] < 0:
            gameOver(screen)
            flagg = 1
        if snake_head[1] >= screenHeight or snake_head[1] < 0:
            gameOver(screen)
            flagg = 1
        for snakeBody in snakeSegments[1:]:
            if snake_head[0] == snakeBody[0] and snake_head[1] == snakeBody[1]:
                gameOver(screen)
                flagg = 1
        if flagg == 1 :
            return 
        # 帧数    
        #fpsClock.tick(5)
        #time.sleep(1)

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