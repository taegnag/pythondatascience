
import pygame
import math
import random
import time
from pygame import mixer
from misc import *

# modified start 1
class Square:
    def __init__(self, name, boardpos):
        self.name = name
        self.boardpos = boardpos

class Property(Square):
    def __init__(self, name, boardpos, colour):
        super().__init__(name, boardpos)
        self.colour = colour
        self.houses = 0
        self.owner = bank
        self.rent = 0
        # self.mortgaged = False
        self.rejected = False  # This is here so the user only has to buy/reject a property once.
        self.paidRent = False
        self.streetOwned = False
        self.buttonPosition = [[0, 0], [0, 0]]
        self.realWorth = 0 # This is what Eve uses to decide what to do with the property
        self.houseWorth = 0 # She uses this to decide whether to buy houses or not. She'll buy houses on any street but the second last.
        self.costsList = []

    def getPrice(self): # Returns the price of a property, based on its position on the board.
        if self.name == 'India':
            return 350
        elif self.name == 'China':
            return 400
        elif self.colour == 8:
            return 200
        
        elif self.boardpos == 5*self.colour + 4:
            return 40 * self.colour + 80
        else:
            return 40 * self.colour + 60

    def getInitialRent(self): # Returns the (houseless) rent of a property, based on its position on the board.
        if self.colour <= 7:
            if self.boardpos == 5 * self.colour + 4 or self.name == 'England':
                self.costsList = houseCostGrid[self.colour][1]
                return houseCostGrid[self.colour][1][0]

            else:
                self.costsList = houseCostGrid[self.colour][0]
                return houseCostGrid[self.colour][0][0]
        elif self.colour == 8:
            return 25
        else:
            return 4*roll

    def getInitialWorth(self): # Returns the initial worth of a property, using initialMod (see around line 1300)
        global initialMod
        if self.colour <= 7:
            rents = sum(self.costsList) + self.getInitialRent()
            worth = rents * initialMod - self.getCostOfHouse()
            return worth
        elif self.colour == 8:
            return 200
        else:
            return 150

    def getInitialHouseWorth(self): # See above, but using houseMod
        global houseMod
        if self.colour <= 7:
            rents = avgDiff([self.getInitialRent()]+self.costsList)
            worth = rents * houseMod
            return worth
        else: # if a property's colour > 7, it's either a station or a utility and therefore can't be developed.
            return 0

    def getCostOfHouse(self): # Returns the cost of a house on a property, given its position on the board.
        multiplier = math.floor(self.colour/2) + 1
        if self.colour < 8:
            return multiplier*50
        else:
            return False

    def drawColour(self): # Draws houses, owner's colour,  and/or mortgaged sign on properties.
        if self.owner.colour:
            if 0 < self.boardpos < 9:
                colourPos = [605-28.5-math.floor(57.25*self.boardpos), 685-30]
                pygame.draw.rect(screen, self.owner.colour, (colourPos, (57, 15)))
                pygame.draw.rect(screen, palette.dutchWhite, (colourPos, (57, 2)))
                self.buttonPosition = [[colourPos[0], colourPos[0]+57], [colourPos[1], colourPos[1]+15]]
                # if self.mortgaged:
                #     screen.blit(mortgagePic, (colourPos[0], colourPos[1] - 77))
                if 0 < self.houses < 4:
                    count = 1
                    for house in range(self.houses):
                        housePos = [colourPos[0] + 14 + count, 610 - 30]
                        screen.blit(buildingPics[0], (housePos))
                        count += 14
                elif self.houses >= 4:
                    hotelPos = [colourPos[0] + 16, 610 - 30]
                    screen.blit(buildingPics[1], (hotelPos))

            elif 9 < self.boardpos < 18:
                colourPos = [0 + 28.5, 607-math.floor(57.25*(self.boardpos-9))-28.5]
                pygame.draw.rect(screen, self.owner.colour, (colourPos, (15, 57)))
                pygame.draw.rect(screen, palette.dutchWhite, ((colourPos[0] + 13, colourPos[1]), (2, 57)))
                self.buttonPosition = [[colourPos[0], colourPos[0]+15], [colourPos[1], colourPos[1]+57]]
                if 0 < self.houses < 4:
                    count = 1
                    for house in range(self.houses):
                        housePos = [71 + 28.5, colourPos[1] + 14 + count]
                        screen.blit(buildingPics[2], (housePos))
                        count += 14
                elif self.houses >= 4:
                    hotelPos = [71 + 28.5, colourPos[1] + 16]
                    screen.blit(buildingPics[3], (hotelPos))

                # if self.mortgaged:
                #     screen.blit(mortgagePic2, (colourPos[0] + 15, colourPos[1]))

            elif 18 < self.boardpos < 27:
                colourPos = [32 + math.ceil(57.25*(self.boardpos-18)) + 28.5, 0 + 30]
                pygame.draw.rect(screen, self.owner.colour, (colourPos, (57, 15)))
                pygame.draw.rect(screen, palette.dutchWhite, ((colourPos[0], colourPos[1] + 13), (57, 2)))
                self.buttonPosition = [[colourPos[0], colourPos[0]+57], [colourPos[1], colourPos[1]+15]]
                if 0 < self.houses <4:
                    count = 1
                    for house in range(self.houses):
                        housePos = [colourPos[0] + 14 + count, 73 + 30]
                        screen.blit(buildingPics[4], (housePos))
                        count += 14
                elif self.houses >= 4:
                    hotelPos = [colourPos[0] + 16, 75 + 30]
                    screen.blit(buildingPics[5], (hotelPos))

                # if self.mortgaged:
                #     screen.blit(mortgagePic, (colourPos[0], colourPos[1] + 15))

            else:
                colourPos = [685 - 30, 35 + math.ceil(57.25 * (self.boardpos - 27)) + 28.5]
                pygame.draw.rect(screen, self.owner.colour, (colourPos, (15, 57)))
                pygame.draw.rect(screen, palette.dutchWhite, ((colourPos), (2, 57)))
                self.buttonPosition = [[colourPos[0], colourPos[0]+15], [colourPos[1], colourPos[1]+57]]
                if 0 < self.houses < 4:
                    count = 1
                    for house in range(self.houses):
                        housePos = [608 - 30, colourPos[1] + 14 + count]
                        screen.blit(buildingPics[6], (housePos))
                        count += 14
                elif self.houses >= 4:
                    hotelPos = [608 - 30, colourPos[1] + 16]
                    screen.blit(buildingPics[7], (hotelPos))

                # if self.mortgaged:
                #     screen.blit(mortgagePic2, (colourPos[0] -77, colourPos[1]))

    def updateRent(self): # Updates a property's rent (who would have thought)
        if self.houses > 0:
            if self.boardpos == 5 * self.colour + 4 or self.name == 'England':
                self.rent = houseCostGrid[self.colour][1][self.houses]
            else:
                self.rent = houseCostGrid[self.colour][0][self.houses]
        return self.rent

class Chance(Square): # There ultimately wasn't much point in writing this class except to help identify squares by their type.
    def __init__(self, name, boardpos):
        super().__init__(name, boardpos)
        if self.name == 'Chance':
            self.list = chance
        else:
            self.list = communityChest

    def pickCard(self):
        return random.choice(self.list)

class TaxSquares(Square): # Again, more of an identifier than anything else.
    def __init__(self, name, boardpos):
        super().__init__(name, boardpos)
        self.paid = False

    def getTax(self):
        if self.name == 'Income Tax':
            return 200
        return 100

class SpecialSquares(Square): # Applies to the squares on the corners.
    def __init__(self, name, boardpos):
        super().__init__(name, boardpos)
        self.paid = False

    def getPayAmount(self, freeParking): # Returns how much money a player gets for landing on a square. See Alert classes for details on alerts
        global alert
        if self.name == 'Go':
            if user.isTurn:
                alert = Alert('Lazy Programming', 'You landed on Go and got $400 #because I was too lazy to fix #that issue. Some people play by #that rule anyway.')
            elif Eve.isTurn:
                alert = EveAlert('Sweet sweet cashola', 'Eve gets $400 by landing on Go')

            return 200
        elif self.name == 'Free Parking':
            if user.isTurn:
                alert = Alert('Rolling in Dough, maybe', ('You got $' + str(freeParking) + ' from Free Parking!'))
            return freeParking
        else:
            return 0
# modified end 1


# -------------------------------------------------------------------------------
# SPRITE CLASSES
class Player: # Class for practical matters considering the user and Eve.
    def __init__(self, name, isTurn, screens):
        self.name = name
        self.piece = None
        self.boardpos = 0
        self.timeMoving = 0
        self.pieceSelected = False
        self.pieceConfirmed = False
        self.colour = None
        self.isTurn = isTurn
        self.money = 1500
        self.screens = screens 
        self.canRoll = True
        self.doublesCount = 0
        self.inJail = False
        self.jailTurns = 0
        self.getOutOfJailFreeCards = []
        self.turnNum = 0
        # The next 4 attributes are boolean statuses (statuses? statii?). Arguably I could have made one string attribute called 'status'. Ah, the joy of hindsight.
        self.isDeveloping = False
        self.isTrading = False
        self.isMortgaging = False
        self.normalGameplay = True
        self.offer = []
        self.bid = '0'
        self.firstTimeInJail = True
        self.paidOOJ = False #OOJ stands for Out Of Jail. It gets tedious to write.


    def choosePiece(self, mousepos): # Lets the user choose a piece.
        if 110 < mousepos[0] < 110 + 1*270:
            if 276 < mousepos[1] < 276 + 128:
                self.piece = boot
                return (110, 276)
            elif 427 < mousepos[1] < 427 + 128:
                self.piece = iron
                return (110, 427)
        elif 110 + 1*270 < mousepos[0] < 110 + 2*270:
            if 276 < mousepos[1] < 276 + 128:
                self.piece = car
                return (110 + 1*270, 276)
            elif 427 < mousepos[1] < 427 + 128:
                self.piece = ship
                return (110 + 1 * 270, 427)
        elif 110 + 2*270 < mousepos[0] < 110 + 3*270:
            if 276 < mousepos[1] < 276 + 128:
                self.piece = dog
                return (110 + 2 * 270, 276)
            elif 427 < mousepos[1] < 427 + 128:
                self.piece = thimble
                return (110 + 2 * 270, 427)
        elif 110 + 3*270 < mousepos[0] < 110 + 4*270:
            if 276 < mousepos[1] < 276 + 128:
                self.piece = hat
                return (110 + 3 * 270, 276)
            elif 427 < mousepos[1] < 427 + 128:
                self.piece = wheelbarrow
                return (110 + 3 * 270, 427)
        else:
            return False

    # modified start 2
    def getPos(self): # 'Boardpos' is an integer from 0-39 depending on what square you're on, but that has to be translated into x and y co-ords, hence this function.
        if 0 <= self.boardpos < 9:
            return [579.5-57*self.boardpos, 600]
        elif 9 <= self.boardpos < 18:
            return [43.5, 579.5-57*(self.boardpos-9)]
        elif 18 <= self.boardpos < 27:
            return [66.5 + 57*(self.boardpos-18), 43.5]
        else:
            return [600, 66.5 + 57*(self.boardpos-27)]

    def move(self): # Moves players forward one place at a time. I'm pretty sure it gets called on every iteration of the loop.
        if self.timeMoving > 0:
            if self.boardpos == 35:
                self.boardpos = 0
                self.money += 200
                self.turnNum += 1
            else:
                self.boardpos += 1
            time.sleep(0.1)
            self.timeMoving -= 1
    # modified end 2
    
class Bank: # An identifier class. It is reminiscent of real life banks though.
    def __init__(self):
        self.colour = None

class AI: # There's an Eve object of the Player class and an AI object of the AI class. I like to think of 'Eve: Player' as Eve's body and 'AI: AI' as her brain.
    def __init__(self):
        self.player = Eve

    # modified start 3
    def wantsProp(self, prop): # Returns boolean of whether she wants to buy a given property or not.
        if prop.getPrice() <= Eve.money * 0.6:
            return True
        return False 
    # modified end 3
    
    def develop(self, currentSquare): # Returns the next property she wants to build a house on.
        underdevelopedCount = 0
        buildingProp = None
        if (self.player.money * 0.6 >= street[0].getCostOfHouse()):
        # if (worthAvg > street[0].getCostOfHouse() and self.player.money > street[0].getCostOfHouse()) or (worthAvg > street[0].getCostOfHouse() - 25 and self.player.money > 2*street[0].getCostOfHouse()):
            for prop in street:
                if prop.houses < street[len(street)-1].houses:
                    underdevelopedCount += 1
            if underdevelopedCount == 0:
                buildingProp = street[len(street)-1]
            elif underdevelopedCount == 2:
                buildingProp = street[1]
            elif underdevelopedCount == 1:
                buildingProp = street[0]

            if buildingProp.houses < 5:
                buildingProp.houses += 1
                self.player.money -= buildingProp.getCostOfHouse()
                return buildingProp
        # if prop.boardpos == currentSquare.boardpos:
        #     if prop.getCostOfHouse() <= Eve.money * 0.6:
        #        return True
        # return False 
        
    # modified start 4
    def emergencyAction(self): # This is what Eve does if she goes to end her turn and she has negative money.
        global properties
        houseProps = [[], [], [], [], [], [], [], []]
        baselineHouseProps = [[], [], [], [], [], [], [], []]
        propsToMort = []
        for prop in properties:
            if prop.owner == self.player:
                if prop.houses > 0:
                    houseProps[prop.colour].append(prop)
                else: 
                    if self.player.money < 0:
                        propsToMort.append(prop)

        streetsToDemolish = [] # She starts by demolishing any houses, because they give a better return (90% back vs 50%)
        while not houseProps == baselineHouseProps: #This loop orders them by worth to cost ratio
            bestToSell = False
            for street in houseProps:
                if len(street) > 0:
                    if not bestToSell or street[0].houseWorth/street[0].getCostOfHouse() < bestToSell.houseWorth/bestToSell.getCostOfHouse():
                        bestToSell = street[0]
            houseProps[bestToSell.colour] = []
            streetsToDemolish.append(streets[bestToSell.colour])

        propsMortgaged = []
        housesSold = []
        for street in streetsToDemolish: # This loop sells the houses
            for iter in range(5):
                for prop in street:

                    if self.player.money < 0 and prop.houses > 0:
                        prop.houses -= 1
                        self.player.money += (9*prop.getCostOfHouse())//10
                        housesSold.append(prop)

                    if self.player.money >= 0:
                        return [housesSold, propsMortgaged, True]

        for prop in propsToMort: # Mortgaging properties
            if self.player.money < 0:
                self.player.money += int(prop.getPrice()*0.7)
                prop.owner = bank
                propsMortgaged.append(prop)
            else:
                return [housesSold, propsMortgaged, True]

        for slist in housesSold: # Mortgaging properties that had houses on them at the start
            if self.player.money < 0:
                # slist[0].mortgaged = True
                self.player.money += int(slist[0].getPrice*0.7)
                propsMortgaged.append(slist[0])
            else:
                return [housesSold, propsMortgaged, True]
            
        if self.player.money >= 0:
            return [housesSold, propsMortgaged, True]

        return [housesSold, propsMortgaged, False] # Means that Eve is still in debt after mortgaging everything.
    # modified end 4
    
    def useGojf(self): # Determines if Eve will use a get out of jail free card when leaving jail.
        if len(self.player.getOutOfJailFreeCards) > 0:
            return True
        return False

# -------------------------------------------------------------------------------
# ALERT CLASSES
class Alert:
    def __init__ (self, heading, body):
        self.heading = heading
        self.body = body
        self.confirmed = True

        if self.heading == 'Chance' or self.heading == 'Community Chest':
            self.type = 'confirm'
            self.image = confirmAlertPic
        elif self.heading.__contains__('Tutorial'):
            self.type = 'confirm'
            self.image = confirmAlertPic
        elif self.heading == 'They see me rollin\'' or self.heading == 'Serial doubles-roller' or self.heading == 'Not-so-smooth criminal':
            self.type = 'confirm'
            self.image = confirmAlertPic
        elif self.body.__contains__('?'):
            self.type = 'choice'
            self.image = choiceAlertPic
        elif self.heading == 'Trade':
            self.type = 'trade'
            self.image = tradeAlertPic
        elif self.heading == 'Dispose' or self.heading == 'Sell house?':
            self.type = 'confirm'
            self.image = confirmAlertPic
        elif self.heading == 'Space Trip':
            self.type = 'choice'
            self.image = choiceAlertPic 
        else:
            self.type = 'basic'
            self.image = alertPic
        self.timePausing = 0

    def write(self):
        headingSize = 36
        bodySize = 24
        headingFont = pygame.font.Font('polly.ttf', headingSize)
        bodyFont = pygame.font.Font('polly.ttf', bodySize)
        lineSpacing = 6

        heading = headingFont.render(self.heading, True, palette.darkGold)

        lines = self.body.split('#')

        screen.blit(self.image, (700, 0))
        screen.blit(heading, (770, 224))
        for i in range(len(lines)):
            lines[i] = bodyFont.render(lines[i], True, palette.axolotl)
            height = 224 + headingSize + lineSpacing + i*(bodySize+lineSpacing)
            screen.blit(lines[i], (770, height))

    def confirmOrDeny(self):
        if self.type == 'choice':
            if inCircle(pygame.mouse.get_pos(), [700+353, 433], 15):
                return 'confirmed'
            if inCircle(pygame.mouse.get_pos(), [700+394, 433], 15):
                return 'denied'
        elif self.type == 'confirm' or self.type == 'trade':
            if inCircle(pygame.mouse.get_pos(), [700 + 394, 433], 15):
                return 'confirmed'
        return False

class EveAlert:

    def __init__ (self, heading, body):
        self.heading = heading
        self.body = body
        self.type = 'confirm'
        self.image = confirmAlertPic
        self.confirmed = False
        self.smallFont = False

    def write(self):
        headingSize = 36
        bodySize = 24
        lineSpacing = 6
        if self.smallFont:
            headingSize = 32
            bodySize = 21
            lineSpacing = 5
        headingFont = pygame.font.Font('polly.ttf', headingSize)
        bodyFont = pygame.font.Font('polly.ttf', bodySize)


        heading = headingFont.render(self.heading, True, palette.darkGold)

        lines = self.body.split('#')

        screen.blit(self.image, (700, 0))
        screen.blit(heading, (770, 224))
        for i in range(len(lines)):
            lines[i] = bodyFont.render(lines[i], True, palette.axolotl)
            height = 224 + headingSize + lineSpacing + i*(bodySize+lineSpacing)
            screen.blit(lines[i], (770, height))

    def confirmOrDeny(self):
        if inCircle(pygame.mouse.get_pos(), [700 + 394, 433], 15):
            self.confirmed = True
            return 'confirmed'
        return False

# -------------------------------------------------------------------------------
# MISC CLASSES
class Roll: # Every side of the dice is its own object, of this class.
    def __init__(self, image, value):
        self.image = image
        self.value = value

class Button: # The menu is made up of buttons, which are in the list 'buttons' and belong to this class.
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.left = pos[0]
        self.top = pos[1]
        self.right = pos[0] + size[0]
        self.bottom = pos[1] + size[1]
        self.middle = ((self.left+self.right)//2, (self.top+self.bottom)//2)
    def mouseHover(self): # Returns True if the mouse is over the button.
        mousepos = pygame.mouse.get_pos()
        if self.left < mousepos[0] < self.right and self.top < mousepos[1] < self.bottom:
            return True
        return False

class Palette: # Aside from the house colours, there are only six colours that I use in the game, ranging from darkish green to yellowish brown. I found the palette online, hence the fancy colour names.
    def __init__(self):
        self.axolotl = (115, 128, 84)
        self.olivine = (163, 168, 109)
        self.dutchWhite = (225, 213, 184)
        self.darkVanilla = (214, 199, 167)
        self.camel = (190, 153, 110)
        self.darkGold = (170, 114, 42)

class Card: # Chance and Community Chest cards
    def __init__(self, text, type, value):
        self.text = text
        self.type = type
        self.value = value
        self.executed = False

    def execute(self, player): # A set of conditionals that do different stuff to the player who picked the card.
        if self.type == 'pay':
            player.money += self.value
        elif self.type == 'move':
            if player.boardpos > self.value:
                player.money += 200
                player.turnNum += 1
            player.boardpos = self.value
        elif self.type == 'go to jail':
            player.inJail = True
        elif self.type == 'gojf':
            if self.text.__contains__('bribed'):
                player.getOutOfJailFreeCards.append(communityChest[4])
            else:
                player.getOutOfJailFreeCards.append(chance[7])
            player.canRoll = False
        elif self.type == 'social':
            for sprite in players:
                if sprite == player:
                    sprite.money += self.value*(len(players)-1)
                else:
                    sprite.money -= self.value
        elif self.type == 'repairs':
            for prop in properties:
                if prop.owner == player:
                    if prop.houses > 4:
                        player.money -= self.value[1]
                    else:
                        player.money -= self.value[0]*prop.houses
        # elif self.type == 'nearestu': # utility 다 삭제했으니까
        #     if 0 < player.boardpos <= 12:
        #         player.boardpos = 12
        #     elif 28 < player.boardpos < 40:
        #         player.boardpos = 12
        #         player.money += 200
        #         player.turnNum += 1
        #     else:
        #         player.boardpos = 28
        elif self.type == 'nearests':
            if 0 < player.boardpos <= 5:
                player.boardpos = 5
            elif player.boardpos <= 13:
                player.boardpos = 13
            elif player.boardpos <= 23:
                player.boardpos = 23
            elif player.boardpos <= 32:
                player.boardpos = 32
            else:
                player.boardpos = 5
                player.money += 200
                player.turnNum += 1
        elif self.type == 'mover':
            player.boardpos += self.value

class Ratio: # Part of Eve's property valuing system
    def __init__(self, cost, rent):
        self.cost = cost
        self.rent = rent
        self.value = self.cost/self.rent

# -------------------------------------------------------------------------------
# MISC FUNCTIONS

def inCircle(mousePos, circleMid, radius): # Checks if the mouse is in a circle with a given position and radius.
    if (mousePos[0]-circleMid[0])**2 + (mousePos[1]-circleMid[1])**2 <= radius**2:
        return True
    return False

def clickingOnButton():
    global buttons
    for button in buttons:
        if button.mouseHover():
            return True
    return False

def rollDice(die):
    roll1 = random.choice(die)
    roll2 = random.choice(die)
    return [roll1, roll2]

def getAvg(listOfRatios):
    sum = 0
    for ratio in listOfRatios:
        sum += ratio.value
    return sum/len(listOfRatios)

def avgDiff(listOfNums):
    diffList = []
    for i in range(len(listOfNums)-1):
        diff = listOfNums[i+1] - listOfNums[i]
        diffList.append(diff)
    avg = sum(diffList)/len(diffList)
    return avg


# -------------------------------------------------------------------------------
# MISC METHODS
def draw(player, pos): # I wrote a function to draw players becasue there are two parts to their pieces: the colour, and the piece itself.
    if player == user:
        screen.blit(userColour, pos)
        screen.blit(user.piece, pos)
    elif player == Eve:
        screen.blit(EveColour, pos)
        screen.blit(Eve.piece, pos)

def boardSetup(): # Sets up all the lists of properties and squares
    global squares, properties, colours
    
    notPropertyNames = ['Go', 'Community Chest', 'Chance', 'Jail', 'Free Parking', 'Space Trip',
                        'Super Tax']

    squareNames = ['Go', 'France', 'Community Chest', 'England',
                    'North Station', 'Thailand', 'Chance', 'Turkey', 'Iran', 
                    'Jail', 'Congo', 'Germany','Vietnam', 'East Station', 'Egypt', 'Community Chest',
                    'Philippines', 'Ethiopia', 
                    'Free Parking', 'Japan', 'Chance', 'Mexico',
                    'Russia', 'South Station', 'Bangladesh', 'Nigeria',
                    'Pakistan', 
                    'Space Trip', 'Brazil', 'Indonesia', 'Community Chest',
                    'America', 'West Station', 'India', 'Super Tax', 'China']

    for i in range(len(squareNames)):
        if not squareNames[i] in notPropertyNames:
            currentProp = Property(squareNames[i], i, 10)
            if currentProp.name.__contains__('Station'):
                currentProp.colour = 8
            # modified start 5
            else:
                if 0 < i < 4:
                    currentProp.colour = 0
                elif 4 < i < 9:
                    currentProp.colour = 1
                elif 9 < i < 13:
                    currentProp.colour = 2
                elif 13 < i < 18:
                    currentProp.colour = 3
                elif 18 < i < 23:
                    currentProp.colour = 4
                elif 23 < i < 27:
                    currentProp.colour = 5
                elif 27 < i < 32:
                    currentProp.colour = 6
                elif 32 < i < 36: 
                    currentProp.colour = 7
                    
            currentProp.rent = currentProp.getInitialRent()
            squares.append(currentProp)
            properties.append(currentProp)
            if currentProp.colour <= 7:
                streets[currentProp.colour].append(currentProp)
        elif squareNames[i] == 'Chance' or squareNames[i] == 'Community Chest':
            currentChance = Chance(squareNames[i], i)
            squares.append(currentChance)
        elif squareNames[i].__contains__('Tax'):
            currentTax = TaxSquares(squareNames[i], i)
            squares.append(currentTax)
        else:
            currentSpecial = SpecialSquares(squareNames[i], i)
            squares.append(currentSpecial)
        # modified end 5

def showMenu(): # Draws the side menu
    global buttons, user, Eve, palette, board, background, buttonActions

    screen.fill(palette.axolotl)
    screen.blit(board, (28.5, 28.5))
    screen.blit(background, (700, 0))

    turnFont = pygame.font.Font('polly.ttf', 45)
    if user.isTurn:
        turnText = turnFont.render('YOUR TURN', True, palette.dutchWhite)
    else:
        turnText = turnFont.render('EVE\'S TURN', True, palette.dutchWhite)
    screen.blit(turnText, (870, 60))

    for button in buttons:
        if button == endTurnButton or button == mortgageButton:
            screen.blit(endTurnBehind, (button.pos))

        if button.mouseHover():
            pygame.draw.rect(screen, palette.dutchWhite, (button.pos, button.size))

        if button == endTurnButton and not etAvailable:
            screen.blit(endTurnUnAv, (button.pos))

        if button == endTurnButton:
            screen.blit(endTurnFront, (button.pos))
        elif button == mortgageButton:
            screen.blit(mortgageFront, (button.pos))

    if buttonActions[0]:
        screen.blit(throw[0].image, (188+11+37, 210+33))
        screen.blit(throw[1].image, (188+38+150, 210+33))


    screen.blit(buttonsPic, (700, 0))

    draw(user, (770, 50))
    draw(Eve, (730, 636))

    moneyFont = pygame.font.Font('polly.ttf', 40)
    userMoney = moneyFont.render('$' + str(user.money), True, palette.darkVanilla)
    EveMoney = moneyFont.render('$' + str(Eve.money), True, palette.darkVanilla)

    screen.blit(userMoney, (760, 150))
    screen.blit(EveMoney, (820, 646))

# -------------------------------------------------------------------------------
#GET RENT METHODS

# These are methods that update the rent value of properties based on houses and neighbours and stuff

def getRentStations():
    global squares
    stations = [squares[4], squares[13], squares[23], squares[32]]
    for currentStation in stations:
        matchesCount = -1
        if currentStation.owner != bank:
            for station in stations:
                if station.owner == currentStation.owner:
                    matchesCount += 1
            currentStation.rent = (2**matchesCount)*25

def getRentProperties():
    global properties, streets
    for street in streets:
        for currentProp in street:
            if currentProp.owner != bank:
                for prop in street:
                    if prop.owner == currentProp.owner:
                        if currentProp.houses >= 0:
                            currentProp.streetOwned = True
                            # currentProp.rent = currentProp.getInitialRent() * 2
                            currentProp.updateRent()
                        else:
                            currentProp.streetOwned = False
   
# -------------------------------------------------------------------------------
#GET WORTH METHODS

# These methods update the realWorth attribute of properties based on their neighbours

def getWorthProperties():
    for prop in properties:
        prop.realWorth = prop.getInitialWorth()
    for street in streets:
        for currentProp in street:
            neighboursOwnedByEve = 0
            neighboursOwnedByUser = 0
            for neighbour in street:
                if neighbour != currentProp:
                    if neighbour.owner == Eve:
                        neighboursOwnedByEve += 1
                    elif neighbour.owner == user:
                        neighboursOwnedByUser += 1

            if neighboursOwnedByEve > 0 and neighboursOwnedByUser > 0:
                currentProp.realWorth -= 50
            else:
                currentProp.realWorth += 150 - (len(street)-neighboursOwnedByUser-neighboursOwnedByEve)*50

            for house in range(currentProp.houses):
                currentProp.realWorth += currentProp.houseWorth

def getWorthStations():
    stations = [squares[4], squares[13], squares[23], squares[32]]
    for station in stations:
        station.realWorth = station.getInitialWorth()
        neighboursOwnedByEve = 0
        neighboursOwnedByUser = 0
        for neighbour in stations:
            if neighbour.owner == Eve:
                neighboursOwnedByEve += 1
            elif neighbour.owner == user:
                neighboursOwnedByUser += 1
        if neighboursOwnedByEve > 0 and neighboursOwnedByUser > 0:
            station.realWorth += 25*(neighboursOwnedByEve + neighboursOwnedByUser)
        else:
            station.realWorth += 50 * (neighboursOwnedByEve + neighboursOwnedByUser)
