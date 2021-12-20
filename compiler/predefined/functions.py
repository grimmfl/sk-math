import ctypes.wintypes

import typed_ast.ast3
import typing_extensions

from compiler.ast.ast import *


class Sqrt(FunctionDefinition):
    def __init__(self, table: "IdentificationTable"):
        location = (0, 0)
        ident = IdentifierReference("x", location)
        ident.set_type(Type.FLOAT)
        const = Constant(0.5, location)
        const.set_type(Type.FLOAT)
        exp = Exponentiation(ident, const, location)
        exp.set_type(Type.FLOAT)
        ret = ReturnStatement(exp, location)
        ret.set_return_type(ReturnType.FLOAT)
        formal_parameters = [FormalParameter(Type.FLOAT, "x", location)]
        super(Sqrt, self).__init__("sqrt", ReturnType.FLOAT, formal_parameters, [ret], location)

        table.add_function("sqrt", self)


class IntToFloat(FunctionDefinition):
    def __init__(self, table: "IdentificationTable"):
        location = (0, 0)
        ident = IdentifierReference("x", location)
        ident.set_type(Type.INT)
        custom_expr = CustomExpression(ident, lambda x: float(x), location)
        custom_expr.set_type(Type.FLOAT)
        ret = ReturnStatement(custom_expr, location)
        ret.set_return_type(ReturnType.FLOAT)
        formal_parameters = [FormalParameter(Type.INT, "x", location)]
        super(IntToFloat, self).__init__("intToFloat", ReturnType.FLOAT, formal_parameters, [ret], location)

        table.add_function("intToFloat", self)


class FloatToInt(FunctionDefinition):
    def __init__(self, table: "IdentificationTable"):
        location = (0, 0)
        ident = IdentifierReference("x", location)
        ident.set_type(Type.FLOAT)
        custom_expr = CustomExpression(ident, lambda x: int(round(x)), location)
        custom_expr.set_type(Type.INT)
        ret = ReturnStatement(custom_expr, location)
        ret.set_return_type(ReturnType.INT)
        formal_parameters = [FormalParameter(Type.FLOAT, "x", location)]
        super(FloatToInt, self).__init__("floatToInt", ReturnType.INT, formal_parameters, [ret], location)

        table.add_function("floatToInt", self)


PREDEFINED_FUNCTIONS = [Sqrt, IntToFloat, FloatToInt]


from compiler.identification_table import IdentificationTable
