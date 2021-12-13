# sk-math

A simple WIP math language with its own compiler written in Python.

## Usage
| Action                  | Command                         |
| ----------------------- | ------------------------------- |
| Write code in editor    | python main.py                  |
| Compile code from file  | python main.py -f \<FILENAME\>  |
| Help                    | python main.py -h               |

#### Editor
I know it sucks but it will get better :D

F10 to compile the written code

## Features

The language currently supports the following operations:
- Addition ( + )
- Subtraction ( - )
- Multiplication ( * )
- Division ( / )
- Exponentiation ( ^ )
- Variable Declarations and Assignments
- Function Definitions and Calls
- Outputs

## Documentation

#### Statements
Statements build the base structure of your code.

A statement can be one of the following:
- Variable Declaration / Assignment
- Function Declaration
- Output

A new line ends a statement and starts a new one

#### Expressions
An expression can be one of the following:
- ```5``` Constant
- ```x``` Variable
- ```foo(x, 1)``` Function Call
- ```5 * x + foo(x, 1) ^ 2``` Arithmetic Expression

Precedences for arithmetic expression follow the basic mathematical rules.

Parantheses are not supported yet.

#### Variable Declaration
- Single Variable Declaration: ```var x```
- Multiple Variable Declaration: ```var x, y, z```

Variables can not be declared more than once in a scope.

#### Variable Assignment
- Constant Assignment: ```x = 5```
- Variable Assignment: ```y = 3 * x + 4.6```

Variables need to be declared before a value can be assigned to them.

The assigned value has to be an expression.

#### Function Definition
```
func foo(x, y, z) {
  var a = x + y
  return a * z
}
```

Functions start a new scope.

Functions always need to have a return statement as the last statement.

Newlines are mandatory after the opening and before the closing brace.

#### Function Calls
```x = foo(1, y, 3) + z```

A function call is not a statement. It always has to be used as an expression.

The actual parameters need to be either constants or variable identifiers. You can not use an expression as a parameter.

#### Outputs
```out 5```

```out 7 + bar(1) * a```

Outputs always need to be an expression.

## Grammar (CFG)

I use a simple LL(2) Top-Down-Parser.

The language is based on the following grammar:

- Language ::= Statement ( '\n' Statement )*
- Statement ::= SimpleStatement | FuncDefinition
- FuncDefinition ::= 'func' ('void' | Type) ID '(' FuncParams ')' '{' FuncBody '}'
- FuncCall ::= ID '(' FuncParams ')'
- FuncParams ::= Ɛ | (Type ID (',' Type ID)*)
- FuncBody ::= ('\n' SimpleStatement)* '\n' (SimpleStatement) '\n'
- SimpleStatement ::= VarDecl | VarAssign | Out | FuncCall | ReturnStatement
- ReturnStatement ::= 'return' Expr
- VarDecl ::= Type ID (',' ID)*
- VarAssign ::= ID '=' Expr
- Out ::= 'out' Expr
- Expr ::= AddSub ( '\n' AddSub )*
- AddSub ::= MulDiv ( ( '+' | '-' ) MulDiv )*
- MulDiv ::= Exponentiation ( ( '\*' | '/' ) Exponentiation )*
- Exponentiation ::= Atom ( '^' Atom )*
- Type ::= 'int' | 'float'
- Atom ::= INT | FLOAT | ID | FuncCall
