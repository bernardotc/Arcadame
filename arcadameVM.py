# -----------------------------------------------------------------------------
# Bernardo Daniel Trevino Caballero     A00813175
# Myriam Maria Gutierrez Aburto         A00617060
# arcadame.py
#
# Virtual Machine for the languange Arcadame
# -----------------------------------------------------------------------------

import sys, getopt
import pygame
import time as tm
import xml.etree.ElementTree as ET
import random
from math import ceil

timeDebug = False
debug = False

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

def getSection(value):
    if (value < 7000):
        return 0
    elif (value < 12000):
        return 1
    elif (value < 17000):
        return 2
    else:
        return 3

def assignValueInMemory(memoryKey, value):
    global memory, offset
    if (memoryKey < 0):
        memoryKey = accessValueInMemory(-1 * memoryKey)
    section = getSection(memoryKey)
    if (debug):
        print "SET = assigning value in section: ", section
    if (section == 0):
        memory[section][memoryKey] = value
    else:
        memory[section][-1 - offset][memoryKey] = value

def accessValueInMemory(memoryKey):
    global memory, offset
    if (memoryKey < 0):
        memoryKey = accessValueInMemory(-1 * memoryKey)
    section = getSection(memoryKey)
    if (debug):
        print "GET = accessing value in section: ", section
    if (section == 0):
        return memory[section][memoryKey]
    elif (section == 3):
        return memory[section][memoryKey]['value']
    else:
        return memory[section][-1 - offset][memoryKey]

def createERAInMemory():
    global memory
    memory[1].append({})
    memory[2].append({})

def deleteERAInMemory():
    global memory
    memory[1].pop()
    memory[2].pop()

def assignParamInMemory(memoryKey1, memoryKey2):
    global memory, offset
    if (memoryKey2 < 0):
        memoryKey2 = accessValueInMemory(-1 * memoryKey2)
    section = getSection(memoryKey2)
    value = accessValueInMemory(memoryKey1)
    if (debug):
        print "Assigning parameters: ", memoryKey1, memoryKey2, value
    memory[section][-1][memoryKey2] = value

def getParamMemoryValue(paramType):
    global parametersMemoryValues
    value = parametersMemoryValues[paramType]
    parametersMemoryValues[paramType] += 1
    return value

def resetParametersMemoryValues():
    global parametersMemoryValues
    parametersMemoryValues = {101: 7000, 102: 8000, 103: 9000, 104: 10000, 105: 11000}

def readRawCode(fileName):
    global functionDictionary, constants, quadruplets, spriteSet
    parameters = []
    tree = ET.parse(fileName)
    for sprite in tree.find('game').find('sprites').findall('sprite'):
        name = sprite.find('spriteName').text
        type = int(sprite.find('type').text)
        spriteSet[name] = {'type': type}
    
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

    for quadruplet in tree.find('quadruplets').findall('quadruplet'):
        operator = int(quadruplet.find('operation').text)
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

def moveObjects():
    global map, time, movableObjects, spriteSet, maxMapRow, objectsCount, avatarPos
    for object in movableObjects:
        if (timeDebug):
            print time, spriteSet[object[0]]['speed'], object[2]
            print time - object[2]
        try:
            if (time * spriteSet[object[0]]['speed'] - object[2] >= 0 and object[3] == 'avatar'):
                object[2] += 1
                spriteListWithObject = map[object[1]]
                for index in range(0, len(spriteListWithObject)):
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
                            if (object[3] == 'avatar'):
                                for index in range(0, len(spriteListWithObject)):
                                    if (spriteListWithObject[index].has_key('avatar')):
                                        avatar = spriteListWithObject.pop(index)
                                        avatar['avatar']['last-position'] = sprite[object[0]]['last-position']
                                        avatarPos = object[1]
                                        map[object[1]].append(avatar)
                        break
            object.pop(3)
        except IndexError:
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

def spawnObjects():
    global spriteSet, map, movableObjects, time
    for spawn in spawnerObjects:
        spawner = spriteSet[spawn[0]]
        if (random.random() <= spawner['prob'] and int(time) % spawner['cooldown'] == 0):
            sprites = map[spawn[1]]
            spawnNew = True
            for index in range(0, len(sprites)):
                if (sprites[index].has_key(spawner['generatedSprite'])):
                    spawnNew = False
                    break
            if (spawnNew):
                map[spawn[1]].append({spawner['generatedSprite'] : spriteSet[spawner['generatedSprite']]})
                movableObjects.append([spawner['generatedSprite'], spawn[1], ceil(time * spriteSet[spawner['generatedSprite']]['speed'])])

def drawObjects():
    global map, maxMapRow, maxMapCol
    win.fill(globals()['color_white'])
    for r in range(0, maxMapRow):
        for c in range(0, maxMapCol):
            sprites = map[(r, c)]
            if (len(sprites) == 0):
                pygame.draw.rect(win, globals()['color_white'], [c * tileWidth, r * tileHeight, (c+1) * tileWidth, (r+1) * tileHeight])
            else:
                sprite = sprites[-1]
                for spriteKey, spritAttrib in sprite.iteritems():
                    if (debug):
                        print [c * tileWidth, r * tileHeight, (c+1) * tileWidth, (r+1) * tileHeight]
                    if (spritAttrib.has_key('color')):
                        pygame.draw.rect(win, globals()['color_' + spritAttrib['color']], [c * tileWidth, r * tileHeight, (c+1) * tileWidth, (r+1) * tileHeight])
    pygame.display.flip()

def doOperation(quadruplet):
    global instructionCounter, functionDictionary, instructionStack, functionScope, offset, spriteSet, map, score, mapRow, mapCol, mapping, objectsCount, time, maxMapRow, maxMapCol, tileWidth, tileHeight, win, clock, avatarPos, tile, file, movableObjects, protect, spriteInTile, protectFrom, protectTile, spawnerObjects
    if (debug):
        print instructionCounter, quadruplet
    if (quadruplet[0] < 10):
        elem1 = accessValueInMemory(quadruplet[1])
        elem2 = accessValueInMemory(quadruplet[2])
        if (quadruplet[0] == 0):
            result = elem1 + elem2
        elif (quadruplet[0] == 1):
            result = elem1 * elem2
        elif (quadruplet[0] == 2):
            result = elem1 - elem2
        elif (quadruplet[0] == 3):
            result = 1.0 * elem1 / elem2
        elif (quadruplet[0] == 4):
            result = elem1 and elem2
        elif (quadruplet[0] == 5):
            result = elem1 or elem2
        elif (quadruplet[0] == 6):
            result = elem1 < elem2
        elif (quadruplet[0] == 7):
            result = elem1 > elem2
        elif (quadruplet[0] == 8):
            result = elem1 != elem2
        elif (quadruplet[0] == 9):
            result = elem1 == elem2
        if (debug):
            print "elem1: ", elem1
            print "elem2: ", elem2
            print "result: ", result
        assignValueInMemory(quadruplet[3], result)
        return True
    elif (quadruplet[0] == 10):
        result = accessValueInMemory(quadruplet[1])
        assignValueInMemory(quadruplet[3], result)
        return True
    elif (quadruplet[0] == 11):
        instructionCounter = quadruplet[3] - 1
        return True
    elif (quadruplet[0] == 12):
        result = accessValueInMemory(quadruplet[1])
        if (debug):
            print "GOTOF result: ", result
        if (result == False):
            instructionCounter = quadruplet[3] - 1
        return True
    elif (quadruplet[0] == 13):
        result = accessValueInMemory(quadruplet[3])
        print "-----> AVM PRINT: ", result
        if (file):
            file.write("-> AVM PRINT: " + str(result) + '\n')
        return True
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
            # TODO
            # raise ERROR
            return False
    elif (quadruplet[0] == 15):
        scan = raw_input('-----> AVM GET_LINE: ')
        file.write("-> AVM GET_LINE: " + str(result) + '\n')
        assignValueInMemory(quadruplet[3], scan)
        return True
    elif (quadruplet[0] == 16):
        scan = raw_input('-----> AVM GET_BOOLEAN: ')
        result = scan.strip()
        if (result == 'True' or result == 'False'):
            file.write("-> AVM GET_BOOLEAN: " + str(result) + '\n')
            assignValueInMemory(quadruplet[3], result)
            return True
        else:
            # TODO
            # raise ERROR
            return False
    elif (quadruplet[0] == 17):
        scan = raw_input('-----> AVM GET_CHAR: ')
        if (len(scan) > 0):
            result = scan[0]
            file.write("-> AVM GET_CHAR: " + str(result) + '\n')
            return True
        else:
            # TODO
            # raise ERROR
            return False
    elif (quadruplet[0] == 18):
        deleteERAInMemory()
        if (debug):
            print "Memory after deleting ERA: ", memory
        instructionCounter = instructionStack.pop()
        functionScope.pop()
        resetParametersMemoryValues()
        return True
    elif (quadruplet[0] == 19):
        createERAInMemory()
        functionScope.append(quadruplet[3])
        offset = 1
        if (debug):
            print "Memory after creating ERA: ", memory
        return True
    elif (quadruplet[0] == 20):
        function = quadruplet[3]
        instructionStack.append(instructionCounter)
        offset = 0
        instructionCounter = functionDictionary[function]['quadruplet'] - 1
        resetParametersMemoryValues()
        return True
    elif (quadruplet[0] == 21):
        value = quadruplet[1]
        if (debug):
            print "Function scope Name for Params: ", functionScope
        paramType = functionDictionary[functionScope[-1]]['parameters'][quadruplet[3] - 1]
        param = getParamMemoryValue(paramType)
        assignParamInMemory(value, param)
        return True
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
    elif (quadruplet[0] == 23):
        result = accessValueInMemory(quadruplet[1])
        if (result >= quadruplet[2] and result <= quadruplet[3]):
            return True
        else:
            # TODO: - raise ERROR
            return False
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
    elif (quadruplet[0] == 31):
        for k in quadruplet[3]:
            map[(mapRow, mapCol)] = list(mapping[k])
            for sprite in mapping[k]:
                for spr, attr in sprite.iteritems():
                    if (spr == 'avatar'):
                        avatarPos = (mapRow, mapCol)
                    if (objectsCount.has_key(spr)):
                        objectsCount[spr] += 1
                    else:
                        objectsCount[spr] = 1
                    if (attr['type'] == 204):
                        movableObjects.append([spr, (mapRow, mapCol), 0])
                    elif (attr['type'] == 205):
                        spawnerObjects.append([spr, (mapRow, mapCol)])
            mapCol += 1
        mapRow += 1
        if (mapCol > maxMapCol):
            maxMapCol = mapCol
        if (mapRow > maxMapRow):
            maxMapRow = mapRow
        mapCol = 0
        return True
    elif (quadruplet[0] == 32):
        score = 0
        time = 0
        if (debug):
            print [maxMapCol * tileWidth, maxMapRow * tileHeight]
        win = pygame.display.set_mode([maxMapCol * tileWidth, maxMapRow * tileHeight])
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game")
        return True
    elif (quadruplet[0] == 33):
        assignValueInMemory(quadruplet[3], objectsCount[quadruplet[1]] == quadruplet[2])
        return True
    elif (quadruplet[0] == 34):
        assignValueInMemory(quadruplet[3], time >= quadruplet[2])
        return True
    elif (quadruplet[0] == 35):
        elem1 = accessValueInMemory(quadruplet[1])
        assignValueInMemory(quadruplet[3], not elem1)
        return True
    elif (quadruplet[0] == 36):
        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.KEYDOWN):
                # DOWN
                if (event.key == pygame.K_DOWN):
                    if (avatarPos[0] < maxMapRow - 1):
                        spriteListWithAvatar = map[avatarPos]
                        for index in range(0, len(spriteListWithAvatar)):
                            if (spriteListWithAvatar[index].has_key('avatar')):
                                avatar = spriteListWithAvatar.pop(index)
                                avatar['avatar']['last-position'] = avatarPos
                                avatarPos = (avatarPos[0] + 1, avatarPos[1])
                                map[avatarPos].append(avatar)
                                break
                # UP
                if (event.key == pygame.K_UP):
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
                    if (avatarPos[1] < maxMapCol - 1):
                        spriteListWithAvatar = map[avatarPos]
                        for index in range(0, len(spriteListWithAvatar)):
                            if (spriteListWithAvatar[index].has_key('avatar')):
                                avatar = spriteListWithAvatar.pop(index)
                                avatar['avatar']['last-position'] = avatarPos
                                avatarPos = (avatarPos[0], avatarPos[1] + 1)
                                map[avatarPos].append(avatar)
                                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
        return True
    elif (quadruplet[0] == 37):
        if (tile[1] < maxMapCol - 1):
            tile = (tile[0], tile[1] + 1)
            assignValueInMemory(quadruplet[3], True)
        elif (tile[0] < maxMapRow - 1):
            tile = (tile[0] + 1, 0)
            assignValueInMemory(quadruplet[3], True)
        else:
            assignValueInMemory(quadruplet[3], False)
            tile = (0,-1)
        if (debug):
            print tile
        spriteInTile = []
        return True
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
                if (protect in spriteInTile and protectFrom in spriteInTile and tile == protectTile):
                    protect = ""
                    protectFrom = ""
                else:
                    spriteList.pop(index)
                    objectsCount[quadruplet[3]] -= 1
                    break
        return True
    elif (quadruplet[0] == 40):
        score += float(quadruplet[1])
        return True
    elif (quadruplet[0] == 41):
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
    elif (quadruplet[0] == 42):
        clock.tick(20)
        time += 1.0 / 20
        spawnObjects()
        moveObjects()
        if (timeDebug):
            print "------------------------------------>", time
        drawObjects()
        return True
    elif (quadruplet[0] == 43):
        value = quadruplet[1]
        if (value is not str):
            value = str(value)
        if (mapping.has_key(value)):
            mapping[value].append({quadruplet[3]: spriteSet[quadruplet[3]]})
        else:
            mapping[value] = [{quadruplet[3]: spriteSet[quadruplet[3]]}]
        return True
    elif (quadruplet[0] == 44):
        createERAInMemory()
        functionScope.append('SimpleGame')
        offset = 0
        instructionStack.append(instructionCounter)
        instructionCounter = 1
        resetParametersMemoryValues()
        return True
    elif (quadruplet[0] == 45):
        drawObjects()
        if (quadruplet[3] == 'true'):
            print "WINNER!"
        else:
            print "YOU LOSE!"
        return True
    elif (quadruplet[0] == 46):
        protectFrom = quadruplet[1]
        protect = quadruplet[3]
        protectTile = tile
        if (debug):
            print protect, protectFrom, protectTile, spriteInTile
        return True
    elif (quadruplet[0] == 47):
        for object in movableObjects:
            if (object[0] == quadruplet[1] and object[1] == tile):
                object.append(quadruplet[3])
#movableObjects.append([quadruplet[3], tile, ceil(time * spriteSet[quadruplet[1]]['speed']), quadruplet[1]])
        return True
    elif (quadruplet[0] == 50):
        deleteERAInMemory()
        instructionCounter = instructionStack.pop()
        functionScope.pop()
        return True
    elif (quadruplet[0] == 99):
        return False

# Main.
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"ho:d:t:",["outputFile=", "debug=","timeDebug="])
except getopt.GetoptError:
    print 'python2.7-32 arcadameVM.py [-o <outputfile>, -d <True|False>, default = False, -t <True|False>, default = False]'
    sys.exit(99)
for opt, arg in opts:
    if opt == '-h':
        print 'python2.7-32 arcadameVM.py [-o <outputfile>, -d <True|False>, default = False, -t <True|False>, default = False]'
        sys.exit(1)
    elif opt in ("-o", "--outputFile"):
        file = file(arg, 'w')
    elif opt in ("-d", "--debug"):
        debug = arg == 'True'
    elif opt in ("-t", "--timeDebug"):
        timeDebug = arg == 'True'

readRawCode('rawCode.dame')
memory[3] = constants
pygame.init()
if (debug):
    print "Initial memory: ", memory
while 1:
    if (doOperation(quadruplets[instructionCounter - 1])):
        instructionCounter += 1;
    else:
        break;
########## TODO - ERASE tm.sleep(5)
if (debug):
    print "Mapping: ", mapping
    print "Map: ", map
    print "Objects: ", objectsCount
    print "Final memory: ", memory
