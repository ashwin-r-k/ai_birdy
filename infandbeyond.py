import pygame
import random
import time
import os
import neat
pygame.font.init()
WIN_WIDTH = 900
WIN_HEIGHT = 800
ROCKET_WIDTH = 100
ASTROID_WIDTH = 200

CLOCK_TICK = 60
STAT_FONT = pygame.font.SysFont("comicsans",50)

rocket_1 = pygame.image.load(os.path.join("imgs","rocket_1.png"))
rocket_2 = pygame.image.load(os.path.join("imgs","rocket_2.png"))
rocket_3 = pygame.image.load(os.path.join("imgs","rocket_3.png"))

rocket_1 = pygame.transform.smoothscale(rocket_1, (ROCKET_WIDTH, rocket_1.get_height()/rocket_1.get_width()*ROCKET_WIDTH))
rocket_2 = pygame.transform.smoothscale(rocket_2, (ROCKET_WIDTH, rocket_1.get_height()/rocket_1.get_width()*ROCKET_WIDTH)) 
rocket_3 = pygame.transform.smoothscale(rocket_3, (ROCKET_WIDTH, rocket_1.get_height()/rocket_1.get_width()*ROCKET_WIDTH)) 


ROCKET_IMGS = [rocket_1,rocket_2,rocket_3]

""" astroid_1 = pygame.image.load(os.path.join("imgs","astroid_1.png"))
astroid_1 = pygame.transform.smoothscale(astroid_1, (ASTROID_WIDTH, astroid_1.get_height()/astroid_1.get_width()*ASTROID_WIDTH))

astroid_2 = pygame.image.load(os.path.join("imgs","astroid_2.png"))
astroid_2 = pygame.transform.smoothscale(astroid_2, (ASTROID_WIDTH, astroid_1.get_height()/astroid_2.get_width()*ASTROID_WIDTH))

astroid_3 = pygame.image.load(os.path.join("imgs","astroid_3.png"))
astroid_3 = pygame.transform.smoothscale(astroid_3, (ASTROID_WIDTH, astroid_3.get_height()/astroid_3.get_width()*ASTROID_WIDTH))

astroid_4 = pygame.image.load(os.path.join("imgs","astroid_4.png"))
astroid_4 = pygame.transform.smoothscale(astroid_4, (ASTROID_WIDTH*1.5, astroid_4.get_height()/astroid_4.get_width()*ASTROID_WIDTH*1.5))

astroid_5 = pygame.image.load(os.path.join("imgs","astroid_5.png"))
astroid_5 = pygame.transform.smoothscale(astroid_5, (ASTROID_WIDTH, astroid_5.get_height()/astroid_5.get_width()*ASTROID_WIDTH))
 """
astroid_4 = pygame.image.load(os.path.join("imgs","astroid_4.png"))
astroid_4 = pygame.transform.smoothscale(astroid_4, (250, 500))

ASTROID_IMG = [astroid_4]


#ASTROID_IMG = [astroid_1,astroid_2,astroid_3,astroid_4,astroid_5]

BASE_IMG = pygame.transform.smoothscale(pygame.image.load(os.path.join("imgs","base_f.png")) ,(900,100))
BG_IMG = pygame.transform.smoothscale(pygame.image.load(os.path.join("imgs","space_bg.png") ),(WIN_WIDTH,WIN_HEIGHT) )

class Rocket:
    IMGS = ROCKET_IMGS
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

class Astroid:
    GAP = 200
    VEL = 5
    
    def __init__(self,x):

        self.x=x
        self.height = 0

        self.top = 0
        self.bottom = 0
        
        self.ASTROID_BOTTOM = random.choice(ASTROID_IMG) #ASTROID_IMG[random.randrange(0,3)]
        self.ASTROID_TOP = pygame.transform.flip(self.ASTROID_BOTTOM,False,True)

        self.img = self.ASTROID_TOP

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,WIN_HEIGHT-100 )
        self.top = self.height - self.ASTROID_TOP.get_height()
        self.bottom =self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL

    def  draw(self,win):
        win.blit(self.ASTROID_TOP,(self.x,self.top))
        win.blit(self.ASTROID_BOTTOM,(self.x,self.bottom))

    def collide(self,rocket):
        rocket_mask = rocket.get_mask()
        top_mask = pygame.mask.from_surface(self.ASTROID_TOP)
        bottom_mask = pygame.mask.from_surface(self.ASTROID_BOTTOM)

        top_offset= (self.x-rocket.x,self.top-round(rocket.y))
        bottom_offset= (self.x-rocket.x,self.bottom-round(rocket.y))

        b_point = rocket_mask.overlap(bottom_mask,bottom_offset)
        t_point = rocket_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True
        return False


class Base:

    VEL = 5
    WIDTH = BASE_IMG.get_width()-100
    IMG = BASE_IMG
    
    def __init__(self,y):
        self.y = y

        self.x1=0
        self.x2=self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0 :
            self.x1 = self.x2 +self.WIDTH

        if self.x2 + self.WIDTH < 0 :
            self.x2 = self.x1 +self.WIDTH
            
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))



def draw_window(win,rockets,astroids,base,score):
    
    win.blit(BG_IMG, (0,0))


    for astroid in astroids:
        astroid.draw(win)
    for rocket in rockets:
        rocket.draw(win)
    base.draw(win)

    text = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(text,( WIN_WIDTH-10-text.get_width() ,10))

    pygame.display.update()

def main(genomes, config):
    nets = []
    ge = []
    rockets = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        rockets.append(Rocket(230,350))
        g.fitness = 0
        ge.append(g)

    score = 0
    astroids = [Astroid(700)]

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    base = Base(WIN_HEIGHT-BASE_IMG.get_height())
    run = True

    while run:
        clock.tick(CLOCK_TICK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #     run = False
            # if rocket.y >= 1000:
            #     run = False
        
        astroid_ind = 0
        if len(rockets)>0:
            if len(astroids)>1 and rockets[0].x> astroids[0].x + astroids[0].ASTROID_TOP.get_width():
                astroid_ind = 1
        else:
            run = False
            break
        
        for x, rocket in enumerate(rockets):
            rocket.move()
            ge[x].fitness += 0.1

            output = nets[x].activate( (rocket.x, abs(rocket.y - astroids[astroid_ind].height),abs(rocket.y - astroids[astroid_ind].bottom )  ))
            
            if output[0] > 0.5:
                rocket.jump()

        rem = []
        add_astroid = False

        for astroid in astroids:

            for x, rocket in enumerate(rockets):

                if astroid.collide(rocket):
                    ge[x].fitness -= 1
                    rockets.pop(x)
                    nets.pop(x)
                    ge.pop(x)
        
                if not astroid.passed and astroid.x < rocket.x:
                    astroid.passed = True
                    add_astroid = True

            if astroid.x+astroid.ASTROID_TOP.get_width() < 0:
                rem.append(astroid)

        if add_astroid:
            score += 1
            for g in ge:
                g.fitness += 5
            #add_astroid = False
            astroids.append(Astroid(700))

        for r in rem:
            astroids.remove(r)

        for x,rocket in enumerate(rockets):
            if (rocket.y + rocket.img.get_height() >=730) or rocket.y <= 0 :
                rockets.pop(x)
                nets.pop(x)
                ge.pop(x)
            

        #rocket.move()
        astroid.move()
        base.move()
        draw_window(win,rockets,astroids,base,score)


#main()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,10)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)

