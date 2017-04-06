import re
import sys

"""
Tokenizes the input file of the quirk language specification and sends tokens to standard output.
Uses the undocumented Scannner class (which I found here http://lucumr.pocoo.org/2015/11/18/pythons-hidden-re-gems/)
to tokenize the text, basically its an easy way to combine regular expressions but order matters so Indent and Number
must be after keywords.
Will raise exception if unsupported characters are used.

if this is too cheaty I attached my original lexer (lexer2.py).
"""


class LexingError(Exception):
    """raises an exception if an unsupported character is used """
    pass


"""returns tokens for the corresponding pattern match"""
scanner = re.Scanner([
    (r'\s+', None,),
    (r'\n', None,),
    (r'var', 'VAR',),
    (r'function', 'FUNCTION',),
    (r'return', 'RETURN',),
    (r'print', 'PRINT',),
    (r'[a-zA-Z]+[a-zA-Z0-9_]*', lambda scan, token: 'IDENT:' + token),
    (r'(\d+(\.\d*)?)|(\.\d+)', lambda scan, token: 'NUMBER:' + token),
    (r'\=', 'ASSIGN',),
    (r'\+', 'ADD',),
    (r'\-', 'SUB',),
    (r'\*', 'MULT',),
    (r'\/', 'DIV',),
    (r'\^', 'EXP',),
    (r'\(', 'LPAREN',),
    (r'\)', 'RPAREN',),
    (r'\{', 'LBRACE',),
    (r'\}', 'RBRACE',),
    (r'\,', 'COMMA',),
    (r'\:', 'COLON'),
])


def read_input():
    """
    reads the input file from standard input, tokenizes, and sends tokens to standard ouput.
    """
    lines = sys.stdin.readlines()
    for line in lines:
        tokens = scanner.scan(line.__str__())
        if len(tokens[1]) > 0:
            raise LexingError(tokens[1], "These tokens are not supported")
        for token in tokens[0]:
            sys.stdout.write(token + '\n')
    sys.stdout.write('EOF\n')

if __name__ == "__main__":
    read_input()
