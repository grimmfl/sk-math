from string import digits
from typing import List, Generic, TypeVar


def flatten(nested_list: List) -> List:
    flat_list = []
    for item in nested_list:
        if type(item) == list:
            flat_list += flatten(item)
        else:
            flat_list.append(item)
    return flat_list


T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self):
        self._stack: List[T] = []

    def push(self, item: T):
        self._stack.append(item)

    def pop(self) -> T:
        return self._stack.pop()

    def peak(self) -> T:
        return self._stack[-1]

    def is_empty(self) -> bool:
        return len(self._stack) == 0


def is_number(text: str) -> bool:
    for letter in text:
        if letter not in digits:
            return False
    return True
