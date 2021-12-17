from enum import Enum


class Type(Enum):
    INT = "int"
    FLOAT = "float"

    def is_numeric(self) -> bool:
        return self == Type.INT or self == Type.FLOAT


class ReturnType(Enum):
    INT = "int"
    FLOAT = "float"
    VOID = "void"


NUMERIC_TYPES = [Type.INT, Type.FLOAT]

PYTHON_PRIMITIVE_TYPE = int or float
