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
        custom_expr = CustomUnaryFunction(ident, lambda x: float(x), location)
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
        custom_expr = CustomUnaryFunction(ident, lambda x: int(round(x)), location)
        custom_expr.set_type(IntType())
        ret = ReturnStatement(custom_expr, location)
        ret.set_return_type(IntType())
        formal_parameters = [FormalParameter(FloatType(), "x", location)]
        super(FloatToInt, self).__init__("floatToInt", IntType(), formal_parameters, [ret], location)

        table.add_function("floatToInt", self)


class Range(FunctionDefinition):
    def __init__(self, table: "IdentificationTable"):
        location = (0, 0)
        from_id: IdentifierReference = IdentifierReference("from", location)
        from_id.set_type(IntType())
        to_id: IdentifierReference = IdentifierReference("to", location)
        to_id.set_type(IntType())
        size: Subtraction = Subtraction(to_id, from_id, location)
        size.set_type(IntType())
        array_type: Type = ArrayType(IntType(), size)
        function: Callable[[AnyType, AnyType], AnyType] = lambda x, y: [i for i in range(x, y)]
        custom_expr: CustomBinaryFunction = CustomBinaryFunction(from_id, to_id, function, location)
        custom_expr.set_type(array_type)
        ret = ReturnStatement(custom_expr, location)
        ret.set_return_type(array_type)
        formal_parameters = [FormalParameter(IntType(), "from", location), FormalParameter(IntType(), "to", location)]
        super(Range, self).__init__("range", array_type, formal_parameters, [ret], location)

        table.add_function("range", self)


PREDEFINED_FUNCTIONS = [Sqrt, IntToFloat, FloatToInt, Range]


from compiler.identification_table import IdentificationTable