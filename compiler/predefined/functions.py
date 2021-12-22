from compiler.ast.ast import *
from compiler.ast.types import *


class Sqrt(FunctionDefinition):
    def __init__(self, table: "IdentificationTable"):
        location = (0, 0)
        ident = IdentifierReference("x", location)
        ident.set_type(FloatType())
        const = Constant(0.5, location)
        const.set_type(FloatType())
        exp = Exponentiation(ident, const, location)
        exp.set_type(FloatType())
        ret = ReturnStatement(exp, location)
        ret.set_return_type(FloatType())
        formal_parameters = [FormalParameter(FloatType(), "x", location)]
        super(Sqrt, self).__init__("sqrt", FloatType(), formal_parameters, [ret], location)

        table.add_function("sqrt", self)


class IntToFloat(FunctionDefinition):
    def __init__(self, table: "IdentificationTable"):
        location = (0, 0)
        ident = IdentifierReference("x", location)
        ident.set_type(IntType())
        custom_expr = CustomExpression(ident, lambda x: float(x), location)
        custom_expr.set_type(FloatType())
        ret = ReturnStatement(custom_expr, location)
        ret.set_return_type(FloatType())
        formal_parameters = [FormalParameter(IntType(), "x", location)]
        super(IntToFloat, self).__init__("intToFloat", FloatType(), formal_parameters, [ret], location)

        table.add_function("intToFloat", self)


class FloatToInt(FunctionDefinition):
    def __init__(self, table: "IdentificationTable"):
        location = (0, 0)
        ident = IdentifierReference("x", location)
        ident.set_type(FloatType())
        custom_expr = CustomExpression(ident, lambda x: int(round(x)), location)
        custom_expr.set_type(IntType())
        ret = ReturnStatement(custom_expr, location)
        ret.set_return_type(IntType())
        formal_parameters = [FormalParameter(FloatType(), "x", location)]
        super(FloatToInt, self).__init__("floatToInt", IntType(), formal_parameters, [ret], location)

        table.add_function("floatToInt", self)


PREDEFINED_FUNCTIONS = [Sqrt, IntToFloat, FloatToInt]


from compiler.identification_table import IdentificationTable