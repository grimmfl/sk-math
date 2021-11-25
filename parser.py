from typing import List
from string import digits
from token import Token
import expressions

OPS = "*/+-^"


class Parser:
    def __init__(self, text: str):
        self.text: str = ""
        self.tokens: List[str] = self._text_to_tokens(text)
        self._current_token_idx = 0
        self.current_token = self.tokens[0]

    @staticmethod
    def _text_to_tokens(text: str) -> List[str]:
        tmp: List[str] = text.split(" ")
        tokens: List[str] = []
        for token in tmp:
            substr_index = 0
            for i in range(1, len(token)):
                last_symbol = token[i - 1]
                current_symbol = token[i]
                if (last_symbol in OPS and current_symbol in digits) or (last_symbol in digits and current_symbol in OPS):
                    tokens.append(token[substr_index:i])
                    substr_index = i
            tokens.append(token[substr_index:])
        return tokens

    def _accept(self, token: Token = None):
        if token is None:
            self._current_token_idx += 1
            self.current_token = self.tokens[self._current_token_idx]
        else:
            if token == Token.ATOM:
                for symbol in self.current_token:
                    if symbol not in digits + ".":
                        raise Exception(f"Syntax Error: Invalid symbol '{symbol}' Atom")
                if self.current_token.count(".") > 1:
                    raise Exception(f"Syntax Error: Atom may only contain one '.'")
                else:
                    self._accept()
            elif self.current_token == token.value:
                self._accept()
            else:
                raise Exception(f"Syntax Error: Expected {token} - Got {self.current_token}")

    def parse(self):
        return self._parse_add_sub()

    def _parse_add_sub(self) -> expressions.Expression:
        x: expressions.Expression = self._parse_mul_div()
        while self.current_token == Token.ADD.value or self.current_token == Token.SUB.value:
            if self.current_token == Token.ADD.value:
                self._accept()
                x = expressions.Addition(x, self._parse_mul_div())
            else:
                self._accept()
                x = expressions.Subtraction(x, self._parse_mul_div())
        return x

    def _parse_mul_div(self) -> expressions.Expression:
        x: expressions.Expression = self._parse_exponentiation()
        while self.current_token == Token.MUL.value or self.current_token == Token.DIV.value:
            if self.current_token == Token.MUL.value:
                self._accept()
                x = expressions.Multiplication(x, self._parse_exponentiation())
            else:
                self._accept()
                x = expressions.Division(x, self._parse_exponentiation())
            self._accept()
        return x

    def _parse_exponentiation(self) -> expressions.Expression:
        x: expressions.Expression = self._parse_atom()
        while self.current_token == Token.EXP.value:
            self._accept()
            x = expressions.Exponentiation(x, self._parse_atom())
        return x

    def _parse_atom(self) -> expressions.Expression:
        if "." in self.current_token:
            x = expressions.Atom(float(self.current_token), is_float=1)
        else:
            x = expressions.Atom(int(self.current_token), is_float=0)
        self._accept()
        return x


if __name__ == "__main__":
    p = Parser("123 + 323*43+36")
    print(p.tokens)
    print(p.parse())