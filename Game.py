import pygame
import time
import random
import sys,os
import math
import sqlite3

class gameEventHandler(object):
    def textObjects(self, text, font, color):
        self.text = text
        self.font = font
        self.color = color
        self.textSurface = font.render(self.text, True, self.color)
        return self.textSurface, self.textSurface.get_rect()

    def largeMessageDisplay(self, text, displayWidth, displayHeight):
        self.text = text
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.largeText = pygame.font.Font("freesansbold.ttf", 135)
        self.textSurf, self.textRect = self.textObjects(self.text, self.largeText, white)
        self.textRect.center = ((self.displayWidth/2), (self.displayHeight/2))
        gameDisplay.blit(self.textSurf, self.textRect)
        pygame.display.update()
        time.sleep(2)

    def smallMessageDisplay(self, text, lineNumber, displayWidth):
        self.text = text
        self.lineNumber = lineNumber
        self.displayWidth = displayWidth
        self.smallText = pygame.font.Font("freesansbold.ttf", 16)
        self.textSurf, self.textRect = self.textObjects(self.text, self.smallText, white)
        self.textRect.center = ((self.displayWidth-60), 15 + (15*self.lineNumber))
        gameDisplay.blit(self.textSurf, self.textRect)
        
    def drawObject(self, myObject, drawX, drawY):
        self.myObject = myObject
        gameDisplay.blit(self.myObject,(drawX, drawY))

    def drawFromFile(self, myFile, drawX, drawY):
        self.myFile = myFile
        if self.myFile == "UFO.png":
            self.objectToDraw = UFO
        if self.myFile == "Blue Bomber.png":
            self.objectToDraw = BlueBomber
        if self.myFile == "H Jet.png":
            self.objectToDraw = HJet
        self.drawObject(self.objectToDraw, drawX, drawY)

    def drawGameStats(self, myHealth, ammo, currentLevel, score, displayWidth):
        self.myHealth = myHealth
        self.ammo = ammo
        self.currentLevel = currentLevel
        self.score = score
        self.displayWidth = displayWidth
        self.smallMessageDisplay("Health: " + str(self.myHealth), 0, self.displayWidth)
        self.smallMessageDisplay("Ammo: " + str(self.ammo), 1, self.displayWidth)
        self.smallMessageDisplay("Level: " + str(self.currentLevel), 2, self.displayWidth)
        self.smallMessageDisplay("Score: " + str(self.score), 3, self.displayWidth)

    def updateScreenAndLimitFPS(self, FPSLimit):
        self.FPSLimit = FPSLimit
        pygame.display.update()
        clock.tick(self.FPSLimit)

    def loadBulletInfoIntomyProjectilesMatrix(self, gunType, belongsToEnemy, dx, difficultySelection, displayHeight):
        self.gunType = gunType
        self.belongsToEnemy = belongsToEnemy
        self.dx = dx
        self.difficultySelection = difficultySelection
        self.displayHeight = displayHeight
        if self.gunType == "Basic Gun":
            self.bulletWidth = 1
            self.bulletLength = 3
            self.speed = -10
            self.r = 128
            self.g = 128
            self.b = 255
            self.damage = 25
            self.dx = 0
        if self.gunType == "Long Gun":
            self.bulletWidth = 4
            self.bulletLength = 10
            self.speed = -20
            self.r = 255
            self.g = 0
            self.b = 0
            self.damage = 34
            self.dx = 0
        if self.gunType == "Laser Gun":
            self.bulletWidth = 3
            self.bulletLength = 100
            self.speed = -25
            self.r = 255
            self.g = 255
            self.b = 0
            self.damage = 50
            self.dx = 0
        if self.gunType == "Plasma Gun":
            self.bulletWidth = 10
            self.bulletLength = 15
            self.speed = -25
            self.r = 0
            self.g = 128
            self.b = 255
            self.damage = 100
            self.dx = 0
        if self.gunType == "Teleport":
            self.bulletWidth = 40
            self.bulletLength = self.displayHeight
            self.speed = 15
            self.r = 0
            self.g = 255
            self.b = 0
            self.damage = 40
        if self.belongsToEnemy == True:
            self.speed = -self.speed
            self.damage = self.damage * (.05 * (1+self.difficultySelection))
            self.returnString = "Enemy Bullet - "
        else:
            self.returnString = "My Bullet - "
        return [self.returnString + self.gunType, self.bulletWidth, self.bulletLength, self.r, self.g, self.b, self.speed, self.damage, self.dx]

    def enemy(self, species):
        self.species = species
        self.speed = 0
        self.weapon = "Teleport"
        self.health = 100
        self.aggression = 1
        self.speed = 1
        self.img = "UFO.png"
        self.dx = 0
        self.dy = 0
        self.width = 0
        self.height = 0
        if self.species == 0:
            self.weapon = "Teleport"
            self.health = 33
            self.aggression = 1
            self.speed = 2
            self.img = "UFO.png"
            self.dx = self.speed
            self.dy = 0
            self.width = 52
            self.height = 40
        if self.species == 1:
            self.weapon = "Basic Gun"
            self.health = 66
            self.aggression = 2
            self.speed = 3
            self.img = "Blue Bomber.png"
            self.dx = self.speed
            self.dy = self.speed
            self.width = 47
            self.height = 46
        if self.species == 2:
            self.weapon = "Laser Gun"
            self.health = 100
            self.aggression = 3
            self.speed = 4
            self.img = "H Jet.png"
            self.dx = self.speed
            self.dy = self.speed
            self.width = 49
            self.height = 37
        self.startingX = random.randint(1, self.displayWidth - self.width - 10)
        self.startingY = 0
        return [self.species, self.weapon, self.health, self.aggression, self.speed, self.img, self.startingX, self.startingY, self.dx, self.dy, self.width, self.height]

    def enemyMovementAI(self, enemyInfo, displayWidth, displayHeight):
        self.enemyInfo = enemyInfo
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        if self.enemyInfo[0] == "Enemy Bullet - Teleport": #Here, we're moving the teleport bullet like an enemy, since it needs to move with the UFO
            if (self.enemyInfo[1] - ((self.enemy(0)[10] - self.enemyInfo[3])/2.0)) + self.enemy(0)[10] + self.enemyInfo[10] > self.displayWidth or self.enemyInfo[1] - ((self.enemy(0)[10] - self.enemyInfo[3])/2.0) + self.enemyInfo[10] <0:
                self.enemyInfo[10] = -self.enemyInfo[10]
            return self.enemyInfo[10]
        else: #Otherwise, if we're not dealing with the teleport bullet, we're dealing with an actual enemy object:
            if self.enemyInfo[0] == 0 or self.enemyInfo[0] == 1:
                #This enemy is the UFO
                if self.enemyInfo[6] + self.enemyInfo[8] < 0:
                    self.enemyInfo[8] = self.enemyInfo[4]
                elif self.enemyInfo[6] + self.enemyInfo[8] + self.enemyInfo[10] > self.displayWidth:
                    self.enemyInfo[8] = -self.enemyInfo[4]
            if self.enemyInfo[0] == 1 or self.enemyInfo[0] == 2:
                #This enemy is the Blue Bomber
                if random.randint(1, 20) == 1:
                    self.enemyInfo[9] = -self.enemyInfo[9]
                if(self.enemyInfo[7] + self.enemyInfo[9] + self.enemyInfo[11] > int(.2*self.displayHeight)) or (self.enemyInfo[7] + self.enemyInfo[9] < 0):
                    self.enemyInfo[9] = -self.enemyInfo[9]
            if self.enemyInfo[0] == 2:
                #This enemy is the H Jet
                if random.randint(1, 40) == 1:
                    self.enemyInfo[8] = -self.enemyInfo[8]
                if(self.enemyInfo[6] + self.enemyInfo[8] + self.enemyInfo[10] > self.displayWidth) or (self.enemyInfo[6] + self.enemyInfo[8] < 0):
                    self.enemyInfo[8] = -self.enemyInfo[8]
            return self.enemyInfo

    def enemyAttackAI(self, aggressionLevel, difficultySelection):
        self.aggressionLevel = aggressionLevel
        self.difficultySelection = difficultySelection
        return random.randint(1, int((1/float(self.aggressionLevel)) * (120/float(1.0 + self.difficultySelection))))

    def addGameObjects(self, enemiesAlive, currentLevel, currentGun, myEnemies, starProbabilitySpace, starDensity, starMoveSpeed, myProjectiles, displayWidth):
        self.enemiesAlive = enemiesAlive
        self.currentLevel = currentLevel
        self.currentGun = currentGun
        self.myEnemies = myEnemies
        self.starProbabilitySpace = starProbabilitySpace
        self.starDensity = starDensity
        self.starMoveSpeed = starMoveSpeed
        self.myProjectiles = myProjectiles
        self.displayWidth = displayWidth
        #ADD ENEMIES
        if self.enemiesAlive == 0:
            self.currentLevel = self.currentLevel + 1
            if self.currentLevel >= 8:
                self.currentGun = "Plasma Gun"
            for i in xrange(self.currentLevel):
                self.enemiesAlive = self.enemiesAlive + 1
                self.myEnemies.append(self.enemy(random.randint(0, min(self.currentLevel-1,2))))

        #ADD STARS
        if random.randint(1, self.starProbabilitySpace) in xrange(1, int(self.starDensity * self.starProbabilitySpace)+1):
            self.rndNumb = random.randint(1, self.displayWidth)
                                    #NAME, X1,    Y1,WIDTH,HEIGHT,   R,   G,   B,    SPEED  NO VALUE THIS IS JUST TO KEEP ALL ROWS IN THE PROJECTILE ARRAY THE SAME LENGTH
            self.myProjectiles.append(["Star", self.rndNumb, 0, 1 , 1 , 255, 255, 255, self.starMoveSpeed, 0, 0])
        return self.currentLevel, self.currentGun, self.enemiesAlive, self.myEnemies, self.myProjectiles

    def movePlayer(self, x, y, rocketWidth, rocketHeight, rocketXDelta, rocketYDelta, displayWidth, displayHeight):
        self.x = x
        self.y = y
        self.rocketWidth = rocketWidth
        self.rocketHeight = rocketHeight
        self.rocketXDelta = rocketXDelta
        self.rocketYDelta = rocketYDelta
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        #TEST FOR PLAYER ATTEMPTING TO TRAVEL BEYOND SCREEN BOUNDS
        if (self.x + self.rocketWidth + self.rocketXDelta > self.displayWidth) or (self.x + self.rocketXDelta < 0):
            self.rocketXDelta = 0
        if (self.y + self.rocketYDelta <0) or (self.y + self.rocketHeight + self.rocketYDelta > self.displayHeight):
            self.rocketYDelta = 0
        self.x = self.x + self.rocketXDelta
        self.y = self.y + self.rocketYDelta
        return self.x, self.y

    def moveAndDrawProjectilesAndEnemies(self, myProjectiles, myEnemies, myHealth, score, enemiesAlive, x, y, rocketWidth, rocketHeight, difficultySelection, displayWidth, displayHeight):
        self.myProjectiles = myProjectiles
        self.myEnemies = myEnemies
        self.myHealth = myHealth
        self.score = score
        self.enemiesAlive = enemiesAlive
        self.x = x
        self.y = y
        self.rocketWidth = rocketWidth
        self.rocketHeight = rocketHeight
        self.difficultySelection = difficultySelection
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.myDeleteList = []
        for self.i in xrange(len(self.myProjectiles)): #for each bullet and star
            if (self.myProjectiles[self.i][0] == "Star" or str(self.myProjectiles[self.i][0])[:4] == "Enem"): #if this projectile is a star or enemy bullet,
                if self.myProjectiles[self.i][2] + self.myProjectiles[self.i][8] + 1 >= self.displayHeight or self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4] + self.myProjectiles[self.i][8] -1 <= 0: #if it's going beyond the top/bottom of the screen
                    self.myDeleteList.append(self.i) #flag it for deletion by putting it in a list which we later use to delete it from myProjectiles. Deleting now wreaks havoc on our for loop
                else:
                    self.hit = False
                    #otherwise if it's not going beyond the screen limits, then if it's an enemy bullet that hit the user, then
                    if str(self.myProjectiles[self.i][0])[:4] == "Enem" and ((self.myProjectiles[self.i][1] + self.myProjectiles[self.i][3] >= x) and (self.myProjectiles[self.i][1] <= x + self.rocketWidth) and (self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4] >= self.y) and (self.myProjectiles[self.i][2] <= self.y + self.rocketHeight)):
                        self.myHealth = self.myHealth - self.myProjectiles[self.i][9]
                        self.myDeleteList.append(self.i)
                        self.hit = True
                    if (str(self.myProjectiles[self.i][0]) == "Enemy Bullet - Teleport"):
                        if self.hit == True:
                            self.y = max(0, self.y - (self.displayHeight/4))
                        else:
                            self.myProjectiles[self.i][10] = self.enemyMovementAI(self.myProjectiles[self.i], self.displayWidth, self.displayHeight)
                            self.myProjectiles[self.i][1] = self.myProjectiles[self.i][1] + self.myProjectiles[self.i][10]
            elif str(self.myProjectiles[self.i][0])[:4] == "My B": #otherwise if it's actually user's bullet
                if self.myProjectiles[self.i][2] + self.myProjectiles[self.i][8] - 1 < 0: #if it's going above the top of the screen,
                    self.myDeleteList.append(self.i) #flag this projectile for deletion
                else:
                    for self.j in xrange(len(self.myEnemies)): #with this bullet, for each enemy:
                        #if this bullet hit this enemy,                                                                                                                                                                                                                                             bulletx              +   bullet width        enemyx                 bulletx               enemyx            + enemywidth            bullety           +  bulletheight                                     enemyy                  bullety                                        enemyy             +enemyheight
                        if ((self.myProjectiles[self.i][1] + self.myProjectiles[self.i][3] >= self.myEnemies[self.j][6]) and (self.myProjectiles[self.i][1] <= self.myEnemies[self.j][6] + self.myEnemies[self.j][10]) and (self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4] >= self.myEnemies[self.j][7]) and (self.myProjectiles[self.i][2] <= self.myEnemies[self.j][7] + self.myEnemies[self.j][11])) or ((self.myProjectiles[self.i][1] + self.myProjectiles[self.i][3] >= self.myEnemies[self.j][6]) and (self.myProjectiles[self.i][1] <= self.myEnemies[self.j][6] + self.myEnemies[self.j][10]) and (self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4] + (self.myProjectiles[self.i][8]/2) >= self.myEnemies[self.j][7]) and (self.myProjectiles[self.i][2] + (self.myProjectiles[self.i][8]/2) <= self.myEnemies[self.j][7] + self.myEnemies[self.j][11])):
                            self.myEnemies[self.j][2] = self.myEnemies[self.j][2] - self.myProjectiles[self.i][9] #reduce enemy health
                            self.myDeleteList.append(self.i) #flag this bullet for deletion
            #move this projectile in the direction it needs to go
            self.myProjectiles[self.i][2] = self.myProjectiles[self.i][2] + self.myProjectiles[self.i][8]
            if (str(self.myProjectiles[self.i][0])[:4] == "My B"):
                                    #SURFACE, (R,G,B), ((X1Y1), (X2Y1), (X2Y2), (X1Y2))
                pygame.draw.polygon(gameDisplay, (self.myProjectiles[self.i][5], self.myProjectiles[self.i][6], self.myProjectiles[self.i][7]), ((self.myProjectiles[self.i][1], self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4]), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]), self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4]),  (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2), self.myProjectiles[self.i][2]), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2), self.myProjectiles[self.i][2])), 0)
            elif (str(self.myProjectiles[self.i][0]) == "Enemy Bullet - Teleport"):
                pygame.draw.polygon(gameDisplay, (self.myProjectiles[self.i][5], self.myProjectiles[self.i][6], self.myProjectiles[self.i][7]), ((self.myProjectiles[self.i][1], max(self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4], self.enemy(0)[11])), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]), max(self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4], self.enemy(0)[11])),  (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2), max(self.myProjectiles[self.i][2], self.enemy(0)[11])), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2), max(self.myProjectiles[self.i][2], self.enemy(0)[11]))), 0)
            else:
                pygame.draw.polygon(gameDisplay, (self.myProjectiles[self.i][5], self.myProjectiles[self.i][6], self.myProjectiles[self.i][7]), ((self.myProjectiles[self.i][1], self.myProjectiles[self.i][2]), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]), self.myProjectiles[self.i][2]),  (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2), self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4]), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2), self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4])), 0)
            
        #delete those projectiles we flagged for deletion
        for self.i in xrange(len(self.myDeleteList)):
            del self.myProjectiles[self.myDeleteList[self.i]-self.i]
        
        self.myDeleteList = []
        for self.i in xrange(len(self.myEnemies)): #for each enemy
            if self.myEnemies[self.i][2] <= 0: #if this enemy's health is <= 0, then
                self.enemiesAlive = self.enemiesAlive - 1
                self.score = self.score + 1
                self.myDeleteList.append(self.i) #flag this enemy for deletion
            else:
                if self.enemyAttackAI(self.myEnemies[self.i][3], self.difficultySelection) == 1: #decide if enemy will attack
                    self.bulletProperties = self.loadBulletInfoIntomyProjectilesMatrix(self.myEnemies[self.i][1], True, self.myEnemies[self.i][8], self.difficultySelection, self.displayHeight) #if the enemy is attacking, then load the bullet in the projectile matrix
                    self.myProjectiles.append([self.bulletProperties[0], self.myEnemies[self.i][6] + (self.myEnemies[self.i][10]/2) - (self.bulletProperties[1]/2), self.myEnemies[self.i][7] , self.bulletProperties[1], self.bulletProperties[2], self.bulletProperties[3], self.bulletProperties[4], self.bulletProperties[5], self.bulletProperties[6], self.bulletProperties[7], self.bulletProperties[8]])
                self.myEnemies[self.i][6] = self.myEnemies[self.i][6] + self.myEnemies[self.i][8] #move this enemy
                self.myEnemies[self.i][7] = self.myEnemies[self.i][7] + self.myEnemies[self.i][9]
                self.drawFromFile(self.myEnemies[self.i][5], self.myEnemies[self.i][6], self.myEnemies[self.i][7])
                self.myEnemies[self.i] = self.enemyMovementAI(self.myEnemies[self.i], self.displayWidth, self.displayHeight) #establish this enemy's next move
        #delete enemies that were flagged for completion
        for self.i in xrange(len(self.myDeleteList)):
            del self.myEnemies[self.myDeleteList[self.i]-self.i]
        return self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.y

    def testIfPlayerLost(self, myHealth, exiting, score, displayWidth, displayHeight):
        self.myHealth = myHealth
        self.exiting = exiting
        self.score = score
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.lost = False
        if self.myHealth <= 0:
            self.lost = True
            self.largeMessageDisplay("YOU LOSE", self.displayWidth, self.displayHeight)
            gameDisplay.fill(black)
            self.largeMessageDisplay(str(self.score) + " pts", self.displayWidth, self.displayHeight)
        return self.lost

    def adjustStarMoveSpeed(self, maximumStarMoveSpeed, numberOfStarSpeeds):
        self.maximumStarMoveSpeed = maximumStarMoveSpeed
        self.numberOfStarSpeeds = numberOfStarSpeeds
        return ((1/float(self.numberOfStarSpeeds))*random.randint(1,self.numberOfStarSpeeds)) * self.maximumStarMoveSpeed

    def handleKeyPresses(self, fromWhere, ammo, currentGun, myProjectiles, rocketAccel, x, y, rocketWidth, difficultySelection, screenSizeSelection, displayType, displayHeight):
        self.fromWhere = fromWhere
        self.ammo = ammo
        self.currentGun = currentGun
        self.myProjectiles = myProjectiles
        self.rocketAccel = rocketAccel
        self.x = x
        self.y = y
        self.rocketWidth = rocketWidth
        self.difficultySelection = difficultySelection
        self.screenSizeSelection = screenSizeSelection
        self.displayType = displayType
        self.displayHeight = displayHeight
        #HANDLE KEY PRESS/RELEASE/USER ACTIONS
        self.keys = pygame.key.get_pressed()
        self.exiting = False
        self.enterPressed = False
        for self.event in pygame.event.get():
            if self.event.type == pygame.QUIT:
                self.exiting = True
            if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_ESCAPE and self.fromWhere == "Game":
                self.myMenu = menuScreen("Pause", screenSizeSelection, difficultySelection, displayType)
                self.difficultySelection, self.screenSizeSelection, self.displayType, self.exiting = self.myMenu.displayMenuScreenAndHandleUserInput()
                del self.myMenu
                #TO DO: TEST IF RESOLUTION WAS REDUCED BECAUSE PLAYER COULD NOW BE OUTSIDE OF SCREEN BOUNDS
            if self.event.type == pygame.KEYDOWN and (self.event.key == pygame.K_KP_ENTER or self.event.key == pygame.K_RETURN):
                self.enterPressed = True
            if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_SPACE and self.ammo >0: #MAKE USER NEED TO PRESS SPACE OVER AND OVER TO FIRE
                self.ammo = self.ammo - 1
                self.bulletProperties = self.loadBulletInfoIntomyProjectilesMatrix(self.currentGun, False, 0, self.difficultySelection, self.displayHeight)
                self.myProjectiles.append([self.bulletProperties[0], x + (self.rocketWidth/2) - int((self.bulletProperties[1]/2)), self.y , self.bulletProperties[1], self.bulletProperties[2], self.bulletProperties[3], self.bulletProperties[4], self.bulletProperties[5], self.bulletProperties[6], self.bulletProperties[7], 0])
                #print "Firing! Damage: " + str(myProjectiles[len(myProjectiles)-1][9])
        self.rocketXDelta = 0
        self.rocketYDelta = 0
        if self.keys[pygame.K_RIGHT] and not self.keys[pygame.K_LEFT]: #WHEREAS DIRECTION KEYS CAN BE HELD DOWN
            self.rocketXDelta = self.rocketAccel
        if self.keys[pygame.K_LEFT] and not self.keys[pygame.K_RIGHT]:
            self.rocketXDelta = -self.rocketAccel
        if self.keys[pygame.K_UP] and not self.keys[pygame.K_DOWN]:
            self.rocketYDelta = -self.rocketAccel
        if self.keys[pygame.K_DOWN] and not self.keys[pygame.K_UP]:
            self.rocketYDelta = self.rocketAccel
        return self.exiting, self.ammo, self.myProjectiles, self.rocketXDelta, self.rocketYDelta, self.enterPressed, self.screenSizeSelection, self.displayType

class highScores(object):
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

class menuScreen(object):
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
        #allResolutionsAvail = pygame.display.list_modes()
        #allResolutionsAvail.sort()
        self.displayWidth = allResolutionsAvail[screenSizeSelection][0]
        self.displayHeight = allResolutionsAvail[screenSizeSelection][1]
        if displayType == "Full Screen":
            gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight), pygame.FULLSCREEN)
        else:
            gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        self.x = (self.displayWidth/2)-(self.rocketWidth/2)
        self.y = (self.displayHeight-self.rocketHeight)
        #self.highScores = loadHighScores()
        self.colorIntensity = 255
        self.colorIntensityDirection = 5
        self.startPlay = False
        self.menuGameEventHandler = gameEventHandler()
        self.screenMoveCounter = 0

    def displayMenuScreenAndHandleUserInput(self):
        while self.exiting == False and self.startPlay == False:
            self.displayTitle()
            self.selectionColorPulsate()
            self.handleMenuBackground()
            self.getKeyPress()
            if self.menuDirectory == "Main":
                self.displayMainMenu()
                if self.menuJustOpened == False:
                    self.handleUserInputMainMenu()
                self.menuJustOpened = False
            elif self.menuDirectory == "Settings":
                self.displaySettingsMenu()
                self.handleUserInputSettingsMenu()
            elif self.menuDirectory == "Credits":
                self.displayCreditsMenu()
                self.handleUserInputCreditsMenu()
            elif self.menuDirectory == "How To Play":
                self.displayHowToMenu()
                self.handleUserInputHowToMenu()
                
            self.rocketYDeltaWas = self.rocketYDelta
            self.rocketXDeltaWas = self.rocketXDelta
            self.menuGameEventHandler.updateScreenAndLimitFPS(60)
            gameDisplay.fill(black)
        return self.difficultySelection, self.screenSizeSelection, self.displayType, self.exiting
    
    def displayTitle(self):
        self.smallText = pygame.font.Font("freesansbold.ttf", 24)
        self.largeText = pygame.font.Font("freesansbold.ttf", 48)
        self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("Spacing Out", self.largeText, white)
        self.textRect.center = ((self.displayWidth/2), (self.screenMoveCounter + 25))
        gameDisplay.blit(self.textSurf, self.textRect)
        if self.menuType == "Pause":
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("-Paused-", self.smallText, white)
            self.textRect.center = ((self.displayWidth/2), (self.screenMoveCounter + 75))
            gameDisplay.blit(self.textSurf, self.textRect)

    def selectionColorPulsate(self):
        if self.colorIntensity + self.colorIntensityDirection > 255:
            self.colorIntensityDirection = -5
        elif self.colorIntensity + self.colorIntensityDirection < 64:
            self.colorIntensityDirection = 5
        self.colorIntensity = self.colorIntensity + self.colorIntensityDirection

    def handleMenuBackground(self):
        self.currentLevel, self.currentGun, self.enemiesAlive, self.myEnemies, self.myProjectiles = self.menuGameEventHandler.addGameObjects(
            self.enemiesAlive, self.currentLevel, self.currentGun, self.myEnemies, self.starProbabilitySpace, self.starDensity, self.starMoveSpeed, self.myProjectiles, self.displayWidth)
        self.starMoveSpeed = self.menuGameEventHandler.adjustStarMoveSpeed(self.maximumStarMoveSpeed, self.numberOfStarSpeeds)
        self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.y = self.menuGameEventHandler.moveAndDrawProjectilesAndEnemies(
            self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.x, self.y, self.rocketWidth, self.rocketHeight, self.difficultySelection, self.displayWidth, self.displayHeight)
        self.menuGameEventHandler.drawObject(myCharacter, self.x, self.y)

    def getKeyPress(self):
        self.exiting, self.ammo, self.myProjectiles, self.rocketXDelta, self.rocketYDelta, self.enterPressed, self.screenSizeSelection, self.displayType =  self.menuGameEventHandler.handleKeyPresses("Main Menu", self.ammo, self.currentGun, self.myProjectiles, self.rocketAccel, self.x, self.y, self.rocketWidth, self.difficultySelection, self.screenSizeSelection, self.displayType, self.displayHeight)

    def displayMainMenu(self):
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
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects(self.text, self.smallText, self.rgb)
            self.textRect.center = ((self.displayWidth/2), (self.displayHeight/2 - self.i*(self.rocketAccel) + self.screenMoveCounter))
            gameDisplay.blit(self.textSurf, self.textRect)

    def displaySettingsMenu(self):
        self.fullScreenWindowChanged = False
        self.screenSizeChoices = pygame.display.list_modes()
        self.screenSizeChoices.sort()
        for self.i in xrange(5):
            self.rgb = (255, 255, 255)
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
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects(self.text, self.smallText, self.rgb)
            self.textRect.center = ((self.displayWidth/2), (self.displayHeight/2 - self.i*(self.rocketAccel)))
            gameDisplay.blit(self.textSurf, self.textRect)

    def displayCreditsMenu(self):
        if self.screenMoveCounter < self.displayHeight:
            self.screenMoveCounter = self.screenMoveCounter + self.maximumStarMoveSpeed
            self.displayTitle()
            self.displayMainMenu()
    
        for self.i in xrange(3):
            self.rgb = (255, 255, 255)
            if self.i == 2:
                self.text = "Programming by Michael Finnegan"
            if self.i == 1:
                self.text = "Art by Michael Finnegan"
            if self.i == 0:
                self.text = "Music/SFX by Michael Finnegan"
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects(self.text, self.smallText, self.rgb)
            #self.textRect.center = ((self.displayWidth/2), (self.displayHeight/2 - self.i*(self.rocketAccel)))
            self.textRect.center = ((self.displayWidth/2), (self.i * 25 + self.screenMoveCounter - self.displayHeight/2))
            gameDisplay.blit(self.textSurf, self.textRect)

    def displayHowToMenu(self):
        if self.screenMoveCounter < self.displayHeight:
            self.screenMoveCounter = self.screenMoveCounter + self.maximumStarMoveSpeed
            self.displayTitle()
            self.displayMainMenu()
    
        for self.i in xrange(3):
            self.rgb = (255, 255, 255)
            if self.i == 2:
                self.text = "Escape key: pause game"
            if self.i == 1:
                self.text = "Space bar: shoot aliens"
            if self.i == 0:
                self.text = "Arrow keys Up, Down, Left, Right: fly spacecraft"
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects(self.text, self.smallText, self.rgb)
            #self.textRect.center = ((self.displayWidth/2), (self.displayHeight/2 - self.i*(self.rocketAccel)))
            self.textRect.center = ((self.displayWidth/2), (self.i * 25 + self.screenMoveCounter - self.displayHeight/2))
            gameDisplay.blit(self.textSurf, self.textRect)

    def handleUserInputMainMenu(self):
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
        if self.enterPressed == True and self.menuSelectionIndex == 1:
            self.menuDirectory = "Credits"
        if self.enterPressed == True and self.menuSelectionIndex == 3:
            self.menuDirectory = "How To Play"
        if self.enterPressed == True and self.menuSelectionIndex == 6:
            self.startPlay = True
        if self.enterPressed == True and self.menuSelectionIndex == 0:
            self.exiting = True

    def handleUserInputSettingsMenu(self):
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
            self.displayWidth = self.screenSizeChoices[self.screenSizeSelection][0]
            self.displayHeight = self.screenSizeChoices[self.screenSizeSelection][1]
            if self.displayType == "Window":
                gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
            else:
                gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight), pygame.FULLSCREEN)
            self.myProjectiles = []
            self.x = (self.displayWidth/2)-(self.rocketWidth/2)
            self.y = (self.displayHeight-self.rocketHeight)
            self.fullScreenWindowChanged = False
        if self.enterPressed == True and self.menuSelectionIndex == 0:
            self.menuDirectory = "Main"
            self.menuSelectionIndex = 2

    def handleUserInputCreditsMenu(self):
        if self.enterPressed == True:
            self.screenMoveCounter = 0
            self.menuDirectory = "Main"

    def handleUserInputHowToMenu(self):
        if self.enterPressed == True:
            self.screenMoveCounter = 0
            self.menuDirectory = "Main"
        
class gameScreen(object):
    def __init__(self, difficultySelection, screenSizeSelection, displayType):
        self.difficultySelection = difficultySelection
        self.screenSizeSelection = screenSizeSelection
        self.displayType = displayType
        self.allResolutionsAvail = pygame.display.list_modes()
        self.allResolutionsAvail.sort()
        self.displayWidth = self.allResolutionsAvail[self.screenSizeSelection][0]
        self.displayHeight = self.allResolutionsAvail[self.screenSizeSelection][1]
        self.exiting = False
        self.lost = False
        self.rocketWidth = 48
        self.rocketHeight = 66
        self.ammo = 50000
        self.enemiesAlive = 0
        self.currentLevel = 0
        self.currentGun = "Long Gun"
        self.myHealth = 100
        self.myProjectiles = [] #[NAME, X1, Y1, WIDTH, HEIGHT, R, G, B, SPEED, 0]
        self.myEnemies = [] #[species, weapon, health, aggression, speed, img, x, y, dx, dy, width, height]
        self.maximumStarMoveSpeed = 4.1
        self.rocketAccel = 10
        self.rocketXDelta = 0
        self.rocketYDelta = 0
        self.starCount = 0
        self.starMoveSpeed = self.maximumStarMoveSpeed
        self.numberOfStarSpeeds = 16
        self.starDensity = .1 #PROBABILITY A NEW LINE CONTAINS A STAR x100%
        self.starProbabilitySpace = 1000 #IF STARDENSITY = .5, THEN 50% PROBABILITY NEW LINE WILL CONTAIN STAR. RAND # GENERATOR WOULD HAVE TO GENERATE 1 THROUGH (.5*1000) FOR .5 PROB TO BE TRUE
        self.score = 0
        self.x = (self.allResolutionsAvail[self.screenSizeSelection][0]/2)-(self.rocketWidth/2)
        self.y = (self.allResolutionsAvail[self.screenSizeSelection][1]-self.rocketHeight)
        self.myGameEventHandler = gameEventHandler()
        
    def gameLoop(self):
        while self.exiting == False and self.lost == False:
        
            #TEST FOR CONDITIONS THAT PREVENT FUTURE USER ACTIONS

            #TEST FOR CONDITIONS THAT ALLOW FUTURE USER ACTIONS

            self.currentLevel, self.currentGun, self.enemiesAlive, self.myEnemies, self.myProjectiles = self.myGameEventHandler.addGameObjects(
                self.enemiesAlive, self.currentLevel, self.currentGun, self.myEnemies, self.starProbabilitySpace, self.starDensity, self.starMoveSpeed, self.myProjectiles, self.allResolutionsAvail[self.screenSizeSelection][0])
            self.exiting, self.ammo, self.myProjectiles, self.rocketXDelta, self.rocketYDelta, self.enterPressed, self.screenSizeSelection, self.displayType = self.myGameEventHandler.handleKeyPresses(
                "Game", self.ammo, self.currentGun, self.myProjectiles, self.rocketAccel, self.x, self.y, self.rocketWidth, self.difficultySelection, self.screenSizeSelection, self.displayType, self.allResolutionsAvail[self.screenSizeSelection][1]) 
            self.x, self.y = self.myGameEventHandler.movePlayer(self.x, self.y, self.rocketWidth, self.rocketHeight, self.rocketXDelta, self.rocketYDelta, self.allResolutionsAvail[self.screenSizeSelection][0], self.allResolutionsAvail[self.screenSizeSelection][1])
            gameDisplay.fill(black)
            self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.y = self.myGameEventHandler.moveAndDrawProjectilesAndEnemies(
                self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.x, self.y, self.rocketWidth, self.rocketHeight, self.difficultySelection, self.allResolutionsAvail[self.screenSizeSelection][0], self.allResolutionsAvail[self.screenSizeSelection][1])
            self.lost = self.myGameEventHandler.testIfPlayerLost(self.myHealth, self.exiting, self.score, self.allResolutionsAvail[self.screenSizeSelection][0], self.allResolutionsAvail[self.screenSizeSelection][1])
            self.myGameEventHandler.drawObject(myCharacter, self.x, self.y)
            self.myGameEventHandler.drawGameStats(self.myHealth, self.ammo, self.currentLevel, self.score, self.allResolutionsAvail[self.screenSizeSelection][0])
            self.starMoveSpeed = self.myGameEventHandler.adjustStarMoveSpeed(self.maximumStarMoveSpeed, self.numberOfStarSpeeds)
            self.myGameEventHandler.updateScreenAndLimitFPS(60)
        
        ##OUT OF THE GAME LOOP
        del self.myGameEventHandler
        return self.difficultySelection, self.screenSizeSelection, self.displayType, self.exiting

pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
clock = pygame.time.Clock()
allResolutionsAvail = pygame.display.list_modes()
allResolutionsAvail.sort()
displayWidth = allResolutionsAvail[(int(len(allResolutionsAvail)/2.0))][0]
displayHeight = allResolutionsAvail[(int(len(allResolutionsAvail)/2.0))][1]
myCharacter = pygame.image.load("Rocket.png")
UFO = pygame.image.load("Ufo.png")
BlueBomber = pygame.image.load("Blue Bomber.png")
HJet = pygame.image.load("H Jet.png")
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Spacing Out')

menuType = "New Game"
screenSizeSelection = int(len(allResolutionsAvail)/2.0)
difficultySelection = 0
displayType = "Window"
exiting = False

while exiting == False:
    myMenu = menuScreen(menuType, screenSizeSelection, difficultySelection, displayType)
    difficultySelection, screenSizeSelection, displayType, exiting = myMenu.displayMenuScreenAndHandleUserInput()
    del myMenu
    if exiting == False:
        myGame = gameScreen(difficultySelection, screenSizeSelection, displayType)
        difficultySelection, screenSizeSelection, displayType, exiting = myGame.gameLoop()
        del myGame
pygame.quit()
quit()
