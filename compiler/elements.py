from enum import Enum
from typing import Any

class ParsedType(Enum):
    STATEMENTS = "statements"
    VAR_DECLARATION = "var_declaration"
    VAR_ASSIGNMENT = "var_assignment"
    OUT_STATEMENT = "out_statement"
    SUBTRACTION = "subtraction"
    ADDITION = "addition"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    EXPONENTIATION = "exponentiation"
    IDENTIFIER = "identifier"
    CONST = "const"


class ParsedElement:
    def __init__(self, a: Any, b: Any, parsed_type: ParsedType):
        self.a = a
        self.b = b
        self.parsed_type = parsed_type

    @staticmethod
    def _print_rec(element, depth: int = 0):
        if element is not None:
            for i in range(0, depth):
                print("|  ", end="")
            if type(element) == float or type(element) == int or type(element) == str:
                print(element)
            else:
                print(element.parsed_type)
                if type(element.a) == list:
                    for item in element.a:
                        ParsedElement._print_rec(item, depth + 1)
                else:
                    ParsedElement._print_rec(element.a, depth + 1)
                ParsedElement._print_rec(element.b, depth + 1)

    def print(self):
        self._print_rec(self, 0)
