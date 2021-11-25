from enum import Enum


class Token(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    EXP = "^"
    NEWL = "\n"
    ATOM = "atom"
