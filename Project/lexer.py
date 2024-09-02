import re

class Token:
    """
    Token class represents a lexical token with a type and a value.
    """
    def __init__(self, type, value):
        self.type = type  # The type of token (e.g., 'NUM_TYPE', 'PRINT', 'VNAME')
        self.value = value  # The actual value of the token (e.g., 'num', 'print', 'V_x')

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    """
    Lexer class is responsible for converting the input source code into tokens.
    """
    
    # List of token specifications as (regex pattern, token type)
    token_exprs = [
        (r'[ \n\t]+', None),  # Ignore whitespace and newline
        (r'//.*', None),  # Ignore comments
        (r'\bmain\b', 'MAIN'),
        (r'\bbegin\b', 'BEGIN'),
        (r'\bend\b', 'END'),
        (r'\bnum\b', 'NUM_TYPE'),
        (r'\btext\b', 'TEXT_TYPE'),
        (r'\bskip\b', 'SKIP'),
        (r'\bhalt\b', 'HALT'),
        (r'\bprint\b', 'PRINT'),
        (r'\binput\b', 'INPUT'),
        (r'\breturn\b', 'RETURN'),  # New terminal token for the return statement
        (r'\bif\b', 'IF'),
        (r'\bthen\b', 'THEN'),
        (r'\belse\b', 'ELSE'),
        (r'\bor\b', 'OR'),
        (r'\band\b', 'AND'),
        (r'\beq\b', 'EQ'),
        (r'\bgrt\b', 'GRT'),
        (r'\badd\b', 'ADD'),
        (r'\bsub\b', 'SUB'),
        (r'\bmul\b', 'MUL'),
        (r'\bdiv\b', 'DIV'),
        (r'\bnot\b', 'NOT'),
        (r'\bsqrt\b', 'SQRT'),
        (r'\bvoid\b', 'VOID'),
        (r'V_[a-z]([a-z]|[0-9])*', 'VNAME'),  # Variable names
        (r'F_[a-z]([a-z]|[0-9])*', 'FNAME'),  # Function names
        (r'"[A-Za-z]{1,8}"', 'CONST_T'),  # Simplified regex for strings (up to 8 characters)
        (r'-?\d+(\.\d+)?', 'CONST_N'),  # Matches both integers and decimals
        (r'=', 'ASSIGN'),
        (r'<', 'INPUT_OP'),
        (r'\(', 'LPAREN'),
        (r'\)', 'RPAREN'),
        (r'\{', 'LBRACE'),
        (r'\}', 'RBRACE'),
        (r',', 'COMMA'),
        (r';', 'SEMICOLON'),
    ]

    def __init__(self, input_text):
        self.input_text = input_text  # The source code input as a string
        self.position = 0  # Current position in the input text

    def tokenize(self):
        """
        Tokenizes the input text into a list of tokens.
        """
        tokens = []  # List to store the generated tokens
        while self.position < len(self.input_text):
            match = None  # To store the matching pattern
            for token_expr in self.token_exprs:
                pattern, tag = token_expr  # Each token expression has a regex pattern and a tag
                regex = re.compile(pattern)
                match = regex.match(self.input_text, self.position)
                if match:
                    text = match.group(0)  # Matched text
                    if tag:  # Only add to tokens if a tag is specified (ignore whitespace/comments)
                        token = Token(tag, text)
                        tokens.append(token)
                    break  # Break after the first match to avoid matching multiple patterns
            if not match:
                raise SyntaxError(f'Unexpected character: {self.input_text[self.position]}')
            else:
                self.position = match.end(0)  # Move the position to the end of the matched text
        return tokens  # Return the list of tokens


# Example usage of the lexer
if __name__ == "__main__":
    # Test input program
    input_program = """
    main
    begin
        num V_x, text V_y,
        V_x < input
        print V_x;
        return V_x
    end
    """

    # Initialize the lexer with the input program
    lexer = Lexer(input_program)
    # Tokenize the input program and print the tokens
    tokens = lexer.tokenize()
    print(tokens)
