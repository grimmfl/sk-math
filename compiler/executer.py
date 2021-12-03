from typing import List, Callable

from compiler.elements import ParsedElement, ParsedType
from helpers import Stack
from typing import Dict


class Executer:
    def __init__(self):
        self.expressions: List[ParsedElement] = []
        self.identifiers: Dict[str, Stack] = {}
        self.scopes: Stack[List[str]] = Stack()
        self.functions: Dict[str, Callable] = {}

    @staticmethod
    def _get_elements_as_list(element) -> List[ParsedElement]:
        if not isinstance(element, ParsedElement):
            return []
        if element.parsed_type == ParsedType.NEWL:
            return Executer._get_elements_as_list(element.a) + Executer._get_elements_as_list(element.b)
        return [element]

    def _pop_scope(self):
        for identifier in self.scopes.pop():
            self.identifiers[identifier].pop()

    def _declare_variables(self, identifiers: List[ParsedElement], throwaway):
        for identifier in identifiers:
            if identifier.a in self.scopes.peak():
                raise Exception(f"The identifier '{identifier.a}' has been declared already.")
            if identifier.a not in self.identifiers.keys():
                self.identifiers[identifier.a] = Stack()
            self.scopes.peak().append(identifier.a)

    def _call_function(self, identifier: ParsedElement, params: ParsedElement):
        return self.functions[identifier.a](params)

    def _resolve_expression(self, expression: ParsedElement) -> int or float:
        switch = {
            ParsedType.ADDITION: lambda a, b: self._resolve_expression(a) + self._resolve_expression(b),
            ParsedType.SUBTRACTION: lambda a, b: self._resolve_expression(a) - self._resolve_expression(b),
            ParsedType.MULTIPLICATION: lambda a, b: self._resolve_expression(a) * self._resolve_expression(b),
            ParsedType.DIVISION: lambda a, b: self._resolve_expression(a) / self._resolve_expression(b),
            ParsedType.EXPONENTIATION: lambda a, b: self._resolve_expression(a) ** self._resolve_expression(b),
            ParsedType.FUNC_CALL: self._call_function,
            ParsedType.CONST: lambda a, b: a,
            ParsedType.IDENTIFIER: lambda a, b: self.identifiers[a].peak()
        }
        return switch[expression.parsed_type](expression.a, expression.b)

    def _assign_variable(self, identifier: ParsedElement, value: ParsedElement):
        if identifier.a in self.scopes.peak():
            self.identifiers[identifier.a].push(self._resolve_expression(value))
        else:
            raise Exception(f"'{identifier.a}' is not declared.")

    def _define_function(self, identifier: ParsedElement, info: ParsedElement):
        def func(params: ParsedElement):
            self.scopes.push([])
            expected_length = len(info.a.a)
            actual_length = len(params.a)
            if expected_length > actual_length:
                raise Exception(f"At function call {identifier.a}: Expected {expected_length} param(s) - Got {actual_length}")

            param_ids = info.a.a
            for i in range(0, len(param_ids)):
                if param_ids[i] in self.identifiers.keys():
                    raise Exception(f"At function call {identifier.a}: Identifier {param_ids[i].a} is already in use.")
                self.identifiers[param_ids[i].a] = Stack()
                self.identifiers[param_ids[i].a].push(self._resolve_expression(params.a[i]))

            statements = info.b.a
            self._execute_statements(statements[:-1], None)
            return_value = self._resolve_expression(statements[-1])
            self._pop_scope()
            return return_value
        self.functions[identifier.a] = func

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
            ParsedType.FUNC_DEFINITION: self._define_function,
        }
        if element.parsed_type in switch.keys():
            switch[element.parsed_type](element.a, element.b)

    def execute(self, element: ParsedElement):
        self.scopes.push([])
        self._execute_element(element)
