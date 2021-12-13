from enum import Enum


class Token(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    EXP = "^"
    NEWL = "\n"
    INT = "int"
    FLOAT = "float"
    VOID = "void"
    ASSIGN = "="
    OUT = "out"
    COM = ","
    ID = "id"
    FUNC = "func"
    LPARAN = "("
    RPARAN = ")"
    LBRACE = "{"
    RBRACE = "}"
    RETURN = "return"
