import pygame
import random
from os import (path, listdir)

x = 5
y = 260
width = 112
height = 80
speed = 10
isJump = False
CountJump = 10
FPS = 30
displayDPI = 600
distance = 0

left = False
right = True
animCount = 0
animBackground = 0

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)

clock = pygame.time.Clock()

pygame.init()

pygame.mixer.music.load('music/test'+str(random.randrange(6))+'.ogg')
pygame.mixer.music.play(-1)

FONT_NAME = 'Eskal.ttf'
font_dir = path.join(path.dirname(__file__), 'font')

def printText(win,message, x, y,size = 36, color = RED):
    font = pygame.font.Font('font/Italic.otf', size)
    #font = pygame.font.SysFont('arial', 36)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect()
    win.blit(text_surface, (x,y)) 
    

img_left = path.join(path.dirname(__file__), 'image/left')
img_right = path.join(path.dirname(__file__), 'image/right')
img_background = path.join(path.dirname(__file__), 'image/background')
img_crown = pygame.image.load('image/crown.png')
img_crown = pygame.transform.scale(img_crown, (20, 20))
img_let = pygame.image.load('image/let.png')
img_let = pygame.transform.scale(img_let, (10, 60))
img_DEMO = pygame.image.load('image/Demo.png')

win = pygame.display.set_mode((displayDPI,displayDPI))

pygame.display.set_caption("Horse")

spriteLeft = []
spriteRight = []
spriteBackground = []

spriteLeft = [pygame.image.load(path.join(img_left, img)) for img in listdir(img_left)]
spriteLeft = list(map(lambda x: pygame.transform.scale(x, (width, height)), spriteLeft))

spriteRight = [pygame.image.load(path.join(img_right, img)) for img in listdir(img_right)]
spriteRight = list(map(lambda x: pygame.transform.scale(x, (width, height)), spriteRight))

spriteBackground = [pygame.image.load(path.join(img_background, img)) for img in listdir(img_background)]


 

lineList = []
lineList.append(20)
for i in range(1,7):
    lineList.append(lineList[i-1] + height)

y = lineList[-1]


class let():
    height = 40
    width = 5
    def __init__ (self,x,y):
        self.x = x
        self.y = y

lets = []

for l in range(100):
    lets.append(let(random.randrange(displayDPI,20000),lineList[random.randrange(7)]))


class horse():
    animCount = 0
    health = 100
    height = height
    width = width
    isJump = False
    countJump = 10
    distance = 0
    speed = 0
    pleyerDistance = 0
    timeSpeed = 0
    def __init__(self,y):
        
        self.y = y

    def cinPleyerDistance(self,PleyerDistance):
        self.pleyerDistance = PleyerDistance

    def printHealth(self,win):
        printText(win,str(self.health),self.distance - self.pleyerDistance + self.width/2 ,self.y+self.health/3 - 5, 12 , RED)
    def Jump(self):
        if self.countJump >= -10:
            if self.countJump > 0  :
                self.y -= (self.countJump **2) / 8
            else:
                self.y += (self.countJump **2) / 8
            self.countJump -= 1
            
        else:
            self.isJump = False
            self.countJump = 10
    def damage(self):
        self.health -= 10

    def changeLine(self):
        if self.y > lineList[0] and random.randrange(2) == 1:
                self.y -= self.height
        elif self.y < lineList[-1]:
                self.y += self.height

    def changeSpeed(self):
        self.timeSpeed += 1
        if self.timeSpeed // FPS:
            self.timeSpeed = 0
            self.speed = random.randrange(8,12)

    def update(self):
        self.changeSpeed()

        
        self.distance += self.speed 

        if self.isJump == True:
            self.Jump()

        if random.randrange(200) == 10:
            self.changeLine()

        for l in lets:
            if self.distance + 150 > l.x and self.distance + 10 < l.x + l.width and self.isJump == False and self.y == l.y:
                if random.randrange(3) == 2:
                    del lets[lets.index(l)]
                    self.damage()
                else:
                    self.isJump = True
    def __del__(self):
        print("delite")
      
    def animPrint(self):
        if self.animCount  >= FPS:
            self.animCount = 0
        else:
            win.blit(spriteRight[self.animCount//10],(self.distance - self.pleyerDistance ,self.y))
            self.animCount+=1
       



class Player(horse):
    x = x
    countChangeLine = 0
    Left = left
    Right = right
    changeLine = False
    animBackground = animBackground

    def __init__(self,y):
        self.speed = speed
        self.y = y

    def printHealth(self,win):
        printText(win,str(self.health),self.x +self.width/2 ,self.y+  self.health/3 - 5, 12 , BLUE)

    def playerShow(self):


            if self.animCount  >= FPS:
                self.animCount = 0
            if self.left:
                win.blit(spriteLeft[self.animCount//10],(self.x,self.y))
                win.blit(img_crown,(self.x+20,self.y-5))
                self.animCount+=1
            elif self.right:
                win.blit(spriteBackground[self.animBackground//4],(0,0))
                win.blit(spriteRight[self.animCount//10],(self.x,self.y))
                win.blit(img_crown,(self.x+self.width-40,self.y-5))
                self.animCount+=1
                if self.x > displayDPI/2-self.width:
                    self.animBackground+=1
                if self.animBackground >= FPS:
                    self.animBackground = 0

            else:
                win.blit(spriteRight[0],(self.x,self.y))
                win.blit(img_crown,(self.x+self.width-40,self.y-5))
        


    def ChangeLines(self):
        if self.changeLine == True:
            self.countChangeLine = self.countChangeLine+1
        if self.countChangeLine == FPS/5:
            self.countChangeLine = 0
            self.changeLine = False

    def key(self):

        self.changeSpeed()

        keys = pygame.key.get_pressed()
        if keys [pygame.K_a] and self.x > 5:
            self.x -= self.speed
            self.distance -= self.speed
            self.left = True
            self.right = False

        elif keys [pygame.K_d]   :
            if self.x < displayDPI/2-width:
                self.x += self.speed 
            self.distance += self.speed 
            self.left = False
            self.right = True

        else:
            self.left = False
            self.right = False
            self.animCount = 0

        if not (self.isJump):
            if keys [pygame.K_w] and self.y > lineList[0] and self.changeLine == False:
                self.y -= self.height
                self.changeLine = True
                
            elif keys [pygame.K_s] and self.y < lineList[-1] and self.changeLine == False:
                self.y += self.height
                self.changeLine = True

            elif keys [pygame.K_SPACE]:
                self.isJump = True
        else:
            self.Jump()
        

        for l in lets:
            if self.distance + 300 >= l.x and self.distance + 250  <= l.x + l.width and self.isJump == False and self.y == l.y:
                    del lets[lets.index(l)]
                    self.damage()
                    print("pregrada")

        


players = Player(lineList[-1])



horses = []

for h in range(6):
    horses.append(horse(lineList[h]))


def printWindow(maxDistance):
    global animCount
    global animBackground
    win.blit(spriteBackground[animBackground//5],(0,0))
    
    

    players.playerShow()
    players.printHealth(win)
    
    printText(win,"Max = " + str(maxDistance),20,15,20,RED)
    printText(win,"You = " + str(players.distance + players.width),130,15,20,RED)
    printText(win,"Distance = " + str(20000),240,15,20,RED)

    for l in lets:
        if l.x < players.distance + displayDPI and l.x > players.distance - players.x:
            win.blit(img_let,(l.x - players.distance ,l.y+20))
    for h in horses:

        if h.distance < players.distance + displayDPI and h.distance > players.distance - players.x:
            h.animPrint()
            h.printHealth(win)
    if players.distance > 10000 and players.distance <10020:

        win.blit(img_DEMO,(0,0))
        players.distance += 20
        pygame.display.update() 
        pygame.time.delay(FPS*10)
        flag = True
        while flag:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    flag = False
            keys = pygame.key.get_pressed()
            if  keys [pygame.K_SPACE]:
                flag = False

    pygame.display.update()  


run = True
countChangeLine = 0
changeLine = False
i = 0
while run:
    
    maxDistance = 0
    #print(distance)
    clock.tick(FPS)
    #pygame.time.delay(FPS*2)
    
    players.ChangeLines()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False

    i += 1
    if i == 30:
        i=0


    players.key()
    

    for h in horses:
       h.cinPleyerDistance(players.distance)
       h.update()
       if h.health <= 0:
           print("dead")
           del horses[horses.index(h)]

       if maxDistance < h.distance:
           maxDistance = h.distance
       if maxDistance < players.distance+players.width:
           maxDistance = players.distance
    printWindow(maxDistance)
    for h1 in horses:
        for h2 in horses:
            if h1 != h2 and h1.y == h2.y and h1.isJump==False and h2.isJump == False:
                if h1.distance + h1.width >= h2.distance and h1.distance + h1.width <= players.distance + players.width:
                    h1.damage()
                    h2.damage()
                    h1.changeLine()
                    h2.changeLine()
                    h1.distance -= random.randrange(10,20)
                    h2.distance -= random.randrange(10,20)

                    print("odnakovi")
    for h in horses:
            if  h.y == players.y and h.isJump==False and players.isJump == False:
                if h.distance + h.width  >= players.distance + 300   and h.distance + h.width  <= players.distance + players.width + 300  :
                    h.damage()
                    players.damage()
                    h.changeLine()
                    #players.changeLine()
                    h.distance -= random.randrange(10,20)
                    players.distance -= random.randrange(10,20)

                    print("odnakovi")
    
    if players.distance >= 20000:
        print("WIN")
        printText(win,"You WIN " ,displayDPI/2,displayDPI/2,50,BLUE)

        break
    if players.health <= 0 or maxDistance > 20000:
        print("You lose")
        printText(win,"You lose" ,displayDPI/2,displayDPI/2,50,BLUE)

        break
pygame.display.update()  
pygame.time.delay(FPS*100)   
pygame.quit()