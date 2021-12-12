from enum import Enum
from typing import Any, Tuple


class NodeName(Enum):
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
    FUNC_DEFINITION = "func_definition"
    FUNC_INFO = "func_info"
    FUNC_PARAMS = "func_params"
    FUNC_BODY = "func_body"
    FUNC_CALL = "func_call"
    FUNC_CALL_PARAMS = "func_call_params"


class AstNode:
    def __init__(self, a: Any, b: Any, name: NodeName, location: Tuple[int, int]):
        self.a = a
        self.b = b
        self.name = name

    @staticmethod
    def _print_rec(element, depth: int = 0):
        if element is not None:
            for i in range(0, depth):
                print("|  ", end="")
            if type(element) == float or type(element) == int or type(element) == str:
                print(element)
            else:
                print(element.name)
                if type(element.a) == list:
                    for item in element.a:
                        AstNode._print_rec(item, depth + 1)
                else:
                    AstNode._print_rec(element.a, depth + 1)
                AstNode._print_rec(element.b, depth + 1)

    def print(self):
        self._print_rec(self, 0)
