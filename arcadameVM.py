# -----------------------------------------------------------------------------
# Bernardo Daniel Trevino Caballero     A00813175
# Myriam Maria Gutierrez Aburto         A00617060
# arcadame.py
#
# Virtual Machine for the languange Arcadame
# -----------------------------------------------------------------------------

# Memory of execution
memory = {0: {}, 1: {'offsetStack': [], 'values': [{}]} 2: {}}

def assignValueInMemory(section, memoryKey, value):
    global memory
    if (section == 0 or section == 3):
        memory[section][memoryKey] = value
    else:
        if (len(memory[section][offsetStack]) == 0):
            memory[section]['values'][0][memoryKey] = value
        else:
            offset = memory[section][offsetStack].top()
            memory[section]['values'][offsetStack][memoryKey] = value

def accessValueInMemory(section, memoryKey):
    global memory
    if (section == 0 or section == 3):
        return memory[section][memoryKey]
    else:
        if (len(memory[section][offsetStack]) == 0):
            return memory[section]['values'][0][memoryKey]
        else:
            offset = memory[section][offsetStack].top()
            return memory[section]['values'][offsetStack][memoryKey]
