from string import digits

from compiler.ast.ast import *
from compiler.errors import SyntaxError
from compiler.parsing.tokens import Token
from helpers import Stack, is_number

OPS = ["*", "/", "+", "-", "^", ",", "var", "out", "=", "(", ")", "{", "}", "return", "func"]


class TopDownParser:
    def __init__(self):
        self.text: str = ""
        self.tokens: List[str] = []
        self.locations: List[Tuple[int, int]] = []
        self._current_token_idx = -1
        self.current_token: str = None
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
        elif token == Token.IDENTIFIER:
            for i in range(0, 10):
                if self.current_token.startswith(str(i)):
                    raise SyntaxError(token, self.current_token, self.current_location)
            self._accept()
        else:
            if self.current_token == token.value:
                self._accept()
            else:
                raise SyntaxError(token, self.current_token, self.current_location)

    def parse(self, text: str) -> Module:
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

    def _parse_statement(self, is_part_of_function=False) -> Statement:
        if self.current_token == Token.FUNC.value and not is_part_of_function:
            return self._parse_function_definition()
        else:
            return self._parse_simple_statement()

    def _parse_simple_statement(self) -> SimpleStatement:
        switch = {
            Token.INT.value: self._parse_variable_declaration,
            Token.FLOAT.value: self._parse_variable_declaration,
            Token.OUT.value: self._parse_out_statement,
            Token.RETURN.value: self._parse_return_statement,
        }
        if self.current_token in switch.keys():
            return switch[self.current_token]()
        if self.next_token == Token.LPARAN.value:
            return self._parse_function_call()
        else:
            return self._parse_variable_assignment()

    def _parse_return_statement(self) -> ReturnStatement:
        location = self.current_location
        self._accept(Token.RETURN)
        value: Expression = self._parse_expression()
        return ReturnStatement(value, location)

    def _parse_variable_declaration(self) -> VariableDeclaration:
        location = self.current_location
        type: Type = self._parse_type()
        identifiers: List[str] = [self._parse_name()]
        while self.current_token == Token.COMMA.value:
            self._accept()
            identifiers.append(self._parse_name())
        return VariableDeclaration(type, identifiers, location)

    def _parse_out_statement(self) -> OutStatement:
        location = self.current_location
        self._accept(Token.OUT)
        expression: Expression = self._parse_expression()
        return OutStatement(expression, location)

    def _parse_function_call(self) -> FunctionCall:
        location = self.current_location
        return FunctionCall(self._parse_call_expression(), location)

    def _parse_call_expression(self) -> CallExpression:
        location = self.current_location
        name: str = self._parse_name()
        self._accept(Token.LPARAN)
        actual_parameters: List[Expression] = self._parse_actual_parameters()
        self._accept(Token.RPARAN)
        return CallExpression(name, actual_parameters, location)

    def _parse_actual_parameters(self) -> List[Expression]:
        if self.current_token == Token.RPARAN.value:
            return []
        parameters: List[Expression] = [self._parse_expression()]
        while self.current_token == Token.COMMA.value:
            self._accept()
            parameters.append(self._parse_expression())
        return parameters

    def _parse_variable_assignment(self) -> VariableAssignment:
        location = self.current_location
        name: str = self._parse_name()
        self._accept(Token.ASSIGN)
        value: Expression = self._parse_expression()
        return VariableAssignment(name, value, location)

    def _parse_function_definition(self) -> FunctionDefinition:
        location = self.current_location
        self._accept(Token.FUNC)
        return_type: ReturnType = self._parse_return_type()
        name: str = self._parse_name()
        self._accept(Token.LPARAN)
        parameters: List[FormalParameter] = self._parse_formal_parameters()
        self._accept(Token.RPARAN)
        self._accept(Token.LBRACE)
        body: List[Statement] = self._parse_function_body()
        self._accept(Token.RBRACE)
        return FunctionDefinition(name, return_type, parameters, body, location)

    def _parse_function_body(self) -> List[Statement]:
        self._accept(Token.NEWL)
        statements: List[Statement] = [self._parse_statement(is_part_of_function=True)]
        self._accept(Token.NEWL)
        while self.current_token != Token.RBRACE.value:
            statements.append(self._parse_statement(is_part_of_function=True))
            self._accept(Token.NEWL)
        return statements

    def _parse_formal_parameters(self) -> List[FormalParameter]:
        parameters: List[FormalParameter] = [self._parse_formal_parameter()]
        while self.current_token == Token.COMMA.value:
            self._accept()
            parameters.append(self._parse_formal_parameter())
        return parameters

    def _parse_formal_parameter(self) -> FormalParameter:
        location = self.current_location
        type: Type = self._parse_type()
        name: str = self._parse_name()
        return FormalParameter(type, name, location)

    def _parse_return_type(self) -> ReturnType:
        switch = {
            Token.INT.value: ReturnType.INT,
            Token.FLOAT.value: ReturnType.FLOAT,
            Token.VOID.value: ReturnType.VOID,
        }
        if self.current_token in switch.keys():
            return_type: ReturnType = switch[self.current_token]
            self._accept()
            return return_type
        raise SyntaxError([Token.INT, Token.FLOAT, Token.VOID], self.current_token, self.current_location)

    def _parse_expression(self) -> Expression:
        return self._parse_add_sub()

    def _parse_add_sub(self) -> Expression:
        location = self.current_location
        x = self._parse_mul_div_mod()
        while self.current_token == Token.ADD.value or self.current_token == Token.SUB.value:
            if self.current_token == Token.ADD.value:
                self._accept()
                x = Addition(x, self._parse_mul_div_mod(), location)
            else:
                self._accept()
                x = Subtraction(x, self._parse_mul_div_mod(), location)
        return x

    def _parse_mul_div_mod(self) -> Expression:
        location = self.current_location
        x = self._parse_exponentiation()
        while self.current_token == Token.MUL.value or self.current_token == Token.DIV.value or self.current_token == Token.MOD.value:
            if self.current_token == Token.MUL.value:
                self._accept()
                x = Multiplication(x, self._parse_exponentiation(), location)
            elif self.current_token == Token.DIV.value:
                self._accept()
                x = Division(x, self._parse_exponentiation(), location)
            else:
                self._accept()
                x = Modulo(x, self._parse_exponentiation(), location)
        return x

    def _parse_exponentiation(self) -> Expression:
        location = self.current_location
        x = self._parse_atom()
        while self.current_token == Token.EXP.value:
            self._accept()
            x = Exponentiation(x, self._parse_atom(), location)
        return x

    def _parse_atom(self) -> Expression:
        if self.next_token == Token.LPARAN.value:
            return self._parse_call_expression()
        if is_number(self.current_token):
            return self._parse_number()
        return self._parse_identifier()

    def _parse_number(self) -> Expression:
        location = self.current_location
        if self.current_token.count(".") == 1:
            value: float = float(self.current_token)
            self._accept()
            return Constant(value, location)
        if self.current_token.count(".") == 0:
            value: int = int(self.current_token)
            self._accept()
            return Constant(value, location)
        raise SyntaxError(Token.FLOAT, self.current_token, location)

    def _parse_identifier(self) -> IdentifierReference:
        location = self.current_location
        return IdentifierReference(self._parse_name(), location)

    def _parse_name(self) -> str:
        name: str = self.current_token
        self._accept(Token.IDENTIFIER)
        return name

    def _parse_type(self) -> Type:
        if self.current_token == Token.INT.value:
            self._accept()
            return Type.INT
        elif self.current_token == Token.FLOAT.value:
            self._accept()
            return Type.FLOAT
        else:
            raise SyntaxError([Token.INT, Token.FLOAT], self.current_token, self.current_location)


if __name__ == "__main__":
    p = TopDownParser()
    t = "func int mul(int x, int y) {\nreturn x * y\n}\nint z\nz = mul(3, 4)\nout z"
    parsed: Module = p.parse(t)
    parsed.print()
