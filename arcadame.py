# -----------------------------------------------------------------------------
# Bernardo Daniel Trevino Caballero     A00813175
# Myriam Maria Gutierrez Aburto         A00617060
# arcadame.py
#
# A simple scanner and parser for the languange Arcadame
# -----------------------------------------------------------------------------

# + = 0
# * = 1
# - = 2
# / = 3
# && = 4
# || = 5
# < = 6
# > = 7
# != = 8
# == = 9
# = = 10
# int = 101
# float = 102
# string = 103
# char = 104
# boolean = 105
# list = 1000
# Immovable = 201
# MovingAvatar = 202
# ShootingAvatar = 203
# Missile = 204
# Spawner = 205
# Passive = 206

import sys, getopt
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

debug = False

# Global variables, dictionaries and lists
avail = {}
stackJumps = []
stackTypes = []
stackOperators = []
stackOp = []
stackOpVisible = []
listCode = []
listSprites = []
killSprites = []
gameAttrs = {}
gameActions = []
gameSections = {}
functionDirectory = {}
variables = {}
constants = {}
parameters = []
globalVariables = {}
typeOfVariable = ""
functionId = ""
listId = ""
sureListId = ""
listScope = ""
paramCounter = 0
goSubFunction = ""
spriteId = ""
temporalStamp = {}

# Error handling by using classes
class LexerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SyntaxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SemanticError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# Semantic cube used for operations.
semanticCube = [[[-1,-1,-1,-1,-1,-1,-1,-1,-1,105,1000], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],       [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],       [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]],
                [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],  [101,101,101,101,-1,-1,105,105,105,105,101],   [102,102,102,102,-1,-1,105,105,105,105,102],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]],
                [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],  [102,102,102,102,-1,-1,105,105,105,105,102],   [102,102,102,102,-1,-1,105,105,105,105,102],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]],
                [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],       [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],       [-1,-1,-1,-1,-1,-1,-1,-1,105,105,103],  [-1,-1,-1,-1,-1,-1,-1,-1,105,105,103],  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]],
                [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],       [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],       [-1,-1,-1,-1,-1,-1,-1,-1,105,105,103],  [-1,-1,-1,-1,-1,-1,-1,-1,105,105,104],  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]],
                [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],       [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],       [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],   [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],   [-1,-1,-1,-1,105,105,-1,-1,105,105,105]]]

# Helper function that converts the different types to int values.
def convertAtomicTypeToCode(type):
    if (type == "int"):
        return 101
    elif (type == "float"):
        return 102
    elif (type == "string"):
        return 103
    elif (type == "char"):
        return 104
    elif (type == "boolean"):
        return 105
    elif (type == "Immovable"):
        return 201
    elif (type == "MovingAvatar"):
        return 202
    elif (type == "ShootingAvatar"):
        return 203
    elif (type == "Missile"):
        return 204
    elif (type == "Spawner"):
        return 205
    elif (type == "Passive"):
        return 206
    elif (type == "color"):
        return 301
    elif (type == "portal"):
        return 302
    elif (type == "orientation"):
        return 303
    elif (type == "speed"):
        return 304
    elif (type == "generatedSprite"):
        return 305
    elif (type == "prob"):
        return 306
    elif (type == "cooldown"):
        return 307

# Helper function that converts the different operations into int values.
def convertOperatorToCode(type):
    if (type == '+'):
        return 0
    elif (type == '*'):
        return 1
    elif (type == '-'):
        return 2
    elif (type == '/'):
        return 3
    elif (type == '&&'):
        return 4
    elif (type == '||'):
        return 5
    elif (type == '<'):
        return 6
    elif (type == '>'):
        return 7
    elif (type == '!='):
        return 8
    elif (type == '=='):
        return 9
    elif (type == '='):
        return 10
    elif (type == 'goto'):
        return 11
    elif (type == 'gotoF'):
        return 12
    elif (type == 'print'):
        return 13
    elif (type == 'getValue'):
        return 14
    elif (type == 'getLine'):
        return 15
    elif (type == 'getBoolean'):
        return 16
    elif (type == 'getChar'):
        return 17
    elif (type == 'endFunc'):
        return 18
    elif (type == 'era'):
        return 19
    elif (type == 'gosub'):
        return 20
    elif (type == 'param'):
        return 21
    elif (type == 'return'):
        return 22
    elif (type == 'verify'):
        return 23
    elif (type == '.='):
        return 30
    elif (type == 'addRowMap'):
        return 31
    elif (type == 'initialize'):
        return 32
    elif (type == 'spriteCounter'):
        return 33
    elif (type == 'timeout'):
        return 34
    elif (type == 'not'):
        return 35
    elif (type == 'checkMove'):
        return 36
    elif (type == 'getNextTile'):
        return 37
    elif (type == 'inTile'):
        return 38
    elif (type == 'killSprite'):
        return 39
    elif (type == 'scoreChange'):
        return 40
    elif (type == 'stepBack'):
        return 41
    elif (type == 'drawMap'):
        return 42
    elif (type == 'mapSprite'):
        return 43
    elif (type == 'startGame'):
        return 44
    elif (type == 'printEndGame'):
        return 45
    elif (type == 'shieldFrom'):
        return 46
    elif (type == 'pullWithIt'):
        return 47
    elif (type == 'endGame'):
        return 50
    elif (type == 'end'):
        return 99

# ==================================== LEXER ======================================
# Define token names
tokens = (
    'SIMPLEGAME', 'PROGRAM', 'SPRITESET', 'IMMOVABLE', 'MOVINGAVATAR', 'SHOOTINGAVATAR', 'MISSILE', 'SPAWNER', 'PASSIVE', 'IMG', 'GENERATEDSPRITE', 'SPEED', 'PORTAL', 'SHRINKFACTOR', 'LIMIT', 'PROB', 'COOLDOWN', 'COLOR', 'ORIENTATION', 'HEALTHPOINTS', 'LIMITHEALTHPOINTS', 'WEAPONSPRITE', 'ENCOUNTERS', 'INTERACTIONLIST', 'KILLSPRITE', 'STEPBACK', 'SCORECHANGE', 'TRANSFORMTO', 'BOUNCEFORWARD', 'CHANGEHEALTHPOINTS', 'ADDTIMER', 'TIME', 'TRANSFORMALL', 'TERMINATIONGOALS', 'SPRITECOUNTER', 'SPRITE', 'MULTISPRITECOUNTER', 'TIMEOUT', 'WIN', 'MAPPING', 'MAP', 'FUNC', 'INT', 'FLOAT', 'STRING', 'CHAR', 'BOOLEAN', 'MAIN', 'VAR', 'PRINT', 'IF', 'ELSE', 'GETVALUE', 'GETLINE', 'GETBOOLEAN', 'GETCHAR', 'WHILE', 'SMALL_END', 'BIG_END', 'STARTGAME', 'RETURN', 'D_2P', 'D_PYC', 'D_C', 'D_PA', 'D_PC', 'D_AMP', 'EQUAL', 'PLUS', 'MINUS', 'TIMES', 'DIVISION', 'MENOR_QUE', 'MAYOR_QUE', 'DIFERENTE_DE', 'IGUAL_QUE', 'AND', 'OR', 'D_CA', 'D_CC', 'ID', 'INT_CT', 'FLOAT_CT', 'STRING_CT', 'BOOLEAN_CT', 'CHAR_CT', 'COLOR_CT', 'MOVEMENT_CT', 'PULLWITHIT', 'SHIELDFROM'
)

# Define regular expressions of tokens
def t_SIMPLEGAME(t):
    'SimpleGame'
    if (debug):
        print(t)
    return t

def t_PROGRAM(t):
    'Program'
    if (debug):
        print(t)
    return t

def t_SPRITESET(t):
    'SpriteSet'
    if (debug):
        print(t)
    return t

def t_IMMOVABLE(t):
    'Immovable'
    if (debug):
        print(t)
    return t

def t_MOVINGAVATAR(t):
    'MovingAvatar'
    if (debug):
        print(t)
    return t

def t_SHOOTINGAVATAR(t):
    'ShootingAvatar'
    if (debug):
        print(t)
    return t

def t_MISSILE(t):
    'Missile'
    if (debug):
        print(t)
    return t

def t_SPAWNER(t):
    'Spawner'
    if (debug):
        print(t)
    return t

def t_PASSIVE(t):
    'Passive'
    if (debug):
        print(t)
    return t

def t_IMG(t):
    'img'
    if (debug):
        print(t)
    return t

def t_GENERATEDSPRITE(t):
    'generatedSprite'
    if (debug):
        print(t)
    return t

def t_SPEED(t):
    'speed'
    if (debug):
        print(t)
    return t

def t_PORTAL(t):
    'portal'
    if (debug):
        print(t)
    return t

def t_SHRINKFACTOR(t):
    'shrinkFactor'
    if (debug):
        print(t)
    return t

def t_LIMIT(t):
    'limit'
    if (debug):
        print(t)
    return t

def t_PROB(t):
    'prob'
    if (debug):
        print(t)
    return t

def t_COOLDOWN(t):
    'cooldown'
    if (debug):
        print(t)
    return t

def t_COLOR(t):
    'color'
    if (debug):
        print(t)
    return t

def t_ORIENTATION(t):
    'orientation'
    if (debug):
        print(t)
    return t

def t_HEALTHPOINTS(t):
    'healthPoints'
    if (debug):
        print(t)
    return t

def t_LIMITHEALTHPOINTS(t):
    'limitHealthPoints'
    if (debug):
        print(t)
    return t

def t_WEAPONSPRITE(t):
    'weaponSprite'
    if (debug):
        print(t)
    return t

def t_ENCOUNTERS(t):
    'encounters'
    if (debug):
        print(t)
    return t

def t_INTERACTIONLIST(t):
    'InteractionList'
    if (debug):
        print(t)
    return t

def t_KILLSPRITE(t):
    'killSprite'
    if (debug):
        print(t)
    return t

def t_STEPBACK(t):
    'stepBack'
    if (debug):
        print(t)
    return t

def t_PULLWITHIT(t):
    'pullWithIt'
    if (debug):
        print(t)
    return t

def t_SHIELDFROM(t):
    'shieldFrom'
    if (debug):
        print(t)
    return t

def t_SCORECHANGE(t):
    'scoreChange'
    if (debug):
        print(t)
    return t

def t_TRANSFORMTO(t):
    'transfromTo'
    if (debug):
        print(t)
    return t

def t_BOUNCEFORWARD(t):
    'bounceForward'
    if (debug):
        print(t)
    return t

def t_CHANGEHEALTHPOINTS(t):
    'changeHealthPoints'
    if (debug):
        print(t)
    return t

def t_ADDTIMER(t):
    'addTimer'
    if (debug):
        print(t)
    return t

def t_TIMEOUT(t):
    'timeout'
    if (debug):
        print(t)
    return t

def t_TIME(t):
    'time'
    if (debug):
        print(t)
    return t

def t_TRANSFORMALL(t):
    'transformAll'
    if (debug):
        print(t)
    return t

def t_TERMINATIONGOALS(t):
    'TerminationGoals'
    if (debug):
        print(t)
    return t

def t_SPRITECOUNTER(t):
    'spriteCounter'
    if (debug):
        print(t)
    return t

def t_SPRITE(t):
    'sprite'
    if (debug):
        print(t)
    return t

def t_MULTISPRITECOUNTER(t):
    'multiSpriteCounter'
    if (debug):
        print(t)
    return t

def t_WIN(t):
    'win'
    if (debug):
        print(t)
    return t

def t_MAPPING(t):
    'Mapping'
    if (debug):
        print(t)
    return t

def t_MAP(t):
    'Map'
    if (debug):
        print(t)
    return t

def t_FUNC(t):
    'func'
    if (debug):
        print(t)
    return t

def t_INT(t):
    'int'
    if (debug):
        print(t)
    return t

def t_FLOAT(t):
    'float'
    if (debug):
        print(t)
    return t

def t_STRING(t):
    'string'
    if (debug):
        print(t)
    return t

def t_CHAR(t):
    'char'
    if (debug):
        print(t)
    return t

def t_BOOLEAN(t):
    'boolean'
    if (debug):
        print(t)
    return t

def t_MAIN(t):
    'Main'
    if (debug):
        print(t)
    return t

def t_VAR(t):
    'var'
    if (debug):
        print(t)
    return t

def t_PRINT(t):
    'print'
    if (debug):
        print(t)
    return t

def t_IF(t):
    'if'
    if (debug):
        print(t)
    return t

def t_ELSE(t):
    'else'
    if (debug):
        print(t)
    return t

def t_GETVALUE(t):
    'getValue'
    if (debug):
        print(t)
    return t

def t_GETLINE(t):
    'getLine'
    if (debug):
        print(t)
    return t

def t_GETBOOLEAN(t):
    'getBoolean'
    if (debug):
        print(t)
    return t

def t_GETCHAR(t):
    'getChar'
    if (debug):
        print(t)
    return t

def t_WHILE(t):
    'while'
    if (debug):
        print(t)
    return t

def t_SMALL_END(t):
    'end'
    if (debug):
        print(t)
    return t

def t_BIG_END(t):
    'End'
    if (debug):
        print(t)
    return t

def t_STARTGAME(t):
    'StartGame'
    if (debug):
        print(t)
    return t

def t_RETURN(t):
    'return'
    if (debug):
        print(t)
    return t

def t_D_2P(t):
    ':'
    if (debug):
        print(t)
    return t

def t_D_PYC(t):
    ';'
    if (debug):
        print(t)
    return t

def t_D_C(t):
    ','
    if (debug):
        print(t)
    return t

def t_D_PA(t):
    '\('
    if (debug):
        print(t)
    return t

def t_D_PC(t):
    '\)'
    if (debug):
        print(t)
    return t

def t_IGUAL_QUE(t):
    '=='
    if (debug):
        print(t)
    return t

def t_EQUAL(t):
    '='
    if (debug):
        print(t)
    return t

def t_PLUS(t):
    '\+'
    if (debug):
        print(t)
    return t

def t_MINUS(t):
    '-'
    if (debug):
        print(t)
    return t

def t_TIMES(t):
    '\*'
    if (debug):
        print(t)
    return t

def t_DIVISION(t):
    '/'
    if (debug):
        print(t)
    return t

def t_MENOR_QUE(t):
    '<'
    if (debug):
        print(t)
    return t

def t_MAYOR_QUE(t):
    '>'
    if (debug):
        print(t)
    return t

def t_DIFERENTE_DE(t):
    '!='
    if (debug):
        print(t)
    return t

def t_AND(t):
    '&&'
    if (debug):
        print(t)
    return t

def t_D_AMP(t):
    '&'
    if (debug):
        print(t)
    return t

def t_OR(t):
    '\|\|'
    if (debug):
        print(t)
    return t

def t_D_CA(t):
    '\['
    if (debug):
        print(t)
    return t

def t_D_CC(t):
    '\]'
    if (debug):
        print(t)
    return t

def t_FLOAT_CT(t):
    r'[0-9]+\.[0-9]+'
    if (debug):
        print(t)
    return t

def t_INT_CT(t):
    r'[0-9]+'
    if (debug):
        print(t)
    return t

def t_BOOLEAN_CT(t):
    r'true|false'
    if (debug):
        print(t)
    return t

def t_CHAR_CT(t):
    r'\'([a-zA-Z]|[0-9]|[ \*\[\]\\\^\-\.\?\+\|\(\)\$\/\{\}\%\<\>=&;,_:\[\]|\'!$#@])\''
    if (debug):
        print(t)
    return t

def t_COLOR_CT(t):
    r'red|green|blue|yellow|black|orange|purple|cyan|white|brown'
    if (debug):
        print(t)
    return t

def t_MOVEMENT_CT(t):
    r'left|right|up|down'
    if (debug):
        print(t)
    return t

def t_STRING_CT(t):
    r'\"([a-zA-Z]|[0-9]|[ \*\[\]\\\^\-\.\?\+\|\(\)\$\/\{\}\%\<\>=&;,_:\[\]\'!$#@])*\"'
    if (debug):
        print(t)
    return t

def t_ID(t):
    r'[a-zA-Z]([a-zA-Z]|[0-9])*(_([a-zA-z]|[0-9])+)*'
    if (debug):
        print(t)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    raise LexerError("Illegal character at '%s'" % t.value[0])

# Build the lexer
import ply.lex as lex
lex.lex()

# ====================================== PARSER ======================================
# Parsing rules
start = 'programa'

def p_programa(p):
    '''programa : SIMPLEGAME generate_initial_goto ID D_2P sprites interactions goals mapping map generate_game block generate_end
                | PROGRAM generate_initial_goto ID D_2P block generate_end'''
    global functionDirectory, constants
    # Save constants to functionDirectory
    functionDirectory["constants"] = constants

def p_generate_initial_goto(p):
    '''generate_initial_goto : '''
    global listCode, stackJumps
    # Initial goto that goes to Main.
    listCode.append([convertOperatorToCode('goto'),-1,-1,'pending'])
    stackJumps.append(len(listCode))

def p_generate_game(p):
    '''generate_game : '''
    global functionDirectory, gameSections
    # Save SimpleGame in function directory
    functionDirectory["SimpleGame"] = {"sections" : gameSections}
    gameSections = {}
    # Generate the quadruplets of the game loop.
    generateIntermediateCodeGame()


def p_generate_end(p):
    '''generate_end : BIG_END'''
    global listCode
    # END of program
    listCode.append([convertOperatorToCode('end'), -1, -1, -1])

def p_sprites(p):
    '''sprites : SPRITESET D_2P sprite D_PYC more_sprites SMALL_END'''
    global gameSections, variables
    # Add the sprites section to the game dictionary
    gameSections[p[1]] = variables
    variables = {}

def p_more_sprites(p):
    '''more_sprites : sprite D_PYC more_sprites
                    | '''

def p_sprite(p):
    '''sprite : sprite_id EQUAL sprite_type sprite_attrs'''
    global variables, gameAttrs, type, spriteId
    # Save sprite in variables
    variables[spriteId] = {"type": convertAtomicTypeToCode(type), "attrs": gameAttrs}
    gameAttrs = {}

def p_sprite_id(p):
    '''sprite_id : ID'''
    global spriteId
    spriteId = p[1]
    # Check if the sprite id was not declared twice
    if (variables.has_key(spriteId)):
        raise SemanticError("Repeated identifier for sprite: " + spriteId)

def p_sprite_type(p):
    '''sprite_type : IMMOVABLE
                   | MOVINGAVATAR
                   | SHOOTINGAVATAR
                   | MISSILE
                   | SPAWNER
                   | PASSIVE'''
    global type
    # Set sprite type
    type = p[1]

def p_sprite_attrs(p):
    '''sprite_attrs : sprite_attr more_sprite_attrs
                    | '''

def p_more_sprite_attrs(p):
    '''more_sprite_attrs : D_C sprite_attr more_sprite_attrs
                        | '''

def p_sprite_attr(p):
    '''sprite_attr : IMG EQUAL STRING_CT
                   | GENERATEDSPRITE EQUAL ID
                   | SPEED EQUAL FLOAT_CT
                   | PORTAL EQUAL BOOLEAN_CT
                   | SHRINKFACTOR EQUAL FLOAT_CT
                   | LIMIT EQUAL INT_CT
                   | PROB EQUAL FLOAT_CT
                   | COOLDOWN EQUAL INT_CT
                   | COLOR EQUAL COLOR_CT
                   | HEALTHPOINTS EQUAL INT_CT
                   | LIMITHEALTHPOINTS EQUAL INT_CT
                   | WEAPONSPRITE EQUAL ID
                   | ORIENTATION EQUAL MOVEMENT_CT'''
    global variables, gameAttrs, listCode, spriteId
    # Save sprite attrs
    if (p[1] == "generatedSprite" or p[1] == "weaponSprite"):
        # Check if the sprite id was declared before
        if (not variables.has_key(p[3])):
            raise SemanticError("Use of undeclared sprite id: " + p[3])
    if (p[1] == "img"):
        gameAttrs[p[1]] = p[3].replace('"', '')
    else:
        gameAttrs[p[1]] = p[3]
    # Generate quadruplet that assigns attributes to sprites
    listCode.append([convertOperatorToCode('.='), convertAtomicTypeToCode(p[1]), p[3], spriteId])

def p_interactions(p):
    '''interactions : INTERACTIONLIST D_2P interaction D_PYC more_interactions SMALL_END'''
    global gameSections, gameActions
    # Add the interaction section to the game dictionary
    gameSections[p[1]] = gameActions
    gameActions = []

def p_more_interactions(p):
    '''more_interactions : interaction D_PYC more_interactions
                         | '''

def p_interaction(p):
    '''interaction : ID more_spritesid ENCOUNTERS ID EQUAL action more_actions'''
    global gameSections, listSprites, gameAttrs, gameActions
    sprites = gameSections["SpriteSet"]
    # Check if the sprite ids were declared before
    if (not sprites.has_key(p[1])):
        raise SemanticError("Use of undeclared sprite id: " + p[1])
    if (not sprites.has_key(p[4])):
        raise SemanticError("Use of undeclared sprite id: " + p[4])
    listSprites.append(p[1])
    listSprites.append(p[4])
    # gameAttrs contain the special actions of some functions
    # listSprites is used as a key in the dictionary (the last is the one that encounters)
    gameActions.append({tuple(listSprites): gameAttrs})
    listSprites = []
    gameAttrs = {}

def p_more_spritesid(p):
    '''more_spritesid : D_C ID more_spritesid
                      | '''
    global gameSections, listSprites
    sprites = gameSections["SpriteSet"]
    try:
        # Check if the sprite exists (this rule is used in mapping)
        if (not sprites.has_key(p[2])):
            raise SemanticError("Use of undeclared sprite id: " + p[2])
        listSprites.append(p[2])
    except IndexError:
        return

def p_more_actions(p):
    '''more_actions : D_C action more_actions
                    | '''

def p_action(p):
    '''action : KILLSPRITE D_PA kill_id D_PC
              | STEPBACK
              | SCORECHANGE D_PA FLOAT_CT D_PC
              | TRANSFORMTO D_PA ID D_PC
              | BOUNCEFORWARD
              | CHANGEHEALTHPOINTS D_PA INT_CT D_PC
              | ADDTIMER TIME EQUAL INT_CT TRANSFORMALL D_PA ID D_C ID D_PC
              | SHIELDFROM D_PA KILLSPRITE D_C ID D_PC
              | PULLWITHIT'''
    global gameSections, listSprites, gameAttrs, killSprites
    sprites = gameSections["SpriteSet"]
    # Check the different actions
    if (p[1] == "killSprite"):
        gameAttrs[p[1]] = killSprites
        killSprites = []
    elif (p[1] == "stepBack" or p[1] == "pullWithIt" or p[1] == "bounceForward"):
        gameAttrs[p[1]] = {}
    elif (p[1] == "transformTo"):
        # Check if the sprite id was declared before
        if (not sprites.has_key(p[3])):
            raise SemanticError("Use of undeclared sprite id: " + p[3])
        gameAttrs[p[1]] = p[3]
    elif (p[1] == "addTimer"):
        # Check if both sprite ids were declared before
        if (not sprites.has_key(p[7])):
            raise SemanticError("Use of undeclared sprite id: " + p[7])
        if (not sprites.has_key(p[9])):
            raise SemanticError("Use of undeclared sprite id: " + p[9])
        gameAttrs[p[1]] = {p[2]: p[4], "from": p[7], "to": p[9]}
    elif (p[1] == "shieldFrom"):
        # Check if the sprite id was declared before
        if (not sprites.has_key(p[5])):
            raise SemanticError("Use of undeclared sprite id: " + p[5])
        gameAttrs[p[1]] = p[5]
    else:
        gameAttrs[p[1]] = p[3]

def p_kill_id(p):
    '''kill_id : ID
               | '''
    global gameSections, killSprites
    sprites = gameSections["SpriteSet"]
    try:
        # Check if the sprite id exists and append it to the killSprites if it does
        if (not sprites.has_key(p[1])):
            raise SemanticError("Use of undeclared sprite id: " + p[1])
        killSprites.append(p[1])
    except IndexError:
        return

def p_goals(p):
    '''goals : TERMINATIONGOALS D_2P goal D_PYC more_goals SMALL_END'''
    global gameSections, variables
    # Add the goal section to the game dictionary
    gameSections[p[1]] = variables
    variables = {}

def p_more_goals(p):
    '''more_goals : goal D_PYC
                  | '''

def p_goal(p):
    '''goal : goal_type LIMIT EQUAL INT_CT WIN EQUAL BOOLEAN_CT'''
    global variables, gameAttrs, type, listSprites
    # gameAttrs contains limit and win condition
    gameAttrs = {p[2]: p[4], p[5]: p[7]}
    # variables has the type of goal and game Attrs
    variables[tuple(listSprites)] = {"type": type, "attrs": gameAttrs}
    listSprites = []
    gameAttrs = {}

def p_goal_type(p):
    '''goal_type : SPRITECOUNTER SPRITE EQUAL ID
                 | MULTISPRITECOUNTER sprite_list
                 | TIMEOUT'''
    global gameSections, listSprites, type
    sprites = gameSections["SpriteSet"]
    # Save the type of goal
    type = p[1]
    if (type == "spriteCounter"):
        # Check if the sprite id was declared before
        if (not sprites.has_key(p[4])):
            raise SemanticError("Use of undeclared sprite id: " + p[4])
        listSprites.append(p[4])

def p_sprite_list(p):
    '''sprite_list : SPRITE EQUAL ID more_sprite_list'''
    global gameSections, listSprites
    sprites = gameSections["SpriteSet"]
    # Check if the sprite id exists and if it does, append it to the list of sprites
    if (not sprites.has_key(p[3])):
        raise SemanticError("Use of undeclared sprite id: " + p[3])
    listSprites.append(p[2])
    return

def p_more_sprite_list(p):
    '''more_sprite_list : D_C sprite_list
                        | '''

def p_mapping(p):
    '''mapping : MAPPING D_2P mapping_rule D_PYC more_mapping_rules SMALL_END'''
    global gameSections, variables
    # Add the mapping to the game dictionary
    gameSections[p[1]] = variables
    variables = {}

def p_more_mapping_rules(p):
    '''more_mapping_rules : mapping_rule D_PYC more_mapping_rules
                          | '''

def p_mapping_rule(p):
    '''mapping_rule : CHAR_CT EQUAL ID more_spritesid'''
    global gameSections, listSprites, variables, listCode
    sprites = gameSections["SpriteSet"]
    # Check all possible cases to conclude there is not semantic error
    if (not sprites.has_key(p[3])):
        raise SemanticError("Use of undeclared sprite id: " + p[3])
    if (p[1] in variables.values()):
        raise SemanticError("Repeated char for mapping: " + p[1])
    if (p[1] == "'\"'"):
        raise SemanticError("Forbidden char for mapping: " + '"')
    # Append the sprite id to the beginning
    listSprites = [p[3]] + listSprites
    variables[p[1].replace("'", "")] = list(listSprites)
    # For each sprite, generate the quadruplet to map the char to the sprite
    for sprite in listSprites:
        listCode.append([convertOperatorToCode('mapSprite'), p[1].replace("'", ""), -1, sprite])
    listSprites = []

def p_map(p):
    '''map : MAP D_2P STRING_CT D_PYC more_tiles SMALL_END'''
    global gameSections, listSprites
    mapping = gameSections["Mapping"]
    # For every char in the string, check if there is a declared char mapping
    for mapping_id in p[3]:
        if ((not mapping.has_key(mapping_id)) and mapping_id != '"'):
            raise SemanticError("Use of undeclared char for mapping: " + mapping_id)
    listSprites = [p[3].replace('"', '')] + listSprites
    # Add the map to the game dictionary
    gameSections[p[1]] = list(listSprites)
    while len(listSprites) > 0:
        listCode.append([convertOperatorToCode('addRowMap'), -1, -1, listSprites.pop(0)])

def p_more_tiles(p):
    '''more_tiles : STRING_CT D_PYC more_tiles
                  | '''
    global listSprites, gameSections, listCode
    mapping = gameSections["Mapping"]
    try:
        # For every char in the string, check if there is a declared char mapping
        for mapping_id in p[1]:
            if ((not mapping.has_key(mapping_id)) and mapping_id != '"'):
                raise SemanticError("Use of undeclared char for mapping: " + mapping_id)
        listSprites = [p[1].replace('"', '')] + listSprites
    except IndexError:
        return

def p_block(p):
    '''block : vars save_vars_in_global_memory functions main_block'''
    global globalVariables
    globalVariables = {}

# Helper function in sintaxis for semantic and compilation (virtual memory)
def p_save_vars_in_global_memory(p):
    '''save_vars_in_global_memory : '''
    global functionDirectory, globalVariables, variables, avail

    # Assign virtual memory to variables in global scope
    for key in variables.keys():
        typeInNumber = variables[key]['type']
        if (not variables[key].has_key('dimension')):
            variables[key]["memory"] = avail[0][typeInNumber]
            avail[0][typeInNumber] += 1
        else:
            # Virtual memory for a list
            variables[key]["memory"] = avail[0][typeInNumber]
            avail[0][typeInNumber] += variables[key]['dimension']['superior']

    # Save global variables with its attributes.
    globalVariables = variables
    variables = {}
    functionDirectory["global"] = globalVariables

def p_vars(p):
    '''vars : var D_PYC vars
            | '''

def p_var(p):
    '''var : VAR type D_2P ID
           | VAR type D_CA INT_CT D_CC D_2P ID'''
    global variables, type, functionDirectory
    # Get var attributes and save it.
    if (debug):
        print functionDirectory
    # var is a list
    if (p[3] != ':'):
        if (variables.has_key(p[7])):
            raise SemanticError("Repeated identifier for variable: " + p[7])
        if (functionDirectory.has_key("variables")):
            if (functionDirectory["variables"].has_value(p[7])):
                raise SemanticError("Var identifier has the same name as a function: " + p[7])
        # Save dimensional var
        variables[p[7]] = {"type": convertAtomicTypeToCode(type), "dimension": {"inferior": 0, "superior": int(p[4]), "-K": 0}}
    # var is not a list
    else:
        if (variables.has_key(p[4])):
            raise SemanticError("Repeated identifier for variable: " + p[4])
        if (functionDirectory.has_key("variables")):
            if (functionDirectory["variables"].has_value(p[4])):
                raise SemanticError("Var identifier has the same name as a function: " + p[4])
        typeInNumber = convertAtomicTypeToCode(type)
        # Save var
        variables[p[4]] = {"type": typeInNumber}

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING
            | CHAR
            | BOOLEAN'''
    global type
    # Save the type of variable
    type = p[1]

def p_functions(p):
    '''functions : function functions
                 | '''

def p_save_function(p):
    '''save_function : '''
    global functionDirectory, variables, parameters, functionId, type, avail, listCode
    # Save the function with its attributes and variables
    if (debug):
        print "#############", variables
    if (functionDirectory.has_key(functionId)):
        raise SemanticError("Repeated identifier for function: " + p[2])
    functionDirectory[functionId] = {"variables": variables, "parameters": parameters, "return": convertAtomicTypeToCode(type), "memory": avail[0][convertAtomicTypeToCode(type)], "start_quadruplet": len(listCode) + 1}
    avail[0][convertAtomicTypeToCode(type)] += 1
    variables = {}
    parameters = []

def p_function(p):
    '''function : FUNC save_function_id D_PA parameters D_PC EQUAL type save_function D_2P code_block SMALL_END generate_end_func'''

def p_generate_end_func(p):
    '''generate_end_func : '''
    global listCode, temporalStamp, functionDirectory, functionId, avail, variables
    # Save variables used in function (for debugging)
    functionDirectory[functionId]['variables'] = variables
    variables = {}
    # Generate endFunc quadruplet
    listCode.append([convertOperatorToCode('endFunc'),-1,-1,-1])
    temporalAuxDictionary = {}
    if (debug):
        print temporalStamp
    # Check how many temporals were used.
    for key in avail[2]:
        temporalAuxDictionary[key] = avail[2][key] - temporalStamp[key]
    # Save the number of temporals used inside the function
    functionDirectory[functionId]["temporals"] = temporalAuxDictionary

def p_save_function_id(p):
    '''save_function_id : ID'''
    global functionId, temporalStamp, avail
    functionId = p[1]
    # Reset the virtual memory counters because it is the start of a new module.
    avail[1] = {101: 7000, 102: 8000, 103: 9000, 104: 10000, 105: 11000}
    avail[2] = {101: 12000, 102: 13000, 103: 14000, 104: 15000, 105: 16000}
    temporalStamp = avail[2].copy()

def p_parameters(p):
    '''parameters : parameter more_parameters
                  | '''

def p_parameter(p):
    '''parameter : type D_2P type_parameter'''

def p_type_parameter(p):
    '''type_parameter : D_AMP ID
                      | ID'''
    global variables, type, parameters, avail, functionDirectory
    # Get parameter attributes and save it.
    if (debug):
        print "####################", functionDirectory
    # Parameter by reference
    if (p[1] == '&'):
        if (variables.has_key(p[2])):
            raise SemanticError("Repeated identifier for variable: " + p[2])
        variables[p[2]] = {"type": convertAtomicTypeToCode(type), "reference_parameter": True, "memory": avail[1][convertAtomicTypeToCode(type)]}
        parameters.append(convertAtomicTypeToCode(type))
    # Normal parameter
    else:
        if (variables.has_key(p[1])):
            raise SemanticError("Repeated identifier for variable: " + p[1])
        variables[p[1]] = {"type": convertAtomicTypeToCode(type), "reference_parameter": False, "memory": avail[1][convertAtomicTypeToCode(type)]}
        parameters.append(convertAtomicTypeToCode(type))
    avail[1][convertAtomicTypeToCode(type)] += 1

def p_more_parameters(p):
    '''more_parameters : D_C parameter more_parameters
                       | '''

def p_main_block(p):
    '''main_block : MAIN set_function_id_main D_2P code_block SMALL_END'''
    global functionDirectory, variables, avail
    if (functionDirectory.has_key(p[1])):
        raise SemanticError("Repeated identifier for function: " + p[1])
    # Save the variables used in main
    functionDirectory["main"]["variables"] = variables
    variables = {}

def p_set_function_id_main(p):
    '''set_function_id_main : '''
    global functionDirectory, functionId, listCode, stackJumps, avail
    # Set the functionId scope
    functionId = "main"
    functionDirectory[functionId] = {"variables" : {}}
    # Set that the initial goto need to jump here.
    firstJump = stackJumps.pop()
    listCode[firstJump - 1][3] = len(listCode) + 1
    # Reset avail because it is a new module.
    avail[1] = {101: 7000, 102: 8000, 103: 9000, 104: 10000, 105: 11000}
    avail[2] = {101: 12000, 102: 13000, 103: 14000, 104: 15000, 105: 16000}

def p_code_block(p):
    '''code_block : vars save_vars_in_local_memory mini_block'''

# Helper function in sintaxis for semantic and compilation (virtual memory)
def p_save_vars_in_local_memory(p):
    '''save_vars_in_local_memory : '''
    global variables, avail
    # Assign virtual memory to variables in local scope
    for key in variables.keys():
        typeInNumber = variables[key]['type']
        if (not variables[key].has_key('dimension')):
            variables[key]["memory"] = avail[1][typeInNumber]
            avail[1][typeInNumber] += 1
        else:
        # Virtual memory for a list
            variables[key]["memory"] = avail[1][typeInNumber]
            avail[1][typeInNumber] += variables[key]['dimension']['superior']

def p_statute(p):
    '''statute : assignation check_stack_equal
               | condition
               | printing
               | reading
               | cycle
               | function_use
               | return'''

# Helper function in sintaxis for semantic (operators)
def p_check_stack_equal(p):
    '''check_stack_equal : '''
    global stackOperators, stackTypes, stackOp, listCode, semanticCube
    if (debug):
        print stackOp
    if (stackOperators):
        if (stackOperators[-1] == '='):
            # Different way to generate quadruplet arithmetic != assignation
            operator = convertOperatorToCode(stackOperators.pop())
            op2 = stackOp.pop()
            op1 = stackOp.pop()
            op2Type = stackTypes.pop()
            op1Type = stackTypes.pop()
            if (debug):
                print op1Type, op2Type
            newType = semanticCube[op1Type-100][op2Type-100][operator]
            if (newType == -1):
                raise SemanticError("Type Mismatch: Trying to assign " + str(op2Type) + " to a " + str(op1Type) + " var!")
            if (op1 >= 14000 and not isinstance(op1, list)):
                raise SemanticError("Trying to assign value to a temporal or constant " + str(op1));
            listCode.append([operator, op2, -1, op1])

def p_function_use(p):
    '''function_use : validate_function_id_do_era push_pa add_parameter more_ids pop_pc validate_params_generate_gosub
                    | STARTGAME D_PA D_PC
                    | validate_function_id_do_era D_PA D_PC validate_params_generate_gosub'''
    global listCode
    # Special quadruplet operation when it is a game.
    if (p[1] == 'StartGame'):
        listCode.append([convertOperatorToCode('startGame'), -1, -1, -1])

def p_validate_function_id_do_era(p):
    '''validate_function_id_do_era : ID'''
    global listCode, functionDirectory, parameters, paramCounter, goSubFunction, stackOp, stackTypes, functionId
    if (not functionDirectory.has_key(p[1])):
        raise SemanticError("Use of undeclared function identifier: " + p[1])
    # Do ERA
    listCode.append([convertOperatorToCode('era'), -1, -1, p[1]])
    # Check parameters of this function and set helper variables for param and gosub operations
    parameters = functionDirectory[p[1]]["parameters"]
    paramCounter = 0
    goSubFunction = p[1]

def p_add_parameter(p):
    '''add_parameter : expression'''
    global stackOp, stackTypes, parameters, paramCounter, listCode
    paramType = stackTypes.pop()
    operand = stackOp.pop()
    try:
        if (parameters[paramCounter] != paramType):
            raise SemanticError("Diferent type of parameter in function. Expected: " + parameters[paramCounter] + " received: " + paramType)
    except IndexError:
        raise SemanticError("Use of more parameters than function declaration.")
    # If it was a valid param, generate quadruplet
    paramCounter += 1
    listCode.append([convertOperatorToCode('param'), operand, -1, paramCounter])

def p_validate_params_generate_gosub(p):
    '''validate_params_generate_gosub : '''
    global functionDirectory, listCode, goSubFunction, parameters, paramCounter, functionId, avail, stackOp, stackTypes
    # Check that there was the exact number of params tha function requires
    if (paramCounter != len(parameters)):
        raise SemanticError("Use of less parameters than expected in function declaration.")
    # Generate gosub quadruplet
    listCode.append([convertOperatorToCode('gosub'), -1, -1, goSubFunction])
    # Guadalupana patch
    listCode.append([convertOperatorToCode('='), functionDirectory[goSubFunction]['memory'], -1, avail[2][functionDirectory[goSubFunction]['return']]])
    stackOp.append(avail[2][functionDirectory[goSubFunction]['return']])
    stackTypes.append(functionDirectory[goSubFunction]['return'])
    avail[2][functionDirectory[goSubFunction]['return']] += 1
    # Reset variables
    goSubFunction = ""
    parameters = []
    paramCounter = 0

def p_more_ids(p):
    '''more_ids : D_C add_parameter more_ids
                | '''

def p_assignation(p):
    '''assignation : received_id value_list push_equal expression'''

# Helper function in sintaxis for semantic (operators)
def p_push_equal(p):
    '''push_equal : EQUAL'''
    global stackOperators
    stackOperators.append(p[1])

def p_value_list(p):
    '''value_list : check_dimension D_CA expression D_CC
                  | '''
    global variables, sureListId, stackOp, stackTypes, listCode, avail, constants, listScope
    try:
        # Check if the id has dimension
        if (p[2] == '['):
            if (debug):
                print "LIST: stack of operands: ", stackOp
            # The id has dimension
            operand = stackOp.pop()
            operandType = stackTypes.pop()
            # Check it was an int value the one at the top of the stack
            if (operandType != convertAtomicTypeToCode('int')):
                raise SemanticError("Expected int value to acess list, recieved: ", operandType)
            # Generate verify quadruplet
            if (listScope == 'local'):
                listCode.append([convertOperatorToCode('verify'), operand, variables[sureListId]['dimension']['inferior'], variables[sureListId]['dimension']['superior']])
                
                # Patch for constants, save the value before useing it so it can be a virtual
                # memory direction
                constant = variables[sureListId]['memory']
                type = variables[sureListId]['type']
            else: # Is in the global scope
                listCode.append([convertOperatorToCode('verify'), operand, functionDirectory['global'][sureListId]['dimension']['inferior'], functionDirectory['global'][sureListId]['dimension']['superior']])
                
                # Patch for constants, save the value before useing it so it can be a virtual
                # memory direction
                constant = functionDirectory['global'][sureListId]['memory']
                type = functionDirectory['global'][sureListId]['type']
            if (not constants.has_key(constant)):
                constants[constant] = {"type": 101, "memory": avail[3][convertAtomicTypeToCode('int')]}
                avail[3][convertAtomicTypeToCode('int')] += 1
  
          # Add virtual memory value to the direction used for list
            listCode.append([convertOperatorToCode('+'), operand, constants[constant]['memory'], avail[2][convertAtomicTypeToCode('int')]])
            stackOp.append(-avail[2][convertAtomicTypeToCode('int')])
            stackTypes.append(type)
            avail[2][convertAtomicTypeToCode('int')] += 1
    except IndexError:
        return

def p_check_dimension(p):
    '''check_dimension : '''
    global listId, sureListId, stackOp, stackTypes, listScope
    try:
        if (not variables[listId].has_key('dimension')):
            raise SemanticError("Trying to access an id that does not have dimension.")
        listScope = 'local'
    except KeyError:
        if (not functionDirectory['global'][listId].has_key('dimension')):
            raise SemanticError("Trying to access an id that does not have dimension.")
        listScope = 'global'
    # You are now sure the id is a list
    stackOp.pop()
    stackTypes.pop()
    sureListId = listId

def p_printing(p):
    '''printing : PRINT D_PA printable D_PC'''

def p_printable(p):
    '''printable : expression generate_print more_printable'''

def p_generate_print(p):
    '''generate_print : '''
    global stackOp, stackTypes, stackOpVisible, listCode
    expression = stackOp.pop()
    stackTypes.pop()
    stackOpVisible.pop()
    listCode.append([convertOperatorToCode("print"), -1, -1, expression])

def p_more_printable(p):
    '''more_printable : D_C printable
                      | '''

def p_condition(p):
    '''condition : IF D_PA expression D_PC generate_gotoF_if D_2P mini_block else_condition SMALL_END generate_end_if'''

def p_generate_gotoF_if(p):
    '''generate_gotoF_if : '''
    global stackOp, stackTypes, stackOperators, stackOpVisible, stackJumps, listCode
    condtionType = stackTypes.pop()
    if (condtionType != convertAtomicTypeToCode("boolean")):
        raise SemanticError("Expected boolean in if condition. Received: " + str(condtionType))
    condition = stackOp.pop()
    stackOpVisible.pop()
    listCode.append([convertOperatorToCode("gotoF"), condition, -1, 'pending'])
    stackJumps.append(len(listCode) - 1) # Make it as a list that starts in 0.

def p_generate_end_if(p):
    '''generate_end_if : '''
    global stackJumps, listCode
    endJump = stackJumps.pop()
    listCode[endJump][3] = len(listCode) + 1 # Because it needs to point to the next one

def p_else_condition(p):
    '''else_condition : ELSE generate_goto_else D_2P mini_block
                      |'''

def p_generate_goto_else(p):
    '''generate_goto_else : '''
    global stackJumps, listCode
    listCode.append([convertOperatorToCode("goto"),'-1','-1','pending'])
    falseJump = stackJumps.pop()
    listCode[falseJump][3] = len(listCode) + 1
    stackJumps.append(len(listCode) - 1)

def p_reading(p):
    '''reading : GETVALUE D_PA received_id D_PC generate_read_value
               | GETLINE D_PA received_id D_PC generate_read_line
               | GETBOOLEAN D_PA received_id D_PC generate_read_boolean
               | GETCHAR D_PA received_id D_PC generate_read_char'''

# Helper functions in sintaxis for semantic (intermediate code generators)
def p_generate_read_value(p):
    '''generate_read_value : '''
    global stackOp, stackTypes, stackOpVisible, listCode
    typeOfVariable = stackTypes.pop()
    if (not (typeOfVariable == convertAtomicTypeToCode('int') or typeOfVariable == convertAtomicTypeToCode('float'))):
        raise SemanticError("Type mismatch: Trying to read an int or float and assign it to a variable type: " + str(typeOfVariable))
    variable = stackOp.pop()
    stackOpVisible.pop()
    listCode.append([convertOperatorToCode("getValue"), -1, -1, variable])

def p_generate_read_line(p):
    '''generate_read_line : '''
    global stackOp, stackTypes, stackOpVisible, listCode
    typeOfVariable = stackTypes.pop()
    if (not (typeOfVariable == convertOperatorToCode('string') or typeOfVariable == convertAtomicTypeToCode('char'))):
        raise SemanticError("Type mismatch: Trying to read a string or char and assign it to a variable type: " + str(typeOfVariable))
    variable = stackOp.pop()
    stackOpVisible.pop()
    listCode.append([convertOperatorToCode("getLine"), -1, -1, variable])

def p_generate_read_boolean(p):
    '''generate_read_boolean : '''
    global stackOp, stackTypes, stackOpVisible, listCode
    typeOfVariable = stackTypes.pop()
    if (not (typeOfVariable == convertAtomicTypeToCode('boolean'))):
        raise SemanticError("Type mismatch: Trying to read a boolean and assign it to a variable type: " + str(typeOfVariable))
    variable = stackOp.pop()
    stackOpVisible.pop()
    listCode.append([convertOperatorToCode("getBoolean"), -1, -1, variable])

def p_generate_read_char(p):
    '''generate_read_char : '''
    global stackOp, stackTypes, stackOpVisible, listCode
    typeOfVariable = stackTypes.pop()
    if (not (typeOfVariable == convertAtomicTypeToCode('char'))):
        raise SemanticError("Type mismatch: Trying to read a char and assign it to a variable type: " + str(typeOfVariable))
    variable = stackOp.pop()
    stackOpVisible.pop()
    listCode.append([convertOperatorToCode("getChar"), -1, -1, variable])

def p_cycle(p):
    '''cycle : WHILE push_cont_in_stackJumps D_PA expression D_PC generate_gotoF_while D_2P mini_block SMALL_END generate_end_while'''

def p_push_cont_in_stackJumps(p):
    '''push_cont_in_stackJumps : '''
    global stackJumps, listCode
    stackJumps.append(len(listCode) + 1)

def p_generate_gotoF_while(p):
    '''generate_gotoF_while : '''
    global stackOp, stackTypes, stackOpVisible, stackJumps, listCode
    condtionType = stackTypes.pop()
    if (condtionType != convertAtomicTypeToCode("boolean")):
        raise SemanticError("Expected boolean in if condition. Received: " + str(condtionType))
    condition = stackOp.pop()
    stackOpVisible.pop()
    listCode.append([convertOperatorToCode("gotoF"), condition, -1, 'pending'])
    stackJumps.append(len(listCode) - 1) # Make it as a list that starts in 0.

def p_generate_end_while(p):
    '''generate_end_while : '''
    global stackJumps, listCode
    falseJump = stackJumps.pop()
    returnJump = stackJumps.pop()
    listCode.append([convertOperatorToCode("goto"), -1, -1, returnJump])
    listCode[falseJump][3] = len(listCode) + 1

def p_return(p):
    '''return : RETURN expression'''
    global listCode, functionDirectory, functionId, stackOp, stackTypes
    if (functionId == 'main'):
        raise SemanticError("Trying to return something inside Main.")
    op = stackOp.pop()
    opType = stackTypes.pop()
    # Check if the return type of the function matches the one in the stack
    if (opType != functionDirectory[functionId]['return']):
        raise SemanticError("Returning a value of type: " + opType + ", expected: " + functionDirectory[functionId]['return'])
    listCode.append([convertOperatorToCode('return'), -1, -1, op])

def p_mini_block(p):
    '''mini_block : statute D_PYC mini_block
                  | '''

def p_expression(p):
    '''expression : big_exp or_exp check_stack_or'''

# Helper function in sintaxis for semantic (operators)
def p_check_stack_or(p):
    '''check_stack_or : '''
    global stackOperators
    if (stackOperators):
        if (stackOperators[-1] == '||'):
            generateArithmeticCode()

def p_or_exp(p):
    '''or_exp : OR expression
              | '''
    global stackOperators
    try:
        # Add operator to the stack
        if (p[1] == '||'):
            stackOperators.append(p[1])
    except IndexError:
        return

def p_big_exp(p):
    '''big_exp : medium_exp and_exp check_stack_and'''

# Helper function in sintaxis for semantic (operators)
def p_check_stack_and(p):
    '''check_stack_and : '''
    global stackOperators
    if (stackOperators):
        if (stackOperators[-1] == '&&'):
            generateArithmeticCode()

def p_and_exp(p):
    '''and_exp : AND big_exp
               | '''
    global stackOperators
    try:
        # Add operator to the stack
        if (p[1] == '&&'):
            stackOperators.append(p[1])
    except IndexError:
        return

def p_medium_exp(p):
    '''medium_exp : exp relational_exp check_stack_mmdi '''

# Helper function in sintaxis for semantic (operators)
def p_check_stack_mmdi(p):
    '''check_stack_mmdi : '''
    global stackOperators
    if (stackOperators):
        if (stackOperators[-1] == '>' or stackOperators[-1] == '<' or stackOperators[-1] == '!=' or stackOperators[-1] == '=='):
            generateArithmeticCode()

def p_relational_exp(p):
    '''relational_exp : MAYOR_QUE exp
                      | MENOR_QUE exp
                      | DIFERENTE_DE exp
                      | IGUAL_QUE exp
                      | '''
    global stackOperators
    try:
        # Add operator to the stack
        if (p[1] == '>' or p[1] == '<' or p[1] == '!=' or p[1] == '=='):
            stackOperators.append(p[1])
    except IndexError:
        return

def p_exp(p):
    '''exp : term check_stack_pm add_term'''

# Helper function in sintaxis for semantic (operators)
def p_check_stack_pm(p):
    '''check_stack_pm : '''
    global stackOperators
    if (stackOperators):
        if (stackOperators[-1] == '+' or stackOperators[-1] == '-'):
            generateArithmeticCode()

def p_add_term(p):
    '''add_term : push_pm exp
                | '''

# Helper function in sintaxis for semantic (operators)
def p_push_pm(p):
    '''push_pm : PLUS
               | MINUS'''
    global stackOperators
    stackOperators.append(p[1])

def p_term(p):
    '''term : factor check_stack_td times_factor'''

# Helper function in sintaxis for semantic (operators)
def p_check_stack_td(p):
    '''check_stack_td : '''
    global stackOperators
    if (stackOperators):
        if (stackOperators[-1] == '*' or stackOperators[-1] == '/'):
            generateArithmeticCode()

def p_times_factor(p):
    '''times_factor : push_td term
                    | '''

# Helper function in sintaxis for semantic (operators)
def p_push_td(p):
    '''push_td : TIMES
               | DIVISION'''
    global stackOperators
    stackOperators.append(p[1])

def p_factor(p):
    '''factor : push_pa expression pop_pc
              | var_ct'''

# Helper function in sintaxis for semantic (operators)
def p_push_pa(p):
    '''push_pa : D_PA'''
    global stackOperators
    stackOperators.append(p[1])

# Helper function in sintaxis for semantic (operators)
def p_pop_pc(p):
    '''pop_pc : D_PC'''
    global stackOperators
    stackOperators.pop()

def p_var_ct(p):
    '''var_ct : received_id value_list
              | received_float
              | received_int
              | received_boolean
              | received_string
              | received_char
              | function_use'''

# Helper functions of var_ct for semantic analysis (operands)
# id checks if the id was declared, if not, there is an error.
def p_received_id(p):
    '''received_id : ID'''
    global stackTypes, stackOp, variables, globalVariables, stackOpVisible, functionDirectory, functionId, listId
    listId = p[1]
    if (debug):
        print variables, functionDirectory, p[1], functionId
    # Check if it was a global id
    if (not variables.has_key(p[1]) and not functionDirectory[functionId]["variables"].has_key(p[1])):
        if (not globalVariables.has_key(p[1])):
            raise SemanticError("Use of undeclared identifier for variable: " + p[1])
        else:
            stackOp.append(globalVariables[p[1]]["memory"])
            stackOpVisible.append(p[1])
            stackTypes.append(globalVariables[p[1]]["type"])
    # It is a local id
    else:
        # In main
        if (variables.has_key(p[1])):
            stackOp.append(variables[p[1]]["memory"])
            stackOpVisible.append(p[1])
            stackTypes.append(variables[p[1]]["type"])
        # Inside a function module
        else:
            stackOp.append(functionDirectory[functionId]["variables"][p[1]]["memory"])
            stackOpVisible.append(p[1])
            stackTypes.append(functionDirectory[functionId]["variables"][p[1]]["type"])

# the rest of the variables check if they exists in virtual memory, if not, add them.
def p_received_float(p):
    '''received_float : FLOAT_CT
                      | MINUS FLOAT_CT'''
    global constants, avail, stackOp, stackTypes, stackOpVisible
    # Check if it is a negative value
    if (p[1] == '-'):
        value = - float(p[2])
    else:
        value = float(p[1])
    if (not constants.has_key(value)):
        constants[value] = {"type": 102, "memory": avail[3][102]}
        avail[3][102] += 1
    stackOp.append(constants[value]["memory"])
    stackOpVisible.append(value)
    stackTypes.append(constants[value]["type"])

def p_received_int(p):
    '''received_int : INT_CT
                    | MINUS INT_CT'''
    global constants, avail, stackOp, stackTypes, stackOpVisible
    # Check if it is a negative value
    if (p[1] == '-'):
        value = - int(p[2])
    else:
        value = int(p[1])
    if (not constants.has_key(value)):
        constants[value] = {"type": 101, "memory": avail[3][101]}
        avail[3][101] += 1
    stackOp.append(constants[value]["memory"])
    stackOpVisible.append(value)
    stackTypes.append(constants[value]["type"])

def p_received_boolean(p):
    '''received_boolean : BOOLEAN_CT'''
    global constants, avail, stackOp, stackTypes, stackOpVisible
    if (not constants.has_key(p[1])):
        constants[p[1]] = {"type": 105, "memory": avail[3][105]}
        avail[3][105] += 1
    stackOp.append(constants[p[1]]["memory"])
    stackOpVisible.append(p[1])
    stackTypes.append(constants[p[1]]["type"])

def p_received_string(p):
    '''received_string : STRING_CT'''
    global constants, avail, stackOp, stackTypes, stackOpVisible
    if (not constants.has_key(p[1])):
        constants[p[1]] = {"type": 103, "memory": avail[3][103]}
        avail[3][103] += 1
    stackOp.append(constants[p[1]]["memory"])
    stackOpVisible.append(p[1])
    stackTypes.append(constants[p[1]]["type"])

def p_received_char(p):
    '''received_char : CHAR_CT'''
    global constants, avail, stackOp, stackTypes, stackOpVisible
    if (not constants.has_key(p[1])):
        constants[p[1]] = {"type": 104, "memory": avail[3][104]}
        avail[3][104] += 1
    stackOp.append(constants[p[1]]["memory"])
    stackOpVisible.append(p[1])
    stackTypes.append(constants[p[1]]["type"])

def p_error(p):
    if p:
        raise SyntaxError("Syntax error at '%s'" % p.value)
    if not p:
        print("EOF")

# Helper function used to generate the code used for arithmetic, logic and relational operations
def generateArithmeticCode():
    global stackOperators, stackTypes, stackOp, avail, listCode, stackOpVisible
    if (debug):
        print "stack of operators: ", stackOperators
        print "stack of operands: ", stackOpVisible
        print "stack of operands: ", stackOp
        print "stack of types: ", stackTypes
    
    # Get all the variables to test and generate a quadruplet
    operator = convertOperatorToCode(stackOperators.pop())
    op2 = stackOp.pop()
    op1 = stackOp.pop()
    stackOpVisible.pop()
    stackOpVisible.pop()
    op2Type = stackTypes.pop()
    op1Type = stackTypes.pop()
    if (debug):
        print op1Type, op2Type
    newType = semanticCube[op1Type-100][op2Type-100][operator]
    # If the semantic cube tell us that the operation is not possible
    if (newType == -1):
        raise SemanticError("Type Mismatch: Trying to " + str(operator) + " = " + str(op1Type) + " :: " + str(op2Type))
    result = avail[2][newType]
    avail[2][newType] += 1
    # Generate the quadruplet, append result to the stacks
    listCode.append([operator, op1, op2, result])
    stackOp.append(result)
    stackOpVisible.append(result)
    stackTypes.append(newType)

# Helper function in game intermediate code, to simulate condition statutes like if and while.
def doGotoF():
    global listCode, stackTypes, stackOp, stackOpVisible
    condtionType = stackTypes.pop()
    if (condtionType != convertAtomicTypeToCode("boolean")):
        raise SemanticError("Expected boolean in game condition. Received: " + str(condtionType))
    condition = stackOp.pop()
    stackOpVisible.pop()
    listCode.append([convertOperatorToCode("gotoF"), condition, -1, 'pending'])
    stackJumps.append(len(listCode) - 1) # Make it as a list that starts in 0.

# Helper function in game intermediate code, to simulate whiles.
def doEndGoto():
    global stackJumps, listCode
    falseJump = stackJumps.pop()
    returnJump = stackJumps.pop()
    listCode.append([convertOperatorToCode("goto"), -1, -1, returnJump])
    listCode[falseJump][3] = len(listCode) + 1

# The main function that calls other specific functions with a particular objective
def generateIntermediateCodeGame():
    global listCode, stackJumps
    # Before game loop initialize variables
    listCode.append([convertOperatorToCode('initialize'), -1, -1, -1])
    # Start of game loop
    stackJumps.append(len(listCode) + 1)
    generateGoalsCode()
    # Check condition so it can continue to game loop
    doGotoF()
    # Game loop important methods
    listCode.append([convertOperatorToCode('drawMap'), -1, -1, -1])
    listCode.append([convertOperatorToCode('checkMove'), -1, -1, 'avatar'])
    # Game interactions
    generateInteractionsCode()
    # End of game loop
    doEndGoto()
    # If it jumps the game loop then the game finished
    generateWinCode()

def generateGoalsCode():
    global functionDirectory, listCode, stackJumps, stackOp, stackOpVisible, stackTypes, stackOperators
    goals = functionDirectory['SimpleGame']['sections']['TerminationGoals']
    count = 0
    # Check every goal stated in the game program
    for key, goal in goals.iteritems():
        if (goal['type'] == 'spriteCounter'):
            listCode.append([convertOperatorToCode('spriteCounter'), key[0], goal['attrs']['limit'], avail[2][convertAtomicTypeToCode('boolean')]])
        elif (goal['type'] == 'timeout'):
            listCode.append([convertOperatorToCode('timeout'), -1, goal['attrs']['limit'], avail[2][convertAtomicTypeToCode('boolean')]])
        stackOp.append(avail[2][convertAtomicTypeToCode('boolean')])
        stackOpVisible.append(avail[2][convertAtomicTypeToCode('boolean')])
        stackTypes.append(convertAtomicTypeToCode('boolean'))
        avail[2][convertAtomicTypeToCode('boolean')] += 1
        count += 1
        # If there is more than one goal, then there needs to be an or operation.
        if (count > 1):
            stackOperators.append('||')
            generateArithmeticCode()
    # Negate the termination goals to use gotoF
    generateNotCode()

def generateNotCode():
    global listCode, stackOp, stackTypes, stackOperators
    if (len(stackOperators) == 0):
        op1 = stackOp.pop()
        op1Type = stackTypes.pop()
        if (op1Type != convertAtomicTypeToCode('boolean')):
            raise SemanticError("Expected boolean in game not condition. Received: " + str(condtionType))
        # Add negation quadruplet
        listCode.append([convertOperatorToCode('not'), op1, -1, avail[2][convertAtomicTypeToCode('boolean')]])
        stackOp.append(avail[2][convertAtomicTypeToCode('boolean')])
        stackOpVisible.append(avail[2][convertAtomicTypeToCode('boolean')])
        stackTypes.append(convertAtomicTypeToCode('boolean'))
        avail[2][convertAtomicTypeToCode('boolean')] += 1

def generateInteractionsCode():
    global functionDirectory, listCode, stackJumps, stackOp, stackOpVisible, stackTypes, stackOperators
    # Inner loop in game loop starts here
    stackJumps.append(len(listCode) + 1)
    # Check if there is a nextTile in map
    listCode.append([convertOperatorToCode('getNextTile'), -1, -1, avail[2][convertAtomicTypeToCode('boolean')]])
    stackOp.append(avail[2][convertAtomicTypeToCode('boolean')])
    stackOpVisible.append(avail[2][convertAtomicTypeToCode('boolean')])
    stackTypes.append(convertAtomicTypeToCode('boolean'))
    avail[2][convertAtomicTypeToCode('boolean')] += 1
    # Inner while starts for the first tile
    doGotoF()
    interactions = functionDirectory['SimpleGame']['sections']['InteractionList']
    # Check each interaction
    for interaction in interactions:
        for keys, actions in interaction.iteritems():
            count = 0
            for key in keys:
                # First check the sprites that it should be in the tile and add them
                listCode.append([convertOperatorToCode('inTile'), key, 'tile', avail[2][convertAtomicTypeToCode('boolean')]])
                stackOp.append(avail[2][convertAtomicTypeToCode('boolean')])
                stackOpVisible.append(avail[2][convertAtomicTypeToCode('boolean')])
                stackTypes.append(convertAtomicTypeToCode('boolean'))
                avail[2][convertAtomicTypeToCode('boolean')] += 1
                count += 1
                if (count > 1):
                    stackOperators.append('&&')
                    generateArithmeticCode()
            # Condition to see if the sprites where in tile, if not skip game functions
            doGotoF()
            # After checking the sprites, set game functions.
            for action, value in actions.iteritems():
                if (action == 'killSprite'):
                    if (len(value) == 0):
                        listCode.append([convertOperatorToCode('killSprite'), -1, -1, keys[0]])
                    else:
                        for val in value:
                            listCode.append([convertOperatorToCode('killSprite'), -1, -1, val])
                elif (action == 'scoreChange'):
                    listCode.append([convertOperatorToCode('scoreChange'), float(value), -1, 'score'])
                elif (action == 'stepBack'):
                    listCode.append([convertOperatorToCode('stepBack'), -1, -1, keys[0]])
                elif (action == 'shieldFrom'):
                    listCode.append([convertOperatorToCode('shieldFrom'), value, -1, keys[0]])
                elif (action == 'pullWithIt'):
                    listCode.append([convertOperatorToCode('pullWithIt'), keys[-1], -1, keys[0]])
            # GotoF jumps here
            endJump = stackJumps.pop()
            listCode[endJump][3] = len(listCode) + 1 # Because it needs to point to the next one
    # Inner while ends
    doEndGoto()

def generateWinCode():
    global functionDirectory, listCode, stackJumps, stackOp, stackOpVisible, stackTypes, stackOperators
    goals = functionDirectory['SimpleGame']['sections']['TerminationGoals']
    # Iterate each goal and check again
    for key, goal in goals.iteritems():
        if (goal['type'] == 'spriteCounter'):
            listCode.append([convertOperatorToCode('spriteCounter'), key[0], goal['attrs']['limit'], avail[2][convertAtomicTypeToCode('boolean')]])
        elif (goal['type'] == 'timeout'):
            listCode.append([convertOperatorToCode('timeout'), -1, goal['attrs']['limit'], avail[2][convertAtomicTypeToCode('boolean')]])
        stackOp.append(avail[2][convertAtomicTypeToCode('boolean')])
        stackOpVisible.append(avail[2][convertAtomicTypeToCode('boolean')])
        stackTypes.append(convertAtomicTypeToCode('boolean'))
        avail[2][convertAtomicTypeToCode('boolean')] += 1
        # Check if condition of goal was met, if not jump
        doGotoF()
        # If goal was met
        listCode.append([convertOperatorToCode('printEndGame'), -1, -1, goal['attrs']['win']])
        # GotoF jumps here
        endJump = stackJumps.pop()
        listCode[endJump][3] = len(listCode) + 1 # Because it needs to point to the next one
    # End of game
    listCode.append([convertOperatorToCode('endGame'), -1, -1, -1])

def generateIntermediateCodeFile():
    global functionDirectory, listCode
    file = open('rawCode.dame', 'w')
    file.write('<intermediateCode>\n\n')
    # Game
    file.write('\t<game>\n\t\t<sprites>\n')
    if (functionDirectory.has_key('SimpleGame')):
        sprites = functionDirectory['SimpleGame']['sections']['SpriteSet']
        for spriteKey, spriteValue in sprites.iteritems():
            # Save spriteName and spriteType
            file.write('\t\t\t<sprite>\n\t\t\t\t<spriteName>' + spriteKey + '</spriteName>\n')
            file.write('\t\t\t\t<type>' + str(spriteValue['type']) + '</type>\n')
            file.write('\t\t\t</sprite>\n')
    file.write('\t\t</sprites>\n\t</game>\n\n')
    
    # Functions
    file.write('\t<functions>\n')
    for function in functionDirectory:
        if (not (function == 'global' or function == 'main' or function == 'constants' or function == 'SimpleGame')):
            spaceForEra = [0, 0, 0, 0, 0]
            # Save functionName
            file.write('\t\t<function>\n\t\t<functionName>' + str(function) + '</functionName>\n')
            # For every parameter save param.
            for param in functionDirectory[function]['parameters']:
                file.write('\t\t\t<parameter>' + str(param) + '</parameter>\n')
            # Save return type
            file.write('\t\t\t<return>' + str(functionDirectory[function]['return']) + '</return>\n')
            # Save virtual memory value
            file.write('\t\t\t<memory>' + str(functionDirectory[function]['memory']) + '</memory>\n')
            # Save initial quadruplet
            file.write('\t\t\t<quadruplet>' + str(functionDirectory[function]['start_quadruplet']) + '</quadruplet>\n')
            # For var in variables, add 1 to the respective type in spaceForEra (a temporal list)
            for var in functionDirectory[function]['variables']:
                spaceForEra[functionDirectory[function]['variables'][var]['type'] - 101] += 1
            # Sum the temporals too, not only variables
            spaceForEra[0] += functionDirectory[function]['temporals'][101]
            spaceForEra[1] += functionDirectory[function]['temporals'][102]
            spaceForEra[2] += functionDirectory[function]['temporals'][103]
            spaceForEra[3] += functionDirectory[function]['temporals'][104]
            spaceForEra[4] += functionDirectory[function]['temporals'][105]
            # Write era based on the variables and temporals
            file.write('\t\t\t<era>\n' +
                       '\t\t\t\t<int>' + str(spaceForEra[0]) + '</int>\n' +
                       '\t\t\t\t<float>' + str(spaceForEra[1]) + '</float>\n' +
                       '\t\t\t\t<string>' + str(spaceForEra[2]) + '</string>\n' +
                       '\t\t\t\t<char>' + str(spaceForEra[3]) + '</char>\n' +
                       '\t\t\t\t<boolean>' + str(spaceForEra[4]) + '</boolean>\n' +
                       '\t\t\t</era>\n')
            file.write('\t\t</function>\n')
    file.write('\t</functions>\n\n')

    # Constants
    file.write('\t<constants>\n')
    constants = functionDirectory['constants']
    for constant in constants:
        # Save constant value, type and virtual memory direction
        file.write('\t\t<constant>\n\t\t\t<constantValue>' + str(constant) + '</constantValue>\n')
        file.write('\t\t\t<type>' + str(constants[constant]['type']) + '</type>\n')
        file.write('\t\t\t<memory>' + str(constants[constant]['memory']) + '</memory>\n')
        file.write('\t\t</constant>\n')
    file.write('\t</constants>\n\n')

    # Quadruplets
    file.write('\t<quadruplets>\n')
    for index, quadruplet in enumerate(listCode):
        # For each quadruplet save index and 4 elements.
        file.write('\t\t<quadruplet>\n\t\t\t<index>' + str(index + 1) + '</index>\n')
        file.write('\t\t\t<operation>' + str(quadruplet[0]) + '</operation>\n')
        file.write('\t\t\t<element1>' + str(quadruplet[1]) + '</element1>\n')
        file.write('\t\t\t<element2>' + str(quadruplet[2]) + '</element2>\n')
        file.write('\t\t\t<result>' + str(quadruplet[3]) + '</result>\n')
        file.write('\t\t</quadruplet>\n')
    file.write('\t</quadruplets>\n\n')
    file.write('</intermediateCode>\n')

# Helper function to initialize variables
def initializeVariables():
    global functionDirectory, avail, stackJumps, stackTypes, stackOperators, stackOp, stackOpVisible, listCode, listSprites, killSprites, gameAttrs, gameActions, gameSections, variables, constants, parameters, globalVariables, typeOfVariable, functionId, listId, sureListId, paramCounter, goSubFunction, spriteId, temporalStamp
    functionDirectory = {"global": {}}
    avail = {0: {101: 2000, 102:3000, 103:4000, 104:5000, 105:6000}, 1: {101: 7000, 102: 8000, 103:9000, 104: 10000, 105: 11000}, 2: {101: 12000, 102: 13000, 103: 14000, 104: 15000, 105:16000}, 3: {101: 17000, 102: 18000, 103: 19000, 104: 20000, 105: 21000}}
    stackJumps = []
    stackTypes = []
    stackOperators = []
    stackOp = []
    stackOpVisible = []
    listCode = []
    listSprites = []
    killSprites = []
    gameAttrs = {}
    gameActions = []
    gameSections = {}
    variables = {}
    constants = {}
    parameters = []
    globalVariables = {}
    typeOfVariable = ""
    functionId = ""
    listId = ""
    sureListId = ""
    listScope = ""
    paramCounter = 0
    goSubFunction = ""
    spriteId = ""
    temporalStamp = {}

# Import yacc
import ply.yacc as yacc
parser = yacc.yacc()

# Main.
argv = sys.argv[1:]
if (len(argv) == 0):
    while 1:
        try:
            s = raw_input('arcadame > ')
        except EOFError:
            break
        # Initialize the global variables in each run
        initializeVariables()

        # Start the scanning and parsing
        with open(s) as fp:
            completeString = ""
            for line in fp:
                completeString += line
            try:
                parser.parse(completeString)
                if (debug):
                    print "dictionary of functions: ", functionDirectory
                    print "list of quadruplets: ", listCode
                generateIntermediateCodeFile()
                print("Correct program")
            except EOFError:
                break
else:
    # Check for special arguments in the execution of this file
    inputFile = ""
    try:
        opts, args = getopt.getopt(argv,"hi:d:",["ifile=","debug="])
    except getopt.GetoptError:
        print 'python arcadame.py [-i <inputfile>, -d <True|False>, default = False]'
        sys.exit(99)
    for opt, arg in opts:
        # Help
        if opt == '-h':
            print 'python arcadame.py [-i <inputfile>,-d <True|False>, default = False]'
            sys.exit(1)
        # Set input file
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        # Set debug to True or False
        elif opt in ("-d", "--debug"):
            debug = arg == 'True'

    # Initialize the global variables
    initializeVariables()
    
    # Start the scanning and parsing
    with open(inputFile) as fp:
        completeString = ""
        for line in fp:
            completeString += line
        try:
            parser.parse(completeString)
            if (debug):
                print "dictionary of functions: ", functionDirectory
                print "list of quadruplets: ", listCode
            generateIntermediateCodeFile()
            print("Correct program")
        except EOFError:
            sys.exit(2)
