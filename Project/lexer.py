# Lexer

import re


class LexicalError(Exception):
    """Exception raised for errors in the lexical analysis phase."""

    def __init__(self, message, line_num, col_num):
        super().__init__(f"{message} at line {line_num}, column {col_num}")
        self.line_num = line_num
        self.col_num = col_num


class Token:
    """
    Token class represents a lexical token with a type and a value.
    """

    def __init__(self, type, value):
        self.type = type  # The type of token (e.g., 'NUM_TYPE', 'PRINT', 'VNAME')
        self.value = (
            value  # The actual value of the token (e.g., 'num', 'print', 'V_x')
        )

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    """
    Lexer class is responsible for converting the input source code into tokens.
    """

    # List of token specifications as (regex pattern, token type)
    token_exprs = [
        (r"[ \n\t]+", None),  # Ignore whitespace and newline
        (r"//.*", None),  # Ignore comments
        # Keywords must be matched before identifiers
        (r"\bmain\b", "MAIN"),
        (r"\bbegin\b", "BEGIN"),
        (r"\bend\b", "END"),
        (r"\bnum\b", "NUM_TYPE"),
        (r"\btext\b", "TEXT_TYPE"),
        (r"\bskip\b", "SKIP"),
        (r"\bhalt\b", "HALT"),
        (r"\bprint\b", "PRINT"),
        (r"\binput\b", "INPUT"),
        (r"\breturn\b", "RETURN"),  # New terminal token for the return statement
        (r"\bif\b", "IF"),
        (r"\bthen\b", "THEN"),
        (r"\belse\b", "ELSE"),
        (r"\bor\b", "OR"),
        (r"\band\b", "AND"),
        (r"\beq\b", "EQ"),
        (r"\bgrt\b", "GRT"),
        (r"\badd\b", "ADD"),
        (r"\bsub\b", "SUB"),
        (r"\bmul\b", "MUL"),
        (r"\bdiv\b", "DIV"),
        (r"\bnot\b", "NOT"),
        (r"\bsqrt\b", "SQRT"),
        (r"\bvoid\b", "VOID"),
        (r"V_[a-z]([a-z]|[0-9])*", "VNAME"),  # Variable names
        (r"F_[a-z]([a-z]|[0-9])*", "FNAME"),  # Function names
        (r'"[^"]*"', "CONST_T"),  # Updated regex for strings
        (r"-?\d+(\.\d+)?", "CONST_N"),  # Matches both integers and decimals
        (r"=", "ASSIGN"),
        (r"<", "INPUT_OP"),
        (r"\(", "LPAREN"),
        (r"\)", "RPAREN"),
        (r"\{", "LBRACE"),
        (r"\}", "RBRACE"),
        (r",", "COMMA"),
        (r";", "SEMICOLON"),
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
                pattern, tag = (
                    token_expr  # Each token expression has a regex pattern and a tag
                )
                regex = re.compile(pattern)
                match = regex.match(self.input_text, self.position)
                if match:
                    text = match.group(0)  # Matched text
                    if (
                        tag
                    ):  # Only add to tokens if a tag is specified (ignore whitespace/comments)
                        token = Token(tag, text)
                        tokens.append(token)
                    break  # Break after the first match to avoid matching multiple patterns
            if not match:
            # Raise a LexicalError if an unexpected character is encountered
                line_num = self.input_text.count("\n", 0, self.position) + 1
                col_num = self.position - self.input_text.rfind("\n", 0, self.position)
                unexpected_char = self.input_text[self.position]
                raise LexicalError(
                    f"Unexpected character {unexpected_char!r}", line_num, col_num
                )
            else:
                self.position = match.end(
                    0
                    )  # Move the position to the end of the matched text

    # Append an end-of-file token to signify the end of input
        tokens.append(Token("EOF", "$"))

        return tokens  # Return the list of tokens


# How the lexer is storing the tokens
"""
[Token(MAIN, main), 
Token(BEGIN, begin), 
Token(NUM_TYPE, num), 
Token(VNAME, V_x), 
Token(COMMA, ,), 
Token(TEXT_TYPE, text), 
Token(VNAME, V_y), 
Token(COMMA, ,), 
Token(VNAME, V_x), 
Token(INPUT_OP, <), 
Token(INPUT, input), 
Token(PRINT, print), 
Token(VNAME, V_x), 
Token(SEMICOLON, ;), 
Token(RETURN, return), 
Token(VNAME, V_x), 
Token(END, end), 
Token(EOF, $)]
"""
