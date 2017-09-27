# Quirk python interpreter

These programs are used to interpret the quirk language. Quirk has limited functionality but can declare variables, functions, perform basic arithmetic, and print arguments.
The specifications for the Quirk language can be found [here](https://github.com/dr-jam/csc521/tree/master/quirk).

## Getting Started

### Prerequisites

Python 3

### Execution
Each program (lexer, parser, interpreter) can be run individually.

To run the lexer with a given input file:
```
python lexer.py < yourprogram.q
```

To run the parser :
```
python lexer.py < yourprogram.q | python parser.py
```

To execute a quirk program from source text:
```
python lexer.py < yourprogram.q | python parser.py | python interpreter.py
```
print statements will output to console and to a "quirk.out" file

## Details

The lexer expects a text file of the quirk program and outputs tokens. The parser will create a parse tree (top-down) from the lexer's tokens and outputs a JSON parse tree. The interpreter will execute this parse tree, outputting arguments to the console and to a "quirk.out" file if printed.

I found a python class from the default re module that greatly simplifies my lexer. I provided my original lexer (lexer2.py) if this seems too easy (or not full credit).

My parser is also different than the suggested implementation. It is a generalized solution that can be modified to parse different languages from a provided grammar specification, more details in that file.
