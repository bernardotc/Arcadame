# -----------------------------------------------------------------------------
# Bernardo Daniel Trevino Caballero     A00813175
# Myriam Maria Gutierrez Aburto         A00617060
# arcadame.py
#
# Virtual Machine for the languange Arcadame
# -----------------------------------------------------------------------------

# Imports that will be used in the VM
import sys, getopt
import pygame
import xml.etree.ElementTree as ET
import random
from math import ceil

# Debug global variables
timeDebug = False
debug = False

# Global variables
functionDictionary = {}
spriteSet = {}
mapping = {}
map = {}
objectsCount = {}
movableObjects = []
spawnerObjects = []
mapRow = 0
mapCol = 0
maxMapRow = 0
maxMapCol = 0
score = 0
time = 0
tileWidth = 50
tileHeight = 50
constants = {}
quadruplets = []
instructionCounter = 1
instructionStack = []
functionScope = []
parametersMemoryValues = {101: 7000, 102: 8000, 103: 9000, 104: 10000, 105: 11000}
offset = 0
protectFrom = ""
protect = ""
protectTile = ()
spriteInTile = []
win = None
clock = None
avatarPos = (0,0)
tile = (0,-1)

# Color constants
color_white = (255, 255, 255)
color_blue = (0, 0, 255)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
color_black = (0, 0, 0)
color_purple = (128, 0, 128)
color_brown = (139, 69, 19)
color_cyan = (0, 255, 255)
color_orange = (255, 165, 0)

# Memory of execution
memory = memory = [{}, [{}], [{}], constants]

# Auxiliary function to get the section depending on the virtual memory key
def getSection(value):
    if (value < 7000):
        return 0
    elif (value < 12000):
        return 1
    elif (value < 17000):
        return 2
    else:
        return 3

# Special function for assigning a value in memory depending on the virtual key
# NOTE that you can assign in 3 sections, the constants section is not assignable.
def assignValueInMemory(memoryKey, value):
    global memory, offset
    # Special condition, a negative means that is an indirect direction
    if (memoryKey < 0):
        memoryKey = accessValueInMemory(-1 * memoryKey)
    # Retrieves section
    section = getSection(memoryKey)
    if (debug):
        print "SET = assigning value in section: ", section
    # Global section, it is just a simple dictionary in execution memory
    if (section == 0):
        memory[section][memoryKey] = value
    # Local and temporal section, it is a stack of dictionaries in execution memory
    # offset is a global variable that changes the dictionary to access. Not always
    # is the top one. Normaly, offset is 0.
    else:
        memory[section][-1 - offset][memoryKey] = value

# Special function for accessing memory using a key based on the virtual memory
def accessValueInMemory(memoryKey):
    global memory, offset
    # Special condition, a negative means that is an indirect direction
    if (memoryKey < 0):
        memoryKey = accessValueInMemory(-1 * memoryKey)
    # Retrieves section
    section = getSection(memoryKey)
    if (debug):
        print "GET = accessing value in section: ", section
    # Global section, it is just a simple dictionary in execution memory
    if (section == 0):
        return memory[section][memoryKey]
    # Constants section, it is just a simple dictionary in execution memory
    elif (section == 3):
        return memory[section][memoryKey]['value']
    # Local and temporal section, it is a stack of dictionaries in execution memory
    else:
        return memory[section][-1 - offset][memoryKey]

# Helper function for creating a new dictionary in the stack of local and temporal sections
def createERAInMemory():
    global memory
    memory[1].append({})
    memory[2].append({})

# Helper function for deleting the tip dictionary in the local and temporal stack of
# the execution memory
def deleteERAInMemory():
    global memory
    memory[1].pop()
    memory[2].pop()

# Helper function for doing assignation in memory when using the param operator
# This is differente than nromal assignation because you need to work in two different
# spaces in memory represented by the two different dictionaries.
# Therefore, these function takes to keys, one in the top - 1 (memoryKey1) dictionary
# and the other (memoryKey2) in the top dictionary.
def assignParamInMemory(memoryKey1, memoryKey2):
    global memory
    # Special condition, a negative means that is an indirect direction
    # It could not happen the other war around because it is not supported
    # In other words, a list could not be a param in a function.
    if (memoryKey2 < 0):
        memoryKey2 = accessValueInMemory(-1 * memoryKey2)
    # Retrieves section
    section = getSection(memoryKey2)
    # Retrieves value. By this point, offset is 1, so retrieves top - 1.
    value = accessValueInMemory(memoryKey1)
    if (debug):
        print "Assigning parameters: ", memoryKey1, memoryKey2, value
    # Needs someway to avoid using offset, therefore only assign the value in the
    # top pf the stack of memory.
    # NOTE: memoryKey2 always is in local section.
    memory[section][-1][memoryKey2] = value

# Helper function to get the corresponding virtual memory of the parameter, depeding on
# the type of the parameter. it simulates the virtual memory.
def getParamMemoryValue(paramType):
    global parametersMemoryValues
    value = parametersMemoryValues[paramType]
    # Increase the counter.
    parametersMemoryValues[paramType] += 1
    return value

# Resets the memory values for parameters to simulate the virtual memory for other functions.
def resetParametersMemoryValues():
    global parametersMemoryValues
    parametersMemoryValues = {101: 7000, 102: 8000, 103: 9000, 104: 10000, 105: 11000}

# Reads the intermediate code accessed in the fileName paramenter.
def readRawCode(fileName):
    global functionDictionary, constants, quadruplets, spriteSet
    # Use ET to parse the xml file ending in .dame
    tree = ET.parse(fileName)
    # First get all the sprites and assign it to spriteSet
    for sprite in tree.find('game').find('sprites').findall('sprite'):
        name = sprite.find('spriteName').text
        type = int(sprite.find('type').text)
        spriteSet[name] = {'type': type}
    
    # Get all functions and its attributes like parameters, quadruplet, returnType and memory
    # Save those values in a function directory
    parameters = []
    for function in tree.find('functions').findall('function'):
        name = function.find('functionName').text
        for parameter in function.findall('parameter'):
            parameters.append(int(parameter.text))
        returnType = function.find('return').text
        memory = function.find('memory').text
        quadruplet = function.find('quadruplet').text
        eraRoot = function.find('era')
        era = [int(eraRoot.find('int').text), int(eraRoot.find('float').text), int(eraRoot.find('string').text), int(eraRoot.find('char').text), int(eraRoot.find('boolean').text)]
        functionDictionary[name] = {'parameters': parameters, 'return': returnType, 'memory': int(memory), 'quadruplet': int(quadruplet), 'era': era}

    # Get constants section from the file, and depending of the type of value
    # convert it to that type in python
    for constant in tree.find('constants').findall('constant'):
        value = constant.find('constantValue').text
        type = int(constant.find('type').text)
        memory = int(constant.find('memory').text)
        if (int(type) == 101):
            constants[memory] = {'type': type, 'value': int(value)}
        elif (int(type) == 102):
            constants[memory] = {'type': type, 'value': float(value)}
        else:
            constants[memory] = {'type': type, 'value': value}

    # Get quadruplets and save them in memory
    for quadruplet in tree.find('quadruplets').findall('quadruplet'):
        operator = int(quadruplet.find('operation').text)
        # Most elements and results are numeric, therefore it is convenient to try to
        # parse it and handle them that way.
        try:
            elem1 = int(quadruplet.find('element1').text)
        except ValueError:
            elem1 = quadruplet.find('element1').text
        try:
            elem2 = int(quadruplet.find('element2').text)
        except ValueError:
            elem2 = quadruplet.find('element2').text
        try:
            result = int(quadruplet.find('result').text)
        except ValueError:
            result = quadruplet.find('result').text
        quadruplets.append([operator, elem1, elem2, result])

    if (debug):
        print "functions: ", functionDictionary
        print "constants: ", constants
        print "sprites: ", spriteSet
        print "quadruplets: ", quadruplets

# Helper function for moving objects that are movable in the game.
def moveObjects():
    global map, time, movableObjects, spriteSet, maxMapRow, objectsCount, avatarPos
    # Get an object of the movable objects.
    for object in movableObjects:
        if (timeDebug):
            print time, spriteSet[object[0]]['speed'], object[2]
            print time - object[2]
        # The following code are almost the same like the one above with some differences.
        # If the object has an avatar involved
        try:
            # Check also if the avatar is included
            if (time * spriteSet[object[0]]['speed'] - object[2] >= 0 and object[3] == 'avatar'):
                object[2] += 1
                # Get the complete tile where the object is from the map
                spriteListWithObject = map[object[1]]
                for index in range(0, len(spriteListWithObject)):
                    if (spriteListWithObject[index].has_key(object[0])):
                        # Finally get the object from the map and modify its last position
                        sprite = spriteListWithObject.pop(index)
                        sprite[object[0]]['last-position'] = object[1]
                        # Check to what direction the object is moving and calculate its new
                        # position (object[1])
                        if (spriteSet[object[0]]['orientation'] == 'up'):
                            object[1] = (object[1][0] - 1, object[1][1])
                        elif (spriteSet[object[0]]['orientation'] == 'down'):
                            object[1] = (object[1][0] + 1, object[1][1])
                        elif (spriteSet[object[0]]['orientation'] == 'left'):
                            object[1] = (object[1][0], object[1][1] - 1)
                        else:
                            object[1] = (object[1][0], object[1][1] + 1)
                        # Check that the new position is inside the game boundaries
                        if (object[1][0] < maxMapRow and object[1][0] >= 0 and object[1][1] < maxMapCol and object[1][1] >= 0):
                            # Append sprite to the new tile in map.
                            map[object[1]].append(sprite)
                            # Repeat the process but now for the sprite avatar.
                            if (object[3] == 'avatar'):
                                for index in range(0, len(spriteListWithObject)):
                                    if (spriteListWithObject[index].has_key('avatar')):
                                        avatar = spriteListWithObject.pop(index)
                                        avatar['avatar']['last-position'] = sprite[object[0]]['last-position']
                                        avatarPos = object[1]
                                        map[object[1]].append(avatar)
                        break
            # Always pop the avatar (4th element in object)
            object.pop(3)
        # If the object has no avatar involved
        except IndexError:
            # The same process as before, except that does not have an avatar (4th element)
            if (time * spriteSet[object[0]]['speed'] - object[2] >= 0):
                object[2] += 1
                spriteListWithObject = map[object[1]]
                for index in range(0, len(spriteListWithObject)):
                    if (debug):
                        print index
                        print len(spriteListWithObject)
                        print spriteListWithObject[index]
                        print spriteListWithObject[index].has_key(object[0]), object[0]
                    if (spriteListWithObject[index].has_key(object[0])):
                        sprite = spriteListWithObject.pop(index)
                        sprite[object[0]]['last-position'] = object[1]
                        if (spriteSet[object[0]]['orientation'] == 'up'):
                            object[1] = (object[1][0] - 1, object[1][1])
                        elif (spriteSet[object[0]]['orientation'] == 'down'):
                            object[1] = (object[1][0] + 1, object[1][1])
                        elif (spriteSet[object[0]]['orientation'] == 'left'):
                            object[1] = (object[1][0], object[1][1] - 1)
                        else:
                            object[1] = (object[1][0], object[1][1] + 1)
                        if (object[1][0] < maxMapRow and object[1][0] >= 0 and object[1][1] < maxMapCol and object[1][1] >= 0):
                            map[object[1]].append(sprite)
                        else:
                            objectsCount[object[0]] -= 1
                            movableObjects.remove(object)
                        break

# Function that helps to spawn objects in the game
def spawnObjects():
    global spriteSet, map, movableObjects, time, objectsCount
    # Get the spawn from the spawner Objects.
    for spawn in spawnerObjects:
        # Get the information of the spawner.
        spawner = spriteSet[spawn[0]]
        # Check if it meets the probability to generate a new sprite and the cooldown time
        # has passed.
        if (random.random() <= spawner['prob'] and int(time) % spawner['cooldown'] == 0):
            # Get the sprites in the tile where the spawn is.
            sprites = map[spawn[1]]
            spawnNew = True
            # Check if there are no generated sprites in the spawner position.
            # If it find a sprite, it means that it was already generated before.
            for index in range(0, len(sprites)):
                if (sprites[index].has_key(spawner['generatedSprite'])):
                    spawnNew = False
                    break
            # If there is no generated Sprite, then:
            if (spawnNew):
                # Append to that map position the generated sprite with its attributes
                map[spawn[1]].append({spawner['generatedSprite'] : spriteSet[spawner['generatedSprite']]})
                # Spawners generate movable objects, therefore included here too.
                movableObjects.append([spawner['generatedSprite'], spawn[1], ceil(time * spriteSet[spawner['generatedSprite']]['speed'])])
                objectsCount[spawner['generatedSprite']] += 1

# Method to draw all objects in map
def drawObjects():
    global map, maxMapRow, maxMapCol
    # Draw the white background
    win.fill(globals()['color_white'])
    # Loop through the map
    for r in range(0, maxMapRow):
        for c in range(0, maxMapCol):
            # Get the sprites in map
            sprites = map[(r, c)]
            # If there are no sprites
            if (len(sprites) == 0):
                pygame.draw.rect(win, globals()['color_white'], [c * tileWidth, r * tileHeight, (c+1) * tileWidth, (r+1) * tileHeight])
            # If there are sprites only draw the one that is at the top (the last one in the list)
            else:
                sprite = sprites[-1]
                for spriteKey, spritAttrib in sprite.iteritems():
                    if (debug):
                        print [c * tileWidth, r * tileHeight, (c+1) * tileWidth, (r+1) * tileHeight]
                    if (spritAttrib.has_key('color')):
                        pygame.draw.rect(win, globals()['color_' + spritAttrib['color']], [c * tileWidth, r * tileHeight, (c+1) * tileWidth, (r+1) * tileHeight])
    # After drawing, refresh screen
    pygame.display.flip()

# The CORE of the VM
# It receives the quadruplet, and this method is a big swith that depending of the operation
# (quadruplet[0]) is the procces to be executed.
def doOperation(quadruplet):
    global instructionCounter, functionDictionary, instructionStack, functionScope, offset, spriteSet, map, score, mapRow, mapCol, mapping, objectsCount, time, maxMapRow, maxMapCol, tileWidth, tileHeight, win, clock, avatarPos, tile, file, movableObjects, protect, spriteInTile, protectFrom, protectTile, spawnerObjects
    if (debug):
        print instructionCounter, quadruplet
    # The first 10 operations are arithmetic or logical.
    if (quadruplet[0] < 10):
        elem1 = accessValueInMemory(quadruplet[1])
        elem2 = accessValueInMemory(quadruplet[2])
        # Plus
        if (quadruplet[0] == 0):
            result = elem1 + elem2
        # Times
        elif (quadruplet[0] == 1):
            result = elem1 * elem2
        # Minus
        elif (quadruplet[0] == 2):
            result = elem1 - elem2
        # Division
        elif (quadruplet[0] == 3):
            result = 1.0 * elem1 / elem2
        # And
        elif (quadruplet[0] == 4):
            result = elem1 and elem2
        # Or
        elif (quadruplet[0] == 5):
            result = elem1 or elem2
        # Lesser than
        elif (quadruplet[0] == 6):
            result = elem1 < elem2
        # Greater than
        elif (quadruplet[0] == 7):
            result = elem1 > elem2
        # Not equal
        elif (quadruplet[0] == 8):
            result = elem1 != elem2
        # Equal
        elif (quadruplet[0] == 9):
            result = elem1 == elem2
        if (debug):
            print "elem1: ", elem1
            print "elem2: ", elem2
            print "result: ", result
        # Save the result from the operation in memory
        assignValueInMemory(quadruplet[3], result)
        return True
    # Assignation
    elif (quadruplet[0] == 10):
        result = accessValueInMemory(quadruplet[1])
        assignValueInMemory(quadruplet[3], result)
        return True
    # GOTO, change the instruction counter (-1 because in the loop it will increase)
    elif (quadruplet[0] == 11):
        instructionCounter = quadruplet[3] - 1
        return True
    # GOTOF, evaluate and then
    # change the instruction counter (-1 because in the loop it will increase)
    elif (quadruplet[0] == 12):
        result = accessValueInMemory(quadruplet[1])
        if (debug):
            print "GOTOF result: ", result
        if (result == False):
            instructionCounter = quadruplet[3] - 1
        return True
    # Print value to console
    elif (quadruplet[0] == 13):
        result = accessValueInMemory(quadruplet[3])
        print "-----> AVM PRINT: ", result
        if (file):
            file.write("-> AVM PRINT: " + str(result) + '\n')
        return True
    # Get value (int or float)
    elif (quadruplet[0] == 14):
        scan = raw_input('-----> AVM GET_VALUE: ')
        try:
            if (quadruplet[3] < 15000):
                result = int(scan.strip())
            else:
                result = float(scan.strip())
            file.write("-> AVM GET_VALUE: " + str(result) + '\n')
            assignValueInMemory(quadruplet[3], result)
            return True
        except:
            # raise ERROR
            return False
    # Get line (char or string)
    elif (quadruplet[0] == 15):
        scan = raw_input('-----> AVM GET_LINE: ')
        file.write("-> AVM GET_LINE: " + str(result) + '\n')
        assignValueInMemory(quadruplet[3], scan)
        return True
    # Get boolean ('true or false')
    elif (quadruplet[0] == 16):
        scan = raw_input('-----> AVM GET_BOOLEAN: ')
        result = scan.strip()
        if (result == 'true' or result == 'false'):
            file.write("-> AVM GET_BOOLEAN: " + str(result) + '\n')
            assignValueInMemory(quadruplet[3], result)
            return True
        else:
            # raise ERROR
            return False
    # Get char (similar to get line, it only takes into account the first character)
    elif (quadruplet[0] == 17):
        scan = raw_input('-----> AVM GET_CHAR: ')
        if (len(scan) > 0):
            result = scan[0]
            file.write("-> AVM GET_CHAR: " + str(result) + '\n')
            return True
        else:
            # raise ERROR
            return False
    # End Function operation. Needs to deleate ERA if it was not done before and
    # set back the instruction pointer
    elif (quadruplet[0] == 18):
        deleteERAInMemory()
        if (debug):
            print "Memory after deleting ERA: ", memory
        instructionCounter = instructionStack.pop()
        functionScope.pop()
        resetParametersMemoryValues()
        return True
    # ERA quadriplet, it creates a new dictionary in memory and sets the offset to 1
    elif (quadruplet[0] == 19):
        createERAInMemory()
        functionScope.append(quadruplet[3])
        offset = 1
        if (debug):
            print "Memory after creating ERA: ", memory
        return True
    # Gosub, it is like goto, but in this case is for a function.
    # It sets offset to 0, and saves instruction pointer
    elif (quadruplet[0] == 20):
        function = quadruplet[3]
        instructionStack.append(instructionCounter)
        offset = 0
        instructionCounter = functionDictionary[function]['quadruplet'] - 1
        resetParametersMemoryValues()
        return True
    # Param operation. It uses the helper functions to manipulate two different spaces
    # in memory.
    elif (quadruplet[0] == 21):
        value = quadruplet[1]
        if (debug):
            print "Function scope Name for Params: ", functionScope
        paramType = functionDictionary[functionScope[-1]]['parameters'][quadruplet[3] - 1]
        param = getParamMemoryValue(paramType)
        assignParamInMemory(value, param)
        return True
    # Return operation. In this case, the function returns a value, and after that
    # you need to delete the memory of the function scope and return the pointer where it
    # was before the function got called.
    elif (quadruplet[0] == 22):
        result = accessValueInMemory(quadruplet[3])
        if (debug):
            print "Function Scope: ", functionScope
            print "Memory direction of function = ", functionDictionary[functionScope[-1]]['memory']
        assignValueInMemory(functionDictionary[functionScope[-1]]['memory'], result)
        deleteERAInMemory()
        if (debug):
            print "Memory after deleting ERA: ", memory
        instructionCounter = instructionStack.pop()
        functionScope.pop()
        return True
    # Verify operation. This is done to handle arrays. Verifies that your assigning a value
    # that is inside the limits of the array (or list).
    elif (quadruplet[0] == 23):
        result = accessValueInMemory(quadruplet[1])
        if (result >= quadruplet[2] and result <= quadruplet[3]):
            return True
        else:
            return False
# ================ BEGINNING OF GAME OPERATIONS ================================
    # Assign operation. Different than 10 in the sense that this needs to be handled like a class.
    # The attributes (color, portal, etc) are stored in the spriteSet.
    elif (quadruplet[0] == 30):
        if (quadruplet[1] == 301):
            spriteSet[quadruplet[3]]['color'] = quadruplet[2]
        elif (quadruplet[1] == 302):
            spriteSet[quadruplet[3]]['portal'] = quadruplet[2]
        elif (quadruplet[1] == 303):
            spriteSet[quadruplet[3]]['orientation'] = quadruplet[2]
        elif (quadruplet[1] == 304):
            spriteSet[quadruplet[3]]['speed'] = float(quadruplet[2])
        elif (quadruplet[1] == 305):
            spriteSet[quadruplet[3]]['generatedSprite'] = quadruplet[2]
        elif (quadruplet[1] == 306):
            spriteSet[quadruplet[3]]['prob'] = float(quadruplet[2])
        elif (quadruplet[1] == 307):
            spriteSet[quadruplet[3]]['cooldown'] = quadruplet[2]
        return True
    # AddRowMap operation. It sets the sprites that correspond to a particular tile in map.
    elif (quadruplet[0] == 31):
        # quadruplet[3] is a string.
        for k in quadruplet[3]:
            # k is a char of the string that is mapped to one or several sprites.
            # Assign those sprites to map.
            map[(mapRow, mapCol)] = list(mapping[k])
            for sprite in mapping[k]:
                # Loop through those sprites and check special conditions.
                for spr, attr in sprite.iteritems():
                    if (spr == 'avatar'):
                        avatarPos = (mapRow, mapCol)
                    if (objectsCount.has_key(spr)):
                        objectsCount[spr] += 1
                    else:
                        objectsCount[spr] = 1
                    # Missile objects
                    if (attr['type'] == 204):
                        movableObjects.append([spr, (mapRow, mapCol), 0])
                    # Spawner objects
                    elif (attr['type'] == 205):
                        spawnerObjects.append([spr, (mapRow, mapCol)])
            mapCol += 1
        mapRow += 1
        # Set the max row and column of the map
        if (mapCol > maxMapCol):
            maxMapCol = mapCol
        if (mapRow > maxMapRow):
            maxMapRow = mapRow
        mapCol = 0
        return True
    # Initialize operation. Set score and time to 0, display game window and set clock.
    elif (quadruplet[0] == 32):
        score = 0
        time = 0
        if (debug):
            print [maxMapCol * tileWidth, maxMapRow * tileHeight]
        win = pygame.display.set_mode([maxMapCol * tileWidth, maxMapRow * tileHeight])
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game")
        return True
    # SpriteCounter operation. Check if a particular sprite has an exact amount of sprites.
    elif (quadruplet[0] == 33):
        assignValueInMemory(quadruplet[3], objectsCount[quadruplet[1]] == quadruplet[2])
        return True
    # Timeout operation. Check if time is greater or equal than a certain value.
    elif (quadruplet[0] == 34):
        assignValueInMemory(quadruplet[3], time >= quadruplet[2])
        return True
    # Not operation. From true to false, or false to true.
    elif (quadruplet[0] == 35):
        elem1 = accessValueInMemory(quadruplet[1])
        assignValueInMemory(quadruplet[3], not elem1)
        return True
    # Check move operation of AVATAR based on keyboard events.
    elif (quadruplet[0] == 36):
        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.KEYDOWN):
                # DOWN
                if (event.key == pygame.K_DOWN):
                    # Validate map limits.
                    if (avatarPos[0] < maxMapRow - 1):
                        # Get the list of sprites that are with the avatar
                        spriteListWithAvatar = map[avatarPos]
                        for index in range(0, len(spriteListWithAvatar)):
                            # Finally get only the avatar sprite
                            if (spriteListWithAvatar[index].has_key('avatar')):
                                # pop the avatar from the tile of the map.
                                avatar = spriteListWithAvatar.pop(index)
                                # Change position.
                                avatar['avatar']['last-position'] = avatarPos
                                # Modify its position
                                avatarPos = (avatarPos[0] + 1, avatarPos[1])
                                # Add it to the map in its new position.
                                map[avatarPos].append(avatar)
                                break
                # NOTE: the process is the same than the one above, it just changes
                # the new avatarPos value.
                # UP
                if (event.key == pygame.K_UP):
                    # Validate map limits.
                    if (avatarPos[0] > 0):
                        spriteListWithAvatar = map[avatarPos]
                        for index in range(0, len(spriteListWithAvatar)):
                            if (spriteListWithAvatar[index].has_key('avatar')):
                                avatar = spriteListWithAvatar.pop(index)
                                avatar['avatar']['last-position'] = avatarPos
                                avatarPos = (avatarPos[0] - 1, avatarPos[1])
                                map[avatarPos].append(avatar)
                                break
                # LEFT
                if (event.key == pygame.K_LEFT):
                    # Validate map limits.
                    if (avatarPos[1] > 0):
                        spriteListWithAvatar = map[avatarPos]
                        for index in range(0, len(spriteListWithAvatar)):
                            if (spriteListWithAvatar[index].has_key('avatar')):
                                avatar = spriteListWithAvatar.pop(index)
                                avatar['avatar']['last-position'] = avatarPos
                                avatarPos = (avatarPos[0], avatarPos[1] - 1)
                                map[avatarPos].append(avatar)
                                break
                # RIGHT
                if (event.key == pygame.K_RIGHT):
                    # Validate map limits.
                    if (avatarPos[1] < maxMapCol - 1):
                        spriteListWithAvatar = map[avatarPos]
                        for index in range(0, len(spriteListWithAvatar)):
                            if (spriteListWithAvatar[index].has_key('avatar')):
                                avatar = spriteListWithAvatar.pop(index)
                                avatar['avatar']['last-position'] = avatarPos
                                avatarPos = (avatarPos[0], avatarPos[1] + 1)
                                map[avatarPos].append(avatar)
                                break
            # This is extra from the movement, but it enables to close window.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
        return True
    # GetNextTile operation. It changes the tile to be checked in the map.
    elif (quadruplet[0] == 37):
        # If possible change columns.
        if (tile[1] < maxMapCol - 1):
            tile = (tile[0], tile[1] + 1)
            assignValueInMemory(quadruplet[3], True)
        # Then row.
        elif (tile[0] < maxMapRow - 1):
            tile = (tile[0] + 1, 0)
            assignValueInMemory(quadruplet[3], True)
        # All the map what iterated, start again.
        else:
            assignValueInMemory(quadruplet[3], False)
            tile = (0,-1)
        if (debug):
            print tile
        # Reset spriteInTile
        spriteInTile = []
        return True
    # inTile operation. Checks if a particular sprite in the current tile.
    elif (quadruplet[0] == 38):
        sprites = map[tile]
        result = False
        for sprite in sprites:
            if (sprite.has_key(quadruplet[1])):
                spriteInTile.append(quadruplet[1])
                result = True
                break;
        assignValueInMemory(quadruplet[3], result)
        return True
    # killSprite. Kill the sprite in quadruplet[3] that is inside the current tile.
    elif (quadruplet[0] == 39):
        spriteList = map[tile]
        if (debug):
            print spriteList
        for index in range(0, len(spriteList)):
            if (debug):
                print index, quadruplet[3]
            if (spriteList[index].has_key(quadruplet[3])):
                if (debug):
                    print protectTile, protect, protectFrom, spriteInTile
                # Check if the tile is protected and therefore cannot be killed
                if (protect in spriteInTile and protectFrom in spriteInTile and tile == protectTile):
                    protect = ""
                    protectFrom = ""
                # Kill the sprite
                else:
                    spriteList.pop(index)
                    objectsCount[quadruplet[3]] -= 1
                    break
        return True
    # ScoreChange. Add value of quadruplet[1] to the score.
    elif (quadruplet[0] == 40):
        score += float(quadruplet[1])
        return True
    # StepBack operation. Returns the sprite to the last position.
    elif (quadruplet[0] == 41):
        # If its the avatar sprite, also set the avatarPos global variable.
        if (quadruplet[3] == 'avatar'):
            spriteListWithAvatar = map[avatarPos]
            for index in range(0, len(spriteListWithAvatar)):
                if (spriteListWithAvatar[index].has_key('avatar')):
                    avatar = spriteListWithAvatar.pop(index)
                    avatarPos = avatar['avatar']['last-position']
                    map[avatarPos].append(avatar)
        else:
            spriteList = map[tile]
            for index in range(0, len(spriteList)):
                if (spriteList[index].has_key(quadruplet[3])):
                    sprite = spriteList.pop(index)
                    lastPos = avatar[quadruplet[3]]['last-position']
                    map[lastPos].append(sprite)
        return True
    # DrawMap. Has some game logic variable like time and frames per second. It calls the helper
    # functions like spanObjects(), moveObjects() and drawObjects().
    elif (quadruplet[0] == 42):
        clock.tick(20)
        time += 1.0 / 20
        spawnObjects()
        moveObjects()
        if (timeDebug):
            print "------------------------------------>", time
        drawObjects()
        return True
    # mapSprite operation. It sets the sprite in quadruplet[3] to a particular char
    # in quadruplet[1]
    elif (quadruplet[0] == 43):
        value = quadruplet[1]
        if (value is not str):
            value = str(value)
        if (mapping.has_key(value)):
            mapping[value].append({quadruplet[3]: spriteSet[quadruplet[3]]})
        else:
            mapping[value] = [{quadruplet[3]: spriteSet[quadruplet[3]]}]
        return True
    # startGame. It works like gosub, with the difference that this is only for the game.
    elif (quadruplet[0] == 44):
        createERAInMemory()
        functionScope.append('SimpleGame')
        offset = 0
        instructionStack.append(instructionCounter)
        instructionCounter = 1
        resetParametersMemoryValues()
        return True
    # printEndGame. When the termination goals of the game are met, this operation is called
    # and prints if you won or lose.
    elif (quadruplet[0] == 45):
        drawObjects()
        if (quadruplet[3] == 'true'):
            print "WINNER!"
        else:
            print "YOU LOSE!"
        return True
    # ShieldFrom. A predefined operation to protect a particular sprite from killSprite.
    elif (quadruplet[0] == 46):
        protectFrom = quadruplet[1]
        protect = quadruplet[3]
        protectTile = tile
        if (debug):
            print protect, protectFrom, protectTile, spriteInTile
        return True
    # PullWithIt. A predefined operation of the game to make a sprite move according to
    # another sprite.
    elif (quadruplet[0] == 47):
        for object in movableObjects:
            if (object[0] == quadruplet[1] and object[1] == tile):
                object.append(quadruplet[3])
        return True
    # endGame. Similar to endFunc.
    elif (quadruplet[0] == 50):
        deleteERAInMemory()
        instructionCounter = instructionStack.pop()
        functionScope.pop()
        return True
# ============= END PROGRAM OPERATION ==========
    elif (quadruplet[0] == 99):
        return False

# Main.
# Run code with certain predefined arguments.
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"ho:d:t:",["outputFile=", "debug=","timeDebug="])
except getopt.GetoptError:
    print 'python2.7-32 arcadameVM.py [-o <outputfile>, -d <True|False>, default = False, -t <True|False>, default = False]'
    sys.exit(99)
for opt, arg in opts:
    # Help
    if opt == '-h':
        print 'python2.7-32 arcadameVM.py [-o <outputfile>, -d <True|False>, default = False, -t <True|False>, default = False]'
        sys.exit(1)
    # Set output file
    elif opt in ("-o", "--outputFile"):
        file = file(arg, 'w')
    # Set debug
    elif opt in ("-d", "--debug"):
        debug = arg == 'True'
    # Set timeDebug
    elif opt in ("-t", "--timeDebug"):
        timeDebug = arg == 'True'

# Read intermediate code.
readRawCode('rawCode.dame')
# Assign constants to execution memory
memory[3] = constants
# Start pygame.
pygame.init()
if (debug):
    print "Initial memory: ", memory
# ============================= MAIN LOOP WHERE MAGIC HAPPENS ==================================
while 1:
    # Evrey quadruplet returns a boolean. If there was an error, it will return False and stop
    # the executrion of the VM.
    if (doOperation(quadruplets[instructionCounter - 1])):
        instructionCounter += 1;
    else:
        break;
if (debug):
    print "Mapping: ", mapping
    print "Map: ", map
    print "Objects: ", objectsCount
    print "Final memory: ", memory
