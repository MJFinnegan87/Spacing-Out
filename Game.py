import pygame
import time
import random
import sys,os
import math
import sqlite3

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
    
def drawObject(myObject, x, y):
    gameDisplay.blit(myObject,(x,y))

def loadBulletInfoIntomyProjectilesMatrix(gunType, belongsToEnemy, dx, difficultySelection):
    if gunType == "Basic Gun":
        bulletWidth = 1
        bulletLength = 3
        speed = -10
        r = 128
        g = 128
        b = 255
        damage = 25
        dx = 0
    if gunType == "Long Gun":
        bulletWidth = 4
        bulletLength = 10
        speed = -20
        r = 255
        g = 0
        b = 0
        damage = 34
        dx = 0
    if gunType == "Laser Gun":
        bulletWidth = 3
        bulletLength = 100
        speed = -25
        r = 255
        g = 255
        b = 0
        damage = 50
        dx = 0
    if gunType == "Plasma Gun":
        bulletWidth = 10
        bulletLength = 15
        speed = -25
        r = 0
        g = 128
        b = 255
        damage = 100
        dx = 0
    if gunType == "Teleport":
        bulletWidth = 40
        bulletLength = display_height
        speed = 15
        r = 0
        g = 255
        b = 0
        damage = 40
    if belongsToEnemy == True:
        speed = -speed
        damage = damage * (.05 * (1+difficultySelection))
        returnString = "Enemy Bullet - "
    else:
        returnString = "My Bullet - "
    return [returnString + gunType, bulletWidth, bulletLength, r, g, b, speed, damage, dx]

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
    if enemyInfo[0] == "Enemy Bullet - Teleport": #Here, we're moving the teleport bullet like an enemy, since it needs to move with the UFO
        if (enemyInfo[1] - ((enemy(0)[10] - enemyInfo[3])/2.0)) + enemy(0)[10] + enemyInfo[10] > display_width or enemyInfo[1] - ((enemy(0)[10] - enemyInfo[3])/2.0) + enemyInfo[10] <0:
            enemyInfo[10] = -enemyInfo[10]
        return enemyInfo[10]
    else: #Otherwise, if we're not dealing with the teleport bullet, we're dealing with an actual enemy object:
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
            if random.randint(1, 40) == 1:
                enemyInfo[8] = -enemyInfo[8]
            if(enemyInfo[6] + enemyInfo[8] + enemyInfo[10] > display_width) or (enemyInfo[6] + enemyInfo[8] < 0):
                enemyInfo[8] = -enemyInfo[8]
        return enemyInfo

def enemyAttackAI(aggressionLevel, difficultySelection):
    return random.randint(1, int((1/float(aggressionLevel)) * (120/float(1.0 + difficultySelection))))

def handleKeyPresses(fromWhere, ammo, currentGun, myProjectiles, rocketAccel, x, y, rocketWidth, difficultySelection, screenSizeSelection, displayType):
    #HANDLE KEY PRESS/RELEASE/USER ACTIONS
    keys = pygame.key.get_pressed()
    exiting = False
    enterPressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exiting = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and fromWhere == "Game":
            screenSizeSelection, displayType = mainMenu("Pause", screenSizeSelection, difficultySelection, displayType)
            #TO DO: TEST IF RESOLUTION WAS REDUCED BECAUSE PLAYER COULD NOW BE OUTSIDE OF SCREEN BOUNDS
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
            enterPressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and ammo >0: #MAKE USER NEED TO PRESS SPACE OVER AND OVER TO FIRE
            ammo = ammo - 1
            bulletProperties = loadBulletInfoIntomyProjectilesMatrix(currentGun, False, 0, difficultySelection)
            myProjectiles.append([bulletProperties[0], x + (rocketWidth/2) - int((bulletProperties[1]/2)) , y , bulletProperties[1], bulletProperties[2], bulletProperties[3], bulletProperties[4], bulletProperties[5], bulletProperties[6], bulletProperties[7], 0])
            #print "Firing! Damage: " + str(myProjectiles[len(myProjectiles)-1][9])
    rocketXDelta = 0
    rocketYDelta = 0
    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]: #WHEREAS DIRECTION KEYS CAN BE HELD DOWN
        rocketXDelta = rocketAccel
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        rocketXDelta = -rocketAccel
    if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        rocketYDelta = -rocketAccel
    if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
        rocketYDelta = rocketAccel
    return exiting, ammo, myProjectiles, rocketXDelta, rocketYDelta, enterPressed, screenSizeSelection, displayType

def addGameObjects(enemiesAlive, currentLevel, currentGun, myEnemies, starProbabilitySpace, starDensity, starMoveSpeed, myProjectiles):
    #ADD ENEMIES
    if enemiesAlive == 0:
        currentLevel = currentLevel + 1
        if currentLevel >= 8:
            currentGun = "Plasma Gun"
        for i in xrange(currentLevel):
            enemiesAlive = enemiesAlive + 1
            myEnemies.append(enemy(random.randint(0, min(currentLevel-1,2))))

    #ADD STARS
    if random.randint(1,starProbabilitySpace) in xrange(1, int(starDensity * starProbabilitySpace)+1):
        rndNumb = random.randint(1, display_width)
                                #NAME, X1,    Y1,WIDTH,HEIGHT,   R,   G,   B,    SPEED  NO VALUE THIS IS JUST TO KEEP ALL ROWS IN THE PROJECTILE ARRAY THE SAME LENGTH
        myProjectiles.append(["Star", rndNumb, 0, 1 , 1 , 255, 255, 255, starMoveSpeed, 0, 0])
    return currentLevel, currentGun, enemiesAlive, myEnemies, myProjectiles

def movePlayer(x, y, rocketWidth, rocketHeight, rocketXDelta, rocketYDelta):
    #TEST FOR PLAYER ATTEMPTING TO TRAVEL BEYOND SCREEN BOUNDS
    if (x + rocketWidth + rocketXDelta > display_width) or (x + rocketXDelta < 0):
        rocketXDelta = 0
    if (y + rocketYDelta <0) or (y + rocketHeight + rocketYDelta > display_height):
        rocketYDelta = 0
    x = x + rocketXDelta
    y = y + rocketYDelta
    return x, y

def moveAndDrawProjectilesAndEnemies(myProjectiles, myEnemies, myHealth, score, enemiesAlive, x, y, rocketWidth, rocketHeight, difficultySelection):
    myDeleteList = []
    
    for i in xrange(len(myProjectiles)): #for each bullet and star
        if (myProjectiles[i][0] == "Star" or str(myProjectiles[i][0])[:4] == "Enem"): #if this projectile is a star or enemy bullet,
            if myProjectiles[i][2] + myProjectiles[i][8] + 1 >= display_height or myProjectiles[i][2] + myProjectiles[i][4] + myProjectiles[i][8] -1 <= 0: #if it's going beyond the top/bottom of the screen
                myDeleteList.append(i) #flag it for deletion by putting it in a list which we later use to delete it from myProjectiles. Deleting now wreaks havoc on our for loop
            else:
                hit = False
                #otherwise if it's not going beyond the screen limits, then if it's an enemy bullet that hit the user, then
                if str(myProjectiles[i][0])[:4] == "Enem" and ((myProjectiles[i][1] + myProjectiles[i][3] >= x) and (myProjectiles[i][1] <= x + rocketWidth) and (myProjectiles[i][2] + myProjectiles[i][4] >= y) and (myProjectiles[i][2] <= y + rocketHeight)):
                    myHealth = myHealth - myProjectiles[i][9]
                    myDeleteList.append(i)
                    hit = True
                if (str(myProjectiles[i][0]) == "Enemy Bullet - Teleport"):
                    if hit == True:
                        y = max(0, y - (display_height/4))
                    else:
                        myProjectiles[i][10] = enemyMovementAI(myProjectiles[i])
                        myProjectiles[i][1] = myProjectiles[i][1] + myProjectiles[i][10]
        elif str(myProjectiles[i][0])[:4] == "My B": #otherwise if it's actually user's bullet
            if myProjectiles[i][2] + myProjectiles[i][8] - 1 < 0: #if it's going above the top of the screen,
                myDeleteList.append(i) #flag this projectile for deletion
            else:
                for j in xrange(len(myEnemies)): #with this bullet, for each enemy:
                    #if this bullet hit this enemy,                                                                                                                                                                                                                                             bulletx              +   bullet width        enemyx                 bulletx               enemyx            + enemywidth            bullety           +  bulletheight                                     enemyy                  bullety                                        enemyy             +enemyheight
                    if ((myProjectiles[i][1] + myProjectiles[i][3] >= myEnemies[j][6]) and (myProjectiles[i][1] <= myEnemies[j][6] + myEnemies[j][10]) and (myProjectiles[i][2] + myProjectiles[i][4] >= myEnemies[j][7]) and (myProjectiles[i][2] <= myEnemies[j][7] + myEnemies[j][11])) or ((myProjectiles[i][1] + myProjectiles[i][3] >= myEnemies[j][6]) and (myProjectiles[i][1] <= myEnemies[j][6] + myEnemies[j][10]) and (myProjectiles[i][2] + myProjectiles[i][4] + (myProjectiles[i][8]/2) >= myEnemies[j][7]) and (myProjectiles[i][2] + (myProjectiles[i][8]/2) <= myEnemies[j][7] + myEnemies[j][11])):
                        myEnemies[j][2] = myEnemies[j][2] - myProjectiles[i][9] #reduce enemy health
                        myDeleteList.append(i) #flag this bullet for deletion
        #move this projectile in the direction it needs to go
        myProjectiles[i][2] = myProjectiles[i][2] + myProjectiles[i][8]
        if (str(myProjectiles[i][0])[:4] == "My B"):
                                #SURFACE, (R,G,B), ((X1Y1), (X2Y1), (X2Y2), (X1Y2))
            pygame.draw.polygon(gameDisplay, (myProjectiles[i][5], myProjectiles[i][6], myProjectiles[i][7]), ((myProjectiles[i][1], myProjectiles[i][2] + myProjectiles[i][4]), (myProjectiles[i][1] + (myProjectiles[i][3]), myProjectiles[i][2] + myProjectiles[i][4]),  (myProjectiles[i][1] + (myProjectiles[i][3]/2), myProjectiles[i][2]), (myProjectiles[i][1] + (myProjectiles[i][3]/2), myProjectiles[i][2])), 0)
        elif (str(myProjectiles[i][0]) == "Enemy Bullet - Teleport"):
            pygame.draw.polygon(gameDisplay, (myProjectiles[i][5], myProjectiles[i][6], myProjectiles[i][7]), ((myProjectiles[i][1], max(myProjectiles[i][2] + myProjectiles[i][4], enemy(0)[11])), (myProjectiles[i][1] + (myProjectiles[i][3]), max(myProjectiles[i][2] + myProjectiles[i][4], enemy(0)[11])),  (myProjectiles[i][1] + (myProjectiles[i][3]/2), max(myProjectiles[i][2], enemy(0)[11])), (myProjectiles[i][1] + (myProjectiles[i][3]/2), max(myProjectiles[i][2], enemy(0)[11]))), 0)
        else:
            pygame.draw.polygon(gameDisplay, (myProjectiles[i][5], myProjectiles[i][6], myProjectiles[i][7]), ((myProjectiles[i][1], myProjectiles[i][2]), (myProjectiles[i][1] + (myProjectiles[i][3]), myProjectiles[i][2]),  (myProjectiles[i][1] + (myProjectiles[i][3]/2), myProjectiles[i][2] + myProjectiles[i][4]), (myProjectiles[i][1] + (myProjectiles[i][3]/2), myProjectiles[i][2] + myProjectiles[i][4])), 0)
        
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
            if enemyAttackAI(myEnemies[i][3], difficultySelection) == 1: #decide if enemy will attack
                bulletProperties = loadBulletInfoIntomyProjectilesMatrix(myEnemies[i][1], True, myEnemies[i][8], difficultySelection) #if the enemy is attacking, then load the bullet in the projectile matrix
                myProjectiles.append([bulletProperties[0], myEnemies[i][6] + (myEnemies[i][10]/2) - (bulletProperties[1]/2), myEnemies[i][7] , bulletProperties[1], bulletProperties[2], bulletProperties[3], bulletProperties[4], bulletProperties[5], bulletProperties[6], bulletProperties[7], bulletProperties[8]])
            myEnemies[i][6] = myEnemies[i][6] + myEnemies[i][8] #move this enemy
            myEnemies[i][7] = myEnemies[i][7] + myEnemies[i][9]
            drawFromFile(myEnemies[i][5], myEnemies[i][6], myEnemies[i][7])
            myEnemies[i] = enemyMovementAI(myEnemies[i]) #establish this enemy's next move
    #delete enemies that were flagged for completion
    for i in xrange(len(myDeleteList)):
        del myEnemies[myDeleteList[i]-i]
    return myProjectiles, myEnemies, myHealth, score, enemiesAlive, y

def testIfPlayerLost(myHealth, exiting, score):
    lost = False
    if myHealth <= 0:
        lost = True
        exiting = True
        largeMessageDisplay("YOU LOSE")
        gameDisplay.fill(black)
        largeMessageDisplay(str(score) + " pts")
    return lost, exiting

def drawFromFile(myFile, x, y):
    if myFile == "Ufo.png":
        drawObject(UFO, x, y)
    if myFile == "Blue Bomber.png":
        drawObject(BlueBomber, x, y)
    if myFile == "H Jet.png":
        drawObject(HJet, x, y)
    
    objectToDraw = pygame.image.load(myFile)
    drawObject(objectToDraw, x, y)

def drawGameStats(myHealth, ammo, currentLevel, score):
    smallMessageDisplay("Health: " + str(myHealth), 0)
    smallMessageDisplay("Ammo: " + str(ammo), 1)
    smallMessageDisplay("Level: " + str(currentLevel), 2)
    smallMessageDisplay("Score: " + str(score), 3)

def adjustStarMoveSpeed(maximumStarMoveSpeed, numberOfStarSpeeds):
    return ((1/float(numberOfStarSpeeds))*random.randint(1,numberOfStarSpeeds)) * maximumStarMoveSpeed

def updateScreenAndLimitFPS(FPSLimit):
    pygame.display.update()
    clock.tick(FPSLimit)

def fillInBlankHighScores(highScoresArray):
    iNeedThisManyMoreBlankSlots = 10 - len(highScoresArray)
    i = 0
    for row in xrange(iNeedThisManyMoreBlankSlots):
        i = i + 1
        highScoresArray.append([i, "-", 0, "", ""])
    return highScoresArray

def loadHighScores():
    connection = sqlite3.connect("High_Scores.db")
    highScoresArray = []
    try:
        c = connection.cursor()
        c.execute("""
        SELECT * FROM HighScoreTable ORDER BY scoreRecordPK
        """)
        for row in c.fetchall():
            highScoresArray.append([row(0), row(1), row(2), row(3), row(4)])
    except:
        connection = sqlite3.connect("High_Scores.db")
        c = connection.cursor()
        c.execute("DROP TABLE IF EXISTS HighScoreTable")
        c.execute("CREATE TABLE HighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
        fillInBlankHighScores(highScoresArray)
        updateHighScores(highScoresArray)
    connection.close()
    return highScoresArray

def updateHighScores(highScoresArray):
    connection = sqlite3.connect("High_Scores.db")
    c = connection.cursor()
    c.execute("DROP TABLE IF EXISTS HighScoreTable")
    c.execute("CREATE TABLE HighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
    i = -1
    for row in highScoresArray:
        i = i + 1
        c.execute("INSERT INTO HighScoreTable Values(?, ?, ?, ?, ?)", tuple((highScoresArray[i][0], highScoresArray[i][1], highScoresArray[i][2], highScoresArray[i][3], highScoresArray[i][4])))
    connection.commit()
    connection.close()

def mainMenu(menuType, screenSizeSelection, difficultySelection, displayType):
    menuDirectory = "Main"
    menuJustOpened = True
    difficultyChoices = ["Easy", "Medium", "Hard", "Expert", "You already lost lol"]
    score = 0
    myHealth = 100
    currentLevel = 0
    enemiesAlive = 1
    starDensity = .1 #PROBABILITY A NEW LINE CONTAINS A STAR x100%
    starProbabilitySpace = 1000 #IF STARDENSITY = .5, THEN 50% PROBABILITY NEW LINE WILL CONTAIN STAR. RAND # GENERATOR WOULD HAVE TO GENERATE 1 THROUGH (.5*1000) FOR .5 PROB TO BE TRUE
    maximumStarMoveSpeed = 4.1
    numberOfStarSpeeds = 16
    starMoveSpeed = maximumStarMoveSpeed
    exiting = False
    menuSelectionIndex = 6
    ammo = 0
    rocketXDelta = 0
    rocketYDelta = 0
    rocketYDeltaWas = 0
    rocketXDeltaWas = 0
    rocketWidth = 48
    rocketHeight = 66
    myProjectiles = []
    myEnemies = []
    currentGun = ""
    rocketAccel = 25
    global display_width
    global display_height
    global gameDisplay
    x = (display_width/2)-(rocketWidth/2)
    y = (display_height-rocketHeight)
    highScores = loadHighScores()
    colorIntensity = 255
    colorIntensityDirection = 5
    while exiting == False:
        if colorIntensity + colorIntensityDirection > 255:
            colorIntensityDirection = -5
        elif colorIntensity + colorIntensityDirection < 64:
            colorIntensityDirection = 5
        colorIntensity = colorIntensity + colorIntensityDirection
        smallText = pygame.font.Font("freesansbold.ttf", 24)
        largeText = pygame.font.Font("freesansbold.ttf", 48)
        textSurf, textRect = textObjects("Spacing Out", largeText, white)
        textRect.center = ((display_width/2), (25))
        gameDisplay.blit(textSurf, textRect)
        if menuType == "Pause":
            textSurf, textRect = textObjects("-Paused-", smallText, white)
            textRect.center = ((display_width/2), (75))
            gameDisplay.blit(textSurf, textRect)
            
        exiting, ammo, myProjectiles, rocketXDelta, rocketYDelta, enterPressed, screenSizeSelection, displayType = handleKeyPresses("Main Menu", ammo, currentGun, myProjectiles, rocketAccel, x, y, rocketWidth, difficultySelection, screenSizeSelection, displayType)
        currentLevel, currentGun, enemiesAlive, myEnemies, myProjectiles = addGameObjects(
            enemiesAlive, currentLevel, currentGun, myEnemies, starProbabilitySpace, starDensity, starMoveSpeed, myProjectiles)
        starMoveSpeed = adjustStarMoveSpeed(maximumStarMoveSpeed, numberOfStarSpeeds)
        myProjectiles, myEnemies, myHealth, score, enemiesAlive, y = moveAndDrawProjectilesAndEnemies(
            myProjectiles, myEnemies, myHealth, score, enemiesAlive, x, y, rocketWidth, rocketHeight, difficultySelection)
        drawObject(myCharacter, x, y)
        if menuDirectory == "Main":
            for i in xrange(7):
                rgb = (255, 255, 255)
                if i == menuSelectionIndex:
                    rgb = (colorIntensity, 0, 0)
                if i == 6:
                    if menuType == "Pause":
                        text = "Resume"
                    else:
                        text = "Play"
                if i == 5:
                    text = "Difficulty: " + difficultyChoices[difficultySelection]
                    if menuType == "Pause":
                        tempRGB = (rgb[0]*.25, rgb[1]*.25, rgb[2]*.25)
                        rgb = tempRGB
                if i == 4:
                    text = "High Scores"
                if i == 3:
                    text = "How To Play"
                if i == 2:
                    text = "Settings"
                if i == 1:
                    text = "Credits"
                if i == 0:
                    text = "Quit"
                textSurf, textRect = textObjects(text, smallText, rgb)
                textRect.center = ((display_width/2), (display_height/2 - i*(rocketAccel)))
                gameDisplay.blit(textSurf, textRect)
            if menuJustOpened == False:
                if rocketYDelta == rocketAccel and rocketYDeltaWas == 0 and menuSelectionIndex >0:
                    menuSelectionIndex = menuSelectionIndex - 1
                    if menuSelectionIndex == 5 and menuType == "Pause":
                        menuSelectionIndex = menuSelectionIndex - 1
                if rocketYDelta == -rocketAccel and rocketYDeltaWas == 0 and menuSelectionIndex < 6:
                    menuSelectionIndex = menuSelectionIndex + 1
                    if menuSelectionIndex == 5 and menuType == "Pause":
                        menuSelectionIndex = menuSelectionIndex + 1                
                if ((rocketXDelta == rocketAccel and rocketXDeltaWas == 0) or (enterPressed == True)) and menuSelectionIndex == 5:
                    difficultySelection = (difficultySelection + 1) %len(difficultyChoices)
                if (rocketXDelta == -rocketAccel and rocketXDeltaWas == 0) and menuSelectionIndex == 5:
                    difficultySelection = (difficultySelection - 1) %len(difficultyChoices)
                if enterPressed == True and menuSelectionIndex == 2:
                    menuDirectory = "Settings"
                    menuSelectionIndex = 4
                if enterPressed == True and menuSelectionIndex == 6:
                    if menuType == "Pause":
                        return screenSizeSelection, displayType
                    else:
                        gameLoop(difficultySelection, screenSizeSelection, displayType)
                if enterPressed == True and menuSelectionIndex == 0:
                    exiting = True
            menuJustOpened = False
        elif menuDirectory == "Settings":
            fullScreenWindowChanged = False
            screenSizeChoices = pygame.display.list_modes()
            screenSizeChoices.sort()
            for i in xrange(5):
                if i == 4:
                    text = "Screen Size: " + str(screenSizeChoices[screenSizeSelection][0]) + "x" + str(screenSizeChoices[screenSizeSelection][1])
                if i == 3:
                    text = "Screen: " + displayType
                if i == 2:
                    text = "Music Volume: 100"
                if i == 1:
                    text = "SFX Volume: 100"
                if i == 0:
                    text = "Go Back"
                if i == menuSelectionIndex:
                    rgb = (colorIntensity, 0, 0)
                else:
                    rgb = (255, 255, 255)
                textSurf, textRect = textObjects(text, smallText, rgb)
                textRect.center = ((display_width/2), (display_height/2 - i*(rocketAccel)))
                gameDisplay.blit(textSurf, textRect)
        
            if rocketYDelta == rocketAccel and rocketYDeltaWas == 0 and menuSelectionIndex >0:
                menuSelectionIndex = menuSelectionIndex - 1
            if rocketYDelta == -rocketAccel and rocketYDeltaWas == 0 and menuSelectionIndex < 4:
                menuSelectionIndex = menuSelectionIndex + 1
            if ((rocketXDelta == rocketAccel and rocketXDeltaWas == 0) or (enterPressed == True)) and menuSelectionIndex == 4:
                screenSizeSelection = (screenSizeSelection + 1) %len(screenSizeChoices)
            if (rocketXDelta == -rocketAccel and rocketXDeltaWas == 0) and menuSelectionIndex == 4:
                screenSizeSelection = (screenSizeSelection - 1) %len(screenSizeChoices)
            if (enterPressed == True or (abs(rocketXDelta) == rocketAccel and rocketXDeltaWas == 0))and menuSelectionIndex == 3:
                if displayType == "Window":
                    displayType = "Full Screen"
                else:
                    displayType = "Window"
                fullScreenWindowChanged = True
            if ((((rocketXDelta == rocketAccel and rocketXDeltaWas == 0) or (enterPressed == True)) and menuSelectionIndex == 4) or ((rocketXDelta == -rocketAccel and rocketXDeltaWas == 0) and menuSelectionIndex == 4)) or fullScreenWindowChanged == True:
                display_width = screenSizeChoices[screenSizeSelection][0]
                display_height = screenSizeChoices[screenSizeSelection][1] - 25
                if displayType == "Window":
                    gameDisplay = pygame.display.set_mode((display_width, display_height))
                else:
                    gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
                myProjectiles = []
                x = (display_width/2)-(rocketWidth/2)
                y = (display_height-rocketHeight)
                fullScreenWindowChanged = False
            if enterPressed == True and menuSelectionIndex == 6:
                gameLoop(difficultySelection, screenSizeSelection, displayType)
            if enterPressed == True and menuSelectionIndex == 0:
                menuDirectory = "Main"
                menuSelectionIndex = 2
        rocketYDeltaWas = rocketYDelta
        rocketXDeltaWas = rocketXDelta
        updateScreenAndLimitFPS(60)
        gameDisplay.fill(black)
    pygame.quit()
    quit()
   
def gameLoop(difficultySelection, screenSizeSelection, displayType):
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
    maximumStarMoveSpeed = 4.1
    rocketAccel = 10
    rocketXDelta = 0
    rocketYDelta = 0
    starCount = 0
    starMoveSpeed = maximumStarMoveSpeed
    numberOfStarSpeeds = 16
    starDensity = .1 #PROBABILITY A NEW LINE CONTAINS A STAR x100%
    starProbabilitySpace = 1000 #IF STARDENSITY = .5, THEN 50% PROBABILITY NEW LINE WILL CONTAIN STAR. RAND # GENERATOR WOULD HAVE TO GENERATE 1 THROUGH (.5*1000) FOR .5 PROB TO BE TRUE
    score = 0
    x = (display_width/2)-(rocketWidth/2)
    y = (display_height-rocketHeight)
        
    # GAME LOOP
    while not exiting:
        
        #TEST FOR CONDITIONS THAT PREVENT FUTURE USER ACTIONS

        #TEST FOR CONDITIONS THAT ALLOW FUTURE USER ACTIONS

        currentLevel, currentGun, enemiesAlive, myEnemies, myProjectiles = addGameObjects(
            enemiesAlive, currentLevel, currentGun, myEnemies, starProbabilitySpace, starDensity, starMoveSpeed, myProjectiles)
        exiting, ammo, myProjectiles, rocketXDelta, rocketYDelta, enterPressed, screenSizeSelection, displayType = handleKeyPresses(
            "Game", ammo, currentGun, myProjectiles, rocketAccel, x, y, rocketWidth, difficultySelection, screenSizeSelection, displayType) 
        x, y = movePlayer(x, y, rocketWidth, rocketHeight, rocketXDelta, rocketYDelta)
        gameDisplay.fill(black)
        myProjectiles, myEnemies, myHealth, score, enemiesAlive, y = moveAndDrawProjectilesAndEnemies(
            myProjectiles, myEnemies, myHealth, score, enemiesAlive, x, y, rocketWidth, rocketHeight, difficultySelection)
        lost, exiting = testIfPlayerLost(myHealth, exiting, score)
        drawObject(myCharacter, x, y)
        drawGameStats(myHealth, ammo, currentLevel, score)
        starMoveSpeed = adjustStarMoveSpeed(maximumStarMoveSpeed, numberOfStarSpeeds)
        updateScreenAndLimitFPS(60)
        
    #OUT OF THE GAME LOOP
    if lost == True:
        mainMenu("New Game", screenSizeSelection, difficultySelection, displayType)
    pygame.quit()
    quit()

pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
clock = pygame.time.Clock()
display_width = pygame.display.list_modes()[(int(len(pygame.display.list_modes())/2.0))][0]
display_height = pygame.display.list_modes()[(int(len(pygame.display.list_modes())/2.0))][1] - 25
myCharacter = pygame.image.load("Rocket.png")
UFO = pygame.image.load("Ufo.png")
BlueBomber = pygame.image.load("Blue Bomber.png")
HJet = pygame.image.load("H Jet.png")
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Spacing Out')
mainMenu("New Game", int(len(pygame.display.list_modes())/2.0), 0, "Window")
gameLoop()
