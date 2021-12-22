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
- Logical Or ( || )
- Logical And ( && )
- Logical Not ( ! )
- Comparisons ( ==, !=, <=, >=, <, > )
- Addition ( + )
- Subtraction ( - )
- Multiplication ( * )
- Division ( / )
- Modulo ( % )
- Exponentiation ( ^ )
- Unary Minus ( - )
- Arrays
- Variable Declarations and Assignments
- Function Definitions and Calls
- If Statements
- Outputs

## Documentation

#### Statements
Statements build the base structure of your code.

A statement can be one of the following:
- Variable Declaration / Assignment
- Function Declaration
- Function Call
- Output
- If Statements

A new line ends a statement and starts a new one

#### Expressions
An expression can be one of the following:
- ```5``` Constant
- ```x``` Variable
- ```foo(x, 1)``` Function Call
- ```(5 * (x + foo(x, 1))) ^ 2``` Arithmetic Expression
- ```x < 5 && y == 27 + 3 || !false``` Boolean Expression

#### Operator Precedences
|   | Symbol          | Operator                          |
| - | --------------- | --------------------------------- |
| 1 | - !             | Unary Minus, Logical Not          |
| 2 | * / %           | Multiplication, Division, Modulo  |
| 3 | + -             | Addition, Subtraction             |
| 4 | == != <= >= < > | Comparisons                       |
| 5 | &&              | Logical and                       |
| 6 | \|\|            | Logical or                        |

You can use parentheses to work around those precedences.

#### If Statements
```
if (x < 5) {
    int y = 3 + 2
    z = y * 7
}
```

The condition needs to be of type ```bool```.

The body needs to start with ```{``` followed by a newline and end with a newline followed by ```}```.

```
if (x < 5) {
    int y = 3 + 2
    z = y * 7
} elif (x < 7) {
    z = z + 7
} elif (x == 7) {
    x = 0
} else {
    z = 2
}
```

If Statements can have multiple ```elif``` blocks and one ```else``` block. The ```elif``` and ```else``` keywords needs to be after the closing ```}``` without a newline.

The body needs to start with ```{``` followed by a newline and end with a newline followed by ```}```.

If Statements can be nested.

#### Variable Declaration
- Single Variable Declaration: ```int x```
- Multiple Variable Declaration: ```float x, y, z```

Variables can not be declared more than once in a scope.

#### Variable Assignment
- Constant Assignment: ```x = true```
- Variable Assignment: ```y = 3.0 * x + 4.6```

Variables need to be declared before a value can be assigned to them.
If the variable is declared as ```float``` the value needs to be a float too. ```4``` is not a float value.

#### Arrays
Array Declaration: ```int[4] testArray1, testArray2```

You can declare arrays by naming the element type, followed by the size of the array surrounded by squared brackets.

Array Assignments:

There are different kinds of assignments:
- Array Assignment: ```testArray1 = [1, 2, 3, 4]```
- Element Assignment: ```testArray2[0] = 10```

You can also use array elements in an expression: ```testArray1[2] + 25```
Or you can use the whole array as an expression: ```out testArray1```

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

The body needs to start with ```{``` followed by a newline and end with a newline followed by ```}```.

If a function has a return type, it needs to return a value of that type.

If your functions does not return anything, you can use ```void``` as the return type:

```
func void bar(int x) {
    out x + 5
}
```

#### Predefined Functions

The following functions are already implemented:

```func float sqrt(float x)``` calculates the square root of a float x

```func float intToFloat(int x)``` casts an integer to a float

```func int floatToInt(float x)``` casts a float to an integer

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
- Statement ::= SimpleStatement | FuncDefinition | IfStatement
- FuncDefinition ::= 'func' ('void' | Type) ID '(' FuncParams ')' '{' Body '}'
- FuncCall ::= ID '(' FuncParams ')'
- FuncParams ::= Ɛ | (Type ID (',' Type ID)*)
- Body ::= ('\n' Statement)* '\n' (Statement) '\n'
- SimpleStatement ::= VarDecl | VarAssign | Out | FuncCall | ReturnStatement
- IfStatement ::= 'if' '(' Expr ')' '{' Body '}' ElifStatement* (ElseStatement | Ɛ)
- ElifStatement ::= 'elif' '(' Expr ')' '{' Body '}'
- ElseStatement ::= 'else' '{' Body '}'
- ReturnStatement ::= 'return' Expr
- VarDecl ::= Type ID (',' ID)*
- VarAssign ::= (ID '=' Expr) | ArrayElementAssign
- ArrayElementAssign ::= ID '\[' Expr '\]' = Expr
- Out ::= 'out' Expr
- Expr ::= Or
- Or ::= And ( '||' And )*
- And ::= Comparison ( '&&' Comparison)*
- Comparison ::= AddSub (Ɛ | (ComparisonOp AddSub))
- ComparisonOp ::= '==' | '!=' | '<=' | '>=' | '<' | '>'
- AddSub ::= MulDiv ( ( '+' | '-' ) MulDiv )*
- MulDiv ::= Exponentiation ( ( '\*' | '/' ) Exponentiation )*
- Exponentiation ::= Atom ( '^' Atom )*
- Type ::= ('int' | 'float' | 'bool') (Ɛ | '\[' Expr '\]')
- Atom ::= INT | FLOAT | ID | FuncCall | 'true' | 'false'
- Array ::= '\[' (Ɛ | (Expr (',' Expr)*)) '\]'
- ArrayElementSelection ::= ID '\[' Expr '\]'
