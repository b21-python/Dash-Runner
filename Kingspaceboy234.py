#Import pygame module
import pygame
from pygame.locals import *
import random

#Initialize the pygame
pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(),36) 
####constants####
#Colors
GREEN = (50, 168, 212) 
ORANGE = (255, 102, 201) 
#Accessors
X = 0
Y = 1  # Move enemies to follow the player

    
W = 2
H = 3

####game variables####for
playerSprite = pygame.image.load("dude.png")

#Player state       X   Y   W   H
player = { "Area":[30, 30, 80, 80], "Color":ORANGE, "Sprite":playerSprite, "Speed":20, "Health": 200}

    #game window size
width = 640
height = 480

####game variables####
sixseven = pygame.image.load("dude.png")

#game window
screen = pygame.display.set_mode([width, height])

obstacles = [Rect (160, 0, 20, 120), Rect (480, 0, 50, 120), Rect(130, 400, 100, 120), Rect(320, 200, 100, 120), Rect (10, 0, 20, 20)]


#       left-a right-d up-w  down-s
keys = { K_a:0, K_d:0, K_w:0, K_s:0 }

#keeps time for game
gameClock = pygame.time.Clock()

gameActive = True

enemyLocations = []
spawnLocaion = [640, 240]
enemySpeed = 5
        

#Main Game loop.  The game runs until the user quits
while gameActive:

    #Limit to 60 FPS
    gameClock.tick(30)

    #Fill screen with bg color
    screen.fill(GREEN)


    pygame.draw.rect(screen, player["Color"], player["Area"])
   
    
    for ob in obstacles:
        pygame.draw.rect(screen, "blue", ob)
        
    for enemy in enemyLocations:
        pygame.draw.rect(screen, "red", [enemy[X], enemy[Y], 10, 10])
        
    text_surface = font.render(str(player["Health"]), True, (0, 0, 0))
    screen.blit(text_surface, dest=(0,0))
    
        
    #Draw arena (surface)
    pygame.display.update()
    

    ##Loop over input to see if the keys w, s, a or d were pressed or released
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:            #A key was pressed
            keys[event.key] = player["Speed"]
        elif event.type == pygame.KEYUP:            #A key was released
            keys[event.key] = 0
        elif event.type == pygame.QUIT:             #The user quit
            gameActive = False

    #Determine new player position based on keyboard input
    xMovement = keys[K_d] - keys[K_a]
    yMovement = keys[K_s] - keys[K_w]
    updatedX = player["Area"][X] + xMovement
    updatedY = player["Area"][Y] + yMovement
    

      
    # Detect if the updated position intersects with any obstacles
    updatedPlayerRect = Rect(updatedX, updatedY, player["Area"][W], player["Area"][H])
    intersectsObstacles = updatedPlayerRect.collidelist(obstacles) != -1

    list_of_lists = [[1, 1, 1, 1], [2, 2, 2, 2]]
    indices1 = updatedPlayerRect.collidelistall(list_of_lists)

    #Update player position if new position is in bounds
    if not intersectsObstacles and updatedX >= 0 and updatedX + player["Area"][W] <= width:
        player["Area"][X] = updatedX 
    if not intersectsObstacles and updatedY >= 0 and updatedY + player["Area"][H] <= height:
        player["Area"][Y] = updatedY
    list = []
    # Move Y  # Move enemies to follow the player
    for enemy in enemyLocations:
        # Determine line of sight by drawing line between
        # enemy and player then test if it intersects with any obstacles
        enemyRect = Rect(enemy[X], enemy[Y], 10, 10)
        hasLineOfSight = True
        for ob in obstacles:
            if ob.clipline(enemyRect.center, updatedPlayerRect.center):
                hasLineOfSight = False
                break
        if updatedPlayerRect.colliderect(enemyRect):
            player["Health"] -=10
            print(player["Health"])
        else:
        #add the enemy to the list
            list.append(enemy)
        # if the enemy cannot see the player do not move it towards the player
        if not hasLineOfSight:
            continue

            list_of_lists = [[1, 1, 1, 1], [2, 2, 2, 2]]
            indices1 = updatedPlayerRect.collidelistall(list_of_lists)

        # Move X
        if player["Area"][X] < enemy[X]:
            enemy[X] -= enemySpeed
        elif player["Area"][X] > enemy[X]:
            enemy[X] += enemySpeed
        # Move Y
        if player["Area"][Y] < enemy[Y]:
            enemy[Y] -= enemySpeed
        elif player["Area"][Y] > enemy[Y]:
            enemy[Y] += enemySpeed
    enemyLocations = list
    # Spawn new enemies
    randval = random.randrange(60)
    if randval == 7:
        print ("spawn")          
        #  enemyLocations.append(spawnLocaion.copy())
        enemyLocations.append([width , random.randrange(height)])
#end game with false gameactive
    if (player["Health"]) <= 0:
    
        gameActive = False
        
while True:
    text_surface = font.render('Your run is OVER!', True, (0, 0, 0))
    screen.blit(text_surface, dest=(180,240))

    pygame.display.update()




#end pygame
pygame.quit()




 