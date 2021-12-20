import typing_extensions

from compiler.errors import *
from compiler.ast.ast import *


class Visitor:
    def __init__(self):
        self._table = IdentificationTable[Type]()

    @staticmethod
    def _check_type(node: "AstNode", type1: Type, type2: Type):
        if type1 != type2:
            raise TypeError(node, type1, type2)

    def visit_module(self, module: "Module"):
        self._table.open_scope()
        for statement in module.statements:
            statement.visit(self)
        self._table.close_scope()

    def visit_addition(self, addition: "Addition") -> Type:
        l_type: Type = addition.left_operand.visit(self)
        r_type: Type = addition.right_operand.visit(self)
        if not l_type.is_numeric():
            raise TypeError(addition, NUMERIC_TYPES, l_type)
        if not r_type.is_numeric():
            raise TypeError(addition, NUMERIC_TYPES, r_type)
        self._check_type(addition, l_type, r_type)
        addition.set_type(l_type)
        return l_type

    def visit_subtraction(self, subtraction: "Subtraction") -> Type:
        l_type: Type = subtraction.left_operand.visit(self)
        r_type: Type = subtraction.right_operand.visit(self)
        if not l_type.is_numeric():
            raise TypeError(subtraction, NUMERIC_TYPES, l_type)
        if not r_type.is_numeric():
            raise TypeError(subtraction, NUMERIC_TYPES, r_type)
        self._check_type(subtraction, l_type, r_type)
        subtraction.set_type(l_type)
        return l_type

    def visit_multiplication(self, multiplication: "Multiplication") -> Type:
        l_type: Type = multiplication.left_operand.visit(self)
        r_type: Type = multiplication.right_operand.visit(self)
        if not l_type.is_numeric():
            raise TypeError(multiplication, NUMERIC_TYPES, l_type)
        if not r_type.is_numeric():
            raise TypeError(multiplication, NUMERIC_TYPES, r_type)
        self._check_type(multiplication, l_type, r_type)
        multiplication.set_type(l_type)
        return l_type

    def visit_division(self, division: "Division") -> Type:
        l_type: Type = division.left_operand.visit(self)
        r_type: Type = division.right_operand.visit(self)
        if not l_type.is_numeric():
            raise TypeError(division, NUMERIC_TYPES, l_type)
        if not r_type.is_numeric():
            raise TypeError(division, NUMERIC_TYPES, r_type)
        self._check_type(division, l_type, r_type)
        division.set_type(l_type)
        return l_type

    def visit_modulo(self, modulo: "Modulo") -> Type:
        l_type: Type = modulo.left_operand.visit(self)
        r_type: Type = modulo.right_operand.visit(self)
        self._check_type(modulo, l_type, Type.INT)
        self._check_type(modulo, r_type, Type.INT)
        modulo.set_type(Type.INT)
        return Type.INT

    def visit_exponentiation(self, exponentiation: "Exponentiation") -> Type:
        l_type: Type = exponentiation.base.visit(self)
        r_type: Type = exponentiation.power.visit(self)
        if not l_type.is_numeric():
            raise TypeError(exponentiation, NUMERIC_TYPES, l_type)
        if not r_type.is_numeric():
            raise TypeError(exponentiation, NUMERIC_TYPES, r_type)
        self._check_type(exponentiation, l_type, r_type)
        exponentiation.set_type(l_type)
        return l_type

    def visit_identifier_reference(self, reference: "IdentifierReference") -> Type:
        type: Type = self._table.get_identifier(reference.identifier, reference)
        reference.set_type(type)
        return type

    def visit_constant(self, constant: "Constant") -> Type:
        switch = {
            float: Type.FLOAT,
            int: Type.INT
        }
        return switch[type(constant.value)]

    def visit_call_expression(self, expression: "CallExpression") -> Type:
        definition: FunctionDefinition = self._table.get_function(expression.name, expression)
        if len(expression.actual_parameters) != len(definition.formal_parameters):
            raise ArgumentCountError(definition.formal_parameters, expression.actual_parameters)
        for i in range(0, len(definition.formal_parameters)):
            formal_type: Type = definition.formal_parameters[i].type
            actual_type: Type = expression.actual_parameters[i].visit(self)
            self._check_type(expression, formal_type, actual_type)
        switch = {
            ReturnType.VOID: None,
            ReturnType.INT: Type.INT,
            ReturnType.FLOAT: Type.FLOAT
        }
        type: Type = switch[definition.return_type]
        expression.set_type(type)
        expression.set_function_definition(definition)
        return type

    def visit_formal_parameter(self, formal_parameter: "FormalParameter"):
        self._table.add_identifier(formal_parameter.identifier, formal_parameter.type, formal_parameter)

    def visit_function_definition(self, function_definition: "FunctionDefinition"):
        self._table.open_scope()
        for parameter in function_definition.formal_parameters:
            parameter.visit(self)
        return_statements: List[ReturnStatement] = []
        for statement in function_definition.body:
            statement.visit(self)
            if isinstance(statement, ReturnStatement):
                return_statements.append(statement)
        if function_definition.return_type == ReturnType.VOID and len(return_statements) > 0:
            raise VoidFunctionReturnError(function_definition.name, function_definition)
        for statement in return_statements:
            type: ReturnType = statement.get_return_type()
            if type != function_definition.return_type:
                raise ReturnTypeError(function_definition.return_type, type, statement)
        self._table.add_function(function_definition.name, function_definition)
        self._table.close_scope()

    def visit_variable_declaration(self, declaration: "VariableDeclaration"):
        for identifier in declaration.identifiers:
            self._table.add_identifier(identifier, declaration.type, declaration)

    def visit_variable_assignment(self, assignment: "VariableAssignment"):
        declaration_type: Type = self._table.get_identifier(assignment.identifier, assignment)
        actual_type: Type = assignment.value.visit(self)
        self._check_type(assignment, declaration_type, actual_type)

    def visit_out_statement(self, statement: "OutStatement"):
        statement.expression.visit(self)

    def visit_function_call(self, call: "FunctionCall"):
        call.call_expression.visit(self)

    def visit_return_statement(self, statement: "ReturnStatement"):
        type: Type = statement.expression.visit(self)
        switch = {
            Type.INT: ReturnType.INT,
            Type.FLOAT: ReturnType.FLOAT
        }
        statement.set_return_type(switch[type])
        return switch[type]


from compiler.identification_table import IdentificationTable
