#{} and () and ; Are uh. Something?

import sys

forbidden = ["while", "print", "let"]#, "if", "else", "elif"]
# token = ("type", "value", ("row", "col"), "special error (empty by defult)") #type if for what type of error to throw
irrelevant = ["{", "}", "(", ")", ";"]


def tokenize(text):
    token = []
    row = -1
    column = 0
    n = 0

    while n < len(text):
        char = text[n]
        row += 1
        if char == " ":
            n += 1
            continue
        elif char.isalpha() or char == "_":
            #its just not rendering for some reason
            
            #get the whole thing.
            word = ""
            while n < len(text):
                if text[n].isalpha() or text[n].isdigit() or text[n] == "_":
                    word += text[n] #build the word hahahah
                    n += 1
                else:
                    break
            #you got the complete word
            #start = n, end = i-1
            if word in forbidden:
                match word:
                    case "let":
                        token.append(("TLet", (row, column), ""))
                    case "while":
                        token.append(("TWhile", (row, column), ""))
                    case "print":
                        token.append(("TPrint", (row, column), ""))
            else:
                token.append(("TVar", (row, column), word))
        elif char.isdigit():
            word = ""
            while n < len(text):
                if text[n].isdigit():
                    word += text[n]
                    n += 1
                else:
                    break
            token.append(("TNumber", (row, column), word))
        elif char == "=":
            if text[n+1] == "=":
                n += 2
                token.append(("TEqEq", (row, column), ""))
            else:
                token.append(("TEq", (row, column), ""))
                n += 1
        elif char == ">":
            token.append(("TMoreThan", (row, column), ""))
            n += 1
        elif char == "+":
            token.append(("TPlus", (row, column), "+"))
            n += 1
        elif char == "-":
            token.append(("TMinus", (row, column), "-"))
            n += 1

        elif char in irrelevant:
            match char:
                case ";":
                    token.append(("TSemiCol", (row, column), ""))
                    n += 1
                case "{":
                    token.append(("TStartCurl", (row, column), ""))
                    n += 1
                case "}":
                    token.append(("TEndCurl", (row, column), ""))
                    n += 1
                case "(":
                    token.append(("TStartBrac", (row, column), ""))
                    n += 1
                case ")":
                    token.append(("TEndBrac", (row, column), ""))
                    n += 1
        
        elif char == "\n":
            n += 1
            column +=1 #i've flipped row and column..
            row = 0
                    
        else:
            n += 1
          
        
    return token
        # match char:
        #     case " ": #isspace

# print(tokenize("\naa bbb print(-) while \n yay == hi = hi")) #this is the lexer


# class parser:

# def __init__(self, tokens):
#     self.tok, self.i = tokens, 0

# def peek_next(tokens):
#     return tokens[-1]
    
def peek(tokens):
    return tokens[-1]

def throw_error(now):
    raise SyntaxError(f"Line {now[1][0]+1}, Column {now[1][1]+1}")

def expect(tokens, typ):
    now = tokens.pop()
    if now[0] != typ:
        raise SyntaxError(now, f"Expected {typ}")
    return now

# def parse_truefalse(tokens):
    # now = tokens.pop()


# def parse_while(tokens):
#     now = tokens.pop()
#     if now[0] != "TWhile": #Suddenly not a while loop
#         SyntaxError(f"Expected TWhile, got {now[0]}")
#     parse_truefalse(tokens)

#     now = tokens.pop()
#     if now[0] != "TStartCurl":
#         SyntaxError(f"Expected TStartCurl, got {now[0]}")


def parse_operad(tokens):
    typ, pos, text = tokens.pop()
    if typ == "TNumber":
        return ("number", text)
    if typ == "TVar":
        return ("variable", text)
    throw_error ((typ, pos, text))

# def parse_arithmetic(tokens): #

def parse_value(tokens):
    left = parse_operad(tokens)

    while peek(tokens)[0] in ("TPlus", "TMinus"):
        op = tokens.pop()
        right = parse_operad(tokens)
        left = ("binop", op[2], left, right)
    
    return left

def parse_condition(tokens):
    left = parse_operad(tokens)
    expect(tokens, "TMoreThan")
    right = parse_operad(tokens)
    return ("compare", ">", left, right)

            
def parse_block(tokens):# (statements*)
    expect(tokens, "TStartCurl")
    statements = []

    while peek(tokens)[0] != "TEndCurl": #??
        statements.append(parse_statement(tokens))
        # if not tokens and now[0] != "TEndCurl": #didnt end with curly brackets. thats ok though...?
    expect(tokens, "TEndCurl")
    return statements

def parse_statement(tokens): # Tokens -> interpreit
    typ = peek(tokens)[0] #TLet TWhile TPrint TVar

    if typ == "TLet": #"let" VARIABLE "=" value ";"            
        tokens.pop() #Get rid of TLet

        name = expect(tokens, "TVar")[2]
        expect(tokens, "TEq")
        value = parse_value(tokens)
        expect(tokens, "TSemiCol")
        return ("declare", name, value)
            # if peek_next(tokens) == "TEq":
        # if now == "TEq":
        #     if tokens[-1][0] in ["TNumber", "TVar"]: #number or a variable
    elif typ == "TVar":
        name = tokens.pop()[2]
        expect(tokens, "TEq")
        value = parse_value(tokens)
        expect(tokens, "TSemiCol")
        return ("assign", name, value)
    
    elif typ == "TPrint":
        tokens.pop()
        expect(tokens, "TStartBrac")
        value = parse_value(tokens)
        expect(tokens, "TEndBrac")
        expect(tokens, "TSemiCol")
        return ("print", "", value)
    
    elif typ == "TWhile":
        tokens.pop()
        condition = parse_condition(tokens)
        statements = parse_block(tokens)
        expect(tokens, "TSemiCol")
        return ("while", condition, statements)
    else:
        throw_error(peek(tokens))

def parse_program(tokens):
    tokens.reverse()
    statement = []
    while tokens:
        statement.append(parse_statement(tokens))
    return ("program", statement)



#----- treee
#('program', [('declare', 'a', ('number', '0')), ('declare', 'b', ('number', '1')), ('declare', 'c', ('number', '0')), 
# ('declare', 'n', ('number', '10')), ('while', ('compare', '>', ('variable', 'n'), ('number', '0')), 
# [('print', '', ('variable', 'a')), ('assign', 'c', ('binop', '+', ('variable', 'a'), ('variable', 'b'))), 
# ('assign', 'a', ('variable', 'b')), ('assign', 'b', ('variable', 'c')), ('assign', 'n', ('binop', '-', ('variable', 'n'), ('number', '1')))])])

def print_tree(node, depth=0):
    indentering = "   " * depth

    typ = node[0]
    if typ == "program":
        print(indentering + "program")
        for syntax in node[1]: #big list program, [...]
            print_tree(syntax, depth + 1)

    elif typ in ("declare", "assign"): # ('declare', 'a', ('number', '0'))
        print(f"{indentering}{typ} ({node[1]})")
        print_tree(node[2], depth + 1)

    elif typ == "print":
        print(indentering + "print")
        print_tree(node[2], depth + 1)

    elif typ == "while":
        print(indentering + "while")
        print_tree(node[1], depth + 1)
        for syntax in node[2]:
            print_tree(syntax, depth + 1)

    elif typ in ("compare", "binop"):
        print(f"{indentering}{typ} ({node[1]})")
        print_tree(node[2], depth + 1)
        print_tree(node[3], depth + 1)

    else:
        print(f"{indentering}{typ} ({node[1]})")



tokens = tokenize(open(sys.argv[1]).read())
tree = parse_program(tokens) #sys.argv[1] -> python main.py fib.txt -> [main.py, fib.txt]
print_tree(tree)


#("declare", name, value) -> name = value
#("assign", name, value) -> name = value
#("print", "", value) -> print(value)
#("while", condition, body) -> while condition:
#   body -> 3 spaces in
#("compare", ">", l, r) -> l > r
#("binop", "+", l, r) -> l + r
