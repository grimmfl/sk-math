from string import digits
from typing import List, Tuple

from compiler.ast import *
from compiler.tokens import Token
from compiler.errors import SyntaxError
from helpers import Stack

OPS = ["*", "/", "+", "-", "^", ",", "var", "out", "=", "(", ")", "{", "}", "return", "func"]


class TopDownParser:
    def __init__(self):
        self.text: str = ""
        self.tokens: List[str] = []
        self.locations: List[Tuple[int, int]] = []
        self._current_token_idx = -1
        self.current_token = None
        self.next_token = None
        self.current_location = None

    @staticmethod
    def _scan(text: str) -> List[str]:
        tmp: List[str] = text.split(" ")
        tokens: List[str] = []
        for token in tmp:
            substr_index = 0
            for i in range(1, len(token)):
                last_symbol = token[i - 1]
                current_symbol = token[i]
                if (last_symbol in OPS and current_symbol in digits)\
                        or (last_symbol in digits and current_symbol in OPS)\
                        or last_symbol == "\n" or current_symbol == "\n"\
                        or (current_symbol in OPS) or (last_symbol in OPS):
                    tokens.append(token[substr_index:i])
                    substr_index = i
            tokens.append(token[substr_index:])
        return [token for token in filter(lambda tok: tok != "", tokens)]

    def _get_locations(self):
        stack = Stack()
        for token in reversed(self.tokens):
            stack.push(token)
        i = 0
        row = 0
        col = 0
        while i < len(self.text):
            if self.text[i:].startswith(stack.peak()):
                token = stack.pop()
                self.locations.append((row, col))
                if token == "\n":
                    row += 1
                    col = 0
                else:
                    col += len(token)
                i += len(token)
            else:
                i += 1

    def _accept(self, token: Token = None):
        if token is None:
            self._current_token_idx += 1
            if self._current_token_idx < len(self.tokens):
                self.current_token = self.tokens[self._current_token_idx]
                self.current_location = self.locations[self._current_token_idx]
                if self._current_token_idx < len(self.tokens) - 1:
                    self.next_token = self.tokens[self._current_token_idx + 1]
            else:
                self.current_token = None
        else:
            if self.current_token == token.value:
                self._accept()
            else:
                raise SyntaxError(token, self.current_token, self.current_location)

    def parse(self, text: str) -> AstNode:
        self.text = text
        self.tokens = self._scan(text)
        self._get_locations()
        self._current_token_idx = 0
        self.current_token = self.tokens[self._current_token_idx]
        self.current_location = self.locations[self._current_token_idx]

        statements = [self._parse_statement()]
        while self.current_token == Token.NEWL.value:
            self._accept()
            if self.current_token != Token.NEWL.value and self.current_token is not None:
                statements.append(self._parse_statement())
        if self.current_token is not None:
            raise SyntaxError(Token.NEWL, self.current_token, self.current_location)
        return Module(statements, location=(0, 0))

    def _parse_statement(self) -> Statement:
        if self.current_token == Token.FUNC.value:
            return self._parse_function_definition()
        else:
            return self._parse_simple_statement()

    def _parse_function_definition(self) -> FunctionDefinition:
        self._accept(Token.FUNC)
        type: Type = self._parse_type()
        name: str = self._parse_identifier()
        self._accept(Token.LPARAN)
        parameters: List[FormalParameter] = self._parse_parameters()
        self._accept(Token.RPARAN)
        self._accept(Token.LBRACE)
        # TODO parse fn body
        self._accept(Token.RBRACE)
        # TODO return


if __name__ == "__main__":
    p = TopDownParser()
    t = "func mul(x, y) {\nreturn x * y\n}\nvar z\nz = mul(3, 4)\nout z"
    parsed = p.parse(t)
    print(p.tokens)
    parsed.print()
