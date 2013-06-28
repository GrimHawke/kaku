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
    global FPSCLOCK, DISPLAYSURF, BUTTONSURF, BASICFONT
    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((800, 650))
    BUTTONSURF = pygame.display.set_mode((800,650))
    pygame.display.set_caption('Learn Japanese!')
    value = [1]
    while True:
        if value[0] == 1:
            value = mainmenu()
        elif value[0] == 2:
            #tutorial
            value = runGame(1, True)
        elif value[0] == 3:
            value = runGame(random.randrange(1,10),False)
        elif value[0] == 4:
            value = runGame(value[1], False)

class Character(object):
    def __init__(self,num):
        self.startingpoints=[]
        self.images=[]
        character = 'number' + '_' + str(num)
        f = open('Numbers/'+character+'.txt','r')
        line = ' '
        i=0
        image=None
        first = False
        while line != '':
            line = f.readline().strip()
            if line == 'STROKE':
                i+=1
                image=pygame.image.load('Numbers/'+character+'_'+str(i)+'.png')
                image.set_colorkey(WHITE)
                self.images.append(image)
                first = True
            elif line!='' and first:
                line = line.split('-')[0].split('|')
                line_x= int(line[0].split(',')[0])
                line_y= int(line[0].split(',')[1])
                self.startingpoints.append((line_x,line_y))
                first = False
            elif line!='' and not first:
                self.startingpoints.append(None)
            
    def __str__(self):
        return '''A character'''

    def return_points(self):
        return self.startingpoints

    def drawStroke(self,num=1):
        DISPLAYSURF.blit(self.images[num-1],(0,0))

class HitButton(object):
    def __init__(self,coord):
        self.radius=70
        self.pos=tuple(coord)
        
    def draw(self):
        pygame.draw.circle(BUTTONSURF,WHITE,self.pos,self.radius+1,1)
        pygame.draw.circle(BUTTONSURF,RED,self.pos,self.radius,1)

    def update(self):
        self.radius-=1
        if self.radius>1:
            self.draw()
            
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
        self.nextbutton = None
        pygame.display.update()

    def update(self,char,strokenum):
        self.xcoord = curve(self.stroke_x, self.t)
        self.ycoord = curve(self.stroke_y, self.t)
        self.t += 0.005*self.mult
        if self.t >= 0.5:
            if (self.nextbutton is None) and (strokenum < len(char.return_points()))and (char.return_points()[strokenum] is not None):
                self.nextbutton = HitButton(char.return_points()[strokenum])
                strokenum+=1
            elif self.nextbutton is not None:
                self.nextbutton.update()
        if self.t >= 1:
            self.active = False
            self.nextbutton=None

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, PURPLE, (int(self.xcoord), int(self.ycoord)), self.radius, 0)
        
class menu1(object):
    def __init__(self):
        self.img = pygame.image.load('titleplaceholder.png')
        self.img.set_colorkey(WHITE)
        self.button_start = button('Start', 650, 400)
        self.button_tutor = button('Tutorial', 650, 480)
        self.button_quit = button('Quit', 650, 560)

    def update(self):
        DISPLAYSURF.blit(self.img, (0,0))
        return [self.button_start.update(), self.button_tutor.update(), self.button_quit.update()]

class menu2(object):
    def __init__(self):
        self.button_menu = button('Menu', 300, 150)
        self.button_restart = button('Restart', 300, 300)
        self.button_resume = button('Resume', 300, 450)

    def update(self):
        transblack=pygame.image.load('translucent_black.png')
        DISPLAYSURF.blit(transblack,(0,0))
        return [self.button_menu.update(), self.button_restart.update(), self.button_resume.update()]
        
class button(object):
    def __init__(self, text, x, y):
        self.fontObj = pygame.font.Font('freesansbold.ttf', 30)
        self.text = self.fontObj.render(text, True, WHITE)
        self.rect = self.text.get_rect()
        self.rect.center = (x,y)
        self.color = RED

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.color, (self.rect.center[0] - 100, self.rect.center[1]-40, 200, 80))
        DISPLAYSURF.blit(self.text, self.rect)
        #blit rectangle of color onto overlay
        #blit text onto overlay

    def check(self):
        coord = pygame.mouse.get_pos()
        if coord[0] >= self.rect.center[0]-100 and coord[0] <= self.rect.center[0]+100 and coord[1] >= self.rect.center[1]-40 and coord[1] <= self.rect.center[1]+40:
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
        

def runGame(choice, is_tutorial):
    characters=[]
    for i in range(10):
        c=Character(i+1)
        characters.append(c)
        
    choice = 5
    ready = False
    pause = False
    accuracy = 0
    num = 0
    strokenum = 0
    count = 0
    mult = 1
    line = ' '
    Circ = HitCirc(['0,0'], False, 1)
    #CircList = list()
    BlitList = list()

    pause_menu = menu2()
    
    character = 'number' + '_' + str(choice)
    Backgrd = Background(choice)
    
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
                pic=pygame.image.load('Numbers/'+character + '_1.png')
                pic.set_colorkey(WHITE)
                DISPLAYSURF.blit(pic,(0,0))
                displayText(300,100,"During the game a stroke will appear like so",BLACK)
            elif(slide==3):
                DISPLAYSURF.blit(pic,(0,0))
                displayText(300,100,"After a certain amount of time a circle will",BLACK)
                displayText(300,140,"appear at the beginning of the stroke",BLACK)
                Circ.draw()
                pygame.display.update()
            elif(slide==4):
                DISPLAYSURF.blit(pic,(0,0))
                displayText(298,100,"Put your mouse over the circle and follow the",BLACK)
                displayText(298,140,"purple path it creates until you reach the end",BLACK)
                Circ.draw()
            pygame.display.update()

    f = open('Numbers/' + character + '.txt', 'r')
    while line != '' and ready and True:
        Backgrd.draw()
        Circ.draw()
        for img in BlitList:
            DISPLAYSURF.blit(img, (0,0))
        if not pause:
            if Circ.active:
                Circ.update(characters[choice-1],strokenum)
                mousehold = pygame.mouse.get_pos()
                dist = math.sqrt((mousehold[0]-Circ.xcoord)**2 + (mousehold[1]-Circ.ycoord)**2)
                Backgrd.check(dist <= Circ.radius)
                if dist <= Circ.radius:
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
                    strokenum += 1
                    Circ.update(characters[choice-1],strokenum)
                    hold = pygame.image.load('Numbers/' + character + '_' + str(num) + '.png')
                    hold.set_colorkey(WHITE)
                    BlitList.append(hold)
        else:
            hold = pause_menu.update()
            if hold[0]:
                return [1]
            elif hold[1]:
                return [4, choice]
            elif hold[2]:
                pause = not pause
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
    if(accuracy2>=80):
        displayText(120,624,string,WHITE)
        displayText(420,624,"Good Job!",WHITE)
        return [3]
    else:
        displayText(120,624,string,WHITE)
        displayText(420,624,"Try Again!",WHITE)
        return [4, choice]

if __name__ == '__main__':
    main()
