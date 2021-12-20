from typing import Dict, TypeVar, Generic

from compiler.errors import *
from helpers import Stack

T = TypeVar("T")


class IdentificationTable(Generic[T]):
    def __init__(self):
        self._identifiers: Dict[str, Stack[T]] = {}
        self._scopes: Stack[List[str]] = Stack()
        self._functions: Dict[str, "FunctionDefinition"] = {}
        for function in PREDEFINED_FUNCTIONS:
            function(self)

    def add_identifier(self, identifier: str, t: T, node: "AstNode"):
        if identifier in self._scopes.peak():
            raise IdentifierInUseError(identifier, node)
        self._scopes.peak().append(identifier)
        if identifier not in self._identifiers.keys():
            self._identifiers[identifier] = Stack()
        self._identifiers[identifier].push(t)

    def update_identifier(self, identifier: str, t: T, node: "AstNode"):
        if identifier not in self._identifiers.keys():
            raise IdentifierNotDeclaredError(identifier, node)
        self._identifiers[identifier].pop()
        self._identifiers[identifier].push(t)

    def get_identifier(self, identifier: str, node: "AstNode") -> T:
        if identifier not in self._identifiers.keys():
            raise IdentifierNotDeclaredError(identifier, node)
        if self._identifiers[identifier].peak() is None:
            raise IdentifierNotAssignedError(identifier, node)
        return self._identifiers[identifier].peak()

    def open_scope(self):
        self._scopes.push([])

    def close_scope(self):
        for identifier in self._scopes.peak():
            self._identifiers[identifier].pop()
        self._scopes.pop()

    def add_function(self, name: str, definition: "FunctionDefinition"):
        if name in self._functions.keys():
            raise FunctionNameInUseError(name, definition)
        self._functions[name] = definition

    def get_function(self, name: str, node: "AstNode") -> "FunctionDefinition":
        if name not in self._functions.keys():
            raise FunctionNotDefinedError(name, node)
        return self._functions[name]


from compiler.ast.ast import *
from compiler.predefined.functions import PREDEFINED_FUNCTIONS
