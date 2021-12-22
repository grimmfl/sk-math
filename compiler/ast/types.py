from enum import Enum
from typing import List


class ReturnType:
    def __init__(self, name):
        self.name: str = name

    def __eq__(self, other) -> bool:
        return isinstance(other, ReturnType) and other.name == self.name

    def __str__(self) -> str:
        return self.name

    def is_primitive(self) -> bool:
        return isinstance(self, PrimitiveType)

    def is_numeric(self) -> bool:
        return isinstance(self, IntType) or isinstance(self, FloatType)

    def is_array(self) -> bool:
        return isinstance(self, ArrayType)
    

class VoidType(ReturnType):
    def __init__(self):
        super(VoidType, self).__init__("void")
    
    
class Type(ReturnType):
    def __init__(self, name, python_type):
        self.python_type: PYTHON_TYPE = python_type
        super(Type, self).__init__(name)

    def __eq__(self, other):
        return isinstance(other, Type) and other.name == self.name


class PrimitiveType(Type):
    def __init__(self, name, python_type):
        super().__init__(name, python_type)
        
        
class FloatType(PrimitiveType):
    def __init__(self):
        super(FloatType, self).__init__("float", float)
        
        
class IntType(PrimitiveType):
    def __init__(self):
        super(IntType, self).__init__("int", int)
        
        
class BoolType(PrimitiveType):
    def __init__(self):
        super(BoolType, self).__init__("bool", bool)


class ArrayType(Type):
    def __init__(self, element_type: Type, size: "Expression"):
        self.element_type: Type = element_type
        self.size: "Expression" = size
        super(ArrayType, self).__init__("array", list)

    def __eq__(self, other) -> bool:
        return isinstance(other, ArrayType) and self.element_type == other.element_type

    def __str__(self) -> str:
        return str(self.element_type) + "[]"


class ComparisonType(Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    LESS = "<"
    GREATER = ">"


NUMERIC_TYPES = [IntType(), FloatType()]
PRIMITIVE_TYPES: List[PrimitiveType] = NUMERIC_TYPES + [BoolType()]

PYTHON_PRIMITIVE_TYPE = int or float or bool
PYTHON_TYPE = PYTHON_PRIMITIVE_TYPE or list


from compiler.ast.ast import Expression
