from compiler.tokens import Token
from typing import Tuple


class SyntaxError(Exception):
    def __init__(self, expected: Token, got: str, location: Tuple[int, int]):
        self.message = f"Expected {expected} - Got '{got}' at ({location[0] + 1}, {location[1] + 1})"
        super(SyntaxError, self).__init__(self.message)