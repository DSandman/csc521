import re
import sys


class LexingError(Exception):
    '''raises an exception if an unsupported character is used '''
    pass


numbers = re.compile(r"^((\d+(\.\d*)?)|(\.\d+))$")
idents = re.compile(r"^[a-zA-Z]+[a-zA-Z0-9_]*$")
symbol = re.compile(r"([\+\-\*/\^\(\)\{\},:=])")

lexicon = {
    'var': 'VAR\n',
    'function': 'FUNCTION\n',
    'return': 'RETURN\n',
    'print': 'PRINT\n',
    '=': 'ASSIGN\n',
    '+': 'ADD\n',
    '-': 'SUB\n',
    '*': 'MULT\n',
    '/': 'DIV\n',
    '^': 'EXP\n',
    '(': 'LPAREN\n',
    ')': 'RPAREN\n',
    '{': 'LBRACE\n',
    '}': 'RBRACE\n',
    ',': 'COMMA\n',
    ':': 'COLON\n'
}


def literals(code):
    if idents.match(code):
        return 'IDENT:' + code + '\n'
    elif numbers.match(code):
        return 'NUMBER:' + code + '\n'
    elif symbol.search(code):
        return mixed(code)
    else:
        print("error, character " + code + " not supported")


def mixed(code):
    parts = symbol.split(code)
    tk = ''
    for part in parts:
        if part != '':
            tk += find(part)
    return tk


def find(code):
    token = lexicon.get(code)
    if token is None:
        token = literals(code)
    return token


def tokenize(source_code):
    chunks = source_code.split()
    for chunk in chunks:
        sys.stdout.write(find(chunk))


def ReadInput():
    lines = sys.stdin.readlines()
    for l in lines:
        line = l.__str__()
        tokenize(line)
    sys.stdout.write("EOF\n")


def main():
    ReadInput()


if __name__ == "__main__": main()
