# owen moogk
# ai flappy bird
# jan 1 2020

# imports
import pygame,random,os,time,neat,sys
from random import randint

# pygame settings
windowWidth = 600
windowHeight = 800
birdHeight = 30
birdWidth = 40

# game settings
gameSpeed = 30
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
baseImg = pygame.image.load(os.path.join("assets","base.png"))

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

# pipe class
class pipe:
    def __init__(self, yBottom,x):
        self.yBottom = yBottom
        self.yTop = yBottom - pipeGap - pipeHeight
        self.x = x
        self.pointScored = False


running = True

# main running loop
while running:
    b1 = bird(birdX,windowHeight/2-100)

    pipes = []
    pipes.append(pipe(randint(pipeGap + 50,windowHeight-200),windowWidth))

    playing = True
    lost = False
    pause = True # this is telling to pause until space is pressed to start the game again. is true when started and after every death
    score = 0

    # when the player is in the game (ie not lost or on the starting screen)
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
                if event.key == pygame.K_SPACE:
                    b1.ySpeed = 0-jumpPower

        # background
        screen.blit(backgroundImg,(0,0))

        # adjusting the y speed of the bird
        b1.ySpeed += gravity
        # moving the bird y
        b1.y += b1.ySpeed

        #y collision detection
        if b1.y < 0:
            playing = False
            lost = True
        if b1.y > 800 - birdHeight:
            playing = False
            lost = True

        # if the forwardmost pipe is off screen then delete
        if pipes[len(pipes)-1].x < windowWidth - 200:
            pipes.append(pipe(randint(pipeGap + 50,windowHeight-200),windowWidth))


        # loop thru pipes
        for i in pipes:

            # move pipes
            i.x -= pipeSpeed
            
            # blit images
            screen.blit(pipeImg,(i.x,i.yBottom))
            screen.blit(pipeImgFlipped, (i.x,i.yTop))

            # when off screen delete
            if i.x < 0 - pipeWidth:
                pipes.remove(pipes[0])
            
            if not i.pointScored and i.x + pipeWidth < birdX:
                i.pointScored = True
                score += 1

        # score onto screen
        score_label = font.render("Score: " + str(score),1,(255,255,255))
        screen.blit(score_label, (10, 10))

        # bird onto screen
        screen.blit(birdImg,(b1.x,b1.y))

        # make sure timing is right
        clock.tick(gameSpeed)

        # final update to the screen
        pygame.display.update()

        # the game is paused at the start screen
        while pause:
            events = pygame.event.get()
            for event in events:
            # if x button pressed stop
                if event.type == pygame.QUIT:
                    running = False
                    pause = False
                    playing = False
                # if key is pressed
                if event.type == pygame.KEYDOWN:
                    # if space is pressed
                    if event.key == pygame.K_SPACE:
                        pause = False