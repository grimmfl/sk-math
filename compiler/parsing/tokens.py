from enum import Enum


class Token(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    EXP = "^"
    MOD = "%"
    NEWL = "\n"
    INT = "int"
    FLOAT = "float"
    VOID = "void"
    ASSIGN = "="
    OUT = "out"
    COMMA = ","
    IDENTIFIER = "id"
    FUNC = "func"
    LPARAN = "("
    RPARAN = ")"
    LBRACE = "{"
    RBRACE = "}"
    RETURN = "return"
