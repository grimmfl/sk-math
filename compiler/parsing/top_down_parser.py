from string import digits

from compiler.ast.ast import *
from compiler.errors import SyntaxError
from compiler.parsing.tokens import Token
from helpers import Stack, is_number

OPS = [Token.__dict__.get(t).value for t in filter(lambda x: not x.startswith("_"), Token.__dict__.keys())]


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
                        or (current_symbol in OPS) or (last_symbol in OPS):
                    if not last_symbol + current_symbol in OPS:  # For ==
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

    def _parse_statement(self, is_nested=False) -> Statement:
        if self.current_token == Token.FUNC.value and not is_nested:
            return self._parse_function_definition()
        else:
            return self._parse_simple_statement()

    def _parse_simple_statement(self) -> SimpleStatement:
        switch = {
            Token.INT.value: self._parse_variable_declaration,
            Token.FLOAT.value: self._parse_variable_declaration,
            Token.BOOL.value: self._parse_variable_declaration,
            Token.OUT.value: self._parse_out_statement,
            Token.RETURN.value: self._parse_return_statement,
            Token.IF.value: self._parse_if_statement,
            Token.FOR.value: self._parse_for_statement
        }
        if self.current_token in switch.keys():
            return switch[self.current_token]()
        if self.next_token == Token.LPAREN.value:
            return self._parse_function_call()
        else:
            return self._parse_variable_assignment()

    def _parse_if_statement(self) -> Statement:
        location = self.current_location
        self._accept(Token.IF)
        self._accept(Token.LPAREN)
        condition: Expression = self._parse_expression()
        self._accept(Token.RPAREN)
        self._accept(Token.LBRACE)
        body: List[Statement] = self._parse_body()
        self._accept(Token.RBRACE)
        elifs: List[IfStatement] = []
        while self.current_token == Token.ELIF.value:
            elif_location = self.current_location
            self._accept()
            self._accept(Token.LPAREN)
            elif_condition: Expression = self._parse_expression()
            self._accept(Token.RPAREN)
            self._accept(Token.LBRACE)
            elif_body: List[Statement] = self._parse_body()
            self._accept(Token.RBRACE)
            elifs.append(IfStatement(elif_condition, elif_body, [], [], elif_location))
        else_body: List[Statement] = []
        if self.current_token == Token.ELSE.value:
            self._accept()
            self._accept(Token.LBRACE)
            else_body = self._parse_body()
            self._accept(Token.RBRACE)
        return IfStatement(condition, body, elifs, else_body, location)

    def _parse_for_statement(self) -> Statement:
        location = self.current_location
        self._accept(Token.FOR)
        self._accept(Token.LPAREN)
        element_type: Type = self._parse_type()
        element_name: str = self._parse_name()
        self._accept(Token.IN)
        array: Expression = self._parse_expression()
        self._accept(Token.RPAREN)
        self._accept(Token.LBRACE)
        body: List[Statement] = self._parse_body()
        self._accept(Token.RBRACE)
        return ForStatement(element_type, element_name, array, body, location)

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
        self._accept(Token.LPAREN)
        actual_parameters: List[Expression] = self._parse_actual_parameters()
        self._accept(Token.RPAREN)
        return CallExpression(name, actual_parameters, location)

    def _parse_actual_parameters(self) -> List[Expression]:
        if self.current_token == Token.RPAREN.value:
            return []
        parameters: List[Expression] = [self._parse_expression()]
        while self.current_token == Token.COMMA.value:
            self._accept()
            parameters.append(self._parse_expression())
        return parameters

    def _parse_variable_assignment(self) -> VariableAssignment:
        if self.next_token == Token.LSQBR.value:
            return self._parse_array_element_assignment()
        location = self.current_location
        name: str = self._parse_name()
        self._accept(Token.ASSIGN)
        value: Expression = self._parse_expression()
        return VariableAssignment(name, value, location)

    def _parse_array_element_assignment(self) -> ArrayElementAssignment:
        location = self.current_location
        name: str = self._parse_name()
        self._accept(Token.LSQBR)
        index: Expression = self._parse_expression()
        self._accept(Token.RSQBR)
        self._accept(Token.ASSIGN)
        value: Expression = self._parse_expression()
        return ArrayElementAssignment(name, index, value, location)

    def _parse_function_definition(self) -> FunctionDefinition:
        location = self.current_location
        self._accept(Token.FUNC)
        return_type: ReturnType = self._parse_return_type()
        name: str = self._parse_name()
        self._accept(Token.LPAREN)
        parameters: List[FormalParameter] = self._parse_formal_parameters()
        self._accept(Token.RPAREN)
        self._accept(Token.LBRACE)
        body: List[Statement] = self._parse_body()
        self._accept(Token.RBRACE)
        return FunctionDefinition(name, return_type, parameters, body, location)

    def _parse_body(self) -> List[Statement]:
        self._accept(Token.NEWL)
        statements: List[Statement] = [self._parse_statement(is_nested=True)]
        self._accept(Token.NEWL)
        while self.current_token != Token.RBRACE.value:
            statements.append(self._parse_statement(is_nested=True))
            self._accept(Token.NEWL)
        return statements

    def _parse_formal_parameters(self) -> List[FormalParameter]:
        parameters: List[FormalParameter] = []
        while self.current_token != Token.RPAREN.value:
            parameters.append(self._parse_formal_parameter())
            if self.current_token != Token.RPAREN.value:
                self._accept(Token.COMMA)
        return parameters

    def _parse_formal_parameter(self) -> FormalParameter:
        location = self.current_location
        type: Type = self._parse_type()
        name: str = self._parse_name()
        return FormalParameter(type, name, location)

    def _parse_return_type(self) -> ReturnType:
        if self.current_token == Token.VOID.value:
            self._accept()
            return VoidType()
        return self._parse_type()

    def _parse_expression(self) -> Expression:
        return self._parse_or()

    def _parse_parentheses(self, operation_tokens: List[Token]) -> Expression or None:
        if self.current_token == Token.LPAREN.value:
            token_after = self._get_token_after_parenthese()
            if token_after in [token.value for token in operation_tokens] or len(operation_tokens) == 0:
                self._accept()
                x = self._parse_expression()
                self._accept(Token.RPAREN)
                return x
        return None

    def _get_token_after_parenthese(self) -> str:
        s = Stack()
        for i in range(self._current_token_idx + 1, len(self.tokens)):
            if self.tokens[i] == Token.LPAREN:
                s.push(())
            if self.tokens[i] == Token.RPAREN:
                if s.is_empty():
                    return self.tokens[i + 1]
                s.pop()

    def _parse_or(self) -> Expression:
        location = self.current_location
        x = self._parse_parentheses([Token.OR])
        x = self._parse_and() if x is None else x
        while self.current_token == Token.OR.value:
            self._accept()
            y = self._parse_parentheses([Token.OR])
            y = self._parse_and() if y is None else y
            x = Or(x, y, location)
        return x

    def _parse_and(self) -> Expression:
        location = self.current_location
        x = self._parse_parentheses([Token.AND])
        x = self._parse_comparison() if x is None else x
        while self.current_token == Token.AND.value:
            self._accept()
            y = self._parse_parentheses([Token.AND])
            y = self._parse_comparison() if y is None else y
            x = And(x, y, location)
        return x

    def _parse_comparison(self) -> Expression:
        location = self.current_location
        switch = {
            Token.EQ.value: ComparisonType.EQUAL,
            Token.NEQ.value: ComparisonType.NOT_EQUAL,
            Token.LEQ.value: ComparisonType.LESS_EQUAL,
            Token.GEQ.value: ComparisonType.GREATER_EQUAL,
            Token.LE.value: ComparisonType.LESS,
            Token.GE.value: ComparisonType.GREATER,
        }
        x = self._parse_parentheses([Token.EQ, Token.NEQ, Token.LEQ, Token.GEQ, Token.LE, Token.GE])
        x = self._parse_add_sub() if x is None else x
        if self.current_token in switch.keys():
            comparison_type: ComparisonType = switch[self.current_token]
            self._accept()
            y = self._parse_parentheses([Token.EQ, Token.NEQ, Token.LEQ, Token.GEQ, Token.LE, Token.GE])
            y = self._parse_add_sub() if y is None else y
            x = Comparison(x, y, comparison_type, location)
        return x

    def _parse_add_sub(self) -> Expression:
        location = self.current_location
        x = self._parse_parentheses([Token.ADD, Token.SUB])
        x = self._parse_mul_div_mod() if x is None else x
        while self.current_token == Token.ADD.value or self.current_token == Token.SUB.value:
            if self.current_token == Token.ADD.value:
                self._accept()
                y = self._parse_parentheses([Token.ADD, Token.SUB])
                y = self._parse_mul_div_mod() if y is None else y
                x = Addition(x, y, location)
            else:
                self._accept()
                y = self._parse_parentheses([Token.ADD, Token.SUB])
                y = self._parse_mul_div_mod() if y is None else y
                x = Subtraction(x, y, location)
        return x

    def _parse_mul_div_mod(self) -> Expression:
        location = self.current_location
        x = self._parse_parentheses([Token.MUL, Token.DIV, Token.MOD])
        x = self._parse_exponentiation() if x is None else x
        while self.current_token == Token.MUL.value or self.current_token == Token.DIV.value or self.current_token == Token.MOD.value:
            if self.current_token == Token.MUL.value:
                self._accept()
                y = self._parse_parentheses([Token.MUL, Token.DIV, Token.MOD])
                y = self._parse_exponentiation() if y is None else y
                x = Multiplication(x, y, location)
            elif self.current_token == Token.DIV.value:
                self._accept()
                y = self._parse_parentheses([Token.MUL, Token.DIV, Token.MOD])
                y = self._parse_exponentiation() if y is None else y
                x = Division(x, y, location)
            else:
                self._accept()
                y = self._parse_parentheses([Token.MUL, Token.DIV, Token.MOD])
                y = self._parse_exponentiation() if y is None else y
                x = Modulo(x, y, location)
        return x

    def _parse_exponentiation(self) -> Expression:
        location = self.current_location
        x = self._parse_parentheses([Token.EXP])
        x = self._parse_unary_operators() if x is None else x
        while self.current_token == Token.EXP.value:
            self._accept()
            y = self._parse_parentheses([Token.EXP])
            y = self._parse_unary_operators() if y is None else y
            x = Exponentiation(x, y, location)
        return x

    def _parse_unary_operators(self) -> Expression:
        location = self.current_location
        if self.current_token == Token.SUB.value:
            self._accept()
            x = self._parse_parentheses([])
            x = self._parse_atom() if x is None else x
            return UnaryMinus(x, location)
        if self.current_token == Token.NOT.value:
            self._accept()
            x = self._parse_parentheses([])
            x = self._parse_atom() if x is None else x
            return Not(x, location)
        x = self._parse_parentheses([])
        x = self._parse_atom() if x is None else x
        return x

    def _parse_atom(self) -> Expression:
        if self.current_token == Token.LSQBR.value:
            return self._parse_array()
        if self.next_token == Token.LSQBR.value:
            return self._parse_array_element_selection()
        if self.current_token == Token.TRUE.value or self.current_token == Token.FALSE.value:
            return self._parse_bool()
        if self.next_token == Token.LPAREN.value:
            return self._parse_call_expression()
        if is_number(self.current_token):
            return self._parse_number()
        return self._parse_identifier()

    def _parse_array_element_selection(self) -> Expression:
        location = self.current_location
        identifier: str = self._parse_name()
        self._accept(Token.LSQBR)
        if self.current_token == Token.COLLON.value or self.next_token == Token.COLLON.value:
            from_expression, to_expression = None, None
            if self.current_token != Token.COLLON.value:
                from_expression: Expression = self._parse_expression()
            self._accept(Token.COLLON)
            if self.current_token != Token.RSQBR.value:
                to_expression: Expression = self._parse_expression()
            self._accept(Token.RSQBR)
            return ArraySubSelection(identifier, from_expression, to_expression, location)
        index: Expression = self._parse_expression()
        self._accept(Token.RSQBR)
        return ArrayElementSelection(identifier, index, location)

    def _parse_array(self) -> Expression:
        location = self.current_location
        self._accept(Token.LSQBR)
        elements: List[Expression] = []
        while self.current_token != Token.RSQBR.value:
            elements.append(self._parse_expression())
            if self.current_token != Token.RSQBR.value:
                self._accept(Token.COMMA)
        self._accept(Token.RSQBR)
        return Array(elements, location)

    def _parse_bool(self) -> Expression:
        location = self.current_location
        if self.current_token == Token.TRUE.value:
            self._accept()
            return Constant(True, location)
        elif self.current_token == Token.FALSE.value:
            self._accept()
            return Constant(False, location)

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
            type = IntType()
        elif self.current_token == Token.FLOAT.value:
            self._accept()
            type = FloatType()
        elif self.current_token == Token.BOOL.value:
            self._accept()
            type = BoolType()
        else:
            raise SyntaxError([Token.INT, Token.FLOAT, Token.BOOL], self.current_token, self.current_location)
        if self.current_token == Token.LSQBR.value:
            self._accept()
            size: Expression = self._parse_expression()
            self._accept(Token.RSQBR)
            return ArrayType(type, size)
        return type


if __name__ == "__main__":
    p = TopDownParser()
    t = "func int mul(int x, int y) {\nreturn x * y\n}\nint z\nz = mul(3, 4)\nout z"
    parsed: Module = p.parse(t)
    parsed.print()
