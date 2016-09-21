# -----------------------------------------------------------------------------
# Bernardo Daniel Trevino Caballero     A00813175
# Myriam Maria Gutierrez Aburto         A00617060
# arcadame.py
#
# A simple scanner and parser for the languange Arcadame
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

debug = True

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

# Parsing rules
start = 'programa'

def p_programa(p):
    '''programa : SIMPLEGAME ID D_2P sprites interactions goals mapping map block BIG_END
                | PROGRAM ID D_2P block BIG_END'''

def p_sprites(p):
    '''sprites : SPRITESET D_2P sprite D_PYC more_sprites SMALL_END'''

def p_more_sprites(p):
    '''more_sprites : sprite D_PYC more_sprites
                    | '''

def p_sprite(p):
    '''sprite : ID EQUAL sprite_type sprite_attrs'''

def p_sprite_type(p):
    '''sprite_type : IMMOVABLE
                   | MOVINGAVATAR
                   | SHOOTINGAVATAR
                   | MISSILE
                   | SPAWNER
                   | PASSIVE'''

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

def p_interactions(p):
    '''interactions : INTERACTIONLIST D_2P interaction D_PYC more_interactions SMALL_END'''

def p_more_interactions(p):
    '''more_interactions : interaction D_PYC more_interactions
                         | '''

def p_interaction(p):
    '''interaction : ID more_spritesid ENCOUNTERS ID EQUAL action more_actions'''

def p_more_spritesid(p):
    '''more_spritesid : D_C ID more_spritesid
                      | '''

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

def p_kill_id(p):
    '''kill_id : ID
               | '''

def p_goals(p):
    '''goals : TERMINATIONGOALS D_2P goal D_PYC more_goals SMALL_END'''

def p_more_goals(p):
    '''more_goals : goal D_PYC
                  | '''

def p_goal(p):
    '''goal : goal_type LIMIT EQUAL INT_CT WIN EQUAL BOOLEAN_CT'''

def p_goal_type(p):
    '''goal_type : SPRITECOUNTER SPRITE EQUAL ID
                 | MULTISPRITECOUNTER sprite_list
                 | TIMEOUT'''

def p_sprite_list(p):
    '''sprite_list : SPRITE EQUAL ID more_sprite_list'''

def p_more_sprite_list(p):
    '''more_sprite_list : D_C sprite_list
                        | '''

def p_mapping(p):
    '''mapping : MAPPING D_2P mapping_rule D_PYC more_mapping_rules SMALL_END'''

def p_more_mapping_rules(p):
    '''more_mapping_rules : mapping_rule D_PYC more_mapping_rules
                          | '''

def p_mapping_rule(p):
    '''mapping_rule : CHAR_CT EQUAL ID more_spritesid'''

def p_map(p):
    '''map : MAP D_2P STRING_CT D_PYC more_tiles SMALL_END'''

def p_more_tiles(p):
    '''more_tiles : STRING_CT D_PYC more_tiles
                  | '''

def p_block(p):
    '''block : vars functions main_block'''

def p_vars(p):
    '''vars : var D_PYC vars
            | '''

def p_var(p):
    '''var : VAR type D_2P ID
           | VAR type D_CA INT_CT D_CC D_2P ID'''

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING
            | CHAR
            | BOOLEAN'''

def p_functions(p):
    '''functions : function functions
                 | '''

def p_function(p):
    '''function : FUNC ID D_PA parameters D_PC EQUAL type D_2P code_block SMALL_END'''

def p_parameters(p):
    '''parameters : parameter more_parameters
                  | '''

def p_parameter(p):
    '''parameter : type D_2P type_parameter'''

def p_type_parameter(p):
    '''type_parameter : D_AMP ID
                      | ID'''

def p_more_parameters(p):
    '''more_parameters : D_C parameter more_parameters
                       | '''

def p_main_block(p):
    '''main_block : MAIN D_2P code_block SMALL_END'''

def p_code_block(p):
    '''code_block : vars mini_block'''

def p_statute(p):
    '''statute : assignation
               | condition
               | printing
               | reading
               | cycle
               | function_use
               | return'''

def p_function_use(p):
    '''function_use : ID D_PA expression more_ids D_PC
                    | STARTGAME D_PA D_PC'''

def p_more_ids(p):
    '''more_ids : D_C expression more_ids
                | '''

def p_assignation(p):
    '''assignation : ID value_list EQUAL expression'''

def p_value_list(p):
    '''value_list : D_CA expression D_CC
                  | '''

def p_printing(p):
    '''printing : PRINT D_PA printable D_PC'''

def p_printable(p):
    '''printable : expression more_printable'''

def p_more_printable(p):
    '''more_printable : D_C printable
                      | '''

def p_condition(p):
    '''condition : IF D_PA expression D_PC D_2P mini_block else_condition SMALL_END'''

def p_else_condition(p):
    '''else_condition : ELSE D_2P mini_block
                      |'''

def p_reading(p):
    '''reading : reading_type D_PA ID D_PC'''

def p_reading_type(p):
    '''reading_type : GETVALUE
                    | GETLINE
                    | GETBOOLEAN
                    | GETCHAR'''

def p_cycle(p):
    '''cycle : WHILE D_PA expression D_PC D_2P mini_block SMALL_END'''

def p_return(p):
    '''return : RETURN expression'''

def p_mini_block(p):
    '''mini_block : statute D_PYC mini_block
                  | '''

def p_expression(p):
    '''expression : big_exp or_exp'''

def p_or_exp(p):
    '''or_exp : OR expression
              | '''

def p_big_exp(p):
    '''big_exp : medium_exp and_exp'''

def p_and_exp(p):
    '''and_exp : AND big_exp
               | '''

def p_medium_exp(p):
    '''medium_exp : exp relational_exp'''

def p_relational_exp(p):
    '''relational_exp : MAYOR_QUE exp
                      | MENOR_QUE exp
                      | DIFERENTE_DE exp
                      | IGUAL_QUE exp
                      | '''

def p_exp(p):
    '''exp : term add_term'''

def p_add_term(p):
    '''add_term : PLUS exp
                | MINUS exp
                | '''

def p_term(p):
    '''term : factor times_factor'''

def p_times_factor(p):
    '''times_factor : TIMES term
                    | DIVISION term
                    | '''

def p_factor(p):
    '''factor : D_PA expression D_PC
              | PLUS var_ct
              | MINUS var_ct
              | var_ct'''

def p_var_ct(p):
    '''var_ct : ID value_list
              | FLOAT_CT
              | INT_CT
              | BOOLEAN_CT
              | STRING_CT
              | CHAR_CT
              | function_use'''

def p_error(p):
    if p:
        raise SyntaxError("Syntax error at '%s'" % p.value)
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