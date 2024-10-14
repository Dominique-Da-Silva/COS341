import xml.etree.ElementTree as ET

'''
===========================================================================================
'''
class Token:
    """
    Token class to store information about each token.
    """
    def __init__(self, token_id, token_class, token_value):
        self.token_id = token_id
        self.token_class = token_class
        self.token_value = token_value

    def __repr__(self):
        return f'Token({self.token_id}, {self.token_class}, {self.token_value})'



'''
===========================================================================================
'''
class ProductionRule:
    """
    Class to represent a production rule in the grammar.
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs  # Left-hand side non-terminal
        self.rhs = rhs  # Right-hand side list of symbols (terminals and/or non-terminals)

    def __repr__(self):
        return f"{self.lhs} -> {' '.join(self.rhs)}"



'''
===========================================================================================
The SLR parser class that reads tokens from the XML file, parses the input, and constructs a parse tree.
'''
class SLRParser:
    '''
    ------------------------------------------------------------------------------------------
    '''
    def __init__(self, xml_file):
        self.tokens = self.load_tokens_from_xml(xml_file)
        self.current_token_index = 0  # Keep track of which token we're parsing

        # Parsing tables
        self.action_table = {}  # Action table for shift/reduce actions
        self.goto_table = {}    # Goto table for non-terminal transitions

        # Grammar rules
        self.grammar_rules = []

        self.stack = []  # Parser stack for handling shifts and reductions

        # Initialize parsing table and grammar rules
        self.initialize_parsing_table()
        self.initialize_grammar_rules()


    '''
    ------------------------------------------------------------------------------------------
    '''
    def initialize_parsing_table(self):
        """
        Initialize the parsing table with the actions and goto entries.
        You need to fill this method with the actual parsing table entries based on your grammar.
        """

        # Example of how to define the action table (to be replaced with your parsing table):

        # The keys are tuples of (state, input_symbol)
        # The values are actions: ('shift', next_state), ('reduce', production_number), or ('accept',)
        # Terminals should match the 'token_class' from your lexer

        # self.action_table = {
        #     (0, 'id'): ('shift', 5),
        #     (0, '('): ('shift', 4),
        #     (1, '+'): ('shift', 6),
        #     (1, 'EOF'): ('accept',),
        #     # ... other entries ...
        # }

        # Example of how to define the goto table:

        # The keys are tuples of (state, non_terminal)
        # The values are the next state numbers

        # self.goto_table = {
        #     (0, 'E'): 1,
        #     (0, 'T'): 2,
        #     (0, 'F'): 3,
        #     # ... other entries ...
        # }

        pass  # Remove this pass statement when you add the parsing table entries


    '''
    ------------------------------------------------------------------------------------------
    '''
    def initialize_grammar_rules(self):
        """
        Initialize the grammar rules used for reductions.
        You need to fill this method with your grammar's production rules.
        """

        # Example of how to define grammar rules:

        # self.grammar_rules = [
        #     ProductionRule('E\'', ['E']),          # Production 0
        #     ProductionRule('E', ['E', '+', 'T']),  # Production 1
        #     ProductionRule('E', ['T']),            # Production 2
        #     ProductionRule('T', ['T', '*', 'F']),  # Production 3
        #     ProductionRule('T', ['F']),            # Production 4
        #     ProductionRule('F', ['(', 'E', ')']),  # Production 5
        #     ProductionRule('F', ['id']),           # Production 6
        # ]

        pass  # Remove this pass statement when you add the grammar rules


    '''
    ------------------------------------------------------------------------------------------
    '''
    def load_tokens_from_xml(self, xml_file):
        """
        Load tokens from an XML file and return a list of Token objects.
        """
        tokens = []
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for tok in root.findall('TOK'):
            token_id = int(tok.find('ID').text)
            token_class = tok.find('CLASS').text
            token_value = tok.find('WORD').text
            tokens.append(Token(token_id, token_class, token_value))

        # Append the EOF token ('$') to signal the end of input
        tokens.append(Token(len(tokens) + 1, 'EOF', '$'))

        return tokens


    '''
    ------------------------------------------------------------------------------------------
    '''
    def current_token(self):
        """
        Returns the current token to be parsed.
        """
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None  # End of input


    '''
    ------------------------------------------------------------------------------------------
    '''
    def advance_token(self):
        """
        Advances to the next token.
        """
        self.current_token_index += 1


    '''
    ------------------------------------------------------------------------------------------
    '''
    def parse(self):
        """
        Main parsing function. Uses the parsing table and grammar rules to construct a parse tree.
        """
        # Initialize stack with state 0
        self.stack = [0]

        while True:
            state = self.stack[-1]  # Current state is on top of the stack
            token = self.current_token()  # Lookahead token

            if token is None:
                # Should not happen as EOF token is added
                raise SyntaxError("Unexpected end of input.")

            # Get the action from the action table
            action = self.action_table.get((state, token.token_class))

            if action is None:
                # Parsing error
                raise SyntaxError(f"Parsing error at token {token.token_value} ({token.token_class}) at position {self.current_token_index}")

            if action[0] == 'shift':
                # Shift action
                next_state = action[1]
                self.stack.append(token.token_class)  # Push the token class (terminal symbol)
                self.stack.append(next_state)         # Push the next state
                self.advance_token()                  # Move to the next token

            elif action[0] == 'reduce':
                # Reduce action
                production_number = action[1]
                production = self.grammar_rules[production_number]

                # Pop 2 * len(rhs) items from stack (symbol and state for each symbol)
                pop_length = 2 * len(production.rhs)
                for _ in range(pop_length):
                    self.stack.pop()

                # Get the current state after popping
                current_state = self.stack[-1]

                # Push the LHS non-terminal
                self.stack.append(production.lhs)

                # Get the next state from the goto table
                goto_state = self.goto_table.get((current_state, production.lhs))
                if goto_state is None:
                    # Goto error
                    raise SyntaxError(f"Goto error for state {current_state} and non-terminal {production.lhs}")

                self.stack.append(goto_state)

                # Optionally, build parse tree nodes here if needed

            elif action[0] == 'accept':
                # Accept action
                print("Parsing completed successfully.")
                return True

            else:
                # Invalid action
                raise SyntaxError(f"Invalid action {action} for state {state} and token {token.token_class}")

            # Uncomment the following lines for debugging purposes
            # print(f"Stack: {self.stack}")
            # print(f"Next token: {token}")