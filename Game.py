import pygame
import time
import random
import sys,os
import math

def textObjects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def largeMessageDisplay(text):
    largeText = pygame.font.Font("freesansbold.ttf", 135)
    textSurf, textRect = textObjects(text, largeText, white)
    textRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(2)

def smallMessageDisplay(text, lineNumber):
    smallText = pygame.font.Font("freesansbold.ttf", 16)
    textSurf, textRect = textObjects(text, smallText, white)
    textRect.center = ((display_width-60), 15 + (15*lineNumber))
    gameDisplay.blit(textSurf, textRect)
    
    
def drawObject(myFile, x, y):
    myCharacter = pygame.image.load(myFile)
    gameDisplay.blit(myCharacter,(x,y))

def loadBulletInfoIntomyProjectilesMatrix(gunType, belongsToEnemy):
    if gunType == "Basic Gun":
        bulletWidth = 1
        bulletLength = 3
        speed = -10
        r = 128
        g = 128
        b = 255
        damage = 25
    if gunType == "Long Gun":
        bulletWidth = 2
        bulletLength = 6
        speed = -20
        r = 255
        g = 0
        b = 0
        damage = 34
    if gunType == "Laser Gun":
        bulletWidth = 3
        bulletLength = 100
        speed = -25
        r = 255
        g = 255
        b = 0
        damage = 50
    if gunType == "Plasma Gun":
        bulletWidth = 10
        bulletLength = 15
        speed = -25
        r = 0
        g = 128
        b = 255
        damage = 100
    if gunType == "Teleport":
        bulletWidth = 40
        bulletLength = 4000
        speed = -15
        r = 0
        g = 255
        b = 0
        damage = 40
    if belongsToEnemy == True:
        speed = -1 * speed
        damage = damage * .05
        returnString = "Enemy Bullet - "
    else:
        returnString = "My Bullet - "
    return [returnString + gunType, bulletWidth, bulletLength, r, g, b, speed, damage]

def enemy(species):
    speed = 0
    weapon = "Teleport"
    health = 100
    aggression = 1
    speed = 1
    img = "UFO.png"
    dx = 0
    dy = 0
    width = 0
    height = 0
    if species == 0:
        weapon = "Teleport"
        health = 33
        aggression = 1
        speed = 2
        img = "UFO.png"
        dx = speed
        dy = 0
        width = 52
        height = 40
    if species == 1:
        weapon = "Basic Gun"
        health = 66
        aggression = 2
        speed = 3
        img = "Blue Bomber.png"
        dx = speed
        dy = speed
        width = 47
        height = 46
    if species == 2:
        weapon = "Laser Gun"
        health = 100
        aggression = 3
        speed = 4
        img = "H Jet.png"
        dx = speed
        dy = speed
        width = 49
        height = 37
    x = random.randint(1, display_width - width - 10)
    y = 0
    return [species, weapon, health, aggression, speed, img, x, y, dx, dy, width, height]

def enemyMovementAI(enemyInfo):

    if enemyInfo[0] == 0 or enemyInfo[0] == 1:
        #This enemy is the UFO
        if enemyInfo[6] + enemyInfo[8] < 0:
            enemyInfo[8] = enemyInfo[4]
        elif enemyInfo[6] + enemyInfo[8] + enemyInfo[10] > display_width:
            enemyInfo[8] = -enemyInfo[4]
    if enemyInfo[0] == 1 or enemyInfo[0] == 2:
        #This enemy is the Blue Bomber
        if random.randint(1, 20) == 1:
            enemyInfo[9] = -enemyInfo[9]
        if(enemyInfo[7] + enemyInfo[9] + enemyInfo[11] > int(.2*display_height)) or (enemyInfo[7] + enemyInfo[9] < 0):
            enemyInfo[9] = -enemyInfo[9]
    if enemyInfo[0] == 2:
        #This enemy is the H Jet
        if random.randint(1, 20) == 1:
            enemyInfo[8] = -enemyInfo[8]
        if(enemyInfo[6] + enemyInfo[8] + enemyInfo[10] > display_width) or (enemyInfo[6] + enemyInfo[8] < 0):
            enemyInfo[8] = -enemyInfo[8]
    return enemyInfo

def enemyAttackAI(aggressionLevel):
    return random.randint(1, int((1/float(aggressionLevel)) * 120))

def gameLoop():
    # INITIALIZATION
    exiting = False
    lost = False
    rocketWidth = 48
    rocketHeight = 66
    ammo = 50000
    enemiesAlive = 0
    currentLevel = 0
    currentGun = "Long Gun"
    myHealth = 100
    myProjectiles = [] #[NAME, X1, Y1, WIDTH, HEIGHT, R, G, B, SPEED, 0]
    myEnemies = [] #[species, weapon, health, aggression, speed, img, x, y, dx, dy, width, height]
    minimumStarMoveSpeed = 1.05
    rocketAccel = 10
    rocketXDelta = 0
    rocketYDelta = 0
    starCount = 0
    starMoveSpeed = 5
    starDensity = .2 #PROBABILITY A NEW LINE CONTAINS A STAR x100%
    starProbabilitySpace = 1000 #IF STARDENSITY = .5, THEN 50% PROBABILITY NEW LINE WILL CONTAIN STAR. RAND # GENERATOR WOULD HAVE TO GENERATE 1 THROUGH (.5*1000) FOR .5 PROB TO BE TRUE
    score = 0
    x = (display_width/2)-(rocketWidth/2)
    y = (display_height-rocketHeight)
        
    # GAME LOOP
    while not exiting:
        
        #TEST FOR CONDITIONS THAT PREVENT FUTURE USER ACTIONS

        #TEST FOR CONDITIONS THAT ALLOW FUTURE USER ACTIONS

        #ADD ENEMIES
        if enemiesAlive == 0:
            currentLevel = currentLevel + 1
            if currentLevel >= 8:
                currentGun = "Plasma Gun"
            for i in xrange(currentLevel):
                enemiesAlive = enemiesAlive + 1
                myEnemies.append(enemy(min(random.randint(0, min(2,currentLevel)),2)))
        
        #ADD STARS
        if random.randint(1,starProbabilitySpace) in xrange(1, int(starDensity * starProbabilitySpace)+1):            
            rndNumb = random.randint(1, display_width)
                                    #NAME, X1,    Y1,WIDTH,HEIGHT,   R,   G,   B,    SPEED  NO VALUE THIS IS JUST TO KEEP ALL ROWS IN THE PROJECTILE ARRAY THE SAME LENGTH
            myProjectiles.append(["Star", rndNumb, 0, 1 , 1 , 255, 255, 255, starMoveSpeed, 0])
                  
        #HANDLE KEY PRESS/RELEASE/USER ACTIONS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exiting = True
                lost = False
            i = 0
            for i in xrange(2):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                    rocketXDelta = rocketAccel
                if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                    rocketXDelta = -rocketAccel
                if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                    rocketYDelta = -rocketAccel
                if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
                    rocketYDelta = rocketAccel
                if i <1:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            rocketXDelta = 0
                            rocketYDelta = 0
                    if keys[pygame.K_SPACE] and ammo >0:
                        ammo = ammo - 1
                        bulletProperties = loadBulletInfoIntomyProjectilesMatrix(currentGun, False)
                        myProjectiles.append([bulletProperties[0], x + (rocketWidth/2) - int((bulletProperties[1]/2)) , y , bulletProperties[1], bulletProperties[2], bulletProperties[3], bulletProperties[4], bulletProperties[5], bulletProperties[6], bulletProperties[7]])
                        #print "Firing! Damage: " + str(myProjectiles[len(myProjectiles)-1][9])
        #DRAW SCREEN/MOVEMENT/ANIMATIONS/CHARACTER/OBJECTS
        #COLLISION DETECTION/OBJECT DELETION/LOSE CHECKING
        #this is all done in 1 for loop because separating
        #these tasks out into multiple for loops takes longer execution time.
        #Looping through all graphics objects

        #TEST FOR PLAYER ATTEMPTING TO TRAVEL BEYOND SCREEN BOUNDS
        if (x + rocketWidth + rocketXDelta > display_width) or (x + rocketXDelta < 0):
            rocketXDelta = 0
        if (y + rocketYDelta <0) or (y + rocketHeight + rocketYDelta > display_height):
            rocketYDelta = 0
        
        x = x + rocketXDelta
        y = y + rocketYDelta
        gameDisplay.fill(black)
        
        myDeleteList = []
        for i in xrange(len(myProjectiles)): #for each bullet and star
            if (myProjectiles[i][0] == "Star" or str(myProjectiles[i][0])[:4] == "Enem"): #if this projectile is a star or enemy bullet (falls down),
                if myProjectiles[i][2] + myProjectiles[i][8] + 1 >= display_height: #if it's going beyond the bottom of the screen
                    myDeleteList.append(i) #flag it for deletion by putting it in a list which we later use to delete it from myProjectiles. Deleting now wreaks havoc on our for loop
                #otherwise if it's not going beyond the bottom of the screen, then if it's an enemy bullet that hit the user, then
                elif str(myProjectiles[i][0])[:4] == "Enem" and ((myProjectiles[i][1] + myProjectiles[i][3] >= x) and (myProjectiles[i][1] <= x + rocketWidth) and (myProjectiles[i][2] + myProjectiles[i][4] >= y) and (myProjectiles[i][2] <= y + rocketHeight)):
                    myHealth = myHealth - myProjectiles[i][9]
                    myDeleteList.append(i)
            elif str(myProjectiles[i][0])[:4] == "My B": #otherwise if it's actually user's bullet (goes up),
                if myProjectiles[i][2] + myProjectiles[i][8] - 1 < 0: #if it's going above the top of the screen,
                    myDeleteList.append(i) #flag this projectile for deletion
                else:
                    for j in xrange(len(myEnemies)): #with this bullet, for each enemy:
                        #if this bullet hit this enemy,
                        if ((myProjectiles[i][1] + myProjectiles[i][3] >= myEnemies[j][6]) and (myProjectiles[i][1] <= myEnemies[j][6] + myEnemies[j][10]) and (myProjectiles[i][2] + myProjectiles[i][4] >= myEnemies[j][7]) and (myProjectiles[i][2] <= myEnemies[j][7] + myEnemies[j][11])):
                            myEnemies[j][2] = myEnemies[j][2] - myProjectiles[i][9] #reduce enemy health
                            myDeleteList.append(i) #flag this bullet for deletion
            #move this projectile in the direction it needs to go
            myProjectiles[i][2] = myProjectiles[i][2] + myProjectiles[i][8]
            pygame.draw.polygon(gameDisplay, (myProjectiles[i][5], myProjectiles[i][6], myProjectiles[i][7]), ((myProjectiles[i][1], myProjectiles[i][2]), (myProjectiles[i][1] + myProjectiles[i][3], myProjectiles[i][2]),  (myProjectiles[i][1], myProjectiles[i][2] + myProjectiles[i][4]), (myProjectiles[i][1] + myProjectiles[i][3], myProjectiles[i][2] + myProjectiles[i][4])), 0)
            
        #delete those projectiles we flagged for deletion
        for i in xrange(len(myDeleteList)):
            del myProjectiles[myDeleteList[i]-i]
        
        myDeleteList = []
        for i in xrange(len(myEnemies)): #for each enemy
            if myEnemies[i][2] <= 0: #if this enemy's health is <= 0, then
                enemiesAlive = enemiesAlive - 1
                score = score + 1
                myDeleteList.append(i) #flag this enemy for deletion
            else:
                if enemyAttackAI(myEnemies[i][3]) == 1: #decide if enemy will attack
                    bulletProperties = loadBulletInfoIntomyProjectilesMatrix(myEnemies[i][1], True) #if the enemy is attacking, then load the bullet in the projectile matrix
                    myProjectiles.append([bulletProperties[0], myEnemies[i][6], myEnemies[i][7] , bulletProperties[1], bulletProperties[2], bulletProperties[3], bulletProperties[4], bulletProperties[5], bulletProperties[6], bulletProperties[7]])
                myEnemies[i][6] = myEnemies[i][6] + myEnemies[i][8] #move this enemy
                myEnemies[i][7] = myEnemies[i][7] + myEnemies[i][9]
                drawObject(myEnemies[i][5], myEnemies[i][6], myEnemies[i][7])
                myEnemies[i] = enemyMovementAI(myEnemies[i]) #establish this enemy's next move
        #delete enemies that were flagged for completion
        for i in xrange(len(myDeleteList)):
            del myEnemies[myDeleteList[i]-i]

        if myHealth <= 0:
            lost = True
            exiting = True
            largeMessageDisplay("YOU LOSE")
            gameDisplay.fill(black)
            largeMessageDisplay(str(score) + " pts")
        drawObject("Rocket.png", x, y)
        smallMessageDisplay("Health: " + str(myHealth), 0)
        smallMessageDisplay("Ammo: " + str(ammo), 1)
        smallMessageDisplay("Level: " + str(currentLevel), 2)
        smallMessageDisplay("Score: " + str(score), 3)
        starMoveSpeed = max(minimumStarMoveSpeed, starMoveSpeed - .05)
        pygame.display.update()
        clock.tick(60)
        
    #OUT OF THE GAME LOOP
    if lost == True:
        gameLoop()
    pygame.quit()
    quit()

pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
clock = pygame.time.Clock()
display_width = 1280
display_height = 720
myCharacter = ""
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Spacing Out')
gameLoop()
