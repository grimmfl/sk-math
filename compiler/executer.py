from typing import List

from compiler.elements import ParsedElement, ParsedType
from helpers import Stack
from typing import Dict


class Executer:
    def __init__(self):
        self.expressions: List[ParsedElement] = []
        self.identifiers: Dict[str, Stack] = {}

    @staticmethod
    def _get_elements_as_list(element) -> List[ParsedElement]:
        if not isinstance(element, ParsedElement):
            return []
        if element.parsed_type == ParsedType.NEWL:
            return Executer._get_elements_as_list(element.a) + Executer._get_elements_as_list(element.b)
        return [element]

    def _declare_variables(self, identifiers: List[ParsedElement], throwaway):
        for identifier in identifiers:
            if identifier.a in self.identifiers.keys():
                raise Exception(f"The identifier {identifier.a} has been declared already.")
            self.identifiers[identifier.a] = Stack()

    def _resolve_expression(self, expression: ParsedElement) -> int or float:
        switch = {
            ParsedType.ADDITION: lambda a, b: self._resolve_expression(a) + self._resolve_expression(b),
            ParsedType.SUBTRACTION: lambda a, b: self._resolve_expression(a) - self._resolve_expression(b),
            ParsedType.MULTIPLICATION: lambda a, b: self._resolve_expression(a) * self._resolve_expression(b),
            ParsedType.DIVISION: lambda a, b: self._resolve_expression(a) / self._resolve_expression(b),
            ParsedType.EXPONENTIATION: lambda a, b: self._resolve_expression(a) ** self._resolve_expression(b),
            ParsedType.CONST: lambda a, b: a,
            ParsedType.IDENTIFIER: lambda a, b: self.identifiers[a].peak()
        }
        return switch[expression.parsed_type](expression.a, expression.b)

    def _assign_variable(self, identifier: ParsedElement, value: ParsedElement):
        if identifier.a in self.identifiers.keys():
            self.identifiers[identifier.a].push(self._resolve_expression(value))
        else:
            raise Exception(f"There is no declared variable for the identifier {identifier.a}.")

    def _print(self, expression: ParsedElement, throwaway):
        print(self._resolve_expression(expression))

    def _execute_statements(self, statements: List[ParsedElement], throwaway):
        for statement in statements:
            self._execute_element(statement)

    def _execute_element(self, element: ParsedElement) -> int or float:
        switch = {
            ParsedType.STATEMENTS: self._execute_statements,
            ParsedType.VAR_DECLARATION: self._declare_variables,
            ParsedType.VAR_ASSIGNMENT: self._assign_variable,
            ParsedType.OUT_STATEMENT: self._print,
        }
        if element.parsed_type in switch.keys():
            switch[element.parsed_type](element.a, element.b)

    def execute(self, element: ParsedElement):
        self._execute_element(element)
