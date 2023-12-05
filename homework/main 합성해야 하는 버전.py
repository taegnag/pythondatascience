# Start here


import pygame
import math
import random
import time
from pygame import mixer
from Classesandfunction import *
from misc import *

# -------------------------------------------------------------------------------
# TUTORIAL

tutorial = True
tuteAlert = Alert('Welcome to Monopoly', 'Would you like a tutorial?')
tuteScreensNum = 7
example = ''

while tutorial:
    screen.fill(palette.axolotl)
    freeParkingValue = freeParkingFont.render('$' + str(freeParking), True, palette.darkVanilla)

    showMenu()

    screen.blit(dieOne.image, (188 + 11 + 37, 210 + 33))
    screen.blit(dieOne.image, (188 + 38 + 150, 210 + 33))

    screen.blit(freeParkingText, (250, 372))
    screen.blit(freeParkingValue, (310, 424))

    for prop in properties:
        prop.drawColour()

    draw(Eve, Eve.getPos())
    draw(user, user.getPos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tuteAlert.confirmOrDeny() == 'confirmed':
                if tuteAlert.heading == 'Welcome to Monopoly':
                    tuteAlert = Alert('Tutorial - 1 of ' + str(tuteScreensNum),
                                      'This is the \'roll\' button. #Press it to roll the dice #in the middle of the board.')
                    for prop in properties:
                        prop.owner = random.choice(players)

                elif tuteAlert.heading.__contains__('1 of'):
                    tuteAlert = Alert('Tutorial - 2 of ' + str(tuteScreensNum),
                                      'This is the \'develop\' button. #Press it to build houses on your #properties later in the game.')

                elif tuteAlert.heading.__contains__('2 of'):
                    tuteAlert = Alert('Tutorial - 3 of ' + str(tuteScreensNum),
                                      'This is the \'trade\' button. #Press it to initialise a trade #with Eve, your opponent.')

                elif tuteAlert.heading.__contains__('3 of'):
                    tuteAlert = Alert('Tutorial - 4 of ' + str(tuteScreensNum),
                                      'This is the \'forfeit\' button. #Press it to quit the game.')

                elif tuteAlert.heading.__contains__('4 of'):
                    tuteAlert = Alert('Tutorial - 5 of ' + str(tuteScreensNum),
                                      'This is the \'Dispose\' button. #Press it to dispose #a property or sell a house.')

                elif tuteAlert.heading.__contains__('5 of'):
                    tuteAlert = Alert('Tutorial - 6 of ' + str(tuteScreensNum),
                                      'This is the \'end turn\' button. #Press it when it is availiable #to end your turn.')

                elif tuteAlert.heading.__contains__('6 of'):
                    if properties[len(properties)-3].owner.colour == palette.axolotl:
                        if properties[len(properties)-3].owner == user:
                            example = 'eg. you own West #Station, so it\'s green. '
                        else:
                            example = 'eg. Eve owns West #Station, so it\'s green. '
                    elif properties[len(properties)-3].owner.colour == palette.camel:
                        if properties[len(properties)-3].owner == user:
                            example = 'eg. you own West #Station, so it\'s beige. '
                        else:
                            example = 'eg. Eve owns West #Station, so it\'s beige. '
                    elif properties[len(properties)-3].owner.colour == palette.darkGold:
                        if properties[len(properties)-3].owner == user:
                            example = 'eg. you own West #Station, so it\'s dark gold. '
                        else:
                            example = 'eg. Eve owns West #Station, so it\'s dark gold. '
                    tuteAlert = Alert('Tutorial - 7 of ' + str(tuteScreensNum),
                                      'These rectangles indicate each #property\'s owner. ' + example + 'Click on #these rectangles to select properties #when disposing or building.')

                elif tuteAlert.heading.__contains__('7 of'):
                    tutorial = False
                    break

                tuteAlert.body += '#Press \'OK\' to continue.'
            if tuteAlert.confirmOrDeny() == 'denied':
                if tuteAlert.heading == 'Welcome to Monopoly':
                    tutorial = False
                    break

    for i in range(tuteScreensNum):
        if tuteAlert.heading.__contains__(str(i+1) + ' of') and i < len(buttons):
            pygame.draw.circle(screen, palette.darkGold, buttons[i].middle, 157//2, 10)
        elif tuteAlert.heading.__contains__('7 of'):
            pygame.draw.circle(screen, palette.darkGold, (693, 350), 45, 10)

    tuteAlert.write()

    pygame.display.update()


for prop in properties:
    prop.owner = bank

# -------------------------------------------------------------------------------
# GAME LOOP
while not (winner==Eve or winner==user):
    freeParkingValue = freeParkingFont.render('$' + str(freeParking), True, palette.darkVanilla)

    showMenu()

    screen.blit(freeParkingText, (250, 372))
    screen.blit(freeParkingValue, (310, 424))

    for prop in properties:
        prop.drawColour()

    getRentProperties()
    getRentStations()

    getWorthProperties()
    getWorthStations()
    
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if user.isTurn: # checking to see if user has clicked on any buttons
                betterTradeMessage = False

                if (alert.type == 'choice' or alert.type == 'confirm')  and clickingOnButton():
                    if alert.type == 'choice' and not alert.body.__contains__('Answer the question woodja'):
                        alert.body += ' #Answer the question woodja'
                    elif alert.type == 'confirm' and not alert.body.__contains__('You gotta click "OK" mate'):
                        alert.body += ' #You gotta click "OK" mate'

                # elif alert.type == 'trade' and clickingOnButton():
                #     betterTradeMessage = True

                elif rollButton.mouseHover() and user.canRoll:
                    beginning = False
                    user.normalGameplay = True
                    user.isMortgaging = False
                    user.isDeveloping = False
                    justLanded = True

                    throw = rollDice(die)
                    buttonActions[0] = True
                    roll = throw[0].value + throw[1].value
                    # roll = 9
            
                    for square in squares:
                        if type(square) == Property:
                            square.rejected = False
                            square.paidRent
                        elif type(square) == TaxSquares or type(square) == SpecialSquares:
                            square.paid = False

                    for comcard in communityChest:
                        comcard.executed = False
                    for chancecard in chance:
                        chancecard.executed = False
                    card = None

                    if throw[0] == throw[1] and user.doublesCount < 3:
                        user.canRoll = True
                        if user.inJail:
                            alert = Alert('They see me rollin\'', 'They hatin\', #\'Cause I be gettin\' #out of jail for free')
                        user.doublesCount += 1
                    else:
                        user.canRoll = False
                    if user.doublesCount >= 3:
                        user.normalGameplay = False
                        user.timeMoving = 0
                        alert = Alert('Serial doubles-roller', 'You rolled doubles 3 times #in a row. You really are #a despicable person.')
                        user.canRoll = False
                    if user.inJail:
                        user.timeMoving = 0
                        user.jailTurns += 1
                    elif alert.heading != 'Serial doubles-roller':
                        user.timeMoving = roll

                elif developButton.mouseHover():
                    alert = Alert('Build?', 'Would you like to develop #your properties?')
                    user.normalGameplay = False

                elif quitButton.mouseHover():
                    alert = Alert('You sure mate?', 'Are you sure you want #to resign? Eve will #automatically win.')
                    user.normalGameplay = False

                elif mortgageButton.mouseHover():
                    alert = Alert('Dispose and friends', 'Do you want to dispose a property #or sell a house?')
                    user.normalGameplay = False

                elif endTurnButton.mouseHover() and etAvailable:
                    if user.money < 0:
                        alert = Alert('Memories from 2008', 'You need $' + str(0-user.money) + ' to continue. #Do you want to declare #bankruptcy?')
                    else:
                        user.isTurn = False
                        Eve.isTurn = True
                        Eve.canRoll = True
                        user.canRoll = True
                        user.doublesCount = 0
                        etAvailable = False

                elif user.isDeveloping:
                    for prop in properties:
                        if prop.buttonPosition[0][0] < pygame.mouse.get_pos()[0] < prop.buttonPosition[0][1] and prop.buttonPosition[1][0] < pygame.mouse.get_pos()[1] < prop.buttonPosition[1][1]:
                            if prop.owner == user:
                                alert = Alert('Build house?', 'Would you like to build 1 house #on ' + prop.name + ' for $' + str(prop.getCostOfHouse()) + '?')
                              
                elif user.isMortgaging:
                    for prop in properties:
                        if prop.owner == user and prop.buttonPosition[0][0] < pygame.mouse.get_pos()[0] < prop.buttonPosition[0][1] and prop.buttonPosition[1][0] < pygame.mouse.get_pos()[1] < prop.buttonPosition[1][1]:
                            if prop.houses <= 0:
                            #     if prop.mortgaged:
                            #         alert = Alert('Unmortgage', 'Unmortgage ' + prop.name + ' for $' + str(prop.getPrice()) + '?')
                            #     else:
                                      alert = Alert('Dispose', 'Dispose ' + prop.name + ' for $' + str(int(prop.getPrice()/2)) + '?')
                            else:
                                alert = Alert('Sell house?', 'Sell house on ' + prop.name + ' for $' + str(int(prop.getCostOfHouse()*0.9)) + '?')

            if alert.confirmOrDeny() == 'denied': # Regardless of whose turn it is, user can confirm/deny alerts
                if alert.heading == 'Unowned Property':
                    squares[user.boardpos].rejected = True
                    alert = Alert('hell nah', "ddd")
                    
                if alert.heading == 'You sure mate?':
                    alert = Alert("That's the spirit", 'Good on ya mate')

                if alert.heading == 'Get out of Jail Free?':
                    alert = Alert('Go to Jail', '')
                    user.getOutOfJailFreeCards.remove(user.getOutOfJailFreeCards[0])
                    user.inJail = True
                    user.jailTurns = 0
                
                if alert.heading == 'Build?':
                    alert = Alert('Bruh', "Why did you click on #the house button then")

                if alert.heading == 'Build house?':
                    alert = Alert('Alrighty then', 'Click on another property to develop')

                if alert.heading == 'Dispose and friends':
                    alert = Alert('You sure?', 'I heard disposal was #really trendy in 2020')

                if alert.heading == 'Dispose':
                    alert = Alert('Flipper-flopper', 'You\'re a flipper flopper #aren\'t you mate')

                if alert.heading == 'Memories from 2008':
                    alert = Alert('OK chief', 'Maybe you should dispose #some properties or something')
                    
                if alert.heading == 'Space Trip':
                    alert = Alert('What a waste', 'you missed a good opportunity...')
                
            if alert.confirmOrDeny() == 'confirmed':
                if alert.heading == 'Unowned Property':
                        squares[user.boardpos].rejected = True
                        squares[user.boardpos].owner = user
                        user.money -= squares[user.boardpos].getPrice()
                        alert = Alert('', '')

                if alert.heading == 'You sure mate?':
                    winner = Eve
                # modified start 6
                if alert.heading == 'Get out of Jail Free?':
                        alert = Alert('Dodgy Dealing', "You did some dodgy deals #but hey, haven't we all")
                        user.getOutOfJailFreeCards.remove(user.getOutOfJailFreeCards[0])
                        user.inJail = False
                        user.jailTurns = 0
                #
                if alert.heading == 'Chance':
                    for cardBoi in chance:
                        if alert.body.__contains__(cardBoi.text):
                            if not cardBoi.executed:
                                cardBoi.execute(user)
                                cardBoi.executed = True

                if alert.heading == 'Community Chest':
                    for cardBoi2 in communityChest:
                        if alert.body.__contains__(cardBoi2.text):
                            if not cardBoi2.executed:
                                cardBoi2.execute(user)
                                cardBoi2.executed = True

                if alert.heading == 'Build?':
                    user.isDeveloping = True
                    user.isTrading = False
                    user.isMortgaging = False
                    alert = Alert('Building', 'Select a property to #develop')

                if alert.heading == 'Build house?':
                    for prop in properties:
                        if alert.body.__contains__(prop.name):
                            if prop.boardpos == user.boardpos and squares[prop.boardpos].owner == user:
                                if user.turnNum == 0:
                                    alert = Alert('Nah mate', "check the rule again")
                                elif user.turnNum == 1 and prop.houses == 0:
                                    prop.houses += 1
                                    user.money -= prop.getCostOfHouse()
                                    alert = Alert('Bob the builder', 'You built 1 house on ' + prop.name)
                                elif user.turnNum == 1 and prop.houses == 1:
                                    alert = Alert('Nah mate', "check the rule again")
                                elif user.turnNum == 2 and prop.houses == 0:
                                    prop.houses += 1
                                    user.money -= prop.getCostOfHouse()
                                    alert = Alert('Bob the builder', 'You built 1 house on ' + prop.name)
                                elif user.turnNum == 2 and prop.houses == 1:
                                    prop.houses += 1
                                    user.money -= prop.getCostOfHouse()
                                    alert = Alert('Bob the builder', 'You built 1 house on ' + prop.name)
                                elif user.turnNum == 2 and prop.houses == 2:
                                    prop.houses += 1
                                    user.money -= prop.getCostOfHouse()
                                    alert = Alert('Bob the builder', 'You built 1 house on ' + prop.name)
                                elif user.turnNum == 2 and prop.houses == 3:
                                    alert = Alert('Nah mate', "check the rule again")
                                elif user.turnNum >= 3 and prop.houses == 0:
                                    prop.houses += 1
                                    user.money -= prop.getCostOfHouse()
                                    alert = Alert('Bob the builder', 'You built 1 house on ' + prop.name)
                                elif user.turnNum >= 3 and prop.houses == 1:
                                    prop.houses += 1
                                    user.money -= prop.getCostOfHouse()
                                    alert = Alert('Bob the builder', 'You built 1 house on ' + prop.name)
                                elif user.turnNum >= 3 and prop.houses == 2:
                                    prop.houses += 1
                                    user.money -= prop.getCostOfHouse()
                                    alert = Alert('Bob the builder', 'You built 1 house on ' + prop.name)
                                elif user.turnNum >= 3 and prop.houses == 3:
                                    prop.houses += 1
                                    user.money -= prop.getCostOfHouse()
                                    alert = Alert('Fancy fancy', 'You built a hotel on ' + prop.name)
                                else:
                                    alert = Alert('Nah mate', "check the rule again")
                            elif prop.boardpos != user.boardpos and squares[prop.boardpos].owner == user:
                                alert = Alert('Nah mate', "check the rule again")

                if alert.heading == 'Dispose and friends':
                    alert = Alert('Manage properties', 'Select a property to manage')
                    user.isMortgaging = True
                    user.isDeveloping = False
                    user.isTrading = False

                if alert.heading == 'Dispose':
                    for prop in properties:
                        if alert.body.__contains__(prop.name):   
                            user.money += int(prop.getPrice() * 0.7)
                            prop.owner = bank
                            alert = Alert('Manage properties', 'Select a property to manage')
                            
                if alert.heading == 'Sell house?':
                    for prop in properties:
                        if alert.body.__contains__(prop.name) and prop.houses > 0:
                            cantSell = False
                            for neighbour in streets[prop.colour]:
                                if neighbour.houses > prop.houses:
                                    cantSell = True
                                    break
                            if cantSell:
                                alert = Alert('Communist ideology', 'You have to develop your #properties equally.')
                            else:
                                prop.houses -= 1
                                user.money += int(prop.getCostOfHouse()*0.9)
                                alert = Alert('Manage properties', 'Select a property to manage')

                if alert.heading == 'They see me rollin\'':
                    user.normalGameplay = True
                    user.inJail = False
                    user.timeMoving = roll

                if alert.heading == 'Serial doubles-roller':
                    user.inJail = True
                    user.jailTurns = 0
                    user.doublesCount = 0
                    alert = Alert('', '')
                    
                if alert.heading == 'Not-so-smooth criminal':
                    user.jailTurns = 0
                    user.inJail = True
                    user.canRoll = False
                    alert = Alert('', '')

                if alert.heading == 'Space Trip':
                    alert = Alert('Traveling', 'Send to random place')
                    SpaceTripNum = random.randint(0,35)
                    squareNames = ['Go', 'France', 'Community Chest', 'England',
                    'North Station', 'Thailand', 'Chance', 'Turkey', 'Iran', 
                    'Jail', 'Congo', 'Germany','Vietnam', 'East Station', 'Egypt', 'Community Chest',
                    'Philippines', 'Ethiopia', 
                    'Free Parking', 'Japan', 'Chance', 'Mexico',
                    'Russia', 'South Station', 'Bangladesh', 'Nigeria',
                    'Pakistan', 
                    'Space Trip', 'Brazil', 'Indonesia', 'Community Chest',
                    'America', 'West Station', 'India', 'Super Tax', 'China']
                    if SpaceTripNum < 27:
                        user.money+=200
                    user.name = squareNames[SpaceTripNum]
                    user.boardpos = SpaceTripNum
                    
                    
                    # user.isTraveling = True

                if alert.heading == 'Memories from 2008':
                    winner = Eve

                if type(alert) == EveAlert:

                    if alert.heading == 'Auction over':
                        Eve.normalGameplay = True

                    if alert.heading == 'Another one bytes the dust':
                        winner = user
                        Eve.isTurn = False
                        user.isTurn = False
                        break
                    
                    if alert.heading == 'Escaping CAPTCHA' or alert.heading == 'Escaping reCAPTCHA':
                        Eve.jailTurns = 0
                        Eve.inJail = False
                        Eve.normalGameplay = True
                        Eve.timeMoving = roll

                    if alert.heading == 'Destructobot':
                        Eve.normalGameplay = False
                        Eve.timeMoving = 0
                        Eve.inJail = True
                        Eve.canRoll = False

                    if alert.heading == 'Artificial estate agent':
                        currentSquare.owner = Eve
                        Eve.money -= currentSquare.getPrice()

                    if alert.heading == 'Rent':
                        Eve.money -= currentSquare.rent
                        currentSquare.owner.money += currentSquare.rent
                        currentSquare.paidRent = True
                        
                    if alert.heading == 'Build':
                        Eve.money -= currentSquare.rent
                        currentSquare.owner.money += currentSquare.rent
                        currentSquare.paidRent = True

                    if alert.heading.__contains__('Eve -'):
                        if alert.heading.__contains__('Community Chest'):
                            for cardBoi in communityChest:
                                if alert.body.__contains__(cardBoi.text):
                                    if not cardBoi.executed:
                                        cardBoi.execute(Eve)
                                        cardBoi.executed = True
                        elif alert.heading.__contains__('Chance'):
                            for cardBoi in chance:
                                if alert.body.__contains__(cardBoi.text):
                                    if not cardBoi.executed:
                                        cardBoi.execute(Eve)
                                        cardBoi.executed = True


                    if alert.body.__contains__('Eve paid'):
                        for square in squares:
                            if alert.heading == square.name:
                                if not square.paid:
                                    Eve.money -= square.getTax()
                                    freeParking += square.getTax()
                                    square.paid = True

                    if alert.heading == 'Artificial unintelligence':
                        Eve.normalGameplay = False
                        Eve.canRoll = False
                        Eve.inJail = True
                        Eve.jailTurns = 0
                    
                    if alert.heading == 'Fictional Trip':
                        exclude_nums=[0,2,6,9,15,18,20,27,30,34]
                        EveSpaceTripNum = random.choice([num for num in range(36) if num not in exclude_nums])
                        
                        if EveSpaceTripNum < 27:
                            Eve.money += 200
                            
                        Eve.boardpos = EveSpaceTripNum
                        
                        if squares[Eve.boardpos].owner == bank:
                            if Eve.money*0.6 >= squares[Eve.boardpos].getPrice():
                                alert = EveAlert('Artificial estate agent',
                                          'Eve buys ' + Eve.name + ' for $' + str(squares[Eve.boardpos].getPrice()))
                                Eve.money -= squares[Eve.boardpos].getPrice()
                                squares[Eve.boardpos].owner = Eve
                                     
                            else:
                                alert = EveAlert('', "Eve didn't buy " + str(currentSquare.name))
                                
                        elif squares[Eve.boardpos].owner == user:
                            Eve.money -= int(squares[Eve.boardpos].getPrice())
                            user.money += int(squares[Eve.boardpos].getPrice())
                            
                    

                    if alert.heading == 'Escaping CAPTCHA' or alert.heading == 'Escaping reCAPTCHA':
                        alert = EveAlert('', '')

                    elif alert.heading.__contains__('Community Chest'):
                        for cardBoi in communityChest:
                            if alert.body.__contains__(cardBoi.text):
                                if cardBoi.type == 'move':
                                    alert = EveAlert('', '')
                                else:
                                    alert = Alert('', '')
                    elif alert.heading.__contains__('Chance'):
                        for cardBoi in chance:
                            if alert.body.__contains__(cardBoi.text):
                                if cardBoi.type == 'move' or cardBoi.type == 'nearests':
                                    alert = EveAlert('', '')
                                else:
                                    alert = Alert('', '')
                    else:
                        alert = Alert('', '')

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    if user.isTurn and (beginning or not((type(alert) == EveAlert) or alert.heading == 'Memories from 2008')):
        if not user.canRoll and user.timeMoving <= 0 and not alert.body.__contains__('?'):
            etAvailable = True

        if user.normalGameplay:
            user.move()
            if user.timeMoving == 0:

                currentSquare = squares[user.boardpos]

                if type(currentSquare) == Property:
                    if currentSquare.owner == bank and not currentSquare.rejected:
                        if not (alert.body.__contains__('Answer the question woodja')):
                            alert = Alert('Unowned Property',
                                          'Buy ' + currentSquare.name + ' for $' + str(currentSquare.getPrice()) + '?')
                    elif currentSquare.owner == Eve:
                        if not currentSquare.paidRent:
                            user.money -= currentSquare.rent
                            currentSquare.owner.money += currentSquare.rent
                            alert = Alert('Rent', ('You paid $' + str(
                                currentSquare.rent) + ' rent to ' + currentSquare.owner.name))
                            currentSquare.paidRent = True
                    elif currentSquare.owner == user:
                        if len(currentSquare.name) > 10:
                            alert = Alert('Home sweet home', 'You take a nice rest in #' + currentSquare.name)
                        else:
                            alert = Alert('Home sweet home', 'You take a nice rest in ' + currentSquare.name)

                elif type(currentSquare) == Chance:
                    if not card:
                        card = currentSquare.pickCard()

                    if not alert.body.__contains__('You gotta click "OK" mate'):
                        alert = Alert(currentSquare.name, card.text)
                    if card.executed:
                        alert = Alert('', '')

                elif type(currentSquare) == TaxSquares:
                    if not currentSquare.paid:
                        user.money -= currentSquare.getTax()
                        freeParking += currentSquare.getTax()
                        currentSquare.paid = True
                    alert = Alert(currentSquare.name,
                                  'You paid $' + str(currentSquare.getTax()) + ' ' + currentSquare.name)

                elif type(currentSquare) == SpecialSquares and not beginning:
                    if not currentSquare.paid:
                        user.money += currentSquare.getPayAmount(freeParking)
                        if currentSquare.name == 'Free Parking':
                            freeParking = 0
                        elif currentSquare.name == 'Jail' and not user.inJail:
                            alert = Alert('Not-so-smooth criminal', "Isn't it fun to gloat at #the people in jail")
                        elif currentSquare.name == 'Space Trip':
                            alert = Alert('Space Trip', "You're on the space ship.")
                        currentSquare.paid = True

        if user.inJail and not alert.heading == 'They see me rollin\'':
            user.boardpos = 9
            if user.jailTurns == 0:
                if len(user.getOutOfJailFreeCards) > 0:
                    alert = Alert('Get out of Jail Free?', 'Do you wish to use a #get out of jail free card?')
            elif user.jailTurns > 0:
                if alert.heading == '':
                    alert = Alert('Do penance, sinner', ('You have ' + str(3 - user.jailTurns) + ' turns left in jail'))
                if user.jailTurns == 3:
                    alert = Alert('A free man', 'get out of jail.')
                    user.inJail = False
                    user.jailTurns = 0
                    
    elif Eve.isTurn:
        if Eve.canRoll and Eve.timeMoving == 0 and alert.confirmed and alert.type != EveAlert:

            Eve.paidOOJ = False
            beginning = False
            Eve.normalGameplay = True
            Eve.isMortgaging = False
            Eve.isTrading = False
            Eve.isDeveloping = False
            alert.confirmed = False

            throw = rollDice(die)
            buttonActions[0] = True
            roll = throw[0].value + throw[1].value
            # roll = 9

            for square in squares:
                if type(square) == Property:
                    square.rejected = False
                    square.paidRent = False

                elif type(square) == TaxSquares or type(square) == SpecialSquares:
                    square.paid = False

            for comcard in communityChest:
                comcard.executed = False
            for chancecard in chance:
                chancecard.executed = False
            card = None

            if throw[0] == throw[1] and Eve.doublesCount < 3:
                Eve.canRoll = True
                if Eve.inJail:
                    if not alert.confirmed:
                        alert = EveAlert('Escaping CAPTCHA', 'Eve rolls doubles and gets #out of jail. Nice.')
                        Eve.inJail = False
                        Eve.normalGameplay = False
                Eve.doublesCount += 1
            else:
                Eve.canRoll = False
            if Eve.doublesCount >= 3:
                Eve.normalGameplay = False
                if not alert.confirmed:
                    alert = EveAlert('Destructobot',
                                 'Uh-oh. Eve has committed #unspeakable acts- namely, #rolling doubles 3 times in #a row')
            if Eve.inJail and not alert.heading.__contains__('Escaping'):
                Eve.timeMoving = 0
                Eve.jailTurns += 1
            elif not alert.heading == 'Destructobot':
                Eve.timeMoving = roll

        if not Eve.canRoll and Eve.timeMoving == 0 and type(alert) != EveAlert:

            if Eve.money < 0:

                Eve.normalGameplay = False
                actions = AI.emergencyAction()
                if not actions[2]:
                    alert = EveAlert('Another one bytes the dust', '')
                else:
                    alert = EveAlert('Stayin\' Alive', '')
                alert.smallFont = True
                if len(actions[0])>0:
                    EveDemMes = 'Eve demolished: '
                    i = 0
                    while len(actions[0]) > 0:
                        prop = actions[0][0]
                        numOfHousesSold = actions[0].count(prop)
                        while prop in actions[0]:
                            actions[0].remove(prop)
                        if i % 2 == 0:
                            EveDemMes += '#'
                        EveDemMes += str(numOfHousesSold) + ' house'
                        if numOfHousesSold > 1:
                            EveDemMes += 's'
                        EveDemMes += ' in ' + prop.name

                        if not(len(actions[0]) == 0):
                            EveDemMes += ', '
                        i += 1
                    alert.body += EveDemMes + '#'

                if len(actions[1]) > 0:
                    EveMortMes = 'Eve mortgaged '
                    for prop in actions[1]:
                        if actions[1].index(prop) % 3 == 1:
                            EveMortMes += '#'
                        if 0 < actions[1].index(prop) == len(actions[1]) - 1:
                            EveMortMes += 'and '
                        EveMortMes += prop.name
                        if actions[1].index(prop) < len(actions[1]) - 1 and not len(actions[1]) == 0:
                            EveMortMes += ','
                    alert.body += EveMortMes + '#'
                if not actions[2]:
                    alert.body += 'Eve has $' + str(0-Eve.money) +' of debt and has #declared bankruptcy.'

            Eve.isTurn = False
            user.isTurn = True
            user.normalGameplay = False
            Eve.doublesCount = 0

        if Eve.normalGameplay and alert.heading != 'Another one bytes the dust' and alert.heading != 'Stayin\' alive':
            Eve.move()
            if Eve.timeMoving == 0:
                currentSquare = squares[Eve.boardpos]

                if type(currentSquare) == Property:
                    if currentSquare.owner == bank and not currentSquare.rejected:
                        if AI.wantsProp(currentSquare):
                            if not alert.confirmed:
                                alert = EveAlert('Artificial estate agent',
                                          'Eve buys ' + currentSquare.name + ' for $' + str(currentSquare.getPrice()))
                        else:
                            alert = EveAlert('',"Eve didn't buy " + str(currentSquare.name))
                            Eve.normalGameplay = True    
                        currentSquare.rejected = True
                    elif currentSquare.owner == user:
                        if not currentSquare.paidRent:
                            if not alert.confirmed:
                                alert = EveAlert('Rent', ('Eve paid $' + str(currentSquare.rent) + ' rent to you.'))

                    elif currentSquare.owner == Eve and alert.heading == 'Artificial estate agent':
                        if len(currentSquare.name) > 9:
                            if not alert.confirmed:
                                alert = EveAlert('Vibin\'', 'Eve takes a nice rest in #' + currentSquare.name)
                        else:
                            if not alert.confirmed:
                                alert = EveAlert('Vibin\'', 'Eve takes a nice rest in ' + currentSquare.name)
                    # elif currentSquare.owner == Eve and not alert.heading == 'Artificial estate agent':
                    #     if AI.develop(currentSquare):
                    #         if not alert.confirmed:
                    #             alert = EveAlert('Build',
                    #                       'Eve buys ' + currentSquare.name + ' house for $' + str(currentSquare.getPrice()))
                         
                elif type(currentSquare) == Chance:
                    if not card:
                        card = currentSquare.pickCard()

                    if not alert.confirmed:
                        alert = EveAlert('Eve - ' + currentSquare.name, card.text)

                elif type(currentSquare) == TaxSquares:
                    if not alert.confirmed:
                        alert = EveAlert(currentSquare.name,'Eve paid $' + str(currentSquare.getTax()) + ' ' + currentSquare.name)

                elif type(currentSquare) == SpecialSquares and not beginning:

                    if not currentSquare.paid:
                        Eve.money += currentSquare.getPayAmount(freeParking)

                        if currentSquare.name == 'Free Parking':
                            if not alert.confirmed:
                                alert = EveAlert('Free Parking', 'Eve got $' + str(freeParking) + ' from free parking.')
                            freeParking = 0
                        elif currentSquare.name == 'Jail' and not Eve.inJail:
                            if not alert.confirmed:
                                alert = EveAlert('Artificial unintelligence',
                                      'Eve got caught robbing #a bank. Clearly AI still has a #long way to go.')
                        elif currentSquare.name == 'Space Trip':
                            if not alert.confirmed:
                                alert = EveAlert('Fictional Trip','Now Eve can take a trip Online.')
                        currentSquare.paid = True

                # if alert.confirmed and Eve.money > 0 and not Eve.inJail:                
                #     if currentSquare.owner == Eve and not alert.heading == 'Artificial estate agent':   
                #         if (prop.boardpos == Eve.boardpos):
                #             if Eve.turnNum == 0:
                #                 alert = EveAlert('Finished turn', 'Eve has finished her turn')
                #             elif Eve.turnNum == 1 and prop.houses == 0 and Eve.money * 0.4 >= prop.getCostOfHouse():
                #                 prop.houses += 1
                #                 Eve.money -= prop.getCostOfHouse()
                #                 alert = EveAlert('Bob the builder', 'You built 1 house on ' + prop.name)
                #             elif Eve.turnNum == 1 and prop.houses == 1:
                #                 alert = EveAlert('Finished turn', 'Eve has finished her turn')
                #             elif Eve.turnNum == 2 and prop.houses == 0 and Eve.money * 0.4 >= prop.getCostOfHouse():
                #                 prop.houses += 1
                #                 Eve.money -= prop.getCostOfHouse()
                #                 alert = EveAlert('Bob the builder', 'You built 1 house on ' + prop.name)
                #             elif Eve.turnNum == 2 and prop.houses == 1 and Eve.money * 0.4 >= prop.getCostOfHouse():
                #                 prop.houses += 1
                #                 Eve.money -= prop.getCostOfHouse()
                #                 alert = EveAlert('Bob the builder', 'You built 1 house on ' + prop.name)
                #             elif Eve.turnNum == 2 and prop.houses == 2 and Eve.money * 0.4 >= prop.getCostOfHouse():
                #                 prop.houses += 1
                #                 Eve.money -= prop.getCostOfHouse()
                #                 alert = EveAlert('Bob the builder', 'You built 1 house on ' + prop.name)
                #             elif Eve.turnNum == 2 and prop.houses == 3:
                #                 alert = EveAlert('Finished turn', 'Eve has finished her turn')
                #             elif Eve.turnNum >= 3 and prop.houses == 0 and Eve.money * 0.4 >= prop.getCostOfHouse():
                #                 prop.houses += 1
                #                 Eve.money -= prop.getCostOfHouse()
                #                 alert = EveAlert('Bob the builder', 'You built 1 house on ' + prop.name)
                #             elif Eve.turnNum >= 3 and prop.houses == 1 and Eve.money * 0.4 >= prop.getCostOfHouse():
                #                 prop.houses += 1
                #                 Eve.money -= prop.getCostOfHouse()
                #                 alert = EveAlert('Bob the builder', 'You built 1 house on ' + prop.name)
                #             elif Eve.turnNum >= 3 and prop.houses == 2 and Eve.money * 0.4 >= prop.getCostOfHouse():
                #                 prop.houses += 1
                #                 Eve.money -= prop.getCostOfHouse()
                #                 alert = EveAlert('Bob the builder', 'You built 1 house on ' + prop.name)
                #             elif Eve.turnNum >= 3 and prop.houses == 3 and Eve.money * 0.4 >= prop.getCostOfHouse():
                #                 prop.houses += 1
                #                 Eve.money -= prop.getCostOfHouse()
                #                 alert = EveAlert('Fancy fancy', 'You built a hotel on ' + prop.name)
                #             else:
                #                 alert = EveAlert('Finished turn', 'Eve has finished her turn') 
                    # if street[0].streetOwned and street[0].owner == Eve and streets.index(street) <= 7:
                    #     AI.develop()
                    # if len(developCountries) == 0:
                    #     alert = EveAlert('Finished turn', 'Eve has finished her turn')
                    # else:
                    #     alert = EveAlert('Developing countries', 'Eve developed ')
                    #     for prop in developCountries:
                    #         if type(prop) == Property:
                    #             if developCountries.index(prop) % 3 == 1:
                    #                 alert.body += '#'
                    #             if 0 < developCountries.index(prop) == len(developCountries) - 1:
                    #                 alert.body += 'and '
                    #             alert.body += prop.name
                    #             if developCountries.index(prop) < len(developCountries) - 1 and not len(developCountries) == 0:
                    #                 alert.body += ', '

        if Eve.inJail and alert.heading != 'Stayin\' Alive' and alert.heading != 'Another one bytes the dust' and alert.heading != 'Developing countries':
            Eve.doublesCount = 0
            Eve.boardpos = 9
            if Eve.jailTurns >= 3:
                if AI.useGojf():
                    Eve.getOutOfJailFreeCards.remove(Eve.getOutOfJailFreeCards[0])
                    Eve.inJail = False
                    Eve.jailTurns = 0
                else:
                    if not Eve.paidOOJ:
                        Eve.money -= 50
                        Eve.paidOOJ = True

                if Eve.firstTimeInJail:
                    if not alert.confirmed:
                        alert = EveAlert('Escaping CAPTCHA', 'Eve has gotten out of jail')
                else:
                    if not alert.confirmed:
                        alert = EveAlert('Escaping reCAPTCHA', 'Eve has gotten out of #jail- again.')

                Eve.firstTimeInJail = False

            elif Eve.jailTurns >= 0:
                if not alert.confirmed:
                    alert = EveAlert('Bot detection', ('Eve has ' + str(3 - Eve.jailTurns) + ' turns left in jail'))

    if beginning:
        alert = welcome
        screen.blit(dieOne.image, (188 + 11 + 37, 210 + 33))
        screen.blit(dieOne.image, (188 + 38 + 150, 210 + 33))

    alert.write()

    # playerCardpos = [995, 145]
    # for gojfcard in user.getOutOfJailFreeCards:
    #     screen.blit(gojfcard.value, (playerCardpos))
    #     playerCardpos[0] += 10
    #     playerCardpos[1] += 2

    # EveCardpos = [1050, 650]
    # for Evegojfcard in Eve.getOutOfJailFreeCards:
    #     screen.blit(Evegojfcard.value, (EveCardpos))
    #     EveCardpos[0] += 10
    #     EveCardpos[1] += 2

    draw(Eve, (Eve.getPos()))
    draw(user, (user.getPos()))

    pygame.display.update()


# -------------------------------------------------------------------------------
# GAME OVER SCREEN

prevScreen = None
currScreen = None
while True:
    screen.fill(winner.colour)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    while currScreen == prevScreen:
        currScreen = random.choice(winner.screens)

    screen.blit(currScreen, (0, 0))
    prevScreen = currScreen

    pygame.display.update()
    time.sleep(0.2)
    
# End here