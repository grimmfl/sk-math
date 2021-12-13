from enum import Enum
from typing import Any, Tuple, List


#class AstNode:
#    def __init__(self, a: Any, b: Any, name: NodeName, location: Tuple[int, int]):
#        self.a = a
#        self.b = b
#        self.name = name
#
#    @staticmethod
#    def _print_rec(element, depth: int = 0):
#        if element is not None:
#            for i in range(0, depth):
#                print("|  ", end="")
#            if type(element) == float or type(element) == int or type(element) == str:
#                print(element)
#            else:
#                print(element.name)
#                if type(element.a) == list:
#                    for item in element.a:
#                        AstNode._print_rec(item, depth + 1)
#                else:
#                    AstNode._print_rec(element.a, depth + 1)
#                AstNode._print_rec(element.b, depth + 1)
#
#    def print(self):
#        self._print_rec(self, 0)
#

class Type(Enum):
    INT = "int"
    FLOAT = "float"


class ReturnType(Type):
    VOID = "void"


class AstNode:
    def __init__(self, location: Tuple[int, int]):
        self.location = location


class Statement(AstNode):
    def __init__(self, location: Tuple[int, int]):
        super().__init__(location)


class Module(AstNode):
    def __init__(self, statements: List[Statement], location: Tuple[int, int]):
        self.statements: List[Statement] = statements
        super().__init__(location)


class Expression(AstNode):
    def __init__(self, location: Tuple[int, int]):
        self._type: Type = None
        super().__init__(location)

    def is_type_set(self) -> bool:
        return self._type is None

    def set_type(self, type: Type):
        self._type = type

    def get_type(self) -> Type:
        return self._type


class Addition(Expression):
    def __init__(self, left_operand: Expression, right_operand: Expression, location: Tuple[int, int]):
        self.left_operand: Expression = left_operand
        self.right_operand: Expression = right_operand
        super().__init__(location)


class Subtraction(Expression):
    def __init__(self, left_operand: Expression, right_operand: Expression, location: Tuple[int, int]):
        self.left_operand: Expression = left_operand
        self.right_operand: Expression = right_operand
        super().__init__(location)


class Multiplication(Expression):
    def __init__(self, left_operand: Expression, right_operand: Expression, location: Tuple[int, int]):
        self.left_operand: Expression = left_operand
        self.right_operand: Expression = right_operand
        super().__init__(location)


class Division(Expression):
    def __init__(self, left_operand: Expression, right_operand: Expression, location: Tuple[int, int]):
        self.left_operand: Expression = left_operand
        self.right_operand: Expression = right_operand
        super().__init__(location)


class Exponentiation(Expression):
    def __init__(self, base: Expression, power: Expression, location: Tuple[int, int]):
        self.base: Expression = base
        self.power: Expression = power
        super().__init__(location)


class IdentifierReference(Expression):
    def __init__(self, identifier: str, location: Tuple[int, int]):
        self.identifier: str = identifier
        super().__init__(location)


class Constant(Expression):
    def __init__(self, value: int or float, location: Tuple[int, int]):
        self.value: int or float = value
        super().__init__(location)


class FormalParameter(AstNode):
    def __init__(self, type: Type, identifier: str, location: Tuple[int, int]):
        self.type: Type = type
        self.identifier: str = identifier
        super().__init__(location)


class FunctionDefinition(Statement):
    def __init__(self, name: str, return_type: ReturnType, formal_parameters: List[FormalParameter], body: List[SimpleStatement],
                 location: Tuple[int, int]):
        self.name: str = name
        self.return_type: ReturnType = return_type
        self.formal_parameters: List[FormalParameter] = formal_parameters
        self.body: List[Statement] = body
        super().__init__(location)


class CallExpression(Expression):
    def __init__(self, name: str, actual_parameters: List[Expression], location: Tuple[int, int]):
        self.name: str = name
        self.actual_parameters: List[Expression] = actual_parameters
        super().__init__(location)

        self._function_definition: FunctionDefinition = None

    def is__function_definition_set(self) -> bool:
        return self._function_definition is None

    def get_function_definition(self) -> FunctionDefinition:
        return self._function_definition

    def set_function_definition(self, definition: FunctionDefinition):
        self._function_definition = definition


class SimpleStatement(Statement):
    def __init__(self, location: Tuple[int, int]):
        super().__init__(location)


class VariableDeclaration(SimpleStatement):
    def __init__(self, type: Type, identifiers: List[str], location: Tuple[int, int]):
        self.type: Type = type
        self.identifiers: List[str] = identifiers
        super().__init__(location)


class VariableAssignment(SimpleStatement):
    def __init__(self, identifier: str, value: Expression, location: Tuple[int, int]):
        self.identifier: str = identifier
        self.value: Expression = value
        super().__init__(location)


class OutStatement(SimpleStatement):
    def __init__(self, expression: Expression, location: Tuple[int, int]):
        self.expression: Expression = expression
        super().__init__(location)


class FunctionCall(SimpleStatement):
    def __init__(self, call_expression: CallExpression, location: Tuple[int, int]):
        self.call_expression: CallExpression = call_expression
        super().__init__(location)


class ReturnStatement(SimpleStatement):
    def __init__(self, expression: Expression, location: Tuple[int, int]):
        self.expression: Expression = expression
        super().__init__(location)
