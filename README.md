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

#### Variable Declaration
- Single Variable Declaration: ```var x```
- Multiple Variable Declaration: ```var x, y, z```

Variables can not be declared more than once in a scope.

#### Variable Assignment
- Constant Assignment: ```x = 5```
- Variable Assignment: ```y = 3 * x + 4.6```

Variables need to be declared because a value can be assigned to them

#### Function Definition
```
func foo(x, y, z) {
  var a = x + y
  return a * z
}
```
- Functions start a new scope.
- Functions always need to have a return statement as the last statement.
- Newlines are mandatory after the opening and before the closing brace.

#### Function Calls
```x = foo(1, y, 3) + z```
- A function call is not a statement. It always has to be used as an expression.
- The actual parameters need to be either constants or variable identifiers. You can not use an expression as a parameter.

#### Outputs
```out 5```

```out 7 + bar(1) * a```

Outputs always need to be an expression.

A new line starts a new command.

Parantheses are not supported yet.

## Grammar (CFG)

I use a simple Top-Down-Parser, so left recursion is not supported.

The language is based on the following grammar:

- Language ::= Statement ( '\n' Statement )*
- Statement ::= SimpleStatement | FuncDefinition
- FuncDefinition ::= 'func' ID '(' FuncParams ')' '{' FuncBody '}'
- FuncCall ::= ID '(' FuncParams ')'
- FuncParams ::= Ɛ | (ID (',' ID)*)
- FuncBody ::= ('\n' SimpleStatement)* '\n' ReturnStatement '\n'
- ReturnStatement ::= 'return' Expr
- SimpleStatement ::= VarDecl | VarAssign | Out
- VarDecl ::= var ID (',' ID)*
- VarAssign ::= ID '=' Expr
- Out ::= 'out' Expr
- Expr ::= AddSub ( '\n' AddSub )*
- AddSub ::= MulDiv ( ( '+' | '-' ) MulDiv )*
- MulDiv ::= Exponentiation ( ( '\*' | '/' ) Exponentiation )*
- Exponentiation ::= Atom ( '^' Atom )*
- Atom ::= INT | FLOAT | ID | FuncCall
