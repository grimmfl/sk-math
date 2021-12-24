from typing import List
from typing import Type as PythonType


class Executor:
    def __init__(self):
        self._table: IdentificationTable = IdentificationTable[PYTHON_TYPE]()

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
        p_type: PythonType = comparison.get_type().python_type
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
        p_type: PythonType = addition.get_type().python_type
        left_op: p_type = addition.left_operand.execute(self)
        right_op: p_type = addition.right_operand.execute(self)
        return left_op + right_op

    def execute_subtraction(self, subtraction: "Subtraction"):
        p_type: PythonType = subtraction.get_type().python_type
        left_op: p_type = subtraction.left_operand.execute(self)
        right_op: p_type = subtraction.right_operand.execute(self)
        return left_op - right_op

    def execute_multiplication(self, multiplication: "Multiplication"):
        p_type: PythonType = multiplication.get_type().python_type
        left_op: p_type = multiplication.left_operand.execute(self)
        right_op: p_type = multiplication.right_operand.execute(self)
        return left_op * right_op

    def execute_division(self, division: "Division"):
        p_type: PythonType = division.get_type().python_type
        left_op: p_type = division.left_operand.execute(self)
        right_op: p_type = division.right_operand.execute(self)
        return left_op / right_op

    def execute_modulo(self, modulo: "Modulo"):
        p_type: PythonType = modulo.get_type().python_type
        left_op: p_type = modulo.left_operand.execute(self)
        right_op: p_type = modulo.right_operand.execute(self)
        return left_op % right_op

    def execute_exponentiation(self, exponentiation: "Exponentiation"):
        p_type: PythonType = exponentiation.get_type().python_type
        left_op: p_type = exponentiation.base.execute(self)
        right_op: p_type = exponentiation.power.execute(self)
        return left_op ** right_op

    def execute_unary_minus(self, unary_minus: "UnaryMinus"):
        p_type: PythonType = unary_minus.get_type().python_type
        value: p_type = unary_minus.value.execute(self)
        return -value

    def execute_not(self, not_expr: "Not"):
        value: bool = not_expr.value.execute(self)
        return not value

    def execute_identifier_reference(self, reference: "IdentifierReference"):
        return self._table.get_identifier(reference.identifier, reference)

    def execute_array_element_selection(self, selection: "ArrayElementSelection"):
        array: list = self._table.get_identifier(selection.identifier, selection)
        index: int = selection.index.execute(self)
        if index < 0 or index >= len(array):
            raise ArrayIndexOutOfBoundsError(index, selection.index)
        return array[index]

    def execute_array_sub_selection(self, selection: "ArraySubSelection"):
        array: list = self._table.get_identifier(selection.identifier, selection)
        from_index: int = 0 if selection.from_index is None else selection.from_index.execute(self)
        to_index: int = len(array) if selection.to_index is None else selection.to_index.execute(self)
        if from_index < 0 or from_index >= len(array):
            raise ArrayIndexOutOfBoundsError(from_index, selection.from_index)
        if to_index < 0 or to_index >= len(array):
            raise ArrayIndexOutOfBoundsError(to_index, selection.to_index)
        return array[from_index:to_index]

    def execute_array(self, array: "Array"):
        value = []
        for element in array.elements:
            value.append(element.execute(self))
        return value

    def execute_constant(self, constant: "Constant"):
        return constant.value

    def execute_formal_parameter(self, parameter: "FormalParameter"):
        self._table.add_identifier(parameter.identifier, None, parameter)

    def execute_function_definition(self, definition: "FunctionDefinition"):
        self._table.add_function(definition.name, definition)

    def execute_if_statement(self, if_statement: "IfStatement"):
        if if_statement.condition.execute(self):
            return self._execute_body(if_statement.body)
        for elif_statement in if_statement.elifs:
            if elif_statement.condition.execute(self):
                return self._execute_body(elif_statement.body)
        else:
            return self._execute_body(if_statement.else_body)

    def execute_for_statement(self, for_statement: "ForStatement"):
        array: List = for_statement.array.execute(self)
        self._table.add_identifier(for_statement.element_name, None, for_statement)
        for element in array:
            self._table.update_identifier(for_statement.element_name, element, for_statement)
            for statement in for_statement.body:
                statement.execute(self)
        self._table.delete_identifier(for_statement.element_name)

    def execute_call_expression(self, call: "CallExpression"):
        self._table.open_scope()
        definition: "FunctionDefinition" = call.get_function_definition()
        for i in range(0, len(call.actual_parameters)):
            identifier: str = definition.formal_parameters[i].identifier
            value: PYTHON_PRIMITIVE_TYPE = call.actual_parameters[i].execute(self)
            self._table.add_identifier(identifier, value, call)
        return_value = self._execute_body(definition.body)
        if isinstance(definition.return_type, ArrayType):
            formal_size: int = definition.return_type.size.execute(self)
            if formal_size != len(return_value):
                raise InvalidArraySizeError(formal_size, len(return_value), call)
        self._table.close_scope()
        return return_value

    def _execute_body(self, body: List["Statement"]):
        for statement in body:
            value = statement.execute(self)
            if isinstance(statement, ReturnStatement) or value is not None:
                return value

    def execute_custom_unary_function(self, expression: "CustomUnaryFunction"):
        value: PYTHON_PRIMITIVE_TYPE = expression.expression.execute(self)
        return expression.function(value)

    def execute_custom_binary_function(self, expression: "CustomBinaryFunction"):
        value1: PYTHON_PRIMITIVE_TYPE = expression.expression1.execute(self)
        value2: PYTHON_PRIMITIVE_TYPE = expression.expression2.execute(self)
        return expression.function(value1, value2)

    def execute_variable_declaration(self, declaration: "VariableDeclaration"):
        value = None
        if isinstance(declaration.type, ArrayType):
            size: int = declaration.type.size.execute(self)
            if size < 0:
                raise NegativeArraySizeError(size, declaration)
            none_array: list = [None for x in range(0, size)]
            value = none_array
        for identifier in declaration.identifiers:
            self._table.add_identifier(identifier, value, declaration)

    def execute_variable_assignment(self, assignment: "VariableAssignment"):
        value: PYTHON_TYPE = assignment.value.execute(self)
        value_type: Type = assignment.value.get_type()
        if isinstance(value_type, ArrayType):
            value: list = value
            old_array = self._table.get_identifier(assignment.identifier, assignment)
            if len(old_array) != len(value):
                raise InvalidArraySizeError(len(old_array), len(value), assignment)
        self._table.update_identifier(assignment.identifier, value, assignment)

    def execute_array_element_assignment(self, assignment: "ArrayElementAssignment"):
        array: list = self._table.get_identifier(assignment.identifier, assignment)
        index: int = assignment.index.execute(self)
        if index < 0 or index >= len(array):
            raise ArrayIndexOutOfBoundsError
        value: PYTHON_PRIMITIVE_TYPE = assignment.value.execute(self)
        array[index] = value
        self._table.update_identifier(assignment.identifier, array, assignment)

    def execute_out_statement(self, out: "OutStatement"):
        value: PYTHON_TYPE = out.expression.execute(self)
        print(self._to_output(value))

    def execute_function_call(self, call: "FunctionCall"):
        call.call_expression.execute(self)

    def execute_return_statement(self, statement: "ReturnStatement"):
        return statement.expression.execute(self)

    @staticmethod
    def _to_output(value: "PYTHON_TYPE") -> str:
        if type(value) is list:
            return "[" + ", ".join(Executor._to_output(element) for element in value) + "]"
        if type(value) is bool:
            return "true" if value else "false"
        return str(value)


from compiler.ast.ast import *
from compiler.identification_table import IdentificationTable
from compiler.errors import NegativeArraySizeError, ArrayIndexOutOfBoundsError, InvalidArraySizeError
