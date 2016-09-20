# -----------------------------------------------------------------------------
# Bernardo Daniel Trevino Caballero     A00813175
# arcadame.py
#
# A simple scanner and parser for the languange Arcadame
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

debug = False

class SemanticError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# Define token names
tokens = (
    'SIMPLEGAME', 'PROGRAM', 'SPRITESET', 'IMMOVABLE', 'MOOVINGAVATAR', 'SHOOTINGAVATAR', 'MISSILE', 'SPAWNER', 'PASSIVE', 'IMG', 'GENERATEDSPRITE', 'SPEED', 'PORTAL', 'SHRINKFACTOR', 'LIMIT', 'PROB', 'COOLDOWN', 'COLOR', 'HEALTHPOINTS', 'LIMITHEALTHPOINTS', 'WEAPONSPRITE', 'ENCOUNTERS', 'INTERACTIONLIST', 'KILLSPRITE', 'STEPBACK', 'SCORECHANGE', 'TRANSFORMTO', 'BOUNCEFORWARD', 'CHANGEHEALTHPOINTS', 'ADDTIMER', 'TIME', 'TRANSFORMALL', 'TERMINATIONGOALS', 'SPRITECOUNTER', 'SPRITE', 'MULTISPRITECOUNTER', 'TIMEOUT', 'WIN', 'MAPPING', 'MAP', 'FUNC', 'INT', 'FLOAT', 'STRING', 'CHAR', 'BOOLEAN', 'MAIN', 'VAR', 'PRINT', 'IF', 'ELSE', 'GETVALUE', 'GETLINE', 'GETBOOLEAN', 'GETCHAR', 'WHILE', 'SMALL_END', 'BIG_END', 'STARTGAME', 'RETURN', 'D_2P', 'D_PYC', 'D_C', 'D_PA', 'D_PC', 'EQUAL', 'PLUS', 'MINUS', 'TIMES', 'DIVISION', 'MENOR_QUE', 'MAYOR_QUE', 'DIFERENTE_DE', 'IGUAL_QUE', 'AND', 'OR', 'D_CA', 'D_CC', 'ID', 'INT_CT', 'FLOAT_CT', 'STRING_CT', 'BOOLEAN_CT', 'CHAR_CT', 'COLOR_CT', 'MOVEMENT_CT', 'PULLWITHIT', 'SHIELDFROM'
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

def t_MOOVINGAVATAR(t):
    'MoovingAvatar'
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
    'bounceForward'
    if (debug):
        print(t)
    return t

def t_BOUNCEFORWARD(t):
    'bounceForward'
    if (debug):
        print(t)
    return t

def t_CHANGEHEALTHPOINTS(t):
    'Program'
    if (debug):
        print(t)
    return t

def t_ADDTIMER(t):
    'addTimer'
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

def t_TIMEOUT(t):
    'timeout'
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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()
while True:
    s = raw_input('arcadame > ')
    lex.input(s)
    while True:
        tok = lex.token()
        if not tok:
            break      # No more input

"""
# Parsing rules

start = 'programa'

def p_programa(p):
    '''programa : PROGRAM ID DELIMITADOR_PYC bloque
                | PROGRAM ID DELIMITADOR_PYC vars bloque'''

class LexerError(Exception): pass

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
        raise LexerError("Illegal character '%s'" % p.value)
    if not p:
        print("EOF")

# Import yacc
import ply.yacc as yacc
parser = yacc.yacc()


# Main. It expects
while 1:
    try:
        s = raw_input('arcadame > ')
    except EOFError:
        break
    with open(s) as fp:
        completeString = ""
        for line in fp:
            completeString += line
        # print completeString
        try:
            parser.parse(completeString)
        except EOFError:
            break
"""
