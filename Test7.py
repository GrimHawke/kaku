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
katakana = ('n', 'wa', 'ra', 'ya', 'ma', 'ha', 'na', 'ta', 'sa', 'ka', 'a',
            'wi', 'ri', 'mi', 'hi', 'ni', 'chi', 'shi', 'ki', 'i',
            'ru', 'yu', 'mu', 'fu', 'nu', 'tsu', 'su', 'ku', 'u',
            'we', 're', 'me', 'he', 'ne', 'te', 'se', 'ke', 'e',
            'wo', 'ro', 'yo', 'mo', 'ho', 'no', 'to', 'so', 'ko', 'o')

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((800, 650))
    pygame.display.set_caption('Learn Japanese!')
    value = [1]
    while True:
        if value[0] == 1:
            value = mainmenu()
        elif value[0] == 2:
            value = runGame(1, 'number', True)
        elif value[0] == 3:
            value = runGame(random.randrange(1,10), 'number', False)
        elif value[0] == 4:
            value = runGame(random.rangerange(0,47), 'katakana', False)
        elif value[0] == 5:
            value = runGame(value[1], str(value[2]), False)

class menu1(object):
    def __init__(self):
        self.img = pygame.image.load('titleplaceholder.png')
        self.img.set_colorkey(WHITE)
        self.button_number = button('Start Numbers', 660, 340, 200, 80, 26)
        self.button_tutor = button('Tutorial', 660, 500, 200, 80, 30)
        self.button_quit = button('Quit', 660, 580, 200, 80, 30)
        self.button_kana = button('Start Kana', 660, 420, 200, 80, 28)

    def update(self):
        DISPLAYSURF.blit(self.img, (0,0))
        displayText(220, 620, "Press p during the game to pause", BLACK)
        return [self.button_number.update(), self.button_tutor.update(), self.button_quit.update(), self.button_kana.update()]

class menu2(object):
    def __init__(self):
        self.button_menu = button('Menu', 700, 110, 120, 50, 26)
        self.button_restart = button('Restart', 700, 235, 120, 50, 26)
        self.button_resume = button('Resume', 700, 360, 120, 50, 26)

    def update(self):
        transblack=pygame.image.load('translucent_black.png')
        DISPLAYSURF.blit(transblack,(0,0))
        coord = pygame.mouse.get_pos()
        if coord[0] >= self.button_resume.rect.center[0]-self.button_resume.xlen/2 and coord[0] <= self.button_resume.rect.center[0]+self.button_resume.xlen/2 and coord[1] >= self.button_resume.rect.center[1]-self.button_resume.ylen/2 and coord[1] <= self.button_resume.rect.center[1]+self.button_resume.ylen/2:
            displayText(700, 510, "Press p", BLACK)
            displayText(700, 540, "to unpause", BLACK)
        return [self.button_menu.update(), self.button_restart.update(), self.button_resume.update()]
        
class button(object):
    def __init__(self, text, x, y, xlen, ylen, fontsize):
        self.fontObj = pygame.font.Font('freesansbold.ttf', fontsize)
        self.text = self.fontObj.render(text, True, WHITE)
        self.rect = self.text.get_rect()
        self.rect.center = (x,y)
        self.xlen = xlen
        self.ylen = ylen
        self.color = RED

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.color, (self.rect.center[0] - self.xlen/2, self.rect.center[1]- self.ylen/2, self.xlen, self.ylen))
        DISPLAYSURF.blit(self.text, self.rect)

    def check(self):
        coord = pygame.mouse.get_pos()
        if coord[0] >= self.rect.center[0]-self.xlen/2 and coord[0] <= self.rect.center[0]+self.xlen/2 and coord[1] >= self.rect.center[1]-self.ylen/2 and coord[1] <= self.rect.center[1]+self.ylen/2:
            self.color = GREEN
            if pygame.mouse.get_pressed()[0]:
                return True
        else:
            self.color = RED
        return False

    def update(self):
        self.draw()
        return self.check()

def displayText(x,y,text,color):
    fontObj = pygame.font.Font('freesansbold.ttf', 25)
    textSurfaceObj = fontObj.render(text, True, color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


class Background(object):
    def __init__(self, num):
        self.grid_img = pygame.image.load('ui.png')
        self.intermediate = True
        self.fontobj=pygame.font.Font('freesansbold.ttf', 30)
        self.textSurfaceObject=self.fontobj.render("This next character is", True, BLACK)
        self.fontrect=self.textSurfaceObject.get_rect()
        self.fontrect.center=(300,220)
        self.textSurfaceObject2=self.fontobj.render(str(num), True, BLACK)
        self.fontrect2=self.textSurfaceObject2.get_rect()
        self.fontrect2.center=(300,260)

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, WHITE, (0, 0, 800, 600))
        DISPLAYSURF.blit(self.grid_img,(0,0))
        if self.intermediate:
            DISPLAYSURF.blit(self.textSurfaceObject,self.fontrect)
            DISPLAYSURF.blit(self.textSurfaceObject2,self.fontrect2)
        else:
            pygame.draw.rect(DISPLAYSURF,BLACK,(0,600,800,50))

    def check(self,scoring):
        if scoring:
            pygame.draw.circle(DISPLAYSURF, GREEN, (700,530),40,0)
        else:
            pygame.draw.circle(DISPLAYSURF, RED, (700,530),40,0)

    def switch_mode(self):
        self.intermediate = not self.intermediate

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
        if self.active:
            pygame.draw.circle(DISPLAYSURF, PURPLE, (int(self.xcoord), int(self.ycoord)), self.radius, 0)

def mainmenu():
    start_menu = menu1()
    while True:
        pygame.draw.rect(DISPLAYSURF,WHITE,(0,0,800,650))
        hold = start_menu.update()
        if hold[0]:
            pygame.draw.rect(DISPLAYSURF,BLACK,(0,600,800,50))
            return [3]
        elif hold[1]:
            return [2]
        elif hold[2]:
            pygame.quit()
            sys.exit()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        

def runGame(choice, kind, is_tutorial):
    ready = False
    pause = False
    accuracy = 0
    num = 0
    count = 0
    mult = 1
    line = ' '
    Circ = HitCirc(['0,0'], False, 1)
    #CircList = list()
    BlitList = list()

    pause_menu = menu2()
    character = ''
    Backgrd = Background(choice)
    if kind == 'number':
        character = str(kind) + '_' + str(choice)
    elif kind == 'katakana':
        character = str(kind) + '_' + str(katakana(choice))
        Backgrd = Background(katakana(choice))
    
    if not is_tutorial:
        while not ready and True:
            Backgrd.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    ready = True
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if pygame.key.get_pressed()[K_ESCAPE]:
                        return [1]
        Backgrd.switch_mode()
    else:
        Circ.active = True
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
                displayText(300,160,"Welcome to the Tutorial!",BLACK)
                displayText(300,210,"Click the mouse",BLACK)
                displayText(300,260,"when you are ready to proceed",BLACK) 
            elif(slide==1):
                displayText(300,160,"The purpose of this game is to teach you",BLACK)
                displayText(300,210,"the basics of writing in Japanese",BLACK)
            elif(slide==2):
                pic=pygame.image.load(character + '_1.png')
                pic.set_colorkey(WHITE)
                DISPLAYSURF.blit(pic,(0,0))
                displayText(300,100,"During the game a stroke will appear like so",BLACK)
            elif(slide==3):
                Circ.draw()
                DISPLAYSURF.blit(pic,(0,0))
                displayText(300,100,"A circle will then appear",BLACK)
                displayText(300,140,"at the beginning of the stroke",BLACK)
                pygame.display.update()
            elif(slide==4):
                Circ.draw()
                DISPLAYSURF.blit(pic,(0,0))
                displayText(298,100,"Put your mouse over the circle and click",BLACK)
                displayText(298,140,"Follow the circle until you reach the end",BLACK)
            pygame.display.update()
        Circ.active = False

    f = open(character + '.txt', 'r')
    while line != '' and ready and True:
        Backgrd.draw()
        for img in BlitList:
            DISPLAYSURF.blit(img, (0,0))
        if not pause:
            if Circ.active:
                Circ.draw()
                Circ.update()
                mousehold = pygame.mouse.get_pos()
                dist = math.sqrt((mousehold[0]-Circ.xcoord)**2 + (mousehold[1]-Circ.ycoord)**2)
                Backgrd.check(dist <= Circ.radius and pygame.mouse.get_pressed()[0])
                if dist <= Circ.radius and pygame.mouse.get_pressed()[0]:
                    accuracy += 1
                for img in BlitList:
                    DISPLAYSURF.blit(img, (0,0))
                count+=1
            else:
                line = f.readline().strip()
                if line == 'STROKE':
                    num += 1
                    pygame.display.update()
                    pygame.time.delay(500)
                elif line != '':
                    line = line.split('-')
                    mult = float(line[1])
                    line = line[0]
                    line = line.split('|')
                    Circ = HitCirc(line, True, mult)
                    Circ.update()
                    hold = pygame.image.load(character + '_' + str(num) + '.png')
                    hold.set_colorkey(WHITE)
                    BlitList.append(hold)
        else:
            hold = pause_menu.update()
            if hold[0]:
                return [1]
            elif hold[1]:
                return [4, choice]
            elif hold[2]:
                displayText(700, 510, "Press p", BLACK)
                displayText(700, 540, "to unpause", BLACK)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if pygame.key.get_pressed()[K_p]:
                    pause = not pause
                if pygame.key.get_pressed()[K_ESCAPE] and pause:
                    return [1]
    f.close()
    accuracy2=int(accuracy)*1.0/int(count)*100
    string="Accuracy:"+str(accuracy2)[:5]+"%"
    if(accuracy2<=80):
        displayText(120,624,string,WHITE)
        displayText(420,624,"Try Again!",WHITE)
        return [5, choice, kind]
    elif (accuracy2 > 80) and (not is_tutorial):
        displayText(120,624,string,WHITE)
        displayText(420,624,"Good Job!",WHITE)
        return [3]
    elif (accuracy2 > 80) and (is_tutorial):
        return [1]

if __name__ == '__main__':
    main()

