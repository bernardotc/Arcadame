# -----------------------------------------------------------------------------
# Bernardo Daniel Trevino Caballero     A00813175
# Myriam Maria Gutierrez Aburto         A00617060
# arcadame.py
#
# Virtual Machine for the languange Arcadame
# -----------------------------------------------------------------------------

import xml.etree.ElementTree as ET
import timeit

timer = timeit.default_timer

totalTimeAccess = 0
totalTimeAssign = 0

timeIt = False
debug = False

functionDictionary = {}
constants = {}
quadruplets = []
instructionCounter = 1;
instructionStack = []
functionScope = ""
parametersMemoryValues = {101: 7000, 102: 8000, 103: 9000, 104: 10000, 105: 11000}

# Memory of execution
memory = [{}, [{}], [{}], constants]

def getSection(value):
    if (value < 7000):
        return 0
    elif (value < 12000):
        return 1
    elif (value < 17000):
        return 2
    else:
        return 3

def getIndirectDirection(result):
    result = result.replace('[', '')
    result = result.replace(']', '')
    return int(result)

def assignValueInMemory(memoryKey, value):
    global memory
        ##if (isinstance(memoryKey, str)):
        ##memoryKey = accessValueInMemory(getIndirectDirection(memoryKey))
    section = getSection(memoryKey)
    if (debug):
        print "SET = assigning value in section: ", section
    if (section == 0):
        memory[section][memoryKey] = value
    else:
        memory[section][-1][memoryKey] = value

def accessValueInMemory(memoryKey):
    global memory
        ##if (isinstance(memoryKey, str)):
        ##memoryKey = accessValueInMemory(getIndirectDirection(memoryKey))
    section = getSection(memoryKey)
    if (debug):
        print "GET = accessing value in section: ", section
    if (section == 0):
        return memory[section][memoryKey]
    elif (section == 3):
        return memory[section][memoryKey]['value']
    else:
        return memory[section][-1][memoryKey]

def createERAInMemory():
    global memory
    memory[1]['values'].append({})
    memory[2]['values'].append({})

def addOffsetsInMemory():
    global memory
    offset = len(memory[1]['values']) - 1
    memory[1]['offsetStack'].append(offset)
    memory[2]['offsetStack'].append(offset)


def deleteERAInMemory():
    global memory
    memory[1]['offsetStack'].pop()
    memory[1]['values'].pop()
    memory[2]['offsetStack'].pop()
    memory[2]['values'].pop()

def assignParamInMemory(memoryKey1, memoryKey2):
    global memory
    if (isinstance(memoryKey2, str)):
        memoryKey2 = accessValueInMemory(getIndirectDirection(memoryKey2))
    section = getSection(memoryKey2)
    value = accessValueInMemory(memoryKey1)
    if (debug):
        print "Assigning parameters: ", memoryKey1, memoryKey2, value
    offset = len(memory[section]['values']) - 1
    memory[section]['values'][offset][memoryKey2] = value

def getParamMemoryValue(paramType):
    global parametersMemoryValues
    value = parametersMemoryValues[paramType]
    parametersMemoryValues[paramType] += 1
    return value

def resetParametersMemoryValues():
    global parametersMemoryValues
    parametersMemoryValues = {101: 7000, 102: 8000, 103: 9000, 104: 10000, 105: 11000}

def readRawCode(fileName):
    global functionDictionary, constants, quadruplets
    parameters = []
    tree = ET.parse(fileName)
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
    global instructionCounter, functionDictionary, instructionStack, functionScope, totalTimeAccess, totalTimeAssign
    if (debug):
        print quadruplet
    if (quadruplet[0] < 10):
        t1 = timer();
        elem1 = accessValueInMemory(quadruplet[1])
        elem2 = accessValueInMemory(quadruplet[2])
        t2 = timer();
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
        t3 = timer()
        assignValueInMemory(quadruplet[3], result)
        t4 = timer()
        if (timeIt):
            print "Access operands : ", t2-t1
            print "Assign result   : ", t4-t3
            totalTimeAccess += t2-t1
            totalTimeAssign += t4-t3
        return True
    elif (quadruplet[0] == 10):
        t1 = timer()
        result = accessValueInMemory(quadruplet[1])
        t2 = timer()
        assignValueInMemory(quadruplet[3], result)
        t3 = timer()
        if (timeIt):
            print "Access operand : ", t2-t1
            print "Assign result  : ", t3-t2
        totalTimeAccess += t2-t1
        totalTimeAssign += t3-t2
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
    elif (quadruplet[0] == 18):
        deleteERAInMemory()
        if (debug):
            print "Memory after deleting ERA: ", memory
        instructionCounter = instructionStack.pop()
        functionScope = ""
        resetParametersMemoryValues()
        return True
    elif (quadruplet[0] == 19):
        createERAInMemory()
        functionScope = quadruplet[3]
        if (debug):
            print "Memory after creating ERA: ", memory
        return True
    elif (quadruplet[0] == 20):
        function = quadruplet[3]
        instructionStack.append(instructionCounter)
        addOffsetsInMemory()
        instructionCounter = functionDictionary[function]['quadruplet'] - 1
        resetParametersMemoryValues()
        return True
    elif (quadruplet[0] == 21):
        value = quadruplet[1]
        if (debug):
            print "Function scope Name for Params: ", functionScope
        paramType = functionDictionary[functionScope]['parameters'][quadruplet[3] - 1]
        param = getParamMemoryValue(paramType)
        assignParamInMemory(value, param)
        return True
    elif (quadruplet[0] == 22):
        result = accessValueInMemory(quadruplet[3])
        assignValueInMemory(functionDictionary[functionScope]['memory'], result)
        deleteERAInMemory()
        if (debug):
            print "Memory after deleting ERA: ", memory
        instructionCounter = instructionStack.pop()
        return True
    elif (quadruplet[0] == 23):
        result = accessValueInMemory(quadruplet[1])
        if (result >= quadruplet[2] and result <= quadruplet[3]):
            return True
        else:
            # TODO: - raise ERROR
            return False
    elif (quadruplet[0] == 30):
        return False

# Main.
readRawCode('rawCode.xml')
if (debug):
    print "Initial memory: ", memory
count = 100000
while count > 0:
    instructionCounter = 1
    memory = [{}, [{}], [{}], constants]
    memory[3] = constants
    while 1:
        if (doOperation(quadruplets[instructionCounter - 1])):
            instructionCounter += 1;
        else:
            break;
    if (debug):
        print "Final memory: ", memory
    count -= 1
print "Total access time: ", totalTimeAccess
print "Total assign time: ", totalTimeAssign
