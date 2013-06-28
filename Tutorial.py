import random, pygame, sys, time, math
from pygame.locals import *

pygame.font.init()
screen_font = pygame.font.Font(None, 40)

FPS = 60
score = 0
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GRAY =  (128, 128, 128)
PURPLE = ( 128, 0, 128)



def TextBubble(x,y,text,size):
    picture=pygame.image.load("TextBubble.png")
    picrect=picture.get_rect()
    picrect.center=(x,y)
    picture.convert_alpha()
    picture.set_colorkey(BLACK)
    fontObj = pygame.font.Font('freesansbold.ttf', size)
    textSurfaceObj = fontObj.render(text, True, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(picture, picrect)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def displayText(x,y,text):
    fontObj = pygame.font.Font('freesansbold.ttf', 25)
    textSurfaceObj = fontObj.render(text, True, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((700, 600))
    pygame.display.set_caption('Pointer Test')
    while True:
        runTutorial()

class Background(object):
    def __init__(self, num):
        self.grid_img = 'hi'
        self.display_grid = False
        self.fontobj=pygame.font.Font('freesansbold.ttf',30)
        self.textSurfaceObject=self.fontobj.render("This next character is",True, BLACK)
        self.fontrect=self.textSurfaceObject.get_rect()
        self.fontrect.center=(300,220)
        self.fontobj2=pygame.font.Font('freesansbold.ttf',30)
        self.textSurfaceObject2=self.fontobj2.render(str(num),True, BLACK)
        self.fontrect2=self.textSurfaceObject2.get_rect()
        self.fontrect2.center=(300,260)

    def draw(self):
        #if self.display_grid:
        pygame.draw.rect(DISPLAYSURF, WHITE, (0, 0, 600, 600))
##        else:
##            pygame.draw.rect(DISPLAYSURF, WHITE, (0, 0, 600, 600))
##            DISPLAYSURF.blit(self.textSurfaceObject,self.fontrect)
##            DISPLAYSURF.blit(self.textSurfaceObject2,self.fontrect2)

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
        self.xcoord = 300
        self.ycoord = 300
        self.t = 0
        self.active = active
        self.beg = False
        self.mult = mult

    def update(self):
        self.xcoord = curve(self.stroke_x, self.t)
        self.ycoord = curve(self.stroke_y, self.t)
        self.t += 0.005*self.mult
        if self.t >= 1.0:
            self.active = False

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, PURPLE, (int(self.xcoord), int(self.ycoord)), self.radius, 0)

def runTutorial():
    while True:
        slide=0
        sub=0
        sub2=0
        ready = False
        accuracy = 0
        num = 0
        count = 0
        mult = 1
        line = ' '
        CircList = list()
        Circ = HitCirc(['0,0'], False, 1)
        BlitList = list()
        choice = 2
        character = 'number' + '_' + str(choice)
        f = open('number_1.txt', 'r')
        Backgrd = Background(choice)
        f.readline().strip()
        line = f.readline().strip()
        line = line.split('-')
        mult = float(line[1])
        line = line[0]
        line = line.split('|')
        Circ = HitCirc(line, True, .5)
        Circ.update()
        while not ready and True:
            #display until ready
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN and sub==0:
                    slide+=1
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if(slide==0):
                    Backgrd.draw()
                    displayText(300,160,"Welcome to the (insert name here) Tutorial!")
                    displayText(300,210,"Click the mouse when you are ready to proceed") 
                    pygame.display.update()
                elif(slide==1):
                    Backgrd.draw()
                    displayText(300,160,"The purpose of this game is to teach you")
                    displayText(300,210,"the basics of writing in japanese")
                    pygame.display.update()
                elif(slide==2):
                    Backgrd.draw()
                    pic=pygame.image.load('number_1_1.png')
                    DISPLAYSURF.blit(pic,(0,0))
                    displayText(300,100,"During the game a stroke will appear like so")
                    pygame.display.update()
                elif(slide==3):
                    Backgrd.draw()
                    DISPLAYSURF.blit(pic,(0,0))
                    displayText(300,100,"After a certain amount of time a circle will")
                    displayText(300,140,"appear at the beginning of the stroke")
                    Circ.draw()
                    pygame.display.update()
                elif(slide==4):
                    Backgrd.draw()
                    DISPLAYSURF.blit(pic,(0,0))
                    sub=1
                    displayText(300,100,"Put your mouse over the circle and follow the")
                    displayText(300,140,"purple path it creates until you get 300 Accuracy")

                    dist=100
                    Circ.draw()
                    pygame.display.update()
                    while(dist>Circ.radius):
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type==MOUSEMOTION:
                                mousehold=event.pos
                                dist = math.sqrt((mousehold[0]-Circ.xcoord)**2 + (mousehold[1]-Circ.ycoord)**2)
                    accuracy=0
                    while sub2==0:
                        if Circ.active==True:
                            Backgrd.draw()
                            DISPLAYSURF.blit(pic,(0,0))
                            displayText(300,100,"Put your mouse over the circle and follow the")
                            displayText(300,140,"purple path it creates until you get 300 Accuracy")
                            string="Accuracy:"+str(accuracy)
                            displayText(100,500,string)
                            Circ.update()
                            Circ.draw()
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type==MOUSEMOTION:
                                    mousehold=event.pos
                            dist = math.sqrt((mousehold[0]-Circ.xcoord)**2 + (mousehold[1]-Circ.ycoord)**2)
                            Backgrd.check(dist <= Circ.radius)
                            if dist <= Circ.radius:
                                accuracy += 1
                            pygame.display.update()
                            count+=1;
                            if(count==399):
                                if(accuracy>=300):
                                   sub2=1
                                   Circ.active=False
                                else:
                                    Circ = HitCirc(line, True, .5)
                                    Backgrd.draw()
                                    DISPLAYSURF.blit(pic,(0,0))
                                    displayText(300,100,"Put your mouse over the circle and follow the")
                                    displayText(300,140,"purple path it creates until you get 300 Accuracy")
                                    Circ.update()
                                    Circ.draw()
                                    dist=100
                                    pygame.display.update()
                                    while(dist>Circ.radius):
                                        for event in pygame.event.get():
                                            if event.type == QUIT:
                                                pygame.quit()
                                                sys.exit()
                                            if event.type==MOUSEMOTION:
                                                mousehold=event.pos
                                                dist = math.sqrt((mousehold[0]-Circ.xcoord)**2 + (mousehold[1]-Circ.ycoord)**2)
                                    accuracy=0
                                    count=0
                    slide+=1
                    pygame.display.update()
                elif(slide==5):
                    pygame.time.delay(200)
                    Backgrd.draw()
                    displayText(300,150,"Great Job!")
                    displayText(300,190,"Some characters may have more than one stroke")
                    displayText(300,230,"so keep an eye out for those.")
                    displayText(300,330,"That's the end of the Tutorial!")
                    displayText(300,370,"Go learn some Japanese!")
            
  

if __name__ == '__main__':
    main()


