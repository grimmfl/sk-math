from enum import Enum
from typing import Any, Callable, Generic, TypeVar


class ExpressionType(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    EXP = "^"
    ATOM = "atom"


class Expression:
    def __init__(self, a: Any, b: Any, expression_type: ExpressionType):
        self.a = a
        self.b = b
        self.type = ExpressionType


class Atom(Expression):
    def __init__(self, x: int or float, is_float: int):
        super().__init__(x, is_float, ExpressionType.ATOM)


class Exponentiation(Expression):
    def __init__(self, base: Expression, exponentiator: Expression):
        super().__init__(base, exponentiator, ExpressionType.EXP)


class Multiplication(Expression):
    def __init__(self, a: Expression, b: Expression):
        super().__init__(a, b, ExpressionType.MUL)


class Division(Expression):
    def __init__(self, a: Expression, b: Expression):
        super().__init__(a, b, ExpressionType.DIV)


class Addition(Expression):
    def __init__(self, a: Expression, b: Expression):
        super().__init__(a, b, ExpressionType.ADD)


class Subtraction(Expression):
    def __init__(self, a: Expression, b: Expression):
        super().__init__(a, b, ExpressionType.SUB)

