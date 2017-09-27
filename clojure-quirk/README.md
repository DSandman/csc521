# Quirk clojure interpreter

This program is used to interpret the quirk language. Quirk has limited functionality but can declare variables, functions, perform basic arithmetic, and print arguments.
The specifications for the Quirk language can be found [here](https://github.com/dr-jam/csc521/tree/master/quirk).

## Getting Started

### Prerequisites

[leiningen](https://leiningen.org/)

### Execution
The parser and interpreter can be run individually.

To run the parser and print the parse tree:
```
lein run -pt < yourprogram.q
```

To execute a quirk program from source text:
```
lein run < yourprogram.q
```
print statements will output to console and to a "quirk.out" file

## Details

The [instaparse](https://github.com/Engelberg/instaparse) modual was used to easily create a parse tree from the quirk grammar. The grammar was modified (Number => MyNumber) as not to override the java method. The grammar can be found in [resources](https://github.com/DSandman/csc521/tree/master/clojure-quirk/resources) file.

The source code in [src](https://github.com/DSandman/csc521/tree/master/clojure-quirk/src/clojure_quirk).

