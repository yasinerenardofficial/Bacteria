import pygame,sys,random,time
from pygame import *
pygame.font.init() 
pygame.init()

#variables
screenwidth=800
screenhight=800
screencentrex=screenwidth/2
screencentrey=screenhight/2
event = pygame.event.get()
surface = pygame.display.set_mode((screenwidth,screenhight))
texte= pygame.font.SysFont('Comic Sans MS', 50)
timer=pygame.time.Clock()
keys=pygame.key.get_pressed()
mousex,mousey=pygame.mouse.get_pos()
chrono=0

#1=morpion 
#2=bacterie
game=2
MOUSEBUTTONisDOWN=0
MOUSEBUTTONisUP=0
fpshow=0


#blocs variables
rows=50
columns=50
ecart=2
blockswidth=screenwidth/rows
blocksheight=screenhight/columns
startposition=0#(screenhight-screenwidth)//2
surfacedeblocsx,surfacedeblocsy=screenwidth,screenhight
generationx=0
generationy=startposition
generationencoure=1
blocsagenerer=rows*columns
blocsizex=(surfacedeblocsx//rows)-ecart
blocsizey=(surfacedeblocsy//columns)-ecart
run=True
score=0
bgcolor = (0, 0, 0)
blocsnombre=0
debug=0
player=1

class carre():
    all=[]
    def __init__(self, x, y):
        self.vi=0
        self.rect = pygame.Rect(x, y, blocsizex, blocsizey)
        carre.all.append(self)
        self.random_color = random.choices(range(256), k=3)
    def draw(self):
        if self.vi==1:
            pygame.draw.rect(surface, self.random_color, self.rect)
    def reset(self):
        #self.random_color=[]
        self.vi=0

def guivetimefrom(value):
    sec=value//60;seca=('{0:02d}'.format(sec))
    min=sec//60;mina=('{0:02d}'.format(min))
    return f"{mina}:{seca}"

class bacterie():
    all=[]
    def __init__(self,x,y,w,h):
        global blocsnombre,blocsizex,blocsizey,keys,chrono
        self.vie=1
        if w==0:
            self.width=blocsizex+1
        else : 
            self.width=w
        if h==0:    
            self.height=blocsizey+1
        else : 
            self.height=h
        self.tag=blocsnombre
        blocsnombre+=1
        self.random_color = random.choices(range(256), k=3)
        self.color=[]
        self.modifiable=0
        self.team=1
        self.birthcount = 0
        self.birthend = random.randint(30,180)
        self.modified_color=[]
        self.rect=pygame.Rect(x,y,self.width,self.height)
        
        self.gavebirth=0
        collisions=[]

        #action to execute
        bacterie.all.append(self)

    def draw(self):
        global blocsnombre,blocsizex,blocsizey,debug,keys,player,MOUSEBUTTONisDOWN,MOUSEBUTTONisUP,\
        mousex,mousey
        if self.vie==1:
            if self.modifiable==0:self.color="white"
            if self.modifiable==1:self.color="grey"
            if self.modifiable==2:self.color,self.modified_color=self.modified_color,self.color
            if self.team==1:self.modified_color="blue"
            if self.team==2:self.modified_color="red"
            if self.team==3:self.modified_color="green"
            if self.team==4:self.modified_color="yellow"
            pygame.draw.rect(surface,self.color,self.rect)
            if self.modifiable==3:    
                self.guivebirth()
            if debug ==1:
                text_surface = texte.render(f"{self.tag}", False, (255,0,0))
                surface.blit(text_surface, ((self.rect.centerx-15),(self.rect.centery-35)))
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if MOUSEBUTTONisDOWN==1:
                        if self.rect.collidepoint(pygame.mouse.get_pos()):
                            if self.modifiable==0:
                                self.modifiable=1
                    if MOUSEBUTTONisUP==1:
                        if self.modifiable==1:
                            self.color,self.modified_color=self.modified_color,self.color
                            self.team=player
                            if player==4:player=1
                            else:player+=1
                            self.modifiable=3
            elif self.modifiable==1:
                    self.modifiable=0
        if self.vie==2:
            pygame.draw.rect(surface, self.random_color, self.rect)
            self=carre(self.rect.x,self.rect.y)
            #self.modified_color,self.random_color=self.random_color,self.modified_color
                
    def reset(self):
        self.vie=1
        self.modifiable=0
        self.color=[]
        self.modified_color=[]
        self.gavebirth=0
        #self.random_color="white"
        self.color,self.modified_color=self.modified_color,self.color

    def guivebirth(self):
        global blockswidth,blocksheight,blocsnombre
        if self.gavebirth==0:
            if self.birthcount>self.birthend :
                for obj in bacterie.all:
                    offset=20
                    if obj is not self and obj.vie==1 and \
                    obj.rect.collidepoint(self.rect.midright[0]+self.rect.width//2 , self.rect.centery) or \
                    obj.rect.collidepoint(self.rect.midleft[0]-self.rect.width//2 , self.rect.centery) or \
                    obj.rect.collidepoint(self.rect.centerx , self.rect.midtop[1]-self.rect.height//2) or \
                    obj.rect.collidepoint(self.rect.centerx , self.rect.midbottom[1]+self.rect.height//2) :
                    #if obj is not self and self.rect.colliderect(obj.rect):
                        if self in bacterie.all:
                            obj.modifiable=3
                            #obj.color = "yellow"
                            #bacterie.all.remove(self)
                            #blocsnombre-=1
                            self.vie=2
                            self.gavebirth=1
                            #self=carre(self.rect.x,self.rect.y)
            else : self.birthcount+=1

def stage_generation():
        bacteriesetup()
        for bacteries in bacterie.all: 
            bacteries.draw()

def bacteriesetup():
    global screenwidth,startposition,surfacedeblocsx,generationx,generationy,generationencoure
    if blocsnombre<blocsagenerer and generationencoure!=0:
        for target in range(0,blocsagenerer):
            new_bloc=bacterie(generationx,generationy,0,0)
            generationx+=blocsizex+ecart
            if generationx>surfacedeblocsx-1:
                generationx=0
                generationy+=blocsizey+ecart
    else:
        generationencoure=0

while run:
    pygame.init()
    chrono+=1
    timer.tick(60)
    fps_text = str(int(timer.get_fps()))    
    pygame.display.set_caption(f"{guivetimefrom(chrono)}   fps:{fps_text}  {('{0:05d}'.format(blocsnombre))}")
    surface.fill(bgcolor)
    for carres in carre.all:
        carres.draw()
    stage_generation()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYUP:
            if event.key==K_F3:
                if debug!=2:debug+=1
                else: debug=0
            if event.key==K_F1:
                if fpshow==1: fpshow=0
                else : fpshow=1
        if event.type == MOUSEBUTTONDOWN:
            MOUSEBUTTONisDOWN=1
        else:
            MOUSEBUTTONisDOWN=0
        if event.type == MOUSEBUTTONUP:
            MOUSEBUTTONisUP=1
        else:
            MOUSEBUTTONisUP=0
    pygame.display.flip()
pygame.quit()