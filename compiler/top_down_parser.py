from string import digits
from typing import List

from compiler.elements import ParsedElement, ParsedType
from compiler.tokens import Token

OPS = ["*", "/", "+", "-", "^", ",", "var", "out", "="]


class TopDownParser:
    def __init__(self):
        self.text: str = ""
        self.tokens: List[str] = []
        self._current_token_idx = -1
        self.current_token = None

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
        return tokens

    def _accept(self, token: Token = None):
        if token is None:
            self._current_token_idx += 1
            if self._current_token_idx < len(self.tokens):
                self.current_token = self.tokens[self._current_token_idx]
        else:
            if token == Token.CONST:
                for symbol in self.current_token:
                    if symbol not in digits + ".":
                        raise SyntaxError(f"Syntax Error: Invalid symbol '{symbol}' Atom")
                if self.current_token.count(".") > 1:
                    raise SyntaxError(f"Syntax Error: Atom may only contain one '.'")
                else:
                    self._accept()
            elif self.current_token == token.value:
                self._accept()
            else:
                raise SyntaxError(f"Syntax Error: Expected {token} - Got {self.current_token}")

    def parse(self, text: str) -> ParsedElement:
        self.tokens = self._scan(text)
        self._current_token_idx = 0
        self.current_token = self.tokens[self._current_token_idx]

        statements = [self._parse_statement()]
        while self.current_token == Token.NEWL.value:
            self._accept()
            statements.append(self._parse_statement())
        return ParsedElement(statements, None, ParsedType.STATEMENTS)

    def _parse_statement(self) -> ParsedElement:
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
        for i in range(0, 10):
            if self.current_token.startswith(str(i)):
                return self._parse_const()
        return self._parse_identifier()

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
