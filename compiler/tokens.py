from enum import Enum


class Token(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    EXP = "^"
    NEWL = "\n"
    VAR = "var"
    ASSIGN = "="
    OUT = "out"
    COM = ","
    CONST = "const"
    ID = "id"
    FUNC = "func"
    LPARAN = "("
    RPARAN = ")"
    LBRACE = "{"
    RBRACE = "}"
    RETURN = "return"
