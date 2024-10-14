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

        self.action_table = {
            (0, 'MAIN'): ('shift', 1),
            (1, 'NUM_TYPE'): ('shift', 4),
            (1, 'TEXT_TYPE'): ('shift', 5),
            (1, 'BEGIN'): ('reduce',1),
            (2, 'BEGIN'): ('shift',7),
            (3, 'VNAME'): ('shift',9),
            (4, 'VNAME'): ('reduce',3),
            (5, 'VNAME') : ('reduce',4),
            (6, 'NUM_TYPE'): ('shift', 14),
            (6, 'END'): ('reduce', 47),
            (6, 'VOID'): ('shift', 15),
            (6, 'EOF'): ('reduce', 47),
            (7, 'VNAME'): ('shift', 9),
            (7, 'END'): ('reduce', 7),
            (7, 'SKIP'): ('shift', 18),
            (7, 'HALT'): ('shift', 19), 
            (7, 'PRINT'): ('shift', 20),
            (7, 'RETURN'): ('shift', 24),
            (7, 'IF'): ('shift', 27),
            (7, 'FNAME'): ('shift', 28),
            (8, 'COMMA'): ('shift', 29),
            (9, 'COMMA'): ('reduce',5),
            (9, 'SEMICOLON'): ('reduce',5),
            (9, 'INPUT_OP'): ('reduce', 5),
            (9, 'ASSIGN'): ('reduce', 5),
            (9, 'RPAREN'): ('reduce', 5),
            (10, 'EOF'): ('accept'),
            (11, 'NUM_TYPE'): ('shift', 14),
            (11, 'END'): ('reduce', 47),
            (11, 'VOID'): ('shift', 15),
            (11, 'EOF'): ('reduce',47),
            (12, 'LBRACE'): ('shift', 33),
            (13, 'FNAME'): ('shift', 28),
            (14, 'FNAME'): ('reduce', 51),
            (15, 'FNAME'): ('reduce', 52),
            (16, 'END'): ('shift', 35),
            (17, 'SEMICOLON'): ('shift', 36),
            (18, 'SEMICOLON'): ('reduce', 9),
            (19, 'SEMICOLON'): ('reduce', 10),
            (20, 'VNAME'): ('shift', 9),
            (20, 'CONST_N'): ('shift', 40),
            (20, 'CONST_T'): ('shift', 41),
            (21, 'SEMICOLON'): ('reduce', 12),
            (22, 'SEMICOLON'): ('reduce', 13),
            (23, 'SEMICOLON'): ('reduce', 14),
        }


        self.goto_table = {
            (1, 'GLOBVARS'): 2,
            (1, 'VTYPE'): 3,
            (2, 'ALGO'): 6,
            (3, 'VNAME'): 8,
            (6, 'FUNCTIONS'):10,
            (6, 'DECL'): 11,
            (6, 'HEADER'): 12,
            (6, 'FTYP'): 13,
            (7, 'VNAME'): 25,
            (7, 'INSTRUC'): 16,
            (7, 'COMMAND'): 17,
            (7, 'ASSIGN'): 21,
            (7, 'CALL'): 22,
            (7, 'BRANCH'): 23,
            (7, 'FNAME'): 26,
            (11, 'FUNCTIONS'): 30,
            (11, 'DECL'): 11,
            (11, 'HEADER'): 12,
            (11, 'FTYP'): 13,
            (12, 'BODY'): 31,
            (12, 'PROLOG'): 32,
            (13, 'FNAME'): 34,
            (20, 'VNAME'): 38,
            (20, 'ATOMIC'): 37,
            (20, 'CONST'): 39, 
        }


    '''
    ------------------------------------------------------------------------------------------
    '''
    def initialize_grammar_rules(self):
        """
        Initialize the grammar rules used for reductions.
        You need to fill this method with your grammar's production rules.
        """

        self.grammar_rules = [
            # Production 0
            ProductionRule('PROG', ['MAIN', 'GLOBVARS', 'ALGO', 'FUNCTIONS']),
            
            # Production 1 (epsilon production)
            ProductionRule('GLOBVARS', []),
            
            # Production 2
            ProductionRule('GLOBVARS', ['VTYP', 'VNAME', 'COMMA', 'GLOBVARS']),
            
            # Production 3
            ProductionRule('VTYP', ['NUM_TYPE']),
            
            # Production 4
            ProductionRule('VTYP', ['TEXT_TYPE']),
            
            # Production 5
            ProductionRule('VNAME', ['VNAME_ID']),
            
            # Production 6
            ProductionRule('ALGO', ['BEGIN', 'INSTRUC', 'END']),
            
            # Production 7 (epsilon production)
            ProductionRule('INSTRUC', []),
            
            # Production 8
            ProductionRule('INSTRUC', ['COMMAND', 'SEMICOLON', 'INSTRUC']),
            
            # Production 9
            ProductionRule('COMMAND', ['SKIP']),
            
            # Production 10
            ProductionRule('COMMAND', ['HALT']),
            
            # Production 11
            ProductionRule('COMMAND', ['PRINT', 'ATOMIC']),
            
            # Production 12
            ProductionRule('COMMAND', ['ASSIGN']),
            
            # Production 13
            ProductionRule('COMMAND', ['CALL']),
            
            # Production 14
            ProductionRule('COMMAND', ['BRANCH']),
            
            # Production 15
            ProductionRule('COMMAND', ['RETURN', 'ATOMIC']),
            
            # Production 16
            ProductionRule('ATOMIC', ['VNAME']),
            
            # Production 17
            ProductionRule('ATOMIC', ['CONST']),
            
            # Production 18
            ProductionRule('CONST', ['CONST_N']),
            
            # Production 19
            ProductionRule('CONST', ['CONST_T']),
            
            # Production 20
            ProductionRule('ASSIGN', ['VNAME', 'INPUT_OP', 'INPUT']),
            
            # Production 21
            ProductionRule('ASSIGN', ['VNAME', 'ASSIGN', 'TERM']),
            
            # Production 22
            ProductionRule('CALL', ['FNAME', 'LPAREN', 'ATOMIC', 'COMMA', 'ATOMIC', 'COMMA', 'ATOMIC', 'RPAREN']),
            
            # Production 23
            ProductionRule('BRANCH', ['IF', 'COND', 'THEN', 'ALGO', 'ELSE', 'ALGO']),
            
            # Production 24
            ProductionRule('TERM', ['ATOMIC']),
            
            # Production 25
            ProductionRule('TERM', ['CALL']),
            
            # Production 26
            ProductionRule('TERM', ['OP']),
            
            # Production 27
            ProductionRule('OP', ['UNOP', 'LPAREN', 'ARG', 'RPAREN']),
            
            # Production 28
            ProductionRule('OP', ['BINOP', 'LPAREN', 'ARG', 'COMMA', 'ARG', 'RPAREN']),
            
            # Production 29
            ProductionRule('ARG', ['ATOMIC']),
            
            # Production 30
            ProductionRule('ARG', ['OP']),
            
            # Production 31
            ProductionRule('COND', ['SIMPLE']),
            
            # Production 32
            ProductionRule('COND', ['COMPOSIT']),
            
            # Production 33
            ProductionRule('SIMPLE', ['BINOP', 'LPAREN', 'ATOMIC', 'COMMA', 'ATOMIC', 'RPAREN']),
            
            # Production 34
            ProductionRule('COMPOSIT', ['BINOP', 'LPAREN', 'SIMPLE', 'COMMA', 'SIMPLE', 'RPAREN']),
            
            # Production 35
            ProductionRule('COMPOSIT', ['UNOP', 'LPAREN', 'SIMPLE', 'RPAREN']),
            
            # Production 36
            ProductionRule('UNOP', ['NOT']),
            
            # Production 37
            ProductionRule('UNOP', ['SQRT']),
            
            # Production 38
            ProductionRule('BINOP', ['OR']),
            
            # Production 39
            ProductionRule('BINOP', ['AND']),
            
            # Production 40
            ProductionRule('BINOP', ['EQ']),
            
            # Production 41
            ProductionRule('BINOP', ['GRT']),
            
            # Production 42
            ProductionRule('BINOP', ['ADD']),
            
            # Production 43
            ProductionRule('BINOP', ['SUB']),
            
            # Production 44
            ProductionRule('BINOP', ['MUL']),
            
            # Production 45
            ProductionRule('BINOP', ['DIV']),
            
            # Production 46
            ProductionRule('FNAME', ['FNAME_ID']),
            
            # Production 47 (epsilon production)
            ProductionRule('FUNCTIONS', []),
            
            # Production 48
            ProductionRule('FUNCTIONS', ['DECL', 'FUNCTIONS']),
            
            # Production 49
            ProductionRule('DECL', ['HEADER', 'BODY']),
            
            # Production 50
            ProductionRule('HEADER', ['FTYP', 'FNAME', 'LPAREN', 'VNAME', 'COMMA', 'VNAME', 'COMMA', 'VNAME', 'RPAREN']),
            
            # Production 51
            ProductionRule('FTYP', ['NUM_TYPE']),
            
            # Production 52
            ProductionRule('FTYP', ['VOID']),
            
            # Production 53
            ProductionRule('BODY', ['PROLOG', 'LOCVARS', 'ALGO', 'EPILOG', 'SUBFUNCS', 'END']),
            
            # Production 54
            ProductionRule('PROLOG', ['LBRACE']),
            
            # Production 55
            ProductionRule('EPILOG', ['RBRACE']),
            
            # Production 56
            ProductionRule('LOCVARS', ['VTYP', 'VNAME', 'COMMA', 'VTYP', 'VNAME', 'COMMA', 'VTYP', 'VNAME', 'COMMA']),
            
            # Production 57
            ProductionRule('SUBFUNCS', ['FUNCTIONS']),         
        ]


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