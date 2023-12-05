squares = []
properties = []
streets = [[],[],[],[],[],[],[],[]]

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
   