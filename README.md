# sk-math

A simple WIP math language with its own compiler written in Python.

### Features

The compiler is not finished yet. Only the Parser is implemented.

The language currently supports the following operations:
- Addition ( + )
- Subtraction ( - )
- Multiplication ( * )
- Division ( / )
- Exponentiation ( ^ )

The language is based on the following grammar:
- Expression ::= AddSub
- AddSub ::= MulDiv ( ( '+' | '-' ) MulDiv )*
- MulDiv ::= Exponentiation ( ( '\*' | '/' ) Exponentiation )*
- Exponentiation ::= Atom ( '^' Atom )*
- Atom ::= INT | FLOAT
