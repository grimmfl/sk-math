from enum import Enum


class Type(Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"

    def is_numeric(self) -> bool:
        return self == Type.INT or self == Type.FLOAT


class ReturnType(Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    VOID = "void"


class ComparisonType(Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    LESS = "<"
    GREATER = ">"


NUMERIC_TYPES = [Type.INT, Type.FLOAT]

PYTHON_PRIMITIVE_TYPE = int or float or bool
