from typing import List, Callable

from compiler.ast import AstNode, NodeName
from helpers import Stack
from typing import Dict


class Executer:
    def __init__(self):
        self.expressions: List[AstNode] = []
        self.identifiers: Dict[str, Stack] = {}
        self.scopes: Stack[List[str]] = Stack()
        self.functions: Dict[str, Callable] = {}

    @staticmethod
    def _get_elements_as_list(element) -> List[AstNode]:
        if not isinstance(element, AstNode):
            return []
        if element.name == NodeName.NEWL:
            return Executer._get_elements_as_list(element.a) + Executer._get_elements_as_list(element.b)
        return [element]

    def _pop_scope(self):
        for identifier in self.scopes.pop():
            self.identifiers[identifier].pop()

    def _declare_variables(self, identifiers: List[AstNode], throwaway):
        for identifier in identifiers:
            if identifier.a in self.scopes.peak():
                raise Exception(f"The identifier '{identifier.a}' has been declared already.")
            if identifier.a not in self.identifiers.keys():
                self.identifiers[identifier.a] = Stack()
            self.scopes.peak().append(identifier.a)

    def _call_function(self, identifier: AstNode, params: AstNode):
        return self.functions[identifier.a](params)

    def _resolve_expression(self, expression: AstNode) -> int or float:
        switch = {
            NodeName.ADDITION: lambda a, b: self._resolve_expression(a) + self._resolve_expression(b),
            NodeName.SUBTRACTION: lambda a, b: self._resolve_expression(a) - self._resolve_expression(b),
            NodeName.MULTIPLICATION: lambda a, b: self._resolve_expression(a) * self._resolve_expression(b),
            NodeName.DIVISION: lambda a, b: self._resolve_expression(a) / self._resolve_expression(b),
            NodeName.EXPONENTIATION: lambda a, b: self._resolve_expression(a) ** self._resolve_expression(b),
            NodeName.FUNC_CALL: self._call_function,
            NodeName.CONST: lambda a, b: a,
            NodeName.IDENTIFIER: lambda a, b: self.identifiers[a].peak()
        }
        return switch[expression.name](expression.a, expression.b)

    def _assign_variable(self, identifier: AstNode, value: AstNode):
        if identifier.a in self.scopes.peak():
            self.identifiers[identifier.a].push(self._resolve_expression(value))
        else:
            raise Exception(f"'{identifier.a}' is not declared.")

    def _define_function(self, identifier: AstNode, info: AstNode):
        def func(params: AstNode):
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

    def _print(self, expression: AstNode, throwaway):
        print(self._resolve_expression(expression))

    def _execute_statements(self, statements: List[AstNode], throwaway):
        for statement in statements:
            self._execute_element(statement)

    def _execute_element(self, element: AstNode) -> int or float:
        switch = {
            NodeName.STATEMENTS: self._execute_statements,
            NodeName.VAR_DECLARATION: self._declare_variables,
            NodeName.VAR_ASSIGNMENT: self._assign_variable,
            NodeName.OUT_STATEMENT: self._print,
            NodeName.FUNC_DEFINITION: self._define_function,
        }
        if element.name in switch.keys():
            switch[element.name](element.a, element.b)

    def execute(self, element: AstNode):
        self.scopes.push([])
        self._execute_element(element)
