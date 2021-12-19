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
- Function Call
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
- Single Variable Declaration: ```int x```
- Multiple Variable Declaration: ```float x, y, z```

Variables can not be declared more than once in a scope.

#### Variable Assignment
- Constant Assignment: ```x = 5```
- Variable Assignment: ```y = 3.0 * x + 4.6```

Variables need to be declared before a value can be assigned to them.
If the variable is declared as ```float``` the value needs to be a float too. ```4``` is not a float value.

#### Function Definition
```
func int foo(int x, int y, int z) {
  var a = x + y
  return a * z
}
```

Functions start a new scope.

The ```func``` keyword is followed by the return type of the function.

Parameters are separated with a ```,``` and need to have a type.

If a function has a return type, it needs to return a value of that type.

If your functions does not return anything, you can use ```void``` as the return type:

```
func void bar(int x) {
    out x + 5
}
```

#### Function Calls
Function calls can be used as statements:

```foo(1, y, 3)```

or  as expressions:

```x = foo(1, y, 3) + z```

The actual parameters can be expressions and need to match the formal parameters of the function definition in count and type.

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
