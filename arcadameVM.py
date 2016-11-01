# -----------------------------------------------------------------------------
# Bernardo Daniel Trevino Caballero     A00813175
# Myriam Maria Gutierrez Aburto         A00617060
# arcadame.py
#
# Virtual Machine for the languange Arcadame
# -----------------------------------------------------------------------------

import xml.etree.ElementTree as ET

debug = True

functionDictionary = {}
constants = {}
quadruplets = []
instructionCounter = 1;

# Memory of execution
memory = {0: {}, 1: {'offsetStack': [], 'values': [{}]}, 2: {'offsetStack': [], 'values': [{}]}, 3: constants}

def getSection(value):
    if (value < 8000):
        return 0
    elif (value < 14000):
        return 1
    elif (value < 20000):
        return 2
    else:
        return 3

def assignValueInMemory(memoryKey, value):
    global memory
    section = getSection(memoryKey)
    if (debug):
        print "SET = assigning value in section: ", section
    if (section == 0):
        memory[section][memoryKey] = value
    else:
        if (len(memory[section]['offsetStack']) == 0):
            memory[section]['values'][0][memoryKey] = value
        else:
            offset = memory[section]['offsetStack'].top()
            memory[section]['values']['offsetStack'][memoryKey] = value

def accessValueInMemory(memoryKey):
    global memory
    section = getSection(memoryKey)
    if (debug):
        print "GET = accessing value in section: ", section
    if (section == 0):
        return memory[section][memoryKey]
    elif (section == 3):
        return memory[section][memoryKey]['value']
    else:
        if (len(memory[section]['offsetStack']) == 0):
            return memory[section]['values'][0][memoryKey]
        else:
            offset = memory[section]['offsetStack'].top()
            return memory[section]['values']['offsetStack'][memoryKey]

def readRawCode(fileName):
    global functionDictionary, constants, quadruplets
    parameters = []
    tree = ET.parse(fileName)
    for function in tree.find('functions').findall('function'):
        name = function.find('functionName').text
        for parameter in function.findall('parameter'):
            parameters.append(parameter.text)
        memory = function.find('return').text
        quadruplet = function.find('quadruplet').text
        eraRoot = function.find('era')
        era = [int(eraRoot.find('int').text), int(eraRoot.find('float').text), int(eraRoot.find('string').text), int(eraRoot.find('char').text), int(eraRoot.find('boolean').text)]
        functionDictionary[name] = {'parameters': parameters, 'memory': int(memory), 'quadruplet': int(quadruplet), 'era': era}

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
        elem1 = int(quadruplet.find('element1').text)
        elem2 = int(quadruplet.find('element2').text)
        try:
            result = int(quadruplet.find('result').text)
        except ValueError:
            result = quadruplet.find('result').text
        quadruplets.append([operator, elem1, elem2, result])

    if (debug):
        print "functions: ", functionDictionary
        print "constants: ", constants
        print "quadruplets: ", quadruplets

def doOperation(quadruplet):
    global instructionCounter
    if (debug):
        print quadruplet
    if (quadruplet[0] < 9):
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
    elif (quadruplet[0] == 13):
        result = accessValueInMemory(quadruplet[3])
        print "-----> AVM PRINT: ", result
        return True
    elif (quadruplet[0] == 14):
        scan = raw_input('-----> AVM GET_VALUE: ')
        try:
            if (quadruplet[3] < 15000):
                result = int(scan.strip())
            else:
                result = float(scan.strip())
            assignValueInMemory(quadruplet[3], result)
            return True
        except:
            # TODO
            # raise ERROR
            return False
    elif (quadruplet[0] == 15):
        scan = raw_input('-----> AVM GET_LINE: ')
        assignValueInMemory(quadruplet[3], scan)
        return True
    elif (quadruplet[0] == 16):
        scan = raw_input('-----> AVM GET_BOOLEAN: ')
        result = scan.strip()
        if (result == 'True' or result == 'False'):
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
            return True
        else:
            # TODO
            # raise ERROR
            return False
    elif (quadruplet[0] == 30):
        return False

# Main.
readRawCode('rawCode.xml')
memory[3] = constants
print "memory: ", memory
while 1:
    if (doOperation(quadruplets[instructionCounter - 1])):
        instructionCounter += 1;
    else:
        break;
print "memory: ", memory
