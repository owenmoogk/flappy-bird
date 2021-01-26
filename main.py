# owen moogk
# flappy bird
# jan 1 2020

# imports
import pygame, random, os, time, sys, pickle
from random import randint

# pygame settings
windowWidth = 600
windowHeight = 800
birdHeight = 30
birdWidth = 40

# game settings
gameSpeed = 40
gravity = 0.8
jumpPower = 12
pipeHeight = 650
pipeWidth = 75 
pipeGap = 200
birdX = 100
pipeSpeed = 5

# clock
clock = pygame.time.Clock()

# images
pipeImg = pygame.transform.scale(pygame.image.load(os.path.join("assets","pipe.png")), (pipeWidth, pipeHeight))
pipeImgFlipped = pygame.transform.flip(pipeImg, False, True)
backgroundImg = pygame.transform.scale(pygame.image.load(os.path.join("assets","background.png")), (windowWidth, windowHeight))
birdImg = pygame.transform.scale(pygame.image.load(os.path.join("assets","bird.png")), (birdWidth, birdHeight))

# fonts
pygame.font.init()
font = pygame.font.SysFont("comicsans", 50)

# display
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Flappy Bird')

# bird class
class bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ySpeed = 0
    def jump(self):
        self.ySpeed = 0-jumpPower
        self.tick_count = 0
        self.height = self.y
    def move(self):
        self.ySpeed += gravity
        self.y += self.ySpeed
    def topBottomCollision(self):
        collided = False
        if self.y < 0:
            collided = True
        if self.y > windowHeight - birdHeight:
            collided = True
        return(collided)

# pipe class
class pipe:
    def __init__(self, yBottom,x):
        self.yBottom = yBottom
        self.yTop = yBottom - pipeGap - pipeHeight
        self.x = x
        self.pointScored = False

def renderScreen(score, bird, pipes):
    screen.blit(backgroundImg,(0,0))
    for pipe in pipes:
        screen.blit(pipeImg,(pipe.x,pipe.yBottom))
        screen.blit(pipeImgFlipped, (pipe.x,pipe.yTop))
    screen.blit(birdImg,(bird.x,bird.y))
    score_label = font.render("Score: " + str(score),1,(255,255,255))
    screen.blit(score_label, (10, 10))
    highScoreLabel = font.render("High Score: "+str(highScore),1,(255,255,255))
    screen.blit(highScoreLabel, (10, 50))

running = True
started = True

while running:
    b1 = bird(birdX,windowHeight/2-100)

    pipes = []
    pipes.append(pipe(randint(pipeGap + 50,windowHeight-200),windowWidth))

    # highscore
    playing = True
    if started == False:
        if score > highScore:
            highScore = score
            pickle.dump(highScore, open("highscore.dat", "wb"))
    else:
        highScore = pickle.load(open("highscore.dat", "rb"))

    score = 0

    while playing:
        # looping thru events
        events = pygame.event.get()
        for event in events:
            # if x button pressed stop just break out of these loops
            if event.type == pygame.QUIT:
                running = False
                playing = False
            # if key is pressed
            if event.type == pygame.KEYDOWN:
                # if space is pressed
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    b1.jump()

        b1.move()
        playing = not b1.topBottomCollision() # if collision is true, playing is false

        # if the forwardmost pipe is off screen then delete
        if pipes[len(pipes)-1].x < windowWidth - 250:
            pipes.append(pipe(randint(pipeGap + 50,windowHeight-200),windowWidth))

        for i in pipes:
            i.x -= pipeSpeed
            if i.x < b1.x + birdWidth and i.x + pipeWidth > b1.x and (i.yBottom < b1.y + birdHeight or i.yBottom - pipeGap > b1.y):
                playing = False
            if i.x < 0 - pipeWidth:
                pipes.remove(pipes[0])
            if not i.pointScored and i.x + pipeWidth < birdX:
                i.pointScored = True
                score += 1

        renderScreen(score, b1, pipes)
        clock.tick(gameSpeed)
        pygame.display.update()