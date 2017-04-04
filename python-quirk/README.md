These programs are used to interpret the quirk language. Quirk has limited functionality but can declare variables and
functions, perform basic arithmetic, and print arguments.

Each program can be run individually. To run a quirk program from source text pipe the files like so:
python lexer.py < yourprogram.q | python parser.py | python interpreter.py

print statements will output to a "quirk.out" file

the lexer expects a text file of the quirk program, it creates tokens from the text.
the parser will create a parse tree from the lexer's tokens.
and the interpreter will execute the parse tree outputing arguments if printed.

I found a class from the default re module that greatly simplifies my lexer. If this seems too lazy (or not full credit)
I provided original lexer(lexer2.py) which is a more standard approach.
