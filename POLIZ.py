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

def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def tokenize(expr: str) -> list:
    pattern = r'\d+\.?\d*|[()+*/^-]|NOT|AND|XOR|OR|LSH|RSH|ROL|ROR|DIV|MOD|ROOT|EXP|LN|LOG|SIN|COS|TAN|COT|ASIN|ACOS|ATAN|ACOT|FLOOR|CEILING|SQRT|CBRT|SQR|CBR'
    tokens = re.findall(pattern, expr.upper())
    return tokens

def process_unary_operations(tokens) -> list:
    res = []
    
    for i, token in enumerate(tokens):
        if token == '-':
            if i == 0 or tokens[i-1] in '(+-*/^' or tokens[i-1] in ['NOT', 'AND', 'XOR', 'OR', 'LSH', 'RSH', 'ROL', 'ROR'] or tokens[i-1] in ['ROOT', 'EXP', 'LN', 'LOG', 'SIN', 'COS', 'TAN', 'COT', 'ASIN', 'ACOS', 'ATAN', 'ACOT', 'FLOOR', 'CEILING', 'SQRT', 'CBRT', 'SQR', 'CBR']:
                res.append('u-')
            else:
                res.append('-')
        elif token == '+':
            if i == 0 or tokens[i-1] in '(+-*/^' or tokens[i-1] in ['NOT', 'AND', 'XOR', 'OR', 'LSH', 'RSH', 'ROL', 'ROR'] or tokens[i-1] in ['ROOT', 'EXP', 'LN', 'LOG', 'SIN', 'COS', 'TAN', 'COT', 'ASIN', 'ACOS', 'ATAN', 'ACOT', 'FLOOR', 'CEILING', 'SQRT', 'CBRT', 'SQR', 'CBR']:
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
        if is_number(token):
            res.append(token)
        
        elif token in ['ROOT', 'EXP', 'LN', 'LOG', 'SIN', 'COS', 'TAN', 'COT', 'ASIN', 'ACOS', 'ATAN', 'ACOT', 'FLOOR', 'CEILING', 'SQRT', 'CBRT', 'SQR', 'CBR']:
            st.append(token)
        
        elif token == '(':
            st.append(token)
        
        elif token == ')':
            while st and st[-1] != '(':
                res.append(st.pop())
            if not st:
                raise ValueError('Unbalanced brackets')
            st.pop()  # Delete '('
            
            if st and st[-1] in ['ROOT', 'EXP', 'LN', 'LOG', 'SIN', 'COS', 'TAN', 'COT', 'ASIN', 'ACOS', 'ATAN', 'ACOT', 'FLOOR', 'CEILING', 'SQRT', 'CBRT', 'SQR', 'CBR']:
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

        if is_number(token):
            st.append(float(token))
        else:
            match(token):
                case 'u-':
                    if st:
                        st.append(-st.pop())
                case 'u+':
                    if st:
                        st.append(+st.pop())
                case 'NOT':
                    if st:
                        st.append(~int(st.pop()))
                case '^':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a ** b)
                case '*':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a * b)
                case '/':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        if b == 0:
                            raise ZeroDivisionError("Division by zero")
                        st.append(a / b)
                case 'DIV':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a // b)
                case 'MOD':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a % b)
                case '+':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a + b)
                case '-':
                    if len(st) >= 2:
                        b = st.pop()
                        a = st.pop()
                        st.append(a - b)
                case 'LSH':
                    if len(st) >= 2:
                        shift = int(st.pop())
                        a = int(st.pop())
                        st.append(a << shift)
                case 'RSH':
                    if len(st) >= 2:
                        shift = int(st.pop())
                        a = int(st.pop())
                        st.append(a >> shift)
                case 'ROL':
                    if len(st) >= 2:
                        shift = int(st.pop())
                        a = int(st.pop())
                        bits = 32
                        st.append((a << shift) | (a >> (bits - shift)))
                case 'ROR':
                    if len(st) >= 2:
                        shift = int(st.pop())
                        a = int(st.pop())
                        bits = 32
                        st.append((a >> shift) | (a << (bits - shift)))
                case 'AND':
                    if len(st) >= 2:
                        b = int(st.pop())
                        a = int(st.pop())
                        st.append(a & b)
                case 'XOR':
                    if len(st) >= 2:
                        b = int(st.pop())
                        a = int(st.pop())
                        st.append(a ^ b)
                case 'OR':
                    if len(st) >= 2:
                        b = int(st.pop())
                        a = int(st.pop())
                        st.append(a | b)
                case 'EXP':
                    if st:
                        st.append(math.exp(st.pop()))
                case 'LN':
                    if st:
                        x = st.pop()
                        if x <= 0:
                            raise ValueError("Operation LN of a non-positive number")
                        st.append(math.log(x))
                case 'LOG':
                    if len(st) >= 2:
                        base = st.pop()
                        x = st.pop()
                        if x <= 0 or base <= 0 or base == 1:
                            raise ValueError("Invalid values for LOG operation")
                        st.append(math.log(x, base))
                case 'SIN':
                    if st:
                        st.append(math.sin(st.pop()))
                case 'COS':
                    if st:
                        st.append(math.cos(st.pop()))
                case 'TAN':
                    if st:
                        x = st.pop()
                        st.append(math.tan(x))
                case 'COT':
                    if st:
                        x = st.pop()
                        st.append(1 / math.tan(x))
                case 'ASIN':
                    if st:
                        x = st.pop()
                        st.append(math.asin(x))
                case 'ACOS':
                    if st:
                        x = st.pop()
                        st.append(math.acos(x))
                case 'ATAN':
                    if st:
                        st.append(math.atan(st.pop()))
                case 'ACOT':
                    if st:
                        x = st.pop()
                        st.append(math.pi/2 - math.atan(x))
                case 'FLOOR':
                    if st:
                        st.append(math.floor(st.pop()))
                case 'CEILING':
                    if st:
                        st.append(math.ceil(st.pop()))
                case 'SQRT':
                    if st:
                        x = st.pop()
                        if x < 0:
                            raise ValueError("Square root of a negative number")
                        st.append(math.sqrt(x))
                case 'CBRT':
                    if st:
                        x = st.pop()
                        st.append(math.cbrt(x))
                case 'SQR':
                    if st:
                        x = st.pop()
                        st.append(x * x)
                case 'CBR':
                    if st:
                        x = st.pop()
                        st.append(x * x * x)
                case 'ROOT':
                    if len(st) >= 2:
                        n = st.pop()
                        x = st.pop()
                        if x < 0 and n % 2 == 0:
                            raise ValueError("Even root of a negative number")
                        st.append(x ** (1/n))
    
    if len(st) != 1:
        raise ValueError("Invalid expression")
    
    return st[0]

def calculate_infix_expression(expression):
    try:
        postfix = infix_to_postfix(expression)
        return calculate_postfix_expression(postfix)
    except Exception as e:
        raise ValueError(f"Error: {e}")