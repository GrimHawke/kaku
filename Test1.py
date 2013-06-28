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

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((700, 600))
    pygame.display.set_caption('Pointer Test')
    while True:
        runGame()

class Background(object):
    def __init__(self):
        self.grid_img = 'hi'

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, WHITE, (0, 0, 600, 600))

    def check(self,scoring):
        if scoring:
            pygame.draw.rect(DISPLAYSURF, GREEN, (600, 0, 100, 600))
        else:
            pygame.draw.rect(DISPLAYSURF, RED, (600, 0, 100, 600))

def curve(points, t):
    if len(points) != 1:
        copy1 = points[0:-1]
        copy2 = points[1::]
        return (1-t)*curve(copy1,t) + t*curve(copy2, t)
    else:
        return points[0]

class HitCirc(object):
    def __init__(self, stroke): #stroke object is list of coordinates for bezier curve
        self.radius = 20
        self.stroke_x = list()
        self.stroke_y = list()
        for thing in stroke:
            hold = thing.split(',')
            self.stroke_x.append(int(hold[0]))
            self.stroke_y.append(int(hold[1]))
        self.xcoord = 300
        self.ycoord = 300
        self.t = 0
        self.active = True
        self.beg = False

    def update(self):
        self.xcoord = curve(self.stroke_x, self.t)
        self.ycoord = curve(self.stroke_y, self.t)
        self.t += 0.005
        if self.t >= 1:
            self.active = False

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, PURPLE, (int(self.xcoord), int(self.ycoord)), self.radius, 0)

def runGame():
    character = 'number_3'
    f = open(character + '.txt', 'r')
    CircList = list()
    Backgrd = Background()
    num = 0
    BlitList = list()
    while True:
        line = f.readline().strip()
        if line != '':
            if line == 'STROKE':
                num += 1
                Backgrd.draw()
            else:
                line = line.split('|')
                Circ = HitCirc(line)
                hold = pygame.image.load(character + '_' + str(num) + '.png')
                hold.set_colorkey(WHITE)
                BlitList.append(hold)
                while Circ.active:
                    pygame.event.get(MOUSEMOTION)
                    Circ.update()
                    Circ.draw()
                    mousehold = pygame.mouse.get_pos()
                    dist = math.sqrt((mousehold[0]-Circ.xcoord)**2 + (mousehold[1]-Circ.ycoord)**2)
                    Backgrd.check(dist <= Circ.radius)
                    for img in BlitList:
                        DISPLAYSURF.blit(img, (0,0))
                    pygame.display.update()
                del Circ
                FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
