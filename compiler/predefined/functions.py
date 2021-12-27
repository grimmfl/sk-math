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

        self.set_required_count(1)
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

        self.set_required_count(1)
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

        self.set_required_count(1)
        table.add_function("floatToInt", self)


class Range(FunctionDefinition):
    def __init__(self, table: "IdentificationTable"):
        location = (0, 0)
        from_id: IdentifierReference = IdentifierReference("from", location)
        from_id.set_type(IntType())
        to_id: IdentifierReference = IdentifierReference("to", location)
        to_id.set_type(IntType())
        step_id: IdentifierReference = IdentifierReference("step", location)
        step_id.set_type(IntType())
        size_fn: Callable[[Any, Any, Any], Any] = lambda x, y, z: int((y - x) / z) if (y - x) % z == 0 else int((y - x) / z) + 1
        size: CustomTernaryFunction = CustomTernaryFunction(from_id, to_id, step_id, size_fn, location)
        size.set_type(IntType())
        array_type: Type = ArrayType(IntType(), size)
        function: Callable[[Any, Any, Any], Any] = lambda x, y, z: [i for i in range(x, y, z)]
        custom_expr: CustomTernaryFunction = CustomTernaryFunction(from_id, to_id, step_id, function, location)
        custom_expr.set_type(array_type)
        ret = ReturnStatement(custom_expr, location)
        ret.set_return_type(array_type)
        formal_parameters = [
            FormalParameter(IntType(), "from", location),
            FormalParameter(IntType(), "to", location),
            FormalParameterWithDefault(IntType(), "step", Constant(1, location), location)
        ]
        super(Range, self).__init__("range", array_type, formal_parameters, [ret], location)

        self.set_required_count(2)
        table.add_function("range", self)


PREDEFINED_FUNCTIONS = [Sqrt, IntToFloat, FloatToInt, Range]


from compiler.identification_table import IdentificationTable