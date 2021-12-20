from typing import Type as PythonType


class Executor:
    def __init__(self):
        self._table: IdentificationTable = IdentificationTable[PYTHON_PRIMITIVE_TYPE]()

    @staticmethod
    def _get_python_type_from_type(type: "Type") -> PythonType:
        switch = {
            Type.INT: int,
            Type.FLOAT: float
        }
        return switch[type]

    def execute_module(self, module: "Module"):
        self._table.open_scope()
        for statement in module.statements:
            statement.execute(self)
        self._table.close_scope()

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

    def execute_call_expression(self, call: "CallExpression"):
        self._table.open_scope()
        definition: "FunctionDefinition" = call.get_function_definition()
        for i in range(0, len(call.actual_parameters)):
            identifier: str = definition.formal_parameters[i].identifier
            value: PYTHON_PRIMITIVE_TYPE = call.actual_parameters[i].execute(self)
            self._table.add_identifier(identifier, value, call)
        for statement in definition.body:
            if isinstance(statement, ReturnStatement):
                value = statement.execute(self)
                self._table.close_scope()
                return value
            statement.execute(self)
        self._table.close_scope()

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
        print(value)

    def execute_function_call(self, call: "FunctionCall"):
        call.call_expression.execute(self)

    def execute_return_statement(self, statement: "ReturnStatement"):
        return statement.expression.execute(self)


from compiler.ast.ast import *
from compiler.identification_table import IdentificationTable
