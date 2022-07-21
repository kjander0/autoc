

import sys

# <statement> = <assignment> | <expression> | <function definition>
# <expression> = <number> | <function call> | <identifier> | <expression> <operator> <expression>

def parse(src):
    state = ParserState(src)
    while True:
        s = parse_statement(state)
        if s is None:
            break

        state.statements.append(s)


    if len(state.errors) == 0:
        return None, state.statements
    
    return state.errors, None            
    

class ParserState:
    def __init__(self, src):
        self.src = src
        self.statements = []
        self.offset = 0
        self.errors = []


class Assignment:
    def __init__(self, ident, expr):
        self.lhs = ident
        self.rhs = expr
    
    def __str__(self):
        return f'{self.lhs} = {self.rhs}'


class Expression:
    def __init__(self, lhs, operator, rhs):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs
    
    def __str__(self):
        return f'{self.lhs} {self.operator} {self.rhs}'


def parse_statement(state):
    eof = read_whitespace(state)
    if eof:
        # TODO: might need to add an error in future (e.g. statement within function)
        return None

    ass = revert_error(parse_assignment, state)
    if ass is not None:
        return ass

    expr = parse_expression(state)
    if expr is None:
        state.errors.append("expected assignment or expression")
        return None
        
    return expr
    

def parse_assignment(state):
    read_whitespace(state)

    ident = parse_identifier(state)
    if ident is None:
        state.errors.append("left side of assignment must be an identifier")
        return None

    read_whitespace(state)

    if read_char(state) != '=':
        state.errors.append("expected '=' for assignment")
        return None
        
    read_whitespace(state)

    expr = parse_expression(state)
    if expr is None:
        state.errors.append("right side of assignment must be an expression")
        return None

    return Assignment(ident, expr)


def parse_expression(state):
    eof = read_whitespace(state)
    if eof: # expressions are recursive so must check or EOF
        state.errors.append('EOF when expecting expression')
        return None

    lhs_expr = revert_error(parse_number, state) or \
               revert_error(parse_identifier, state) or \
               revert_error(parse_function_call, state) or \
               parse_expression(state)

    if lhs_expr is None:
        state.errors.append('expected expresion')
        return None

    operator = revert_error(parse_operator, state)
    if operator is None:
        return Expression(lhs_expr, None, None)

    rhs_expr = parse_expression(state)
    if rhs_expr is None:
        state.errors.append("expected expression on right hand side of operator")
        return None

    return Expression(lhs_expr, operator, rhs_expr)


def parse_identifier(state):
    read_whitespace(state)
    
    start_offset = state.offset
    while True:
        c = peek_char(state)
        if c is None or c.isspace():
            break
        
        if not c.isalnum():
            state.errors.append("invalid identifier")
            return None
            
        state.offset += 1
            
    ident = state.src[start_offset:state.offset]
    if len(ident) == 0:
        state.errors.append("expected identiier")
        return None
    
    
    if ident[0].isdigit():
        state.errors.append("identifier must begin with a letter")
        return None

    return ident


def parse_number(state):
    read_whitespace(state)

    start_offset = state.offset
    while True:
        c = peek_char(state)
        if c is None or c.isspace():
            break

        if not c.isdigit():
            state.errors.append("not a number")
            return None
        state.offset += 1
    
    num_str = state.src[start_offset:state.offset]
    
    if len(num_str) == 0:
        state.errors.append("expected digit")
        return None
     
    return int(num_str)

def parse_operator(state):
    read_whitespace(state)
    c = read_char(state)
    if c is None or c != '+':
        state.errors.append(f'{c} is not an operator')
        return None
    return c


def parse_function_call(state):
    return None

def read_whitespace(state):
    while True:
        c = read_char(state)
        if c is None:
            return True # EOF reached
        if not c.isspace():
            state.offset -= 1
            return False


def peek_char(state):
    if state.offset >= len(state.src):
        return None # EOF
    return state.src[state.offset]


def read_char(state):
    if state.offset >= len(state.src):
        return None # EOF
    c = state.src[state.offset]
    state.offset += 1
    return c
    
def read_char_no_newline(state):
    c = read_char(state)
    if c == '\n':
        return None
    return None


def revert_error(parse_func, state):
    start_offset = state.offset
    val = parse_func(state)
    if val is None:
        state.offset = start_offset
        clear_errors(state)
    return val
    

def clear_errors(state):
    state.errors = []




