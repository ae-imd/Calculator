import re
import math

PRIORITY = {
    'NOT': 2, 'u-': 2, 'u+': 2,
    '^': 3,
    '*': 4, '/': 4, 'DIV': 4, 'MOD': 4,
    '+': 5, '-': 5,
    'LSH': 6, 'RSH': 6, 'ROL': 6, 'ROR': 6,
    'AND': 7, 'XOR': 8, 'OR': 9,
    'ROOT': 10, 'EXP': 10, 'LN': 10, 'LOG': 10,
    'SIN': 10, 'COS': 10, 'TAN': 10, 'COT': 10,
    'ASIN': 10, 'ACOS': 10, 'ATAN': 10, 'ACOT': 10,
    'FLOOR': 10, 'CEILING': 10, 'SQRT': 10, 'CBRT': 10, 'SQR': 10, 'CBR': 10,
}

CONSTANTS = {
    'E': math.e,
    'PI': math.pi,
    'PHI': (1 + math.sqrt(5)) / 2
}


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def tokenize(expr: str) -> list:
    expr = expr.replace(' ', '')

    if not expr:
        raise ValueError("Empty expression")

    pattern = r'\d+\.?\d*|[()+*/^,\-]|NOT|AND|XOR|OR|LSH|RSH|ROL|ROR|DIV|MOD|ROOT|EXP|LN|LOG|SIN|COS|TAN|COT|ASIN|ACOS|ATAN|ACOT|FLOOR|CEILING|SQRT|CBRT|SQR|CBR|E|PI|PHI'
    tokens = re.findall(pattern, expr.upper())

    remaining = re.sub(pattern, '', expr.upper())
    if remaining:
        raise ValueError(f"Invalid characters: {remaining}")
    
    return tokens

def process_unary_operations(tokens) -> list:
    res = []
    
    for i, token in enumerate(tokens):
        if token == '-':
            if i == 0 or tokens[i-1] in '(+-*/^,' or tokens[i-1] in ['NOT', 'AND', 'XOR', 'OR', 'LSH', 'RSH', 'ROL', 'ROR'] or tokens[i-1] in ['ROOT', 'EXP', 'LN', 'LOG', 'SIN', 'COS', 'TAN', 'COT', 'ASIN', 'ACOS', 'ATAN', 'ACOT', 'FLOOR', 'CEILING', 'SQRT', 'CBRT', 'SQR', 'CBR', 'DIV', 'MOD']:
                if i + 1 < len(tokens) and tokens[i+1] in ['+', '-', '*', '/', '^', ',']:
                    raise ValueError('Wrong syntax')
                res.append('u-')
            else:
                res.append('-')
        elif token == '+':
            if i == 0 or tokens[i-1] in '(+-*/^,' or tokens[i-1] in ['NOT', 'AND', 'XOR', 'OR', 'LSH', 'RSH', 'ROL', 'ROR'] or tokens[i-1] in ['ROOT', 'EXP', 'LN', 'LOG', 'SIN', 'COS', 'TAN', 'COT', 'ASIN', 'ACOS', 'ATAN', 'ACOT', 'FLOOR', 'CEILING', 'SQRT', 'CBRT', 'SQR', 'CBR', 'DIV', 'MOD']:
                if i + 1 < len(tokens) and tokens[i+1] in ['+', '-', '*', '/', '^', ',']:
                    raise ValueError('Wrong syntax')
                res.append('u+')
            else:
                res.append('+')
        else: 
            res.append(token)

    return res

def infix_to_postfix(expr: str) -> list:
    res = []
    st = [] # stack
    tokens = tokenize(expr)
    tokens = process_unary_operations(tokens)

    for token in tokens:
        if is_number(token) or token in CONSTANTS:
            res.append(token)
        
        elif token in ['ROOT', 'EXP', 'LN', 'LOG', 'SIN', 'COS', 'TAN', 'COT', 'ASIN', 'ACOS', 'ATAN', 'ACOT', 'FLOOR', 'CEILING', 'SQRT', 'CBRT', 'SQR', 'CBR', 'DIV', 'MOD', 'LSH', 'RSH', 'ROL', 'ROR', 'AND', 'XOR', 'OR']:
            st.append(token)
        
        elif token == '(':
            st.append(token)
        
        elif token == ')':
            while st and st[-1] != '(':
                res.append(st.pop())
            if not st:
                raise ValueError('Unbalanced brackets')
            st.pop()  # Delete '('
            
            if st and st[-1] in ['ROOT', 'EXP', 'LN', 'LOG', 'SIN', 'COS', 'TAN', 'COT', 'ASIN', 'ACOS', 'ATAN', 'ACOT', 'FLOOR', 'CEILING', 'SQRT', 'CBRT', 'SQR', 'CBR', 'DIV', 'MOD', 'LSH', 'RSH', 'ROL', 'ROR', 'AND', 'XOR', 'OR']:
                res.append(st.pop())
        
        elif token in PRIORITY:
            while (st and st[-1] != '(' and 
                   st[-1] in PRIORITY and 
                   PRIORITY[st[-1]] <= PRIORITY[token]):
                res.append(st.pop())
            st.append(token)
    
    while st:
        if st[-1] == '(':
            raise ValueError('Unbalanced brackets')
        res.append(st.pop())
    
    return res

def calculate_postfix_expression(postfix: list) -> float:
    st = [] # stack
    
    for token in postfix:

        if is_number(token): st.append(float(token))
        elif token in CONSTANTS: st.append(CONSTANTS[token])
        else:
            match(token):
                case 'u-':
                    if st:
                        st.append(-st.pop())
                    else: raise ValueError("Wrong syntax")
                case 'u+':
                    if st:
                        st.append(+st.pop())
                    else: raise ValueError("Wrong syntax")
                case 'NOT':
                    if st:
                        st.append(~int(st.pop()))
                    else: raise ValueError("Wrong syntax")
                case '^':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a ** b)
                    else: raise ValueError("Wrong syntax")
                case '*':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a * b)
                    else: raise ValueError("Wrong syntax")
                case '/':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        if b == 0:
                            raise ZeroDivisionError("Division by zero")
                        st.append(a / b)
                    else: raise ValueError("Wrong syntax")
                case 'DIV':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a // b)
                    else: raise ValueError("Wrong syntax")
                case 'MOD':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a % b)
                    else: raise ValueError("Wrong syntax")
                case '+':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a + b)
                    else: raise ValueError("Wrong syntax")
                case '-':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a - b)
                    else: raise ValueError("Wrong syntax")
                case 'LSH':
                    if len(st) >= 2:
                        shift = int(st.pop())
                        a = int(st.pop())
                        st.append(a << shift)
                    else: raise ValueError("Wrong syntax")
                case 'RSH':
                    if len(st) >= 2:
                        shift = int(st.pop())
                        a = int(st.pop())
                        st.append(a >> shift)
                    else: raise ValueError("Wrong syntax")
                case 'ROL':
                    if len(st) >= 2:
                        shift = int(st.pop())
                        a = int(st.pop())
                        bits = 32
                        st.append((a << shift) | (a >> (bits - shift)))
                    else: raise ValueError("Wrong syntax")
                case 'ROR':
                    if len(st) >= 2:
                        shift = int(st.pop())
                        a = int(st.pop())
                        bits = 32
                        st.append((a >> shift) | (a << (bits - shift)))
                    else: raise ValueError("Wrong syntax")
                case 'AND':
                    if len(st) >= 2:
                        b = int(st.pop())
                        a = int(st.pop())
                        st.append(a & b)
                    else: raise ValueError("Wrong syntax")
                case 'XOR':
                    if len(st) >= 2:
                        b = int(st.pop())
                        a = int(st.pop())
                        st.append(a ^ b)
                    else: raise ValueError("Wrong syntax")
                case 'OR':
                    if len(st) >= 2:
                        b = int(st.pop())
                        a = int(st.pop())
                        st.append(a | b)
                    else: raise ValueError("Wrong syntax")
                case 'EXP':
                    if st:
                        st.append(math.exp(st.pop()))
                    else: raise ValueError("Wrong syntax")
                case 'LN':
                    if st:
                        x = st.pop()
                        if x <= 0:
                            raise ValueError("Operation LN of a non-positive number")
                        st.append(math.log(x))
                    else: raise ValueError("Wrong syntax")
                case 'LOG':
                    if len(st) >= 2:
                        base = st.pop()
                        x = st.pop()
                        if x <= 0 or base <= 0 or base == 1:
                            raise ValueError("Invalid values for LOG operation")
                        st.append(math.log(x, base))
                    else: raise ValueError("Wrong syntax")
                case 'SIN':
                    if st:
                        st.append(math.sin(st.pop()))
                    else: raise ValueError("Wrong syntax")
                case 'COS':
                    if st:
                        st.append(math.cos(st.pop()))
                    else: raise ValueError("Wrong syntax")
                case 'TAN':
                    if st:
                        x = st.pop()
                        st.append(math.tan(x))
                    else: raise ValueError("Wrong syntax")
                case 'COT':
                    if st:
                        x = st.pop()
                        st.append(1 / math.tan(x))
                    else: raise ValueError("Wrong syntax")
                case 'ASIN':
                    if st:
                        x = st.pop()
                        st.append(math.asin(x))
                    else: raise ValueError("Wrong syntax")
                case 'ACOS':
                    if st:
                        x = st.pop()
                        st.append(math.acos(x))
                    else: raise ValueError("Wrong syntax")
                case 'ATAN':
                    if st:
                        st.append(math.atan(st.pop()))
                    else: raise ValueError("Wrong syntax")
                case 'ACOT':
                    if st:
                        x = st.pop()
                        st.append(math.pi/2 - math.atan(x))
                    else: raise ValueError("Wrong syntax")
                case 'FLOOR':
                    if st:
                        st.append(math.floor(st.pop()))
                    else: raise ValueError("Wrong syntax")
                case 'CEILING':
                    if st:
                        st.append(math.ceil(st.pop()))
                    else: raise ValueError("Wrong syntax")
                case 'SQRT':
                    if st:
                        x = st.pop()
                        if x < 0:
                            raise ValueError("Square root of a negative number")
                        st.append(math.sqrt(x))
                    else: raise ValueError("Wrong syntax")
                case 'CBRT':
                    if st:
                        x = st.pop()
                        st.append(math.cbrt(x))
                    else: raise ValueError("Wrong syntax")
                case 'SQR':
                    if st:
                        x = st.pop()
                        st.append(x * x)
                    else: raise ValueError("Wrong syntax")
                case 'CBR':
                    if st:
                        x = st.pop()
                        st.append(x * x * x)
                    else: raise ValueError("Wrong syntax")
                case 'ROOT':
                    if len(st) >= 2:
                        n = st.pop()
                        x = st.pop()
                        if x < 0 and n % 2 == 0:
                            raise ValueError("Even root of a negative number")
                        st.append(pow(x, 1/n))
                    else: raise ValueError("Wrong syntax")
    
    if len(st) != 1:
        raise ValueError("Invalid expression")
    
    return st[0]

def calculate_infix_expression(expression):
    try:
        postfix = infix_to_postfix(expression)
        return calculate_postfix_expression(postfix)
    except Exception as e:
        raise ValueError(f"Error: {e}")