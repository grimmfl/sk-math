import ctypes.wintypes
from typing import Type as PythonType
from typing import List


class Executor:
    def __init__(self):
        self._table: IdentificationTable = IdentificationTable[PYTHON_PRIMITIVE_TYPE]()

    @staticmethod
    def _get_python_type_from_type(type: "Type") -> PythonType:
        switch = {
            Type.INT: int,
            Type.FLOAT: float,
            Type.BOOL: bool,
        }
        return switch[type]

    def execute_module(self, module: "Module"):
        self._table.open_scope()
        for statement in module.statements:
            statement.execute(self)
        self._table.close_scope()

    def execute_or(self, or_expr: "Or"):
        left_op: bool = or_expr.left_operand.execute(self)
        right_op: bool = or_expr.right_operand.execute(self)
        return left_op or right_op

    def execute_and(self, and_expr: "And"):
        left_op: bool = and_expr.left_operand.execute(self)
        right_op: bool = and_expr.right_operand.execute(self)
        return left_op and right_op

    def execute_comparison(self, comparison: "Comparison"):
        p_type: PythonType = self._get_python_type_from_type(comparison.get_type())
        left_op: p_type = comparison.left_operand.execute(self)
        right_op: p_type = comparison.right_operand.execute(self)
        switch = {
            ComparisonType.EQUAL: lambda x, y: x == y,
            ComparisonType.NOT_EQUAL: lambda x, y: x != y,
            ComparisonType.LESS_EQUAL: lambda x, y: x <= y,
            ComparisonType.GREATER_EQUAL: lambda x, y: x >= y,
            ComparisonType.LESS: lambda x, y: x < y,
            ComparisonType.GREATER: lambda x, y: x > y,
        }
        return switch[comparison.comparison_type](left_op, right_op)

    def execute_addition(self, addition: "Addition"):
        p_type: PythonType = self._get_python_type_from_type(addition.get_type())
        left_op: p_type = addition.left_operand.execute(self)
        right_op: p_type = addition.right_operand.execute(self)
        return left_op + right_op

    def execute_subtraction(self, subtraction: "Subtraction"):
        p_type: PythonType = self._get_python_type_from_type(subtraction.get_type())
        left_op: p_type = subtraction.left_operand.execute(self)
        right_op: p_type = subtraction.right_operand.execute(self)
        return left_op - right_op

    def execute_multiplication(self, multiplication: "Multiplication"):
        p_type: PythonType = self._get_python_type_from_type(multiplication.get_type())
        left_op: p_type = multiplication.left_operand.execute(self)
        right_op: p_type = multiplication.right_operand.execute(self)
        return left_op * right_op

    def execute_division(self, division: "Division"):
        p_type: PythonType = self._get_python_type_from_type(division.get_type())
        left_op: p_type = division.left_operand.execute(self)
        right_op: p_type = division.right_operand.execute(self)
        return left_op / right_op

    def execute_modulo(self, modulo: "Modulo"):
        p_type: PythonType = self._get_python_type_from_type(modulo.get_type())
        left_op: p_type = modulo.left_operand.execute(self)
        right_op: p_type = modulo.right_operand.execute(self)
        return left_op % right_op

    def execute_exponentiation(self, exponentiation: "Exponentiation"):
        p_type: PythonType = self._get_python_type_from_type(exponentiation.get_type())
        left_op: p_type = exponentiation.base.execute(self)
        right_op: p_type = exponentiation.power.execute(self)
        return left_op ** right_op

    def execute_identifier_reference(self, reference: "IdentifierReference"):
        return self._table.get_identifier(reference.identifier, reference)

    def execute_constant(self, constant: "Constant"):
        return constant.value

    def execute_formal_parameter(self, parameter: "FormalParameter"):
        self._table.add_identifier(parameter.identifier, None, parameter)

    def execute_function_definition(self, definition: "FunctionDefinition"):
        self._table.add_function(definition.name, definition)

    def execute_if_statement(self, if_statement: "IfStatement"):
        if if_statement.condition.execute(self):
            return self._execute_body(if_statement.body)
        else:
            return self._execute_body(if_statement.else_body)

    def execute_call_expression(self, call: "CallExpression"):
        self._table.open_scope()
        definition: "FunctionDefinition" = call.get_function_definition()
        for i in range(0, len(call.actual_parameters)):
            identifier: str = definition.formal_parameters[i].identifier
            value: PYTHON_PRIMITIVE_TYPE = call.actual_parameters[i].execute(self)
            self._table.add_identifier(identifier, value, call)
        return_value = self._execute_body(definition.body)
        self._table.close_scope()
        return return_value

    def _execute_body(self, body: List["Statement"]):
        for statement in body:
            value = statement.execute(self)
            if isinstance(statement, ReturnStatement) or value is not None:
                return value

    def execute_custom_expression(self, expression: "CustomExpression"):
        value: PYTHON_PRIMITIVE_TYPE = expression.expression.execute(self)
        return expression.function(value)

    def execute_variable_declaration(self, declaration: "VariableDeclaration"):
        for identifier in declaration.identifiers:
            self._table.add_identifier(identifier, None, declaration)

    def execute_variable_assignment(self, assignment: "VariableAssignment"):
        value: PYTHON_PRIMITIVE_TYPE = assignment.value.execute(self)
        self._table.update_identifier(assignment.identifier, value, assignment)

    def execute_out_statement(self, out: "OutStatement"):
        value: PYTHON_PRIMITIVE_TYPE = out.expression.execute(self)
        print(self._to_output(value))

    def execute_function_call(self, call: "FunctionCall"):
        call.call_expression.execute(self)

    def execute_return_statement(self, statement: "ReturnStatement"):
        return statement.expression.execute(self)

    @staticmethod
    def _to_output(value: "PYTHON_PRIMITIVE_TYPE") -> str:
        if type(value) is bool:
            return "true" if value else "false"
        return str(value)


from compiler.ast.ast import *
from compiler.identification_table import IdentificationTable
