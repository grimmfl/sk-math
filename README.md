# sk-math

A simple WIP math language with its own compiler written in Python.

### Usage

python main.py -f <FILENAME>

Currently, you can only compile scripts from a file. I am working on an editor. 

### Features

The language currently supports the following operations:
- Addition ( + )
- Subtraction ( - )
- Multiplication ( * )
- Division ( / )
- Exponentiation ( ^ )
- Variable Declaration: var x, y, z
- Variable Assignments: x = 4 * y + z
- Outputs: out x + 4

A new line starts a new command.

Parantheses are not supported yet.

I use a simple Top-Down-Parser, so left recursion is not supported.

The language is based on the following grammar:

- Language ::= Statement ( '\n' Statement )*
- Statement ::= VarDecl | VarAssign | Out
- VarDecl ::= var ID (',' ID)*
- VarAssign ::= ID '=' Expr
- Out ::= 'out' Expr
- Expr ::= AddSub ( '\n' AddSub )*
- AddSub ::= MulDiv ( ( '+' | '-' ) MulDiv )*
- MulDiv ::= Exponentiation ( ( '\*' | '/' ) Exponentiation )*
- Exponentiation ::= Atom ( '^' Atom )*
- Atom ::= INT | FLOAT | ID
