
import pygame
import math
import random
import time
from pygame import mixer
from Classesandfunction import Roll
# -------------------------------------------------------------------------------
#PIECES
boot = pygame.image.load('pieces/boot.png')
car = pygame.image.load('pieces/car.png')
dog = pygame.image.load('pieces/dog.png')
hat = pygame.image.load('pieces/hat.png')
iron = pygame.image.load('pieces/iron.png')
ship = pygame.image.load('pieces/ship.png')
thimble = pygame.image.load('pieces/thimble.png')
wheelbarrow = pygame.image.load('pieces/wheelbarrow.png')

pieces = [boot, car, dog, hat, iron, ship, thimble, wheelbarrow]


# -------------------------------------------------------------------------------
#DICE
dieOne = Roll(pygame.image.load('dice/one.png'), 1)
dieTwo = Roll(pygame.image.load('dice/two.png'), 2)
dieThree = Roll(pygame.image.load('dice/three.png'), 3)
dieFour = Roll(pygame.image.load('dice/four.png'), 4)
dieFive = Roll(pygame.image.load('dice/five.png'), 5)
dieSix = Roll(pygame.image.load('dice/six.png'), 6)

die = [dieOne, dieTwo, dieThree, dieFour, dieFive, dieSix]

roll = 0
throw = [0, 0]

# -------------------------------------------------------------------------------
#BUTTONS
background = pygame.image.load('background.png')
buttonsPic = pygame.image.load('buttons.png')

endTurnBehind = pygame.image.load('endTurnBehind.png')
endTurnFront = pygame.image.load('endTurnFront.png')
endTurnUnAv = pygame.image.load('endTurnUnAv.png')
etAvailable = False

mortgageFront = pygame.image.load('mortgageFront.png')

rollButton = Button([1143, 0], [157, 161])
developButton = Button([1143, 161], [157, 161])
tradeButton = Button([1143, 318], [157, 161])
quitButton = Button([1143, 475], [157, 161])
endTurnButton = Button([849, 475], [157, 161])
mortgageButton = Button([996, 475], [157, 161])

buttons = [rollButton, developButton, tradeButton, quitButton, mortgageButton, endTurnButton]
buttonActions = [False, False, False, False, False]

# -------------------------------------------------------------------------------
#CHANCE AND COMMUNITY CHEST
gojfCC = pygame.image.load('gojfComChest.png')
gojfC = pygame.image.load('gojfChance.png')

communityChest = [
    Card('Advance to Go. Collect $400.', 'move', 0), Card("The bank's web server got #COVID and accidentally deposits #into your account. Collect $200.", 'pay', 200),
    Card("You hurt yourself but there's #no socialised medicine. #Pay $50 and remember- you have #nothing to lose but your chains.", 'pay', -50),
    Card('You made some banger #investments. Collect $50.', 'pay', 50), Card('You argue that you murdered #the child in self defence: #Get out of Jail free.', 'gojf', gojfCC),
    Card('The government planted drugs #on you to meet prison quotas. #Go to Jail. Go directly to Jail. #Do not pass Go, do not collect $200.', 'go to jail', 0),
    Card('Your great-Aunt Gertrude #kicks the bucket. Inherit $100', 'pay', 100),
    Card('Happy Birthday! #Collect $10 from every player', 'social', 10), Card('You and your life insurance mature. #Collect $100', 'pay', 100),
    Card("You got COVID- pay #hospital fees of $50", 'pay', -50), Card('Your friend Banquo was #prophecised to father #a line of kings. #Pay $50 to hire a hitman', 'pay', -50),
    Card('You find $25 bucks on the #ground. Its your lucky day.', 'pay', 25), Card('Make hardcore repairs #on all your property. #For each house pay $40, #for each hotel pay $115', 'repairs', [40, 115]),
    Card('You have come last in a #beauty contest. Collect $10 #sympathy money', 'pay', 10), Card('Your co-worker gives you $100 #not to tell anyone about his #heroin addiction', 'pay', 100)
]
chance = [
    Card('Advance to Go. Collect $400.', 'move', 0), Card('Advance to Russia. #If you pass Go, collect $200.', 'move', 22), Card('Advance to China. #If you pass Go, collect $200.', 'move', 35),
    Card('Advance to Congo. #If you pass Go, collect $200.', 'move', 10), Card('Advance to North Station. #If you pass Go, collect $200.', 'move', 4),
    # Card('Advance to the nearest utility. #If you pass Go, collect $200', 'nearestu', 0),
    Card('Advance to the nearest station. #If you pass Go, collect $200', 'nearests', 0),
    Card('Bank pays you some of that #sweet sweet mullah. Collect $50.', 'pay', 50), Card('You bribe the cops with donuts: #Get out of jail free', 'gojf', gojfC), Card('Go back 3 spaces', 'mover', -3),
    Card('You infringed the copyright of #a popular board game. #Go to Jail. Go directly to Jail. #Do not pass Go, do not collect $200.', 'go to jail', 0),
    Card('Make general repairs on all your #property. For each house pay $25, #for each hotel pay $100', 'repairs', [25, 100]), Card('25 bucks fall out of your pocket. #You lament the lack of women\'s #shorts with reasonably-sized pockets', 'pay', -25),
    Card("You have mysteriously #become everybody's grandma. #Pay each player #$50 as a present.", 'social', -50), Card('Your investment in divorce #lawyers was successful. #Collect $150.', 'pay', 150)
]


# -------------------------------------------------------------------------------
#PROPERTY DECO

housePic = pygame.image.load('house.png')
hotelPic = pygame.image.load('hotel.png')
houseSidePic = pygame.image.load('houseSide.png')
hotelSidePic = pygame.image.load('hotelSide.png')

buildingPics = [
    housePic, hotelPic,
    houseSidePic, hotelSidePic,
    pygame.transform.rotate(housePic, 180), pygame.transform.rotate(hotelPic, 180),
    pygame.transform.rotate(houseSidePic, 180), pygame.transform.rotate(hotelSidePic, 180),
]

# Rent you pay at each house level for each street
houseCostGrid = [
    [
        [2, 10, 30, 90, 160, 250], [4, 20, 60, 180, 320, 450]
    ], [
        [6, 30, 90, 270, 400, 550], [8, 40, 100, 300, 450, 600]
    ], [
        [10, 50, 150, 450, 625, 750], [12, 60, 180, 500, 700, 900]
    ], [
        [14, 70, 200, 550, 750, 950], [16, 80, 220, 600, 800, 1000]
    ], [
        [18, 90, 250, 700, 875, 1050], [20, 100, 300, 750, 925, 1100]
    ], [
        [22, 110, 330, 800, 975, 1150], [24, 120, 360, 850, 1025, 1200]
    ], [
        [26, 130, 390, 900, 1100, 1275], [28, 150, 450, 1000, 1200, 1400]
    ], [
        [35, 175, 500, 1100, 1300, 1500], [50, 200, 600, 1400, 1700, 2000]
    ]
]

mortgagePic = pygame.image.load('mortgage.png')
mortgagePic2 = pygame.transform.rotate(mortgagePic, 90)

# -------------------------------------------------------------------------------
# WINDOW
pygame.init()

screen = pygame.display.set_mode((1300, 700))

pygame.display.set_caption("Monopoly")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# -------------------------------------------------------------------------------
# COLOURS
palette = Palette()

playerColours = [palette.axolotl, palette.camel, palette.darkGold]
colours = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'indigo', 'purple', 'station', 'utility', 'undefined']

axolotlPiece = pygame.image.load('pieces/axolotlPiece.png')
darkVanillaPiece = pygame.image.load('pieces/darkVanillaPiece.png')
camelPiece = pygame.image.load('pieces/camelPiece.png')
darkGoldPiece = pygame.image.load('pieces/darkGoldPiece.png')

pieceColours = [axolotlPiece, camelPiece, darkGoldPiece]

# -------------------------------------------------------------------------------
# FREE PARKING
freeParking = 0

freeParkingFont = pygame.font.Font('polly.ttf', 40)
freeParkingText = freeParkingFont.render("Free Parking:", True, palette.darkVanilla)
freeParkingValue = freeParkingFont.render('$' + str(freeParking), True, palette.darkVanilla)

# -------------------------------------------------------------------------------
# ALERTS
choiceAlertPic = pygame.image.load('choiceAlert.png')
alertPic = pygame.image.load('alert.png')
confirmAlertPic = pygame.image.load('confirmAlert.png')
tradeAlertPic = pygame.image.load('tradeAlert.png')

# moneyToTake = MoneyOffer(0)
# moneyToGive = MoneyOffer(0)

auctionPic = pygame.image.load('auction.png')

welcome = Alert('Welcome to Monopoly',
"Your opponent is an AI called #Eve. She likes walks on the beach #and daydreaming about the robot #revolution.")

# -------------------------------------------------------------------------------
# SPRITES

# Here are the screens for the animations when someone wins. I'm not sure how to actually do gifs so I draw different pictures every 0.2 seconds.
ugos1 = pygame.image.load('game over/user1.png')
ugos2 = pygame.image.load('game over/user2.png')
ugos3 = pygame.image.load('game over/user3.png')
ugos4 = pygame.image.load('game over/user4.png')
ugos5 = pygame.image.load('game over/user5.png')

ugoScreens = [ugos1, ugos2, ugos3, ugos4, ugos5]

cgos1 = pygame.image.load('game over/CPU1.png')
cgos2 = pygame.image.load('game over/CPU2.png')
cgos3 = pygame.image.load('game over/CPU3.png')

cgoScreens = [cgos1, cgos2, cgos3]

user = Player('You', True, ugoScreens)
Eve = Player('Eve', False, cgoScreens)
players = [user, Eve]

bank = Bank()

winner = None

# -------------------------------------------------------------------------------
# BOARD
board = pygame.image.load("board(643x643).png")

squares = []
properties = []
streets = [[],[],[],[],[],[],[],[]]
boardSetup()

# -------------------------------------------------------------------------------
# AI SETUP
AI = AI()

costRatios = []
houseRatios = []

# Here is where it sets up initialMod and houseMod

for prop in properties:
    if prop.colour <= 7:
        costs = prop.getCostOfHouse() + prop.getPrice()
        rents = sum(prop.costsList) + prop.getInitialRent()
        ratio = Ratio(costs, rents)
        costRatios.append(ratio)

        costs = prop.getCostOfHouse()
        rents = avgDiff([prop.getInitialRent()]+prop.costsList)
        ratio = Ratio(costs, rents)
        houseRatios.append(ratio)

initialMod = getAvg(costRatios)
houseMod = getAvg(houseRatios)

for prop in properties:
    if prop.colour <= 7:
        prop.realWorth = prop.getInitialWorth()
        prop.houseWorth = prop.getInitialHouseWorth()


# -------------------------------------------------------------------------------
# SELECTING PIECES AND COLOURS

choosePieceFont = pygame.font.Font('polly.ttf', 100)
choosePieceText = choosePieceFont.render("Select Piece:", True, palette.darkVanilla)

while not user.pieceConfirmed:

    screen.fill(palette.axolotl)
    screen.blit(pygame.image.load('choosePiece.png'), (0, 0))

    if user.pieceSelected:
        pygame.draw.rect(screen, palette.olivine, (user.pieceSelected, (270, 128)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if user.pieceSelected and inCircle(pygame.mouse.get_pos(), [1139, 206], 32.5):
                user.pieceConfirmed = True
            else:
                user.pieceSelected = user.choosePiece(pygame.mouse.get_pos())

    screen.blit(choosePieceText, (150, 125))
    screen.blit(pygame.image.load('piecesForChoosing.png'), (0, 0))

    pygame.display.update()

pieces.remove(user.piece)

user.colour = random.choice(playerColours)
userColour = pieceColours[playerColours.index(user.colour)]

playerColours.remove(user.colour)
pieceColours.remove(userColour)

Eve.piece = random.choice(pieces)

Eve.colour = random.choice(playerColours)
EveColour = pieceColours[playerColours.index(Eve.colour)]

playerColours.remove(Eve.colour)
pieceColours.remove(EveColour)



# -------------------------------------------------------------------------------
# MUSIC

beginning = True
mixer.music.load('music.wav')
mixer.music.play(-1)
