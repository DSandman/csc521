These programs are used to interpret the quirk language, which has limited in functionality.
to run a quirk program:

python lexer.py < yourprogram.q | python parser.py | python interpreter.py

the lexer.py will create tokens of the input text
the parser.py will create an AST of those tokens 
and the interpreter.py will execute the AST
