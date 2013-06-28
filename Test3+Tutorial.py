import random, pygame, sys, time, math
from pygame.locals import *

FPS = 60
score = 0
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GRAY =  (128, 128, 128)
PURPLE = ( 128, 0, 128)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((700, 600))
    pygame.display.set_caption('Learn Japanese!')
    runGame(1, True)
    while True:
        runGame(random.randrange(1,10), False)

def displayText(x,y,text):
    fontObj = pygame.font.Font('freesansbold.ttf', 25)
    textSurfaceObj = fontObj.render(text, True, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

class Background(object):
    def __init__(self, num):
        self.grid_img = 'hi'
        self.display_grid = False
        self.fontobj=pygame.font.Font('freesansbold.ttf', 30)
        self.textSurfaceObject=self.fontobj.render("This next character is", True, BLACK)
        self.fontrect=self.textSurfaceObject.get_rect()
        self.fontrect.center=(300,220)
        self.textSurfaceObject2=self.fontobj.render(str(num), True, BLACK)
        self.fontrect2=self.textSurfaceObject2.get_rect()
        self.fontrect2.center=(300,260)

    def draw(self):
        if self.display_grid:
            pygame.draw.rect(DISPLAYSURF, WHITE, (0, 0, 600, 600))
        else:
            pygame.draw.rect(DISPLAYSURF, WHITE, (0, 0, 600, 600))
            DISPLAYSURF.blit(self.textSurfaceObject,self.fontrect)
            DISPLAYSURF.blit(self.textSurfaceObject2,self.fontrect2)

    def check(self,scoring):
        if scoring:
            pygame.draw.rect(DISPLAYSURF, GREEN, (600, 0, 100, 600))
        else:
            pygame.draw.rect(DISPLAYSURF, RED, (600, 0, 100, 600))

    def switch_mode(self):
        self.display_grid = True

def curve(points, t):
    if len(points) != 1:
        copy1 = points[0:-1]
        copy2 = points[1::]
        return (1-t)*curve(copy1,t) + t*curve(copy2, t)
    else:
        return points[0]

class HitCirc(object):
    def __init__(self, stroke, active, mult): #stroke object is list of coordinates for bezier curve
        self.radius = 30
        self.stroke_x = list()
        self.stroke_y = list()
        for thing in stroke:
            hold = thing.split(',')
            self.stroke_x.append(int(hold[0]))
            self.stroke_y.append(int(hold[1]))
        self.xcoord = 109
        self.ycoord = 299
        self.t = 0
        self.active = active
        self.mult = mult

    def update(self):
        self.xcoord = curve(self.stroke_x, self.t)
        self.ycoord = curve(self.stroke_y, self.t)
        self.t += 0.005*self.mult
        if self.t >= 1:
            self.active = False

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, PURPLE, (int(self.xcoord), int(self.ycoord)), self.radius, 0)

def runGame(choice, is_tutorial):
    ready = False
    accuracy = 0
    num = 0
    count = 0
    mult = 1
    line = ' '
    Circ = HitCirc(['0,0'], False, 1)
    #CircList = list()
    BlitList = list()
    
    character = 'number' + '_' + str(choice)
    Backgrd = Background(choice)
    
    if not is_tutorial:
        while not ready and True:
            Backgrd.draw()
            pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                ready = True
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    else:
        Backgrd.switch_mode()
        ready = True
        slide = 0
        while slide < 5:
            Backgrd.draw()
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    slide+=1
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if(slide==0):
                displayText(300,160,"Welcome to the Tutorial!")
                displayText(300,210,"Click the mouse when you are ready to proceed") 
            elif(slide==1):
                displayText(300,160,"The purpose of this game is to teach you")
                displayText(300,210,"the basics of writing in Japanese")
            elif(slide==2):
                pic=pygame.image.load(character + '_1.png')
                pic.set_colorkey(WHITE)
                DISPLAYSURF.blit(pic,(0,0))
                displayText(300,100,"During the game a stroke will appear like so")
            elif(slide==3):
                DISPLAYSURF.blit(pic,(0,0))
                displayText(300,100,"After a certain amount of time a circle will")
                displayText(300,140,"appear at the beginning of the stroke")
                Circ.draw()
                pygame.display.update()
            elif(slide==4):
                DISPLAYSURF.blit(pic,(0,0))
                displayText(300,100,"Put your mouse over the circle and follow the")
                displayText(300,140,"purple path it creates until you reach the end")
            pygame.display.update()
    Backgrd.switch_mode()

    f = open(character + '.txt', 'r')
    while line != '' and ready and True:
        if Circ.active:
            Circ.update()
            Circ.draw()
            mousehold = pygame.mouse.get_pos()
            dist = math.sqrt((mousehold[0]-Circ.xcoord)**2 + (mousehold[1]-Circ.ycoord)**2)
            Backgrd.check(dist <= Circ.radius)
            if dist <= Circ.radius:
                accuracy += 1
            for img in BlitList:
                DISPLAYSURF.blit(img, (0,0))
            pygame.display.update()
            count+=1
        else:
            line = f.readline().strip()
            if line == 'STROKE':
                num += 1
                Backgrd.draw()
                for img in BlitList:
                    DISPLAYSURF.blit(img, (0,0))
                pygame.display.update()
                pygame.time.delay(500)
            elif line != '':
                line = line.split('-')
                mult = float(line[1])
                line = line[0]
                line = line.split('|')
                Circ = HitCirc(line, True, mult)
                hold = pygame.image.load(character + '_' + str(num) + '.png')
                hold.set_colorkey(WHITE)
                BlitList.append(hold)
            for img in BlitList:
                DISPLAYSURF.blit(img, (0,0))
            pygame.display.update()
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    print accuracy, count, accuracy*1.0/count
    f.close()

if __name__ == '__main__':
    main()
