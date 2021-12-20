from typing import Tuple, List, Any, Callable

from compiler.ast.types import *


class AstNode:
    def __init__(self, location: Tuple[int, int]):
        self.location = location

    @staticmethod
    def _print_type(node: Any):
        for attribute in node.__dict__.keys():
            if attribute.startswith("_"):
                print(f": {node.__dict__.get(attribute)}", end="")
                return

    @staticmethod
    def _print_rec(node: Any, depth: int = 0):
        if node is not None:
            if not type(node) == list:
                for i in range(0, depth):
                    print("| ", end="")
            if isinstance(node, AstNode):
                print(node.__class__.__name__, end="")
                AstNode._print_type(node)
                print()
                for attribute in node.__dict__.keys():
                    if attribute != "location":
                        AstNode._print_rec(node.__dict__.get(attribute), depth + 1)
            elif type(node) == list:
                for sub_node in node:
                    AstNode._print_rec(sub_node, depth)
            else:
                print(node)

    def print(self):
        self._print_rec(self)

    def visit(self, visitor_instance: "Visitor"):
        pass

    def execute(self, executor_instance: "Executor"):
        return executor_instance


class Statement(AstNode):
    def __init__(self, location: Tuple[int, int]):
        super().__init__(location)


class Module(AstNode):
    def __init__(self, statements: List[Statement], location: Tuple[int, int]):
        self.statements: List[Statement] = statements
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_module(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_module(self)


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

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_addition(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_addition(self)


class Subtraction(Expression):
    def __init__(self, left_operand: Expression, right_operand: Expression, location: Tuple[int, int]):
        self.left_operand: Expression = left_operand
        self.right_operand: Expression = right_operand
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_subtraction(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_subtraction(self)


class Multiplication(Expression):
    def __init__(self, left_operand: Expression, right_operand: Expression, location: Tuple[int, int]):
        self.left_operand: Expression = left_operand
        self.right_operand: Expression = right_operand
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_multiplication(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_multiplication(self)


class Division(Expression):
    def __init__(self, left_operand: Expression, right_operand: Expression, location: Tuple[int, int]):
        self.left_operand: Expression = left_operand
        self.right_operand: Expression = right_operand
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_division(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_division(self)


class Exponentiation(Expression):
    def __init__(self, base: Expression, power: Expression, location: Tuple[int, int]):
        self.base: Expression = base
        self.power: Expression = power
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_exponentiation(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_exponentiation(self)


class IdentifierReference(Expression):
    def __init__(self, identifier: str, location: Tuple[int, int]):
        self.identifier: str = identifier
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_identifier_reference(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_identifier_reference(self)


class Constant(Expression):
    def __init__(self, value: int or float, location: Tuple[int, int]):
        self.value: int or float = value
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_constant(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_constant(self)


class FormalParameter(AstNode):
    def __init__(self, type: Type, identifier: str, location: Tuple[int, int]):
        self.type: Type = type
        self.identifier: str = identifier
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_formal_parameter(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_formal_parameter(self)


class FunctionDefinition(Statement):
    def __init__(self, name: str, return_type: ReturnType, formal_parameters: List[FormalParameter], body: List[Statement],
                 location: Tuple[int, int]):
        self.name: str = name
        self.return_type: ReturnType = return_type
        self.formal_parameters: List[FormalParameter] = formal_parameters
        self.body: List[Statement] = body
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_function_definition(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_function_definition(self)


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

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_call_expression(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_call_expression(self)


class CustomExpression(Expression):
    def __init__(self, expression: Expression, function: Callable[[Any], Any], location: Tuple[int, int]):
        self.expression: Expression = expression
        self.function: Callable[[Any], Any] = function
        super().__init__(location)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_custom_expression(self)


class SimpleStatement(Statement):
    def __init__(self, location: Tuple[int, int]):
        super().__init__(location)


class VariableDeclaration(SimpleStatement):
    def __init__(self, type: Type, identifiers: List[str], location: Tuple[int, int]):
        self.type: Type = type
        self.identifiers: List[str] = identifiers
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_variable_declaration(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_variable_declaration(self)


class VariableAssignment(SimpleStatement):
    def __init__(self, identifier: str, value: Expression, location: Tuple[int, int]):
        self.identifier: str = identifier
        self.value: Expression = value
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_variable_assignment(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_variable_assignment(self)


class OutStatement(SimpleStatement):
    def __init__(self, expression: Expression, location: Tuple[int, int]):
        self.expression: Expression = expression
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_out_statement(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_out_statement(self)


class FunctionCall(SimpleStatement):
    def __init__(self, call_expression: CallExpression, location: Tuple[int, int]):
        self.call_expression: CallExpression = call_expression
        super().__init__(location)

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_function_call(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_function_call(self)


class ReturnStatement(SimpleStatement):
    def __init__(self, expression: Expression, location: Tuple[int, int]):
        self.expression: Expression = expression
        super().__init__(location)

        self._return_type: ReturnType = None

    def set_return_type(self, return_type: ReturnType):
        self._return_type = return_type

    def get_return_type(self) -> ReturnType:
        return self._return_type

    def is_return_type_set(self) -> bool:
        return self._return_type is not None

    def visit(self, visitor_instance: "Visitor"):
        return visitor_instance.visit_return_statement(self)

    def execute(self, executor_instance: "Executor"):
        return executor_instance.execute_return_statement(self)


from compiler.contextual_analysis.visitor import Visitor
from compiler.execution.executor import Executor
