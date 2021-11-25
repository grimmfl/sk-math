from typing import Any

from token import Token


class Expression:
    def __init__(self, a: Any, b: Any, expression_type: Token):
        self.a = a
        self.b = b
        self.type = expression_type

    @staticmethod
    def _print_rec(expression, depth: int = 0):
        for i in range(0, depth):
            print("|  ", end="")
        if isinstance(expression, Expression):
            print(expression.type)
            Expression._print_rec(expression.a, depth + 1)
            Expression._print_rec(expression.b, depth + 1)
        elif type(expression) == int or type(expression) == float:
            print(expression)

    def print(self):
        self._print_rec(self, 0)


class Atom(Expression):
    def __init__(self, x: int or float, is_float: int):
        super().__init__(x, is_float, Token.ATOM)


class Exponentiation(Expression):
    def __init__(self, base: Expression, exponentiator: Expression):
        super().__init__(base, exponentiator, Token.EXP)


class Multiplication(Expression):
    def __init__(self, a: Expression, b: Expression):
        super().__init__(a, b, Token.MUL)


class Division(Expression):
    def __init__(self, a: Expression, b: Expression):
        super().__init__(a, b, Token.DIV)


class Addition(Expression):
    def __init__(self, a: Expression, b: Expression):
        super().__init__(a, b, Token.ADD)


class Subtraction(Expression):
    def __init__(self, a: Expression, b: Expression):
        super().__init__(a, b, Token.SUB)

