import pygame
import time
import random
import sys,os
import math
import sqlite3
from operator import itemgetter

class GameEventHandler(object):
    def textObjects(self, text, font, color):
        self.text = text
        self.font = font
        self.color = color
        self.textSurface = font.render(self.text, True, self.color)
        return self.textSurface, self.textSurface.get_rect()

    def largeMessageDisplay(self, text, displayWidth, displayHeight, fontSize, verticalPosition = .5, waitTwoSeconds = True):
        self.text = text
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.verticalPosition = verticalPosition
        self.waitTwoSeconds = waitTwoSeconds
        self.textPosition = (self.verticalPosition * self.displayHeight)
        self.largeText = pygame.font.Font("freesansbold.ttf", fontSize) #135
        self.textSurf, self.textRect = self.textObjects(self.text, self.largeText, white)
        self.textRect.center = ((self.displayWidth/2.0), self.textPosition)
        gameDisplay.blit(self.textSurf, self.textRect)
        pygame.display.update()
        if self.waitTwoSeconds == True:
            time.sleep(2)

    def smallMessageDisplay(self, text, lineNumber, displayWidth):
        self.text = text
        self.lineNumber = lineNumber
        self.displayWidth = displayWidth
        self.smallText = pygame.font.Font("freesansbold.ttf", 16)
        self.textSurf, self.textRect = self.textObjects(self.text, self.smallText, white)
        self.textRect.center = ((self.displayWidth-60), 15 + (15*self.lineNumber))
        gameDisplay.blit(self.textSurf, self.textRect)

    def handleIfUserGotHighScore(self, difficultySelection, score, displayWidth, displayHeight):
        self.myHighScoreDatabase = HighScoresDatabase()
        self.myHighScores = self.myHighScoreDatabase.loadHighScores()
        self.difficultySelection = difficultySelection
        self.score = score
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight

        self.alreadyRecievedHighScoreInfo = False
        for self.handleHighScoreCounter in xrange(self.myHighScoreDatabase.numberOfRecordsPerDifficulty):
            if self.score > int(self.myHighScores[self.difficultySelection][self.handleHighScoreCounter][2]) and self.alreadyRecievedHighScoreInfo == False:
                self.highScoreName, self.highScoreState, self.highScoreCountry = self.newHighScore(self.displayWidth, self.displayHeight)
                self.alreadyRecievedHighScoreInfo = True
        if self.alreadyRecievedHighScoreInfo == True:
            self.myHighScores[self.difficultySelection].append([0, self.highScoreName, self.score, self.highScoreState, self.highScoreCountry])
            self.myHighScores[self.difficultySelection] = sorted(self.myHighScores[self.difficultySelection], key = itemgetter(2), reverse = True)
            self.myHighScores[self.difficultySelection].pop()
            for self.handleHighScoreCounter in xrange(self.myHighScoreDatabase.numberOfRecordsPerDifficulty):
                self.myHighScores[self.difficultySelection][self.handleHighScoreCounter][0] = self.handleHighScoreCounter + 1
            self.myHighScoreDatabase.updateHighScoresForThisDifficulty(self.myHighScores[self.difficultySelection], self.difficultySelection)
        del self.myHighScoreDatabase

    def textInput(self, questionString, displayWidth, displayHeight):
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.questionString = questionString
        self.inputString = ""
        while 1 == 1:
            for self.event in pygame.event.get():
                gameDisplay.fill(black)
                self.largeMessageDisplay(self.questionString, self.displayWidth, self.displayHeight, 64, .25, False)
                self.largeMessageDisplay(self.inputString + "_", self.displayWidth, self.displayHeight, 64, .75, False)
        
                if self.event.type == pygame.QUIT:
                    pass
                    #self.exiting = True
                if self.event.type == pygame.KEYDOWN and (self.event.key == pygame.K_BACKSPACE or self.event.key == pygame.K_DELETE):
                    self.inputString = self.inputString[:len(self.inputString) - 1]
                if self.event.type == pygame.KEYDOWN and (self.event.key == pygame.K_KP_ENTER or self.event.key == pygame.K_RETURN):
                    return self.inputString
                if len(self.inputString) < 17:
                    if self.event.type == pygame.KEYDOWN:
                        if self.event.key == pygame.K_a:
                            self.inputString = self.inputString + "A"
                        elif self.event.key == pygame.K_b:
                            self.inputString = self.inputString + "B"
                        elif self.event.key == pygame.K_c:
                            self.inputString = self.inputString + "C"
                        elif self.event.key == pygame.K_d:
                            self.inputString = self.inputString + "D"
                        elif self.event.key == pygame.K_e:
                            self.inputString = self.inputString + "E"
                        elif self.event.key == pygame.K_f:
                            self.inputString = self.inputString + "F"
                        elif self.event.key == pygame.K_g:
                            self.inputString = self.inputString + "G"
                        elif self.event.key == pygame.K_h:
                            self.inputString = self.inputString + "H"
                        elif self.event.key == pygame.K_i:
                            self.inputString = self.inputString + "I"
                        elif self.event.key == pygame.K_j:
                            self.inputString = self.inputString + "J"
                        elif self.event.key == pygame.K_k:
                            self.inputString = self.inputString + "K"
                        elif self.event.key == pygame.K_l:
                            self.inputString = self.inputString + "L"
                        elif self.event.key == pygame.K_m:
                            self.inputString = self.inputString + "M"
                        elif self.event.key == pygame.K_n:
                            self.inputString = self.inputString + "N"
                        elif self.event.key == pygame.K_o:
                            self.inputString = self.inputString + "O"
                        elif self.event.key == pygame.K_p:
                            self.inputString = self.inputString + "P"
                        elif self.event.key == pygame.K_q:
                            self.inputString = self.inputString + "Q"
                        elif self.event.key == pygame.K_r:
                            self.inputString = self.inputString + "R"
                        elif self.event.key == pygame.K_s:
                            self.inputString = self.inputString + "S"
                        elif self.event.key == pygame.K_t:
                            self.inputString = self.inputString + "T"
                        elif self.event.key == pygame.K_u:
                            self.inputString = self.inputString + "U"
                        elif self.event.key == pygame.K_v:
                            self.inputString = self.inputString + "V"
                        elif self.event.key == pygame.K_w:
                            self.inputString = self.inputString + "W"
                        elif self.event.key == pygame.K_x:
                            self.inputString = self.inputString + "X"
                        elif self.event.key == pygame.K_y:
                            self.inputString = self.inputString + "Y"
                        elif self.event.key == pygame.K_z:
                            self.inputString = self.inputString + "Z"
                        elif self.event.key == pygame.K_SPACE:
                            self.inputString = self.inputString + " "

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

    def updateScreenAndLimitFPS(self, limit):
        self.limit = limit
        pygame.display.update()
        clock.tick(self.limit)

    def newHighScore(self, displayWidth, displayHeight):
        self.dislpayWidth = displayWidth
        self.displayHeight = displayHeight
        gameDisplay.fill(black)
        self.largeMessageDisplay("New High Score!", self.dislpayWidth, self.displayHeight, 64)
        gameDisplay.fill(black)
        self.highScoreName = self.textInput("Enter Your Name", self.dislpayWidth, self.displayHeight)
        gameDisplay.fill(black)
        self.highScoreState = self.textInput("Enter Your State", self.dislpayWidth, self.displayHeight)
        gameDisplay.fill(black)
        self.highScoreCountry = self.textInput("Enter Your Country", self.dislpayWidth, self.displayHeight)
        gameDisplay.fill(black)
        return self.highScoreName, self.highScoreState, self.highScoreCountry

    def bonusAttributes(self, bonusType):
        if bonusType == "Health":
            return ["Health Bonus", self.rndNumb, 0, 80 , 30 , 255, 255, 255, self.starMoveSpeed, -5, 0, 0]
        elif bonusType == "Ammo":
            return ["Ammo Bonus", self.rndNumb, 0, 80 , 30 , 255, 255, 255, self.starMoveSpeed, 0, 0, 500]

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

    def generateBonus(self, myProjectiles, difficultySelection, displayWidth, starMoveSpeed):
        self.difficultySelection = difficultySelection
        self.myProjectiles = myProjectiles
        self.displayWidth = displayWidth
        self.starMoveSpeed = starMoveSpeed
        #ADD HEALTH BONUS
        if random.randint(1, 20) == 1:
            self.rndNumb = random.randint(1, self.displayWidth - self.bonusAttributes("Health")[3])
            self.myProjectiles.append(self.bonusAttributes("Health"))
        #ADD AMMO BONUS
        if random.randint(1, 20) == 1:
            self.rndNumb = random.randint(1, self.displayWidth - self.bonusAttributes("Ammo")[3])
            self.myProjectiles.append(self.bonusAttributes("Ammo"))
        
        return self.myProjectiles

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
                                        #label, x, y, width, height, r, g, b, speed, damage, dx, ammo
            self.myProjectiles.append(["Star", self.rndNumb, 0, 1 , 1 , 255, 255, 255, self.starMoveSpeed, 0, 0, 0])

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

    def moveAndDrawProjectilesAndEnemies(self, myProjectiles, myEnemies, myHealth, score, enemiesAlive, x, y, rocketWidth, rocketHeight, difficultySelection, displayWidth, displayHeight, ammo, starMoveSpeed):
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
        self.ammo = ammo
        self.starMoveSpeed = starMoveSpeed
        self.myDeleteList = []
        for self.i in xrange(len(self.myProjectiles)): #for each bullet, star, and game bonus
            if (self.myProjectiles[self.i][0] == "Star" or str(self.myProjectiles[self.i][0])[:4] == "Enem" or "Bonus" in self.myProjectiles[self.i][0]): #if this projectile is a star or enemy bullet,
                if self.myProjectiles[self.i][2] + self.myProjectiles[self.i][8] + 1 >= self.displayHeight or self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4] + self.myProjectiles[self.i][8] -1 <= 0: #if it's going beyond the top/bottom of the screen
                    self.myDeleteList.append(self.i) #flag it for deletion by putting it in a list which we later use to delete it from myProjectiles. Deleting now wreaks havoc on our for loop
                else:
                    self.hit = False
                    #otherwise if it's not going beyond the screen limits, then if it's an enemy bullet that hit the user, then
                    if (str(self.myProjectiles[self.i][0])[:4] == "Enem" or "Bonus" in self.myProjectiles[self.i][0]) and ((self.myProjectiles[self.i][1] + self.myProjectiles[self.i][3] >= x) and (self.myProjectiles[self.i][1] <= x + self.rocketWidth) and (self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4] >= self.y) and (self.myProjectiles[self.i][2] <= self.y + self.rocketHeight)):
                        self.myHealth = min(self.myHealth - self.myProjectiles[self.i][9], 100) #Health bonus shouldn't make player health > 100
                        self.ammo = self.ammo + self.myProjectiles[self.i][11]
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
                        if ((self.myProjectiles[self.i][1] + self.myProjectiles[self.i][3] >= self.myEnemies[self.j][6]) and (self.myProjectiles[self.i][1] <= self.myEnemies[self.j][6] + self.myEnemies[self.j][10]) and (self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4] >= self.myEnemies[self.j][7]) and (self.myProjectiles[self.i][2] <= self.myEnemies[self.j][7] + self.myEnemies[self.j][11])) or ((self.myProjectiles[self.i][1] + self.myProjectiles[self.i][3] >= self.myEnemies[self.j][6]) and (self.myProjectiles[self.i][1] <= self.myEnemies[self.j][6] + self.myEnemies[self.j][10]) and (self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4] + (self.myProjectiles[self.i][8]/2.0) >= self.myEnemies[self.j][7]) and (self.myProjectiles[self.i][2] + (self.myProjectiles[self.i][8]/2.0) <= self.myEnemies[self.j][7] + self.myEnemies[self.j][11])):
                            self.myEnemies[self.j][2] = self.myEnemies[self.j][2] - self.myProjectiles[self.i][9] #reduce enemy health
                            self.myDeleteList.append(self.i) #flag this bullet for deletion
                            self.myProjectiles = self.generateBonus(self.myProjectiles, self.difficultySelection, self.displayWidth, self.starMoveSpeed)
            #move this projectile in the direction it needs to go
            self.myProjectiles[self.i][2] = self.myProjectiles[self.i][2] + self.myProjectiles[self.i][8]
            #draw this projectile
            if (str(self.myProjectiles[self.i][0])[:4] == "My B"):
                                    #SURFACE, (R,G,B), ((X1Y1), (X2Y1), (X2Y2), (X1Y2))
                pygame.draw.polygon(gameDisplay, (self.myProjectiles[self.i][5], self.myProjectiles[self.i][6], self.myProjectiles[self.i][7]), ((self.myProjectiles[self.i][1], self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4]), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]), self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4]),  (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2.0), self.myProjectiles[self.i][2]), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2.0), self.myProjectiles[self.i][2])), 0)
            elif (str(self.myProjectiles[self.i][0]) == "Enemy Bullet - Teleport"):
                pygame.draw.polygon(gameDisplay, (self.myProjectiles[self.i][5], self.myProjectiles[self.i][6], self.myProjectiles[self.i][7]), ((self.myProjectiles[self.i][1], max(self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4], self.enemy(0)[11])), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]), max(self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4], self.enemy(0)[11])),  (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2.0), max(self.myProjectiles[self.i][2], self.enemy(0)[11])), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2.0), max(self.myProjectiles[self.i][2], self.enemy(0)[11]))), 0)
            elif (str(self.myProjectiles[self.i][0]) == "Health Bonus"): #but if it's a game bonus, then display
                self.drawObject(HealthBonus, self.myProjectiles[self.i][1], self.myProjectiles[self.i][2])
            elif (str(self.myProjectiles[self.i][0]) == "Ammo Bonus"): #but if it's a game bonus, then display
                self.drawObject(AmmoBonus, self.myProjectiles[self.i][1], self.myProjectiles[self.i][2])
            else:
                pygame.draw.polygon(gameDisplay, (self.myProjectiles[self.i][5], self.myProjectiles[self.i][6], self.myProjectiles[self.i][7]), ((self.myProjectiles[self.i][1], self.myProjectiles[self.i][2]), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]), self.myProjectiles[self.i][2]),  (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2.0), self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4]), (self.myProjectiles[self.i][1] + (self.myProjectiles[self.i][3]/2.0), self.myProjectiles[self.i][2] + self.myProjectiles[self.i][4])), 0)
            

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
                    self.myProjectiles.append([self.bulletProperties[0], self.myEnemies[self.i][6] + (self.myEnemies[self.i][10]/2.0) - (self.bulletProperties[1]/2.0), self.myEnemies[self.i][7], self.bulletProperties[1], self.bulletProperties[2], self.bulletProperties[3], self.bulletProperties[4], self.bulletProperties[5], self.bulletProperties[6], self.bulletProperties[7], self.bulletProperties[8], 0])
                self.myEnemies[self.i][6] = self.myEnemies[self.i][6] + self.myEnemies[self.i][8] #move this enemy
                self.myEnemies[self.i][7] = self.myEnemies[self.i][7] + self.myEnemies[self.i][9]
                self.drawFromFile(self.myEnemies[self.i][5], self.myEnemies[self.i][6], self.myEnemies[self.i][7])
                self.myEnemies[self.i] = self.enemyMovementAI(self.myEnemies[self.i], self.displayWidth, self.displayHeight) #establish this enemy's next move
        #delete enemies that were flagged for completion
        for self.i in xrange(len(self.myDeleteList)):
            del self.myEnemies[self.myDeleteList[self.i]-self.i]
        return self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.y, self.ammo

    def testIfPlayerLost(self, myHealth, exiting, score, displayWidth, displayHeight):
        self.myHealth = myHealth
        self.exiting = exiting
        self.score = score
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.lost = False
        if self.myHealth <= 0:
            self.lost = True
            self.largeMessageDisplay("YOU LOSE", self.displayWidth, self.displayHeight, 135)
            gameDisplay.fill(black)
            self.largeMessageDisplay(str(self.score) + " pts", self.displayWidth, self.displayHeight, 135)
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
                self.myMenu = MenuScreen("Pause", screenSizeSelection, difficultySelection, displayType)
                self.difficultySelection, self.screenSizeSelection, self.displayType, self.exiting = self.myMenu.displayMenuScreenAndHandleUserInput()
                del self.myMenu
                #TO DO: TEST IF RESOLUTION WAS REDUCED BECAUSE PLAYER COULD NOW BE OUTSIDE OF SCREEN BOUNDS
            if self.event.type == pygame.KEYDOWN and (self.event.key == pygame.K_KP_ENTER or self.event.key == pygame.K_RETURN):
                self.enterPressed = True
            if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_SPACE and self.ammo >0: #MAKE USER NEED TO PRESS SPACE OVER AND OVER TO FIRE
                self.ammo = self.ammo - 1
                self.bulletProperties = self.loadBulletInfoIntomyProjectilesMatrix(self.currentGun, False, 0, self.difficultySelection, self.displayHeight)
                self.myProjectiles.append([self.bulletProperties[0], x + (self.rocketWidth/2.0) - int((self.bulletProperties[1]/2.0)), self.y, self.bulletProperties[1], self.bulletProperties[2], self.bulletProperties[3], self.bulletProperties[4], self.bulletProperties[5], self.bulletProperties[6], self.bulletProperties[7], 0, 0])
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

class HighScoresDatabase(object):
    def __init__(self):
        self.numberOfRecordsPerDifficulty = 10
        
    def fillInBlankHighScores(self, highScoresArray):
        self.workingArray = highScoresArray
        self.iNeedThisManyMoreBlankSlots = self.numberOfRecordsPerDifficulty - len(self.workingArray)
        self.n = 0
        self.b = [[],]
        for self.row in xrange(self.iNeedThisManyMoreBlankSlots):
            self.n = self.n + 1
            self.b.append([self.n, "-", 0, "-", "-"])
        self.b.remove([])
        #self.workingArray.append(self.b)
        #return self.workingArray
        return self.b

    def loadHighScores(self):
        try:
            self.highScoresArray = [[],]
            self.connection = sqlite3.connect("High_Scores.db")
            self.c = self.connection.cursor()
            self.row = ([])
            for self.loadCounter in xrange(5):
                self.a = [[],]
                if self.loadCounter == 0:
                    self.c.execute("""SELECT * FROM easyHighScoreTable ORDER BY scoreRecordPK""")
                elif self.loadCounter == 1:
                    self.c.execute("""SELECT * FROM mediumHighScoreTable ORDER BY scoreRecordPK""")
                elif self.loadCounter == 2:
                    self.c.execute("""SELECT * FROM hardHighScoreTable ORDER BY scoreRecordPK""")
                elif self.loadCounter == 3:
                    self.c.execute("""SELECT * FROM expertHighScoreTable ORDER BY scoreRecordPK""")
                elif self.loadCounter == 4:
                    self.c.execute("""SELECT * FROM lolHighScoreTable ORDER BY scoreRecordPK""")  
                for self.row in self.c.fetchall():
                    self.a.append([self.row[0], str(self.row[1]), self.row[2], str(self.row[3]), str(self.row[4])])
                #self.highScoresArray.append([row(0), row(1), row(2), row(3), row(4)])
                self.a.remove([])
                #self.a = self.a.append(self.fillInBlankHighScores(self.a))
                #self.a.remove([])
                #print self.a
                self.highScoresArray.insert(self.loadCounter, self.a)
        except:
            self.initializeDatabase()
        
        self.connection.close()
        return self.highScoresArray

    def initializeDatabase(self):
        self.connection = sqlite3.connect("High_Scores.db")
        self.c = self.connection.cursor()
        self.c.execute("DROP TABLE IF EXISTS easyHighScoreTable")
        self.c.execute("CREATE TABLE easyHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
        self.c.execute("DROP TABLE IF EXISTS mediumHighScoreTable")
        self.c.execute("CREATE TABLE mediumHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
        self.c.execute("DROP TABLE IF EXISTS hardHighScoreTable")
        self.c.execute("CREATE TABLE hardHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
        self.c.execute("DROP TABLE IF EXISTS expertHighScoreTable")
        self.c.execute("CREATE TABLE expertHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
        self.c.execute("DROP TABLE IF EXISTS lolHighScoreTable")
        self.c.execute("CREATE TABLE lolHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
        for self.loadCounter in xrange(5):
            #self.highScoresArray.append([])
            self.highScoresArray.insert(self.loadCounter, self.fillInBlankHighScores(self.highScoresArray[self.loadCounter]))
            #self.highScoresArray = self.fillInBlankHighScores(self.highScoresArray[self.loadCounter])
        self.highScoresArray.remove([])
        for self.loadCounter in xrange(5):
            self.updateHighScoresForThisDifficulty(self.highScoresArray[self.loadCounter], self.loadCounter)
        self.connection.close()
        return self.highScoresArray
                
    def updateHighScoresForThisDifficulty(self, workingArray, difficulty):
        try:
            self.workingArray = workingArray
            self.difficulty = difficulty
            self.connection = sqlite3.connect("High_Scores.db")
            self.c = self.connection.cursor()
            self.updateCounter = -1
            for self.row in self.workingArray:
                self.updateCounter = self.updateCounter + 1
                if self.difficulty == 0:
                    if self.updateCounter == 0:
                        self.c.execute("DROP TABLE IF EXISTS easyHighScoreTable")
                        self.c.execute("CREATE TABLE easyHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
                    self.c.execute("INSERT INTO easyHighScoreTable Values(?, ?, ?, ?, ?)", tuple((int(workingArray[self.updateCounter][0]), self.workingArray[self.updateCounter][1], int(self.workingArray[self.updateCounter][2]), self.workingArray[self.updateCounter][3], self.workingArray[self.updateCounter][4])))
                if self.difficulty == 1:
                    if self.updateCounter == 0:
                        self.c.execute("DROP TABLE IF EXISTS mediumHighScoreTable")
                        self.c.execute("CREATE TABLE mediumHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
                    self.c.execute("INSERT INTO mediumHighScoreTable Values(?, ?, ?, ?, ?)", tuple((int(workingArray[self.updateCounter][0]), self.workingArray[self.updateCounter][1], int(self.workingArray[self.updateCounter][2]), self.workingArray[self.updateCounter][3], self.workingArray[self.updateCounter][4])))
                if self.difficulty == 2:
                    if self.updateCounter == 0:
                        self.c.execute("DROP TABLE IF EXISTS hardHighScoreTable")
                        self.c.execute("CREATE TABLE hardHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
                    self.c.execute("INSERT INTO hardHighScoreTable Values(?, ?, ?, ?, ?)", tuple((int(workingArray[self.updateCounter][0]), self.workingArray[self.updateCounter][1], int(self.workingArray[self.updateCounter][2]), self.workingArray[self.updateCounter][3], self.workingArray[self.updateCounter][4])))
                if self.difficulty == 3:
                    if self.updateCounter == 0:
                        self.c.execute("DROP TABLE IF EXISTS expertHighScoreTable")
                        self.c.execute("CREATE TABLE expertHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
                    self.c.execute("INSERT INTO expertHighScoreTable Values(?, ?, ?, ?, ?)", tuple((int(workingArray[self.updateCounter][0]), self.workingArray[self.updateCounter][1], int(self.workingArray[self.updateCounter][2]), self.workingArray[self.updateCounter][3], self.workingArray[self.updateCounter][4])))
                if self.difficulty == 4:
                    if self.updateCounter == 0:
                        self.c.execute("DROP TABLE IF EXISTS lolHighScoreTable")
                        self.c.execute("CREATE TABLE lolHighScoreTable(scoreRecordPK INT, Name TEXT, Score INT, State TEXT, Country TEXT)")
                    self.c.execute("INSERT INTO lolHighScoreTable Values(?, ?, ?, ?, ?)", tuple((int(workingArray[self.updateCounter][0]), self.workingArray[self.updateCounter][1], int(self.workingArray[self.updateCounter][2]), self.workingArray[self.updateCounter][3], self.workingArray[self.updateCounter][4])))
                self.connection.commit()
        except:
            self.initializeDatabase()
        self.connection.close()

class MenuScreen(object):
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
        self.x = (self.displayWidth/2.0)-(self.rocketWidth/2.0)
        self.y = (self.displayHeight-self.rocketHeight)
        self.colorIntensity = 255
        self.colorIntensityDirection = 5
        self.startPlay = False
        self.menuGameEventHandler = GameEventHandler()
        self.screenMoveCounter = 0
        self.myHighScoreDatabase = HighScoresDatabase()
        self.myHighScores = self.myHighScoreDatabase.loadHighScores()
        self.highScoreDifficulty = 0

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
            elif self.menuDirectory == "High Scores":
                self.displayHighScoresMenu()
                self.handleUserInputHighScoresMenu()
                
            self.rocketYDeltaWas = self.rocketYDelta
            self.rocketXDeltaWas = self.rocketXDelta
            self.menuGameEventHandler.updateScreenAndLimitFPS(FPSLimit)
            gameDisplay.fill(black)
        return self.difficultySelection, self.screenSizeSelection, self.displayType, self.exiting
    
    def displayTitle(self):
        self.smallText = pygame.font.Font("freesansbold.ttf", 24)
        self.largeText = pygame.font.Font("freesansbold.ttf", 48)
        self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("Spacing Out", self.largeText, white)
        self.textRect.center = ((self.displayWidth/2.0), (self.screenMoveCounter + 25))
        gameDisplay.blit(self.textSurf, self.textRect)
        if self.menuType == "Pause":
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("-Paused-", self.smallText, white)
            self.textRect.center = ((self.displayWidth/2.0), (self.screenMoveCounter + 75))
            gameDisplay.blit(self.textSurf, self.textRect)

    def selectionColorPulsate(self):
        if self.colorIntensity + self.colorIntensityDirection > 255:
            self.colorIntensityDirection = -5
        elif self.colorIntensity + self.colorIntensityDirection < 65:
            self.colorIntensityDirection = 5
        self.colorIntensity = self.colorIntensity + self.colorIntensityDirection

    def handleMenuBackground(self):
        self.currentLevel, self.currentGun, self.enemiesAlive, self.myEnemies, self.myProjectiles = self.menuGameEventHandler.addGameObjects(
            self.enemiesAlive, self.currentLevel, self.currentGun, self.myEnemies, self.starProbabilitySpace, self.starDensity, self.starMoveSpeed, self.myProjectiles, self.displayWidth)
        self.starMoveSpeed = self.menuGameEventHandler.adjustStarMoveSpeed(self.maximumStarMoveSpeed, self.numberOfStarSpeeds)
        self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.y, self.ammo = self.menuGameEventHandler.moveAndDrawProjectilesAndEnemies(
            self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.x, self.y, self.rocketWidth, self.rocketHeight, self.difficultySelection, self.displayWidth, self.displayHeight, self.ammo, self.starMoveSpeed)
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
            self.textRect.center = ((self.displayWidth/2.0), (self.displayHeight/2.0 - self.i*(self.rocketAccel) + self.screenMoveCounter))
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
            self.textRect.center = ((self.displayWidth/2.0), (self.displayHeight/2.0 - self.i*(self.rocketAccel)))
            gameDisplay.blit(self.textSurf, self.textRect)

    def displayCreditsMenu(self):
        if self.screenMoveCounter < self.displayHeight:
            self.screenMoveCounter = self.screenMoveCounter + self.maximumStarMoveSpeed
            self.displayTitle()
            self.displayMainMenu()
    
        for self.i in xrange(3):
            self.rgb = (255, 255, 255)
            if self.i == 2:
                self.text = "Programming by Mike Finnegan"
            if self.i == 1:
                self.text = "Art by Mike Finnegan"
            if self.i == 0:
                self.text = "Music/SFX by Mike Finnegan"
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects(self.text, self.smallText, self.rgb)
            #self.textRect.center = ((self.displayWidth/2), (self.displayHeight/2 - self.i*(self.rocketAccel)))
            self.textRect.center = ((self.displayWidth/2.0), ((self.i * self.rocketAccel) + self.screenMoveCounter - self.displayHeight/2.0))
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
            self.textRect.center = ((self.displayWidth/2.0), ((self.i * self.rocketAccel) + self.screenMoveCounter - self.displayHeight/2.0))
            gameDisplay.blit(self.textSurf, self.textRect)

    def displayHighScoresMenu(self):
        if self.menuSelectionIndex == 0:
            self.rgb = (self.colorIntensity, 0, 0)
        else:
            self.rgb = (255, 255, 255)
        if self.highScoreDifficulty == 0:
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("<<  Easy High Scores  >>", self.smallText, self.rgb)
        if self.highScoreDifficulty == 1:
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("<<  Medium High Scores  >>", self.smallText, self.rgb)
        if self.highScoreDifficulty == 2:
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("<<  Hard High Scores  >>", self.smallText, self.rgb)
        if self.highScoreDifficulty == 3:
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("<<  Expert High Scores  >>", self.smallText, self.rgb)
        if self.highScoreDifficulty == 4:
            self.textSurf, self.textRect = self.menuGameEventHandler.textObjects("<<  You already lost lol High Scores  >>", self.smallText, self.rgb)
        self.textRect.center = ((self.displayWidth/2.0), (self.screenMoveCounter + 90))
        gameDisplay.blit(self.textSurf, self.textRect)
        for self.i in xrange(-1, 11):
            for self.j in xrange(5):
                if self.i == -1:
                    self.rgb = (255, 255, 255)
                    if self.j == 0:
                        self.text = "Rank"
                    elif self.j == 1:
                        self.text = "Name"
                    elif self.j == 2:
                        self.text = "Score"
                    elif self.j == 3:
                        self.text = "State"
                    elif self.j == 4:
                        self.text = "Country"
                    self.textSurf, self.textRect = self.menuGameEventHandler.textObjects(self.text, self.smallText, self.rgb)
                    #self.textRect.center = ((self.displayWidth/2), (self.displayHeight/2 - self.i*(self.rocketAccel)))
                    self.textRect.center = ((self.displayWidth*((self.j+1)/6.0)), ((self.i * self.rocketAccel) + self.displayHeight/2.0))
                elif self.i == self.myHighScoreDatabase.numberOfRecordsPerDifficulty:
                    if self.menuSelectionIndex == 1:
                        self.rgb = (self.colorIntensity, 0, 0)
                    else:
                        self.rgb = (255, 255, 255)
                    self.text = "Go Back"
                    self.textSurf, self.textRect = self.menuGameEventHandler.textObjects(self.text, self.smallText, self.rgb)
                    self.textRect.center = ((self.displayWidth*.8), (self.displayHeight * .95))
                else:
                    self.rgb = (255, 255, 255)
                    self.text = str(self.myHighScores[self.highScoreDifficulty][self.i][self.j])
                    self.textSurf, self.textRect = self.menuGameEventHandler.textObjects(self.text, self.smallText, self.rgb)
                    #self.textRect.center = ((self.displayWidth/2), (self.displayHeight/2 - self.i*(self.rocketAccel)))
                    self.textRect.center = ((self.displayWidth*((self.j+1)/6.0)), ((self.i * self.rocketAccel) + self.displayHeight/2.0))
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
        if self.enterPressed == True and self.menuSelectionIndex == 1:
            self.menuDirectory = "Credits"
        if self.enterPressed == True and self.menuSelectionIndex == 3:
            self.menuDirectory = "How To Play"
        if self.enterPressed == True and self.menuSelectionIndex == 6:
            self.startPlay = True
            del self.myHighScoreDatabase
        if self.enterPressed == True and self.menuSelectionIndex == 0:
            self.exiting = True
        if self.enterPressed == True and self.menuSelectionIndex == 4:
            self.menuDirectory = "High Scores"
            self.menuSelectionIndex = 0
        if self.enterPressed == True and self.menuSelectionIndex == 2:
            self.menuDirectory = "Settings"
            self.menuSelectionIndex = 4

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
            self.x = (self.displayWidth/2.0)-(self.rocketWidth/2.0)
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

    def handleUserInputHighScoresMenu(self):
        if (self.rocketYDelta == self.rocketAccel and self.rocketYDeltaWas == 0):
            self.menuSelectionIndex = (self.menuSelectionIndex + 1) % 2
        if (self.rocketYDelta == -self.rocketAccel and self.rocketYDeltaWas == 0):
            self.menuSelectionIndex = (self.menuSelectionIndex - 1) % 2
        if (self.menuSelectionIndex == 0 and self.rocketXDelta == self.rocketAccel and self.rocketXDeltaWas == 0):
            self.highScoreDifficulty = (self.highScoreDifficulty + 1) % 5
        if (self.menuSelectionIndex == 0 and self.rocketXDelta == -self.rocketAccel and self.rocketXDeltaWas == 0):
            self.highScoreDifficulty = (self.highScoreDifficulty - 1) % 5
        if self.menuSelectionIndex == 1 and self.enterPressed == True:
            self.screenMoveCounter = 0
            self.menuDirectory = "Main"
            self.menuSelectionIndex = 4
        
class GameScreen(object):
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
        self.ammo = int(1000 * (1/(float(1 + self.difficultySelection))))
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
        self.x = (self.allResolutionsAvail[self.screenSizeSelection][0]/2.0)-(self.rocketWidth/2.0)
        self.y = (self.allResolutionsAvail[self.screenSizeSelection][1]-self.rocketHeight)
        self.myGameEventHandler = GameEventHandler()
        
    def gameLoop(self):
        while self.exiting == False and self.lost == False:
        
            #TEST FOR CONDITIONS THAT PREVENT FUTURE USER ACTIONS

            #TEST FOR CONDITIONS THAT ALLOW FUTURE USER ACTIONS

            self.currentLevel, self.currentGun, self.enemiesAlive, self.myEnemies, self.myProjectiles = self.myGameEventHandler.addGameObjects(
                self.enemiesAlive, self.currentLevel, self.currentGun, self.myEnemies, self.starProbabilitySpace, self.starDensity, self.starMoveSpeed, self.myProjectiles, self.allResolutionsAvail[self.screenSizeSelection][0])
            self.exiting, self.ammo, self.myProjectiles, self.rocketXDelta, self.rocketYDelta, self.enterPressed, self.screenSizeSelection, self.displayType = self.myGameEventHandler.handleKeyPresses(
                "Game", self.ammo, self.currentGun, self.myProjectiles, self.rocketAccel, self.x, self.y, self.rocketWidth, self.difficultySelection, self.screenSizeSelection, self.displayType, self.allResolutionsAvail[self.screenSizeSelection][1]) 
            self.x, self.y = self.myGameEventHandler.movePlayer(self.x, self.y, self.rocketWidth, self.rocketHeight, self.rocketXDelta, self.rocketYDelta, self.allResolutionsAvail[self.screenSizeSelection][0], self.allResolutionsAvail[self.screenSizeSelection][1])
            #gameDisplay.fill(black)
            gameDisplay.blit(background, (0, 0))
            self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.y, self.ammo = self.myGameEventHandler.moveAndDrawProjectilesAndEnemies(
                self.myProjectiles, self.myEnemies, self.myHealth, self.score, self.enemiesAlive, self.x, self.y, self.rocketWidth, self.rocketHeight, self.difficultySelection, self.allResolutionsAvail[self.screenSizeSelection][0], self.allResolutionsAvail[self.screenSizeSelection][1], self.ammo, self.starMoveSpeed)
            self.lost = self.myGameEventHandler.testIfPlayerLost(self.myHealth, self.exiting, self.score, self.allResolutionsAvail[self.screenSizeSelection][0], self.allResolutionsAvail[self.screenSizeSelection][1])
            self.myGameEventHandler.drawObject(myCharacter, self.x, self.y)
            self.myGameEventHandler.drawGameStats(self.myHealth, self.ammo, self.currentLevel, self.score, self.allResolutionsAvail[self.screenSizeSelection][0])
            self.starMoveSpeed = self.myGameEventHandler.adjustStarMoveSpeed(self.maximumStarMoveSpeed, self.numberOfStarSpeeds)
            self.myGameEventHandler.updateScreenAndLimitFPS(FPSLimit)
        
        #OUT OF THE GAME LOOP
        self.myGameEventHandler.handleIfUserGotHighScore(self.difficultySelection, self.score, self.displayWidth, self.displayHeight)
        del self.myGameEventHandler
        return self.difficultySelection, self.screenSizeSelection, self.displayType, self.exiting

FPSLimit = 60
pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
clock = pygame.time.Clock()
allResolutionsAvail = pygame.display.list_modes()
allResolutionsAvail.sort()
displayWidth = allResolutionsAvail[(int(len(allResolutionsAvail)/2.0))][0]
displayHeight = allResolutionsAvail[(int(len(allResolutionsAvail)/2.0))][1]
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
background = pygame.image.load("background6.png").convert()
myCharacter = pygame.image.load("rocket.png")
HealthBonus = pygame.image.load("health bonus.png")
AmmoBonus = pygame.image.load("ammo bonus.png")
UFO = pygame.image.load("ufo.png")
BlueBomber = pygame.image.load("blue bomber.png")
HJet = pygame.image.load("h jet.png")
pygame.display.set_caption('Spacing Out')

menuType = "New Game"
screenSizeSelection = int(len(allResolutionsAvail)/2.0)
difficultySelection = 0
displayType = "Window"
exiting = False

while exiting == False:
    myMenu = MenuScreen(menuType, screenSizeSelection, difficultySelection, displayType)
    difficultySelection, screenSizeSelection, displayType, exiting = myMenu.displayMenuScreenAndHandleUserInput()
    del myMenu
    if exiting == False:
        myGame = GameScreen(difficultySelection, screenSizeSelection, displayType)
        difficultySelection, screenSizeSelection, displayType, exiting = myGame.gameLoop()
        del myGame
pygame.quit()
quit()
