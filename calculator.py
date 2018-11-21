import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = ['INT', 'REAL', 'NOME', 'MENOS', 'MAIS', 'DIVISAO', 'MULTIPLICACAO', 'ATRIBUICAO']

t_MENOS = r'\-'
t_MAIS = r'\+'
t_DIVISAO = r'\/'
t_MULTIPLICACAO = r'\*'
t_ATRIBUICAO = r'\='
t_ignore = r' '



def t_REAL(t):
    r'\d+\.\d'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NOME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NOME'
    return t

def t_error(t):
    print("Palavra não reconhecida")
    t.lexer.skip(1)

lexer = lex.lex()

#associativo a esquerda
#mais e menos tem a msm precedencia, e mult e div tem a msm precedencia
precedence = (
    ('left', 'MAIS', 'MENOS'),
    ('left', 'MULTIPLICACAO', 'DIVISAO')
)

def p_calc(p):
    '''
    calc : expressao
         | atribuicao
         | vazio
    '''
    print(run(p[1]))

def p_atribuicao(p):
    '''
    atribuicao : NOME ATRIBUICAO expressao
    '''
    p[0] = ('=', p[1], p[3])

def p_expressao(p):
    '''
    expressao : expressao MENOS expressao
              | expressao MAIS expressao
              | expressao DIVISAO expressao
              | expressao MULTIPLICACAO expressao
    '''
    p[0] = (p[2], p[1], p[3])

def p_expressao_int_real(p):
    '''
    expressao : INT
               | REAL
    '''
    p[0] = p[1]

def p_expressao_var(p):
    '''
    expressao : NOME
    '''
    p[0] = ('var', p[1])

def p_error(p):
    print('Erro de Sintaxe')

def p_vazio(p):
    '''
    vazio : 
    '''
    p[0] = None

parser = yacc.yacc()

ambiente = {}
def run(p):
    global ambiente
    if type(p) == tuple:
        if p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '=':
            ambiente[p[1]] = run(p[2])
            print(ambiente)
        elif p[0] == 'var':
            if p[1] not in ambiente:
                return 'Variável não declarada'
            return ambiente[p[1]]
    else:
        return p

while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)