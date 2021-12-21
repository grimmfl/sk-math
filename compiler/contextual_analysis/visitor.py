import typing_extensions

from compiler.errors import *
from compiler.ast.ast import *


class Visitor:
    def __init__(self):
        self._table = IdentificationTable[Type]()
        self._currently_in_function = False

    @staticmethod
    def _check_type(node: "AstNode", type1: Type, type2: Type):
        if type1 != type2:
            raise TypeError(node, type1, type2)

    def visit_module(self, module: "Module"):
        self._table.open_scope()
        for statement in module.statements:
            statement.visit(self)
        self._table.close_scope()

    def visit_or(self, or_expr: "Or") -> Type:
        l_type: Type = or_expr.left_operand.visit(self)
        r_type: Type = or_expr.right_operand.visit(self)
        self._check_type(or_expr, Type.BOOL, l_type)
        self._check_type(or_expr, Type.BOOL, r_type)
        or_expr.set_type(Type.BOOL)
        return Type.BOOL

    def visit_and(self, and_expr: "And") -> Type:
        l_type: Type = and_expr.left_operand.visit(self)
        r_type: Type = and_expr.right_operand.visit(self)
        self._check_type(and_expr, Type.BOOL, l_type)
        self._check_type(and_expr, Type.BOOL, r_type)
        and_expr.set_type(Type.BOOL)
        return Type.BOOL

    def visit_comparison(self, comparison: "Comparison") -> Type:
        l_type: Type = comparison.left_operand.visit(self)
        r_type: Type = comparison.right_operand.visit(self)
        if not l_type.is_numeric():
            raise TypeError(comparison, NUMERIC_TYPES, l_type)
        if not r_type.is_numeric():
            raise TypeError(comparison, NUMERIC_TYPES, r_type)
        self._check_type(comparison, l_type, r_type)
        comparison.set_type(Type.BOOL)
        return Type.BOOL

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
        self._check_type(modulo, Type.INT, l_type)
        self._check_type(modulo, Type.INT, r_type)
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

    def visit_unary_minus(self, unary_minus: "UnaryMinus") -> Type:
        type: Type = unary_minus.value.visit(self)
        if not type.is_numeric():
            raise TypeError(unary_minus, NUMERIC_TYPES, type)
        unary_minus.set_type(type)
        return type

    def visit_not(self, not_expr: "Not") -> Type:
        type: Type = not_expr.value.visit(self)
        self._check_type(not_expr, Type.BOOL, type)
        not_expr.set_type(Type.BOOL)
        return Type.BOOL

    def visit_identifier_reference(self, reference: "IdentifierReference") -> Type:
        type: Type = self._table.get_identifier(reference.identifier, reference)
        reference.set_type(type)
        return type

    def visit_constant(self, constant: "Constant") -> Type:
        switch = {
            float: Type.FLOAT,
            int: Type.INT,
            bool: Type.BOOL
        }
        constant.set_type(switch[type(constant.value)])
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
            ReturnType.FLOAT: Type.FLOAT,
            ReturnType.BOOL: Type.BOOL,
        }
        type: Type = switch[definition.return_type]
        expression.set_type(type)
        expression.set_function_definition(definition)
        return type

    def visit_formal_parameter(self, formal_parameter: "FormalParameter"):
        self._table.add_identifier(formal_parameter.identifier, formal_parameter.type, formal_parameter)

    def visit_function_definition(self, function_definition: "FunctionDefinition"):
        self._currently_in_function = True
        self._table.add_function(function_definition.name, function_definition)
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
        self._table.update_function(function_definition.name, function_definition)
        self._table.close_scope()
        self._currently_in_function = False

    def visit_if_statement(self, if_statement: "IfStatement"):
        cond_type: Type = if_statement.condition.visit(self)
        self._check_type(if_statement, Type.BOOL, cond_type)
        for statement in if_statement.body:
            statement.visit(self)
        for elif_statement in if_statement.elifs:
            elif_statement.visit(self)
        for statement in if_statement.else_body:
            statement.visit(self)

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
        if not self._currently_in_function:
            raise ReturnOutsideOfFunctionError(statement)
        type: Type = statement.expression.visit(self)
        switch = {
            Type.INT: ReturnType.INT,
            Type.FLOAT: ReturnType.FLOAT,
            Type.BOOL: ReturnType.BOOL,
        }
        statement.set_return_type(switch[type])
        return switch[type]


from compiler.identification_table import IdentificationTable
