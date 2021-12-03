from string import digits
from typing import List, Tuple

from compiler.elements import ParsedElement, ParsedType
from compiler.tokens import Token
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
            if token == Token.CONST:
                for symbol in self.current_token:
                    if symbol not in digits + ".":
                        raise SyntaxError(f"Invalid symbol '{symbol}' Atom at {self.current_location}")
                if self.current_token.count(".") > 1:
                    raise SyntaxError(f"Atom may only contain one '.' at {self.current_location}")
                else:
                    self._accept()
            elif self.current_token == token.value:
                self._accept()
            else:
                raise SyntaxError(f"Expected {token} - Got '{self.current_token}' at {self.current_location}")

    def parse(self, text: str) -> ParsedElement:
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
            raise SyntaxError(f"Expected newline or EOF - Got '{self.current_token}' at {self.current_location}")
        return ParsedElement(statements, None, ParsedType.STATEMENTS)

    def _parse_statement(self) -> ParsedElement:
        if self.current_token == Token.FUNC.value:
            return self._parse_func_definition()
        else:
            return self._parse_simple_statement()

    def _parse_func_definition(self) -> ParsedElement:
        self._accept(Token.FUNC)
        identifier = self._parse_identifier()
        self._accept(Token.LPARAN)
        params = self._parse_func_params()
        self._accept(Token.RPARAN)
        self._accept(Token.LBRACE)
        body = self._parse_func_body()
        self._accept(Token.RBRACE)
        info = ParsedElement(params, body, ParsedType.FUNC_INFO)
        return ParsedElement(identifier, info, ParsedType.FUNC_DEFINITION)

    def _parse_func_params(self) -> ParsedElement:
        params = []
        if self.current_token != Token.RPARAN.value:
            params = [self._parse_identifier()]
            while self.current_token == Token.COM.value:
                self._accept()
                params.append(self._parse_identifier())
        return ParsedElement(params, None, ParsedType.FUNC_PARAMS)

    def _parse_func_body(self) -> ParsedElement:
        statements = []
        while self.next_token != Token.RETURN.value:
            if self.next_token == Token.RBRACE.value:
                self._accept(Token.RETURN)
            self._accept(Token.NEWL)
            statements.append(self._parse_simple_statement())
        self._accept(Token.NEWL)
        statements.append(self._parse_return_statement())
        self._accept(Token.NEWL)
        return ParsedElement(statements, None, ParsedType.FUNC_BODY)

    def _parse_return_statement(self) -> ParsedElement:
        self._accept(Token.RETURN)
        return self._parse_add_sub()

    def _parse_simple_statement(self) -> ParsedElement:
        if self.current_token == Token.VAR.value:
            return self._parse_var_declaration()
        elif self.current_token == Token.OUT.value:
            return self._parse_out_statement()
        else:
            return self._parse_var_assignment()

    def _parse_var_declaration(self) -> ParsedElement:
        self._accept(Token.VAR)
        identifiers = [self._parse_identifier()]
        while self.current_token == Token.COM.value:
            self._accept()
            identifiers.append(self._parse_identifier())
        return ParsedElement(identifiers, None, ParsedType.VAR_DECLARATION)

    def _parse_out_statement(self) -> ParsedElement:
        self._accept(Token.OUT)
        x = self._parse_add_sub()
        return ParsedElement(x, None, ParsedType.OUT_STATEMENT)

    def _parse_var_assignment(self) -> ParsedElement:
        identifier = self._parse_identifier()
        self._accept(Token.ASSIGN)
        expr = self._parse_add_sub()
        return ParsedElement(identifier, expr, ParsedType.VAR_ASSIGNMENT)

    def _parse_add_sub(self) -> ParsedElement:
        x: ParsedElement = self._parse_mul_div()
        while self.current_token == Token.ADD.value or self.current_token == Token.SUB.value:
            if self.current_token == Token.ADD.value:
                self._accept()
                x = ParsedElement(x, self._parse_mul_div(), ParsedType.ADDITION)
            else:
                self._accept()
                x = ParsedElement(x, self._parse_mul_div(), ParsedType.SUBTRACTION)
        return x

    def _parse_mul_div(self) -> ParsedElement:
        x: ParsedElement = self._parse_exponentiation()
        while self.current_token == Token.MUL.value or self.current_token == Token.DIV.value:
            if self.current_token == Token.MUL.value:
                self._accept()
                x = ParsedElement(x, self._parse_exponentiation(), ParsedType.MULTIPLICATION)
            else:
                self._accept()
                x = ParsedElement(x, self._parse_exponentiation(), ParsedType.DIVISION)
        return x

    def _parse_exponentiation(self) -> ParsedElement:
        x: ParsedElement = self._parse_atom()
        while self.current_token == Token.EXP.value:
            self._accept()
            x = ParsedElement(x, self._parse_atom(), ParsedType.EXPONENTIATION)
        return x

    def _parse_atom(self) -> ParsedElement:
        if self.next_token == Token.LPARAN.value:
            return self._parse_func_call()
        else:
            for i in range(0, 10):
                if self.current_token.startswith(str(i)):
                    return self._parse_const()
            return self._parse_identifier()

    def _parse_func_call(self):
        identifier = self._parse_identifier()
        self._accept(Token.LPARAN)
        params = self._parse_func_call_params()
        self._accept(Token.RPARAN)
        return ParsedElement(identifier, params, ParsedType.FUNC_CALL)

    def _parse_func_call_params(self) -> ParsedElement:
        params = []
        if self.current_token != Token.RPARAN.value:
            params.append(self._parse_atom())
            while self.current_token == Token.COM.value:
                self._accept()
                params.append(self._parse_atom())
        return ParsedElement(params, None, ParsedType.FUNC_CALL_PARAMS)

    def _parse_identifier(self):
        x = ParsedElement(self.current_token, None, ParsedType.IDENTIFIER)
        self._accept()
        return x

    def _parse_const(self) -> ParsedElement:
        if "." in self.current_token:
            x = ParsedElement(float(self.current_token), 1, ParsedType.CONST)
        else:
            x = ParsedElement(int(self.current_token), 0, ParsedType.CONST)
        self._accept(Token.CONST)
        return x


if __name__ == "__main__":
    p = TopDownParser()
    t = "func mul(x, y) {\nreturn x * y\n}\nvar z\nz = mul(3, 4)\nout z"
    parsed = p.parse(t)
    print(p.tokens)
    parsed.print()
