import xml.etree.ElementTree as ET

class Token:
    """
    Token class to store information about each token.
    """
    def __init__(self, token_id, token_class, token_value):
        self.token_id = token_id  # Token ID from the XML file
        self.token_class = token_class  # Class of the token (e.g., 'reserved_keyword', 'N')
        self.token_value = token_value  # Actual value of the token (e.g., 'else', '56.7')

    def __repr__(self):
        return f'Token({self.token_id}, {self.token_class}, {self.token_value})'


class SLRParser:
    """
    The SLR parser class that reads tokens from the XML file, parses the input, and constructs a parse tree.
    """

    def __init__(self, xml_file):
        self.tokens = self.load_tokens_from_xml(xml_file)
        self.current_token_index = 0  # Keep track of which token we're parsing
        self.parsing_table = {}  # Placeholder for the parsing table (to be filled)
        self.grammar_rules = []  # Placeholder for grammar rules (to be filled)
        self.stack = []  # Parser stack for handling shifts and reductions

    def load_tokens_from_xml(self, xml_file):
        """
        Load tokens from an XML file and return a list of Token objects.
        """
        tokens = []
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for tok in root.findall('TOK'):
            token_id = tok.find('ID').text
            token_class = tok.find('CLASS').text
            token_value = tok.find('WORD').text
            tokens.append(Token(token_id, token_class, token_value))

        # Append the EOF token ('$') to signal the end of input
        tokens.append(Token(len(tokens)+1, 'EOF', '$'))

        return tokens

    def current_token(self):
        """
        Returns the current token to be parsed.
        """
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def advance_token(self):
        """
        Advances to the next token.
        """
        self.current_token_index += 1

    def parse(self):
        """
        Main parsing function. Uses the parsing table and grammar rules to construct a parse tree.
        """
        # Initialize stack with state 0
        self.stack = [0]

        # Start parsing tokens one by one
        
