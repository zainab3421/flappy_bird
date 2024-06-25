import pygame
import random
from pygame.locals import *
pygame.init()

playing = True
score = 0
flying = False
game_over = False

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("FLAPPY BIRD :D")

ground_scroll = 0
scroll_speed = 4

pipe_gap = 150
pipe_frequency = 2000
last_pipe = pygame.time.get_ticks() - pipe_frequency
pass_pipe = False

bg = pygame.image.load("images/flappy_bg.png")
ground_img = pygame.image.load("images/ground.png")
restart_button = pygame.image.load("images/restart_button.png")

class Birdy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f"images/flappy_{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velo = 0
        self.click = False
    def update(self):
        if flying:
            self.velo += 0.5
            if self.velo > 8:
                self.velo = 8
            if self.rect.bottom < 650:
                self.rect.y += int(self.velo)
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velo = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index],self.velo*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-90)

class Pipes(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/pipe.png")
        self.rect = self.image.get_rect()
        if pos == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y-int(pipe_gap/2)]
        if pos == -1:
            self.rect.topleft = [x,y+int(pipe_gap/2)]
    def update(self):
        self.rect.x = self.rect.x - scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action

button = Button(screen_width//2-50,screen_height//2+50,restart_button)

birdies = pygame.sprite.Group()
pipes = pygame.sprite.Group()
flappy = Birdy(100,int(screen_height/2))
birdies.add(flappy)

while playing:
    clock.tick(fps)
    for event in pygame.event.get():
        #game quit
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()
    screen.blit(bg,(0,0))
    font = pygame.font.SysFont("Bauhaus 93",50)
    text = font.render("Score:"+str(score),True,(0,0,0))
    screen.blit(text,(20,20))
    birdies.draw(screen)
    pipes.draw(screen)
    birdies.update()
    screen.blit(ground_img,(ground_scroll,650))
    if len(pipes) > 0:
        if birdies.sprites()[0].rect.left > pipes.sprites()[0].rect.left\
            and birdies.sprites()[0].rect.right < pipes.sprites()[0].rect.right\
            and pass_pipe == False:
                pass_pipe = True
        if pass_pipe == True and game_over == False:
            if birdies.sprites()[0].rect.left > pipes.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    if pygame.sprite.groupcollide(birdies,pipes,False,False):
        game_over = True
    if flappy.rect.bottom >= 650:
        game_over = True
        flying = False
    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            bottom_pipe = Pipes(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipes(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipes.add(top_pipe)
            pipes.add(bottom_pipe)
            last_pipe = time_now
    ground_scroll = ground_scroll-scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0
    pipes.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    if game_over:
        font=pygame.font.SysFont("Bauhaus",72)
        text=font.render("Game Over!",True,(0,0,0))
        screen.blit(text,(250,350))
        if button.draw():
            game_over = False
            flying = True
            score = 0
            pipes.empty()
            flappy.rect.x = 100
            flappy.rect.y = int(screen_height/2)

    pygame.display.update()
