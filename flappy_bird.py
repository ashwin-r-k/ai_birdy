import pygame
import random
import time
import os
import neat

WIN_WIDTH = 500
WIN_HEIGHT = 800
ROCKET_WIDTH = 100
CLOCK_TICK = 60

rocket_1 = pygame.image.load(os.path.join("imgs","rocket_1.png"))
rocket_2 = pygame.image.load(os.path.join("imgs","rocket_2.png"))
rocket_3 = pygame.image.load(os.path.join("imgs","rocket_3.png"))

rocket_1 = pygame.transform.smoothscale(rocket_1, (ROCKET_WIDTH, rocket_1.get_height()/rocket_1.get_width()*ROCKET_WIDTH))
rocket_2 = pygame.transform.smoothscale(rocket_2, (ROCKET_WIDTH, rocket_1.get_height()/rocket_1.get_width()*ROCKET_WIDTH)) 
rocket_3 = pygame.transform.smoothscale(rocket_3, (ROCKET_WIDTH, rocket_1.get_height()/rocket_1.get_width()*ROCKET_WIDTH)) 


BIRD_IMGS = [rocket_1,rocket_2,rocket_3]

#BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png") )),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png") )),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png") )) ]
PIPE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png") ))]
BASE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png") ))]
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png") ))
#bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VELOCITY = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count=0
        self.img = self.IMGS[0]
    
    def jump(self,):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.velocity*self.tick_count+1.5*self.tick_count**2

        if d >=16:
            d = 16
        if d < 0 :
            d = -2
        
        self.y = self.y +d

        if d <0 or self.y < self.height :
            if self.tilt < self.MAX_ROTATION:
                self.tilt =self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VELOCITY

    def draw(self,win):
        self.img_count += 1
        
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
       # elif self.img_count < self.ANIMATION_TIME*4:
        #    self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*3 +1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self,x):
        self.x=x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom =self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL

    def  draw(self,win):
        win.blit()
        

def draw_window(win,bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,200)
    win =pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(CLOCK_TICK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #bird.move()
        draw_window(win,bird)

    pygame.quit()

main()

