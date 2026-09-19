import pygame
from sys import exit # terminate the program
import random

GAME_WIDTH = 750
GAME_HEIGHT = 250

class Block(pygame.Rect): #inherits from pygame.Rect
    def __init__(self, coordinates, size, image):
        pygame.Rect.__init__(self, coordinates, size)
        self.image = image 
        self.velocity_x = 0
        self.velocity_y = 0

#load the image
DINO_IMAGE = pygame.transform.scale(pygame.image.load("dino.png"), (88,94)) #width, height
DINO_DEAD_IMAGE = pygame.transform.scale(pygame.image.load("dino-dead.png"), (88,94)) 
GAME_OVER_IMAGE = pygame.transform.scale(pygame.image.load("game-over.png"),(120, 90))
CACTUS1_IMAGE = pygame.transform.scale(pygame.image.load("cactus1.png"), (34,70))
CACTUS2_IMAGE = pygame.transform.scale(pygame.image.load("cactus2.png"), (69,70))
CACTUS3_IMAGE = pygame.transform.scale(pygame.image.load("cactus3.png"), (102,70))
CACTUS_IMAGES = [CACTUS1_IMAGE, CACTUS2_IMAGE, CACTUS3_IMAGE]

pygame.init()                                                #needed to initialize pygame
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))  #create game window
pygame.display.set_caption("Chrome Dinosaur Game")           #title of the window
clock = pygame.time.Clock()                                  #used for the frame rate
GAME_FONT = pygame.font.SysFont("Courier", 20)

VELOCITY_X = -8   #Left
VELOCITY_Y = -10  #Up
GRAVITY = 0.4

#dino = pygame.Rect(50, 50, 88, 94)
dino = Block((50, GAME_HEIGHT - DINO_IMAGE.get_height()), DINO_IMAGE.get_size(), DINO_IMAGE)
text = Block((GAME_WIDTH//2 - GAME_OVER_IMAGE.get_width()//2, GAME_HEIGHT//2 - GAME_OVER_IMAGE.get_height()//2), GAME_OVER_IMAGE.get_size(), GAME_OVER_IMAGE)
cactus_list = []
last_place_cactus_time = 0
game_over = False
score = 0 

def place_cactus():
    random_cactus_image = random.choice(CACTUS_IMAGES)  #select a value from the list
    random_cactus = Block((GAME_WIDTH, GAME_HEIGHT-random_cactus_image.get_height()), random_cactus_image.get_size(), random_cactus_image)
    random_cactus.velocity_x = VELOCITY_X
    cactus_list.append(random_cactus)

def move():
    global cactus_list, game_over, score, text

    score += 1

    dino.velocity_y += GRAVITY
    dino.y += dino.velocity_y
    if dino.y >= GAME_HEIGHT - dino.height :
        dino.y = GAME_HEIGHT - dino.height

    for cactus in cactus_list:
        cactus.x += cactus.velocity_x
        if dino.colliderect(cactus) :   #caollison 
            game_over = True
            dino.image = DINO_DEAD_IMAGE


    cactus_list = [cactus for cactus in cactus_list if cactus.x + cactus.width > 0] #filtering the cactus getting out of screen 


def draw():
    window.fill("gray")
    window.blit(dino.image, dino) #Draw the image stored in DINO_IMAGE onto the window surface at the position specified by dino

    for cactus in cactus_list:
        window.blit(cactus.image, cactus)

    text_render = GAME_FONT.render(str(score), True, "black")
    window.blit(text_render, (5, 20))

#game loop
while True: 
    for event in pygame.event.get():   #listen for all user events (button, key, mouse)
        if event.type == pygame.QUIT:  #user clicks on X button of window
            pygame.quit()              #exit pygame
            exit()                     #terminate the python program completely

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    cactus_list.clear()
                    game_over = False
                    dino.y = GAME_HEIGHT - dino.height 
                    dino.velocity_y = 0
                    dino.image = DINO_IMAGE
                
                elif dino.y >= GAME_HEIGHT - dino.height: #only on ground
                    dino.velocity_y = VELOCITY_Y

    now = pygame.time.get_ticks() #nbr miliseconds since the start
    if now  - last_place_cactus_time >= 1000: # 1000ms = 1s
        place_cactus()
        last_place_cactus_time = now

    if not game_over:
        #print(len(cactus_list))
        move()
        draw()
        pygame.display.update()        #constantly refresh the game window
        clock.tick(60)                 #60 frames/second refreshing  (fps)
    else :
        window.blit(text.image, text)
        pygame.display.update()
