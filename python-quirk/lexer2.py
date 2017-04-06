import re
import sys

"""
Tokenizes the input file of the quirk language specification and sends tokens to standard output.
"""


class LexingError(Exception):
    """raises an exception if an unsupported character is used """
    pass

# precompile regular expressions
numbers = re.compile(r"^((\d+(\.\d*)?)|(\.\d+))$")
idents = re.compile(r"^[a-zA-Z]+[a-zA-Z0-9_]*$")
symbol = re.compile(r"([+\-*/\^(){\},:=])")

# keywords and symbols reserved by the language
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
    """
    Uses regular expressions to find indents or numbers
    :param code: chunk of code being tokenized
    :return: a literal(ident or number) token, or a list of tokens
    """
    if idents.match(code):
        return 'IDENT:' + code + '\n'
    elif numbers.match(code):
        return 'NUMBER:' + code + '\n'
    elif symbol.search(code):
        return mixed(code)
    else:
        raise LexingError("error, character ", code, " not supported")


def mixed(code):
    """
    splits the chunk of code by symbols and gets the tokens. This means math expressions are whitespace agnostic.
    :param code: chunk of code being tokenized
    :return: list of tokens of the code
    """
    parts = symbol.split(code)
    tk = ''
    for part in parts:
        if part != '':
            tk += find(part)
    return tk


def find(code):
    """
    checks if the string is in the lexicon, if not test for literals and mixed.
    :param code: chunk of code being tokenized
    :return: token or tokens of the code
    """
    token = lexicon.get(code)
    if token is None:
        token = literals(code)
    return token


def tokenize(source_code):
    """
    splits code by whitespace then looks for tokens, output tokens to stdout
    :param source_code: line of the source code
    :return:
    """
    chunks = source_code.split()
    for chunk in chunks:
        sys.stdout.write(find(chunk))


def read_input():
    """
    reads the quirk source code from stdin
    """
    lines = sys.stdin.readlines()
    for l in lines:
        line = l.__str__()
        tokenize(line)
    sys.stdout.write("EOF\n")


if __name__ == "__main__":
    read_input()
