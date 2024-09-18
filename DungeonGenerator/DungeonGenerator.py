import random
import time
from collections import defaultdict
import keyboard

playerPos = [0,0]
dungeonSize = input("Dungeon Size: ")
dungeonSize = int(dungeonSize)

emptyDungeon = [["" for _ in range(dungeonSize)] for _ in range(dungeonSize)]
def clearDungeon(dun):
    for y in range(0, len(dun)):
        for x in range(0,len(dun[y])):
            dun[y][x] = ""

inputDict = defaultdict(lambda: "??!!")
inputDict["W"] = "U"
inputDict["A"] = "L"
inputDict["S"] = "D"
inputDict["D"] = "R"
def clearScreen():
    print("\n" * 50)

def getDirectionInput(prompt, allowed):
    inp = input(prompt)
    inp = inp.upper()
    inp = inputDict[inp]
    if inp in allowed:
        return inp
    else:
        print('Invalid Input')
        return getDirectionInput(prompt, allowed)
    

def shuffle_string(s):
    # Convert the string to a list of characters
    char_list = list(s)
    
    # Shuffle the list
    random.shuffle(char_list)
    
    # Join the list back into a string
    return ''.join(char_list)

def validateDungeonSpace(dun, x, y, direc):
    #print("Checking ", x, ", ", y)
    if x < 0:
        #print("Too Far Left")
        return False
    if y < 0:
        #print("Too Far Up")
        return False
    if y > len(dun)-1:
        #print("Too Far Down")
        return False
    if x > len(dun[y])-1:
        #print("Too Far Right")
        return False
    
    if dun[y][x] != "":
        roomShape = dun[y][x]
        if direc == "D" and "U" in roomShape:
            return True
        elif direc == "U" and "D" in roomShape:
            return True
        elif direc == "R" and "L" in roomShape:
            return True
        elif direc == "L" and "R" in roomShape:
            return True
        else:
            return False

    #print(x, ", ", y, " is a safe spot")
    return True

def getRoomShape(roomShape):
    roomShape = roomShape.upper()
    roomShapeArray = ["     ","     ","     "]

    if "H" not in roomShape:
        if "U" in roomShape or "L" in roomShape or "D" in roomShape or "R" in roomShape:
            #roomShapeArray[1] = "|     |"
            #roomShapeArray[3] = "|     |"
            #Top and Bottom Logic
            if "U" in roomShape:
                roomShapeArray[0] = "+   +"
            else:
                roomShapeArray[0] = "+---+"

            if "D" in roomShape:
                roomShapeArray[2] = "+   +"
            else:
                roomShapeArray[2] = "+---+"

            #Left and Right Logic
            if "R" in roomShape and "L" in roomShape:
                roomShapeArray[1] = "     "

            elif "R" in roomShape:
                roomShapeArray[1] = "|    "

            elif "L" in roomShape:
                roomShapeArray[1] = "    |"
    
            else:
                roomShapeArray[1] = "|   |"

    if "X" in roomShape:
        roomShapeArray[1] = roomShapeArray[1][:2] + "X" + roomShapeArray[1][3:]

    return roomShapeArray

def printDungeon(dun):
    for row in dun:
        for i in range(0, 3):
            lineString = ""
            for room in row:
                lineString = lineString + getRoomShape(room)[i]

            print(lineString)

def generateDungeon(dun, threshhold):
    middle = (int)((len(dun) - 1)/2)
    generationNodes = []
    startingPointX = random.randint(0, len(dun) - 1)
    startingPointY = random.randint(0, len(dun) - 1)
    generationNodes.append([startingPointX, startingPointY])
    dun[startingPointY][startingPointX] = "URDLX"
    possibleRooms = ["U","L","D","R","UD", "RL", "UR", "RD", "DL", "UL", "URL", "URD", "RDL", "UDL", "URDL"]
    uRooms=[]
    rRooms=[]
    dRooms=[]
    lRooms=[]
    for room in possibleRooms:
        if "U" in room:
            uRooms.append(room)
        if "R" in room:
            rRooms.append(room)
        if "D" in room:
            dRooms.append(room)
        if "L" in room:
            lRooms.append(room)

    numGenerated = 0

    #print(generationNodes)
    while len(generationNodes) > 0:
        numGenerated = numGenerated + 1
        newX = 0
        newY = 0
        roomList = []
        x = generationNodes[0][0]
        y = generationNodes[0][1]
        #print(x, ",", y)
        roomShape = dun[y][x]
        roomShape = shuffle_string(roomShape)
        #roomShape = shuffle_string(roomShape)
        removalString = ""
        for direction in roomShape:
            if direction in "ULDR":
                if direction == "R":
                    newX = x + 1
                    newY = y
                    roomList = lRooms
                elif direction == "L":
                    newX = x - 1
                    newY = y
                    roomList = rRooms
                elif direction == "U":
                    newX = x
                    newY = y - 1
                    roomList = dRooms
                elif direction == "D":
                    newX = x
                    newY = y + 1
                    roomList = uRooms

                if validateDungeonSpace(dun, newX, newY, direction):
                
                    if(dun[newY][newX] == ""):
                        rand = random.randint(0, len(roomList) - 1)
                        newRoomShape = roomList[rand]
                        hiddenRand = random.randint(1,20)
                        if hiddenRand <= 10:
                            newRoomShape = newRoomShape + "H"
                        #print(roomShape, " is connecting to ", newRoomShape, "At position ", newX,", ",newY, "after picking from list: ", roomList)
                        dun[newY][newX] = newRoomShape
                        #newRoomShape = shuffle_string(newRoomShape)
                        generationNodes.append([newX, newY])

                else:
                    removalString = removalString + direction

        for char in removalString:
            roomShape = roomShape.replace(char, '')

        dun[y][x] = roomShape

        generationNodes.pop(0)
        random.shuffle(generationNodes)
        #printDungeon(dun)
        #print(generationNodes)

    print("Number of Generated Rooms: ", numGenerated)
    if(numGenerated > (dungeonSize * dungeonSize) * threshhold):
        return dun
    else:
        #time.sleep(1)
        clearDungeon(dun)
        return generateDungeon(dun, threshhold - .01)

def getPlayerPosition(dun):
    for y in range(0, len(dun)):
        for x in range(0, len(dun[y])):
            if "X" in dun[y][x]:
                return [x, y]

    return [0, 0]


generatedDungeon = generateDungeon(emptyDungeon, 0.75)

clearScreen()
printDungeon(generatedDungeon)

def move(moveDir):
    playerPos = getPlayerPosition(generatedDungeon)
    x = playerPos[0]
    y = playerPos[1]
    newX = x + moveDir[0]
    newY = y + moveDir[1]
    direc = "W"
    if moveDir == [0, 1]:
        direc = "D"
    elif moveDir == [0, -1]:
        direc = "U"
    elif moveDir == [1, 0]:
        direc = "R"
    elif moveDir == [-1, 0]:
        direc = "L"
    
    print(direc)
    if validateDungeonSpace(generatedDungeon, newX, newY, direc) and generatedDungeon[newY][newX] != "":
        generatedDungeon[y][x] = generatedDungeon[y][x].replace('X', '')
        generatedDungeon[y][x] = generatedDungeon[y][x].replace('H', '')
        generatedDungeon[newY][newX] = generatedDungeon[newY][newX] + "X"
        generatedDungeon[newY][newX] = generatedDungeon[newY][newX].replace('H', '')
        clearScreen()
        printDungeon(generatedDungeon)
        return

    else:
        clearScreen()
        printDungeon(generatedDungeon)
        print("Invalid")


keyboard.add_hotkey('w', lambda: move([0,-1]))
keyboard.add_hotkey('s', lambda: move([0,1]))
keyboard.add_hotkey('a', lambda: move([-1,0]))
keyboard.add_hotkey('d', lambda: move([1,0]))

try:
    while True:
        time.sleep(0.1)  # Slight delay to prevent high CPU usage
except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
