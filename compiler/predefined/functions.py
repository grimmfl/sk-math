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


PREDEFINED_FUNCTIONS = [Sqrt]


from compiler.identification_table import IdentificationTable
