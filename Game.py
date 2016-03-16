import pygame
import time
import random
import sys,os
import math
import sqlite3

def textObjects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def largeMessageDisplay(text, display_width, display_height):
    largeText = pygame.font.Font("freesansbold.ttf", 135)
    textSurf, textRect = textObjects(text, largeText, white)
    textRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(2)

def smallMessageDisplay(text, lineNumber, display_width):
    smallText = pygame.font.Font("freesansbold.ttf", 16)
    textSurf, textRect = textObjects(text, smallText, white)
    textRect.center = ((display_width-60), 15 + (15*lineNumber))
    gameDisplay.blit(textSurf, textRect)
    
def drawObject(myObject, x, y):
    gameDisplay.blit(myObject,(x,y))

def loadBulletInfoIntomyProjectilesMatrix(gunType, belongsToEnemy, dx, difficultySelection, display_height):
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

def enemyMovementAI(enemyInfo, display_width, display_height):
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

def handleKeyPresses(fromWhere, ammo, currentGun, myProjectiles, rocketAccel, x, y, rocketWidth, difficultySelection, screenSizeSelection, displayType, display_height):
    #HANDLE KEY PRESS/RELEASE/USER ACTIONS
    keys = pygame.key.get_pressed()
    exiting = False
    enterPressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exiting = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and fromWhere == "Game":
            myMenu = mainMenu("Pause", screenSizeSelection, difficultySelection, displayType)
            difficultySelection, screenSizeSelection, displayType, exiting = myMenu.displayMenu()
            del myMenu
            #TO DO: TEST IF RESOLUTION WAS REDUCED BECAUSE PLAYER COULD NOW BE OUTSIDE OF SCREEN BOUNDS
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
            enterPressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and ammo >0: #MAKE USER NEED TO PRESS SPACE OVER AND OVER TO FIRE
            ammo = ammo - 1
            bulletProperties = loadBulletInfoIntomyProjectilesMatrix(currentGun, False, 0, difficultySelection, display_height)
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

def addGameObjects(enemiesAlive, currentLevel, currentGun, myEnemies, starProbabilitySpace, starDensity, starMoveSpeed, myProjectiles, display_width):
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

def movePlayer(x, y, rocketWidth, rocketHeight, rocketXDelta, rocketYDelta, display_width, display_height):
    #TEST FOR PLAYER ATTEMPTING TO TRAVEL BEYOND SCREEN BOUNDS
    if (x + rocketWidth + rocketXDelta > display_width) or (x + rocketXDelta < 0):
        rocketXDelta = 0
    if (y + rocketYDelta <0) or (y + rocketHeight + rocketYDelta > display_height):
        rocketYDelta = 0
    x = x + rocketXDelta
    y = y + rocketYDelta
    return x, y

def moveAndDrawProjectilesAndEnemies(myProjectiles, myEnemies, myHealth, score, enemiesAlive, x, y, rocketWidth, rocketHeight, difficultySelection, display_width, display_height):
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
                        myProjectiles[i][10] = enemyMovementAI(myProjectiles[i], display_width, display_height)
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
                bulletProperties = loadBulletInfoIntomyProjectilesMatrix(myEnemies[i][1], True, myEnemies[i][8], difficultySelection, display_height) #if the enemy is attacking, then load the bullet in the projectile matrix
                myProjectiles.append([bulletProperties[0], myEnemies[i][6] + (myEnemies[i][10]/2) - (bulletProperties[1]/2), myEnemies[i][7] , bulletProperties[1], bulletProperties[2], bulletProperties[3], bulletProperties[4], bulletProperties[5], bulletProperties[6], bulletProperties[7], bulletProperties[8]])
            myEnemies[i][6] = myEnemies[i][6] + myEnemies[i][8] #move this enemy
            myEnemies[i][7] = myEnemies[i][7] + myEnemies[i][9]
            drawFromFile(myEnemies[i][5], myEnemies[i][6], myEnemies[i][7])
            myEnemies[i] = enemyMovementAI(myEnemies[i], display_width, display_height) #establish this enemy's next move
    #delete enemies that were flagged for completion
    for i in xrange(len(myDeleteList)):
        del myEnemies[myDeleteList[i]-i]
    return myProjectiles, myEnemies, myHealth, score, enemiesAlive, y

def testIfPlayerLost(myHealth, exiting, score, display_width, display_height):
    lost = False
    if myHealth <= 0:
        lost = True
        largeMessageDisplay("YOU LOSE", display_width, display_height)
        gameDisplay.fill(black)
        largeMessageDisplay(str(score) + " pts", display_width, display_height)
    return lost

def drawFromFile(myFile, x, y):
    if myFile == "Ufo.png":
        drawObject(UFO, x, y)
    if myFile == "Blue Bomber.png":
        drawObject(BlueBomber, x, y)
    if myFile == "H Jet.png":
        drawObject(HJet, x, y)
    
    objectToDraw = pygame.image.load(myFile)
    drawObject(objectToDraw, x, y)

def drawGameStats(myHealth, ammo, currentLevel, score, display_width):
    smallMessageDisplay("Health: " + str(myHealth), 0, display_width)
    smallMessageDisplay("Ammo: " + str(ammo), 1, display_width)
    smallMessageDisplay("Level: " + str(currentLevel), 2, display_width)
    smallMessageDisplay("Score: " + str(score), 3, display_width)

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

class mainMenu(object):
    def __init__(self, menuType, screenSizeSelection, difficultySelection, displayType):
        self.menuType = menuType
        self.screenSizeSelection = screenSizeSelection
        self.difficultySelection = difficultySelection
        self.displayType = displayType
        self.menuDirectory = "Main"
        self.menuJustOpened = True
        self.difficultyChoices = ["Easy", "Medium", "Hard", "Expert", "You already lost lol"]
        self.score = 0
        self.myHealth = 100
        self.currentLevel = 0
        self.enemiesAlive = 1
        self.starDensity = .1 #PROBABILITY A NEW LINE CONTAINS A STAR x100%
        self.starProbabilitySpace = 1000 #IF STARDENSITY = .5, THEN 50% PROBABILITY NEW LINE WILL CONTAIN STAR. RAND # GENERATOR WOULD HAVE TO GENERATE 1 THROUGH (.5*1000) FOR .5 PROB TO BE TRUE
        self.maximumStarMoveSpeed = 4.1
        self.numberOfStarSpeeds = 16
        self.starMoveSpeed = self.maximumStarMoveSpeed
        self.exiting = False
        self.menuSelectionIndex = 6
        self.ammo = 0
        self.rocketXDelta = 0
        self.rocketYDelta = 0
        self.rocketYDeltaWas = 0
        self.rocketXDeltaWas = 0
        self.rocketWidth = 48
        self.rocketHeight = 66
        self.myProjectiles = []
        self.myEnemies = []
        self.currentGun = ""
        self.rocketAccel = 25
        allResolutionsAvail = pygame.display.list_modes()
        allResolutionsAvail.sort()
        self.display_width = allResolutionsAvail[screenSizeSelection][0]
        self.display_height = allResolutionsAvail[screenSizeSelection][1]
        if displayType == "Full Screen":
            self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height), pygame.FULLSCREEN)
        else:
            self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        self.x = (self.display_width/2)-(self.rocketWidth/2)
        self.y = (self.display_height-self.rocketHeight)
        self.highScores = loadHighScores()
        self.colorIntensity = 255
        self.colorIntensityDirection = 5

    def displayMenu(self):
        while self.exiting == False:
            if self.colorIntensity + self.colorIntensityDirection > 255:
                self.colorIntensityDirection = -5
            elif self.colorIntensity + self.colorIntensityDirection < 64:
                self.colorIntensityDirection = 5
            self.colorIntensity = self.colorIntensity + self.colorIntensityDirection
            self.smallText = pygame.font.Font("freesansbold.ttf", 24)
            self.largeText = pygame.font.Font("freesansbold.ttf", 48)
            self.textSurf, self.textRect = textObjects("Spacing Out", self.largeText, white)
            self.textRect.center = ((self.display_width/2), (25))
            self.gameDisplay.blit(self.textSurf, self.textRect)
            if self.menuType == "Pause":
                self.textSurf, self.textRect = textObjects("-Paused-", self.smallText, white)
                self.textRect.center = ((self.display_width/2), (75))
                self.gameDisplay.blit(self.textSurf, self.textRect)
                
            self.exiting, self.ammo, self.myProjectiles, self.rocketXDelta, self.rocketYDelta, self.enterPressed, self.screenSizeSelection, self.displayType = handleKeyPresses("Main Menu", self.ammo, self.currentGun, self.myProjectiles, self.rocketAccel, self.x, self.y, self.rocketWidth, self.difficultySelection, self.screenSizeSelection, self.displayType, self.display_height)
            self.currentLevel, self.currentGun, self.enemiesAlive, self.myEnemies, self.myProjectiles = addGameObjects(
                self.enemiesAlive, self.currentLevel, self.currentGun, self.myEnemies, self.starProbabilitySpace, self.starDensity, self.starMoveSpeed, self.myProjectiles, self.display_width)
            self.starMoveSpeed = adjustStarMoveSpeed(self.maximumStarMoveSpeed, self.numberOfStarSpeeds)
            self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.y = moveAndDrawProjectilesAndEnemies(
                self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.x, self.y, self.rocketWidth, self.rocketHeight, self.difficultySelection, self.display_width, self.display_height)
            drawObject(myCharacter, self.x, self.y)
            if self.menuDirectory == "Main":
                for self.i in xrange(7):
                    self.rgb = (255, 255, 255)
                    if self.i == self.menuSelectionIndex:
                        self.rgb = (self.colorIntensity, 0, 0)
                    if self.i == 6:
                        if self.menuType == "Pause":
                            self.text = "Resume"
                        else:
                            self.text = "Play"
                    if self.i == 5:
                        self.text = "Difficulty: " + self.difficultyChoices[self.difficultySelection]
                        if self.menuType == "Pause":
                            self.tempRGB = (self.rgb[0]*.25, self.rgb[1]*.25, self.rgb[2]*.25)
                            self.rgb = self.tempRGB
                    if self.i == 4:
                        self.text = "High Scores"
                    if self.i == 3:
                        self.text = "How To Play"
                    if self.i == 2:
                        self.text = "Settings"
                    if self.i == 1:
                        self.text = "Credits"
                    if self.i == 0:
                        self.text = "Quit"
                    self.textSurf, self.textRect = textObjects(self.text, self.smallText, self.rgb)
                    self.textRect.center = ((self.display_width/2), (self.display_height/2 - self.i*(self.rocketAccel)))
                    self.gameDisplay.blit(self.textSurf, self.textRect)
                if self.menuJustOpened == False:
                    if self.rocketYDelta == self.rocketAccel and self.rocketYDeltaWas == 0 and self.menuSelectionIndex >0:
                        self.menuSelectionIndex = self.menuSelectionIndex - 1
                        if self.menuSelectionIndex == 5 and self.menuType == "Pause":
                            self.menuSelectionIndex = self.menuSelectionIndex - 1
                    if self.rocketYDelta == -self.rocketAccel and self.rocketYDeltaWas == 0 and self.menuSelectionIndex < 6:
                        self.menuSelectionIndex = self.menuSelectionIndex + 1
                        if self.menuSelectionIndex == 5 and self.menuType == "Pause":
                            self.menuSelectionIndex = self.menuSelectionIndex + 1    
                    if ((self.rocketXDelta == self.rocketAccel and self.rocketXDeltaWas == 0) or (self.enterPressed == True)) and self.menuSelectionIndex == 5:
                        self.difficultySelection = (self.difficultySelection + 1) %len(self.difficultyChoices)
                    if (self.rocketXDelta == -self.rocketAccel and self.rocketXDeltaWas == 0) and self.menuSelectionIndex == 5:
                        self.difficultySelection = (self.difficultySelection - 1) %len(self.difficultyChoices)
                    if self.enterPressed == True and self.menuSelectionIndex == 2:
                        self.menuDirectory = "Settings"
                        self.menuSelectionIndex = 4
                    if self.enterPressed == True and self.menuSelectionIndex == 6:
                        return self.difficultySelection, self.screenSizeSelection, self.displayType, self.exiting
                    if self.enterPressed == True and self.menuSelectionIndex == 0:
                        self.exiting = True
                self.menuJustOpened = False
            elif self.menuDirectory == "Settings":
                self.fullScreenWindowChanged = False
                self.screenSizeChoices = pygame.display.list_modes()
                self.screenSizeChoices.sort()
                for self.i in xrange(5):
                    if self.i == 4:
                        self.text = "Screen Size: " + str(self.screenSizeChoices[self.screenSizeSelection][0]) + "x" + str(self.screenSizeChoices[self.screenSizeSelection][1])
                    if self.i == 3:
                        self.text = "Screen: " + self.displayType
                    if self.i == 2:
                        self.text = "Music Volume: 100"
                    if self.i == 1:
                        self.text = "SFX Volume: 100"
                    if self.i == 0:
                        self.text = "Go Back"
                    if self.i == self.menuSelectionIndex:
                        self.rgb = (self.colorIntensity, 0, 0)
                    else:
                        self.rgb = (255, 255, 255)
                    self.textSurf, self.textRect = textObjects(self.text, self.smallText, self.rgb)
                    self.textRect.center = ((self.display_width/2), (self.display_height/2 - self.i*(self.rocketAccel)))
                    self.gameDisplay.blit(self.textSurf, self.textRect)
            
                if self.rocketYDelta == self.rocketAccel and self.rocketYDeltaWas == 0 and self.menuSelectionIndex >0:
                    self.menuSelectionIndex = self.menuSelectionIndex - 1
                if self.rocketYDelta == -self.rocketAccel and self.rocketYDeltaWas == 0 and self.menuSelectionIndex < 4:
                    self.menuSelectionIndex = self.menuSelectionIndex + 1
                if ((self.rocketXDelta == self.rocketAccel and self.rocketXDeltaWas == 0) or (self.enterPressed == True)) and self.menuSelectionIndex == 4:
                    self.screenSizeSelection = (self.screenSizeSelection + 1) %len(self.screenSizeChoices)
                if (self.rocketXDelta == -self.rocketAccel and self.rocketXDeltaWas == 0) and self.menuSelectionIndex == 4:
                    self.screenSizeSelection = (self.screenSizeSelection - 1) %len(self.screenSizeChoices)
                if (self.enterPressed == True or (abs(self.rocketXDelta) == self.rocketAccel and self.rocketXDeltaWas == 0))and self.menuSelectionIndex == 3:
                    if self.displayType == "Window":
                        self.displayType = "Full Screen"
                    else:
                        self.displayType = "Window"
                    self.fullScreenWindowChanged = True
                if ((((self.rocketXDelta == self.rocketAccel and self.rocketXDeltaWas == 0) or (self.enterPressed == True)) and self.menuSelectionIndex == 4) or ((self.rocketXDelta == -self.rocketAccel and self.rocketXDeltaWas == 0) and self.menuSelectionIndex == 4)) or self.fullScreenWindowChanged == True:
                    self.display_width = self.screenSizeChoices[self.screenSizeSelection][0]
                    self.display_height = self.screenSizeChoices[self.screenSizeSelection][1]
                    if self.displayType == "Window":
                        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
                    else:
                        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height), pygame.FULLSCREEN)
                    self.myProjectiles = []
                    self.x = (self.display_width/2)-(self.rocketWidth/2)
                    self.y = (self.display_height-self.rocketHeight)
                    self.fullScreenWindowChanged = False
                if self.enterPressed == True and self.menuSelectionIndex == 6:
                    gameLoop(self.difficultySelection, self.screenSizeSelection, self.displayType)
                if self.enterPressed == True and self.menuSelectionIndex == 0:
                    self.menuDirectory = "Main"
                    self.menuSelectionIndex = 2
            self.rocketYDeltaWas = self.rocketYDelta
            self.rocketXDeltaWas = self.rocketXDelta
            updateScreenAndLimitFPS(60)
            self.gameDisplay.fill(black)
        return self.difficultySelection, self.screenSizeSelection, self.displayType, self.exiting
   
def gameLoop(difficultySelection, screenSizeSelection, displayType):
    # INITIALIZATION
    allResolutionsAvail = pygame.display.list_modes()
    allResolutionsAvail.sort()
    display_width = allResolutionsAvail[screenSizeSelection][0]
    display_height = allResolutionsAvail[screenSizeSelection][1]
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
    x = (allResolutionsAvail[screenSizeSelection][0]/2)-(rocketWidth/2)
    y = (allResolutionsAvail[screenSizeSelection][1]-rocketHeight)
    # GAME LOOP
    while not exiting and lost == False:
        
        #TEST FOR CONDITIONS THAT PREVENT FUTURE USER ACTIONS

        #TEST FOR CONDITIONS THAT ALLOW FUTURE USER ACTIONS

        currentLevel, currentGun, enemiesAlive, myEnemies, myProjectiles = addGameObjects(
            enemiesAlive, currentLevel, currentGun, myEnemies, starProbabilitySpace, starDensity, starMoveSpeed, myProjectiles, allResolutionsAvail[screenSizeSelection][0])
        exiting, ammo, myProjectiles, rocketXDelta, rocketYDelta, enterPressed, screenSizeSelection, displayType = handleKeyPresses(
            "Game", ammo, currentGun, myProjectiles, rocketAccel, x, y, rocketWidth, difficultySelection, screenSizeSelection, displayType, allResolutionsAvail[screenSizeSelection][1]) 
        x, y = movePlayer(x, y, rocketWidth, rocketHeight, rocketXDelta, rocketYDelta, allResolutionsAvail[screenSizeSelection][0], allResolutionsAvail[screenSizeSelection][1])
        gameDisplay.fill(black)
        myProjectiles, myEnemies, myHealth, score, enemiesAlive, y = moveAndDrawProjectilesAndEnemies(
            myProjectiles, myEnemies, myHealth, score, enemiesAlive, x, y, rocketWidth, rocketHeight, difficultySelection, allResolutionsAvail[screenSizeSelection][0], allResolutionsAvail[screenSizeSelection][1])
        lost = testIfPlayerLost(myHealth, exiting, score, allResolutionsAvail[screenSizeSelection][0], allResolutionsAvail[screenSizeSelection][1])
        drawObject(myCharacter, x, y)
        drawGameStats(myHealth, ammo, currentLevel, score, allResolutionsAvail[screenSizeSelection][0])
        starMoveSpeed = adjustStarMoveSpeed(maximumStarMoveSpeed, numberOfStarSpeeds)
        updateScreenAndLimitFPS(60)
        
    #OUT OF THE GAME LOOP
    if lost == True:
        return  difficultySelection, screenSizeSelection, displayType, exiting
    return difficultySelection, screenSizeSelection, displayType, exiting

pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
clock = pygame.time.Clock()
allResolutionsAvail = pygame.display.list_modes()
allResolutionsAvail.sort()
display_width = allResolutionsAvail[(int(len(allResolutionsAvail)/2.0))][0]
display_height = allResolutionsAvail[(int(len(allResolutionsAvail)/2.0))][1]
myCharacter = pygame.image.load("Rocket.png")
UFO = pygame.image.load("Ufo.png")
BlueBomber = pygame.image.load("Blue Bomber.png")
HJet = pygame.image.load("H Jet.png")
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Spacing Out')

#myMenu = mainMenu("New Game", int(len(pygame.display.list_modes())/2.0), 0, "Window")
menuType = "New Game"
screenSizeSelection = int(len(allResolutionsAvail)/2.0)
difficultySelection = 0
displayType = "Window"
exiting = False

while exiting == False:
    myMenu = mainMenu(menuType, screenSizeSelection, difficultySelection, displayType)
    difficultySelection, screenSizeSelection, displayType, exiting = myMenu.displayMenu()
    del myMenu
    if exiting == False:
        difficultySelection, screenSizeSelection, displayType, exiting = gameLoop(difficultySelection, screenSizeSelection, displayType)

pygame.quit()
quit()
