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
            (24, 'VNAME'): ('shift', 8),
            (24, 'CONST_N'): ('shift', 40),
            (24, 'CONST_T'): ('shift', 41),
            (25, 'INPUT_OP'): ('shift', 43),
            (25, 'ASSIGN'): ('shift', 44),
            (26, 'LPAREN'): ('shift', 45),
            (27, 'NOT'): ('shift', 59),
            (27, 'SQRT'): ('shift', 60),
            (27, 'OR'): ('shift', 51),
            (27, 'AND'): ('shift', 52),
            (27, 'EQ'): ('shift', 53),
            (27, 'GRT'): ('shift', 54),
            (27, 'ADD'): ('shift', 55),
            (27, 'SUB'): ('shift', 56),
            (27, 'MUL'): ('shift', 57),
            (27, 'DIV'): ('shift', 58),
            (28, 'LPAREN'): ('reduce', 46),
            (29, 'NUM_TYPE'): ('shift', 4),
            (29, 'TEXT_TYPE'): ('shift', 5),
            (29, 'BEGIN'): ('reduce', 1),
            (30, 'END'): ('reduce', 48),
            (30, 'EOF'): ('reduce', 48),
            (31, 'NUM_TYPE'): ('reduce', 49),
            (31, 'END'): ('reduce', 49),
            (31, 'VOID'): ('reduce', 49),
            (31, 'EOF'): ('reduce', 49),
            (32, 'NUM_TYPE'): ('shift', 4),
            (32, 'TEXT_TYPE'): ('shift', 5),
            (33, 'NUM_TYPE'): ('reduce', 54),
            (33, 'TEXT_TYPE'): ('reduce', 54),
            (34, 'LPAREN'): ('shift', 64),
            (35, 'NUM_TYPE'): ('reduce', 6),
            (35, 'SEMICOLON'): ('reduce', 6),
            (35, 'ELSE'): ('reduce', 6),
            (35, 'VOID'): ('reduce', 6),
            (35, 'RBRACE'): ('reduce', 6),
            (35, 'EOF'): ('reduce', 6),
            (36, 'VNAME'): ('shift', 9),
            (36, 'END'): ('reduce', 7),
            (36, 'SKIP'): ('shift', 18),
            (36, 'HALT'): ('shift', 19),
            (36, 'PRINT'): ('shift', 20),
            (36, 'RETURN'): ('shift', 24),
            (36, 'IF'): ('shift', 27),
            (36, 'FNAME'): ('shift', 28),
            (37, 'SEMICOLON'): ('reduce', 11),
            (38, 'COMMA'): ('reduce', 16),
            (38, 'SEMICOLON'): ('reduce', 16),
            (38, 'RPAREN'): ('reduce', 16),
            (39, 'COMMA'): ('reduce', 17),
            (39, 'SEMICOLON'): ('reduce', 17),
            (39, 'RPAREN'): ('reduce', 17),
            (40, 'COMMA'): ('reduce', 18),
            (40, 'SEMICOLON'): ('reduce', 18),
            (40, 'RPAREN'): ('reduce', 18),
            (41, 'COMMA'): ('reduce', 19),
            (41, 'SEMICOLON'): ('reduce', 19),
            (41, 'RPAREN'): ('reduce', 19),
            (42, 'SEMICOLON'): ('reduce', 15),
            (43, 'INPUT'): ('shift', 66),
            (44, 'VNAME'): ('shift', 9),
            (44, 'NUM_TYPE'): ('shift', 40),
            (44, 'TEXT_TYPE'): ('shift', 41),
            (44, 'NOT'): ('shift', 59),
            (44, 'SQRT'): ('shift', 60),
            (44, 'OR'): ('shift', 51),
            (44, 'AND'): ('shift', 52),
            (44, 'EQ'): ('shift', 53),
            (44, 'GRT'): ('shift', 54),
            (44, 'ADD'): ('shift', 55),
            (44, 'SUB'): ('shift', 56),
            (44, 'MUL'): ('shift', 57),
            (44, 'DIV'): ('shift', 58),
            (44, 'FNAME'): ('shift', 28),
            (45, 'VNAME'): ('shift', 9),
            (45, 'NUM_TYPE'): ('shift', 40),
            (45, 'TEXT_TYPE'): ('shift', 41),
            (46, 'THEN'): ('shift', 74),
            (47, 'THEN'): ('reduce', 31),
            (48, 'THEN'): ('reduce', 32),
            (49, 'LPAREN'): ('shift', 75),
            (50, 'LPAREN'): ('shift', 76),
            (51, 'LPAREN'): ('reduce', 38),
            (52, 'LPAREN'): ('reduce', 39),
            (53, 'LPAREN'): ('reduce', 40),
            (54, 'LPAREN'): ('reduce', 41),
            (55, 'LPAREN'): ('reduce', 42),
            (56, 'LPAREN'): ('reduce', 43),
            (57, 'LPAREN'): ('reduce', 44),
            (58, 'LPAREN'): ('reduce', 45),
            (59, 'LPAREN'): ('reduce', 36),
            (60, 'LPAREN'): ('reduce', 47),
            (61, 'BEGIN'): ('reduce', 2),
            (62, 'BEGIN'): ('shift', 7),
            (63, 'VNAME'): ('shift', 9),
            (64, 'VNAME'): ('shift', 9),
            (65, 'END'): ('reduce', 8),
            (66, 'SEMICOLON'): ('reduce', 20),
            (67, 'SEMICOLON'): ('reduce', 21),
            (68, 'SEMICOLON'): ('reduce', 24),
            (69, 'SEMICOLON'): ('reduce', 25),
            (70, 'SEMICOLON'): ('reduce', 26),
            (71, 'LPAREN'): ('shift', 80),
            (72, 'LPAREN'): ('shift', 81),
            (73, 'COMMA'): ('shift', 82),
            (74, 'BEGIN'): ('shift', 7),
            (75, 'VNAME'): ('shift', 9),
            (75, 'CONST_N'): ('shift', 40),
            (75, 'CONST_T'): ('shift', 41),
            (75, 'OR'): ('shift', 51),
            (75, 'AND'): ('shift', 52),
            (75, 'EQ'): ('shift', 53),
            (75, 'GRT'): ('shift', 54),
            (75, 'ADD'): ('shift', 55),
            (75, 'SUB'): ('shift', 56),
            (75, 'MUL'): ('shift', 57),
            (75, 'DIV'): ('shift', 58),
            (76, 'AND'): ('shift', 52),
            (76, 'EQ'): ('shift', 53),
            (76, 'GRT'): ('shift', 54),
            (76, 'ADD'): ('shift', 55),
            (76, 'SUB'): ('shift', 56),
            (76, 'MUL'): ('shift', 57),
            (76, 'DIV'): ('shift', 58),
            (77, 'RBRACE'): ('shift', 89),
            (78, 'COMMA'): ('shift', 90),
            (79, 'COMMA'): ('shift', 91),
            (80, 'VNAME'): ('shift', 9),
            (80, 'CONST_N'): ('shift', 40),
            (80, 'CONST_T'): ('shift', 41),
            (80, 'NOT'): ('shift', 59),
            (80, 'SQRT'): ('shift', 60),
            (80, 'OR'): ('shift', 51),
            (80, 'AND'): ('shift', 52),
            (80, 'EQ'): ('shift', 53),
            (80, 'GRT'): ('shift', 54),
            (80, 'ADD'): ('shift', 55),
            (80, 'SUB'): ('shift', 56),
            (80, 'MUL'): ('shift', 57),
            (80, 'DIV'): ('shift', 58),
            (81, 'VNAME'): ('shift', 9),
            (81, 'CONST_N'): ('shift', 40),
            (81, 'CONST_T'): ('shift', 41),
            (81, 'NOT'): ('shift', 59),
            (81, 'SQRT'): ('shift', 60),
            (81, 'OR'): ('shift', 51),
            (81, 'AND'): ('shift', 52),
            (81, 'EQ'): ('shift', 53),
            (81, 'GRT'): ('shift', 54),
            (81, 'ADD'): ('shift', 55),
            (81, 'SUB'): ('shift', 56),
            (81, 'MUL'): ('shift', 57),
            (81, 'DIV'): ('shift', 58),
            (82, 'VNAME'): ('shift', 9),
            (82, 'CONST_N'): ('shift', 40),
            (82, 'CONST_T'): ('shift', 41),
            (83, 'ELSE'): ('shift', 97),
            (84, 'COMMA'): ('shift', 98),
            (85, 'COMMA'): ('shift', 99),
            (86, 'LPAREN'): ('shift', 100),
            (87, 'RPAREN'): ('shift', 101),
            (88, 'NUM_TYPE'): ('shift', 14),
            (88, 'END'): ('reduce', 47),
            (88, 'VOID'): ('shift', 15),
            (88, 'EOF'): ('reduce', 47),
            (89, 'NUM_TYPE'): ('reduce', 55),
            (89, 'END'): ('reduce', 55),
            (89, 'VOID'): ('reduce', 55),
            (89, 'EOF'): ('reduce', 55),
            (90, 'NUM_TYPE'): ('shift', 4),
            (90, 'TEXT_TYPE'): ('shift', 5),
            (91, 'VNAME'): ('shift', 9),
            (92, 'RPAREN'): ('shift', 106),
            (93, 'COMMA'): ('reduce', 29),
            (93, 'RPAREN'): ('reduce', 29),
            (94, 'COMMA'): ('reduce', 30),
            (94, 'RPAREN'): ('reduce', 30),
            (95, 'COMMA'): ('shift', 107),
            (96, 'COMMA'): ('shift', 108),
            (97, 'BEGIN'): ('shift', 7),
            (98, 'VNAME'): ('shift', 9),
            (98, 'CONST_N'): ('shift', 40),
            (98, 'CONST_T'): ('shift', 41),
            (99, 'OR'): ('shift', 51),
            (99, 'AND'): ('shift', 52),
            (99, 'EQ'): ('shift', 53),
            (99, 'GRT'): ('shift', 54),
            (99, 'ADD'): ('shift', 55),
            (99, 'SUB'): ('shift', 56),
            (99, 'MUL'): ('shift', 57),
            (99, 'DIV'): ('shift', 58),
            (100, 'VNAME'): ('shift', 9),
            (100, 'CONST_N'): ('shift', 40),
            (100, 'CONST_T'): ('shift', 41),
            (101, 'THEN'): ('reduce', 35),
            (102, 'END'): ('shift', 112),
            (103, 'END'): ('reduce', 57),
            (104, 'VNAME'): ('shift', 9),
            (105, 'COMMA'): ('shift', 114),
            (106, 'COMMA'): ('reduce', 27),
            (106, 'SEMICOLON'): ('reduce', 27),
            (106, 'RPAREN'): ('reduce', 27),
            (107, 'VNAME'): ('shift', 9),
            (107, 'CONST_N'): ('shift', 40),
            (107, 'CONST_T'): ('shift', 41),
            (107, 'NOT'): ('shift', 59),
            (107, 'SQRT'): ('shift', 60),
            (107, 'OR'): ('shift', 51),
            (107, 'AND'): ('shift', 52),
            (107, 'EQ'): ('shift', 53),
            (107, 'GRT'): ('shift', 54),
            (107, 'ADD'): ('shift', 55),
            (107, 'SUB'): ('shift', 56),
            (107, 'MUL'): ('shift', 57),
            (107, 'DIV'): ('shift', 58),
            (108, 'VNAME'): ('shift', 9),
            (108, 'CONST_N'): ('shift', 40),
            (108, 'CONST_T'): ('shift', 41),
            (109, 'SEMICOLON'): ('reduce', 23),
            (110, 'RPAREN'): ('shift', 117),
            (111, 'RPAREN'): ('shift', 118),
            (112, 'NUM_TYPE'): ('reduce', 53),
            (112, 'END'): ('reduce', 53),
            (112, 'VOID'): ('reduce', 53),
            (112, 'EOF'): ('reduce', 53),
            (113, 'COMMA'): ('shift', 119),
            (114, 'VNAME'): ('shift', 9),
            (115, 'RPAREN'): ('shift', 121),
            (116, 'RPAREN'): ('shift', 122),
            (117, 'COMMA'): ('reduce', 33),
            (117, 'RPAREN'): ('reduce', 33),
            (117, 'THEN'): ('reduce', 33),
            (118, 'THEN'): ('reduce', 34),
            (119, 'NUM_TYPE'): ('shift', 4),
            (119, 'TEXT_TYPE'): ('shift', 5),
            (120, 'RPAREN'): ('shift', 124),
            (121, 'COMMA'): ('reduce', 28),
            (121, 'SEMICOLON'): ('reduce', 28),
            (121, 'RPAREN'): ('reduce', 28),
            (122, 'SEMICOLON'): ('reduce', 22),
            (123, 'VNAME'): ('shift', 9),
            (124, 'LBRACE'): ('reduce', 50),
            (125, 'COMMA'): ('shift', 126),
            (126, 'BEGIN'): ('reduce', 56)
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
            (24, 'VNAME'): 38,
            (24, 'ATOMIC'): 42,
            (24, 'CONST'): 39,
            (27, 'COND'): 46,
            (27, 'SIMPLE'): 47,
            (27, 'COMPOSIT'): 48,
            (27, 'UNOP'): 50,
            (27, 'BINOP'): 49,
            (29, 'GLOBVARS'): 61,
            (29, 'VTYP'): 3,
            (32, 'VTYP'): 63,
            (32, 'LOCVARS'): 62,
            (36, 'VNAME'): 25,
            (36, 'INSTRUC'): 65,
            (36, 'COMMAND'): 17,
            (36, 'ASSIGN'): 21,
            (36, 'CALL'): 22,
            (36, 'BRANCH'): 23,
            (36, 'FNAME'): 26,
            (44, 'VNAME'): 38,
            (44, 'ATOMIC'): 68,
            (44, 'CONST'): 39,
            (44, 'CALL'): 69,
            (44, 'TERM'): 67,
            (44, 'OP'): 70,
            (44, 'UNOP'): 71,
            (44, 'BINOP'): 72,
            (44, 'FNAME'): 26,
            (45, 'VNAME'): 38,
            (45, 'ATOMIC'): 73,
            (45, 'CONST'): 39,
            (62, 'ALGO'): 77,
            (63, 'VNAME'): 78,
            (64, 'VNAME'): 79,
            (74, 'ALGO'): 83,
            (75, 'VNAME'): 38,
            (75, 'ATOMIC'): 84,
            (75, 'CONST'): 39,
            (75, 'SIMPLE'): 85,
            (75, 'BINOP'): 86,
            (76, 'SIMPLE'): 87,
            (76, 'BINOP'): 86,
            (77, 'EPILOG'): 88, 
            (80, 'VNAME'): 38,
            (80, 'ATOMIC'): 93,
            (80, 'CONST'): 39,
            (80, 'OP'): 94,
            (80, 'ARG'): 92,
            (80, 'UNOP'): 71,
            (80, 'BINOP'): 72,
            (81, 'VNAME'): 38,
            (81, 'ATOMIC'): 93,
            (81, 'CONST'): 39,
            (81, 'OP'): 94,
            (81, 'ARG'): 95,
            (81, 'UNOP'): 71,
            (81, 'BINOP'): 72,
            (82, 'VNAME'): 38,
            (82, 'CONST'): 39,
            (82, 'ATOMIC'): 96,
            (88, 'FUNCTIONS'): 103,
            (88, 'DECL'): 11,
            (88, 'HEADER'): 12,
            (88, 'FTYP'): 13,
            (88, 'SUBFUNCS'): 102,
            (90, 'VTYP'): 104,
            (91, 'VNAME'): 105,
            (97, 'ALGO'): 109,
            (98, 'VNAME'): 38,
            (98, 'ATOMIC'): 110,
            (98, 'CONST'): 39,
            (99, 'SIMPLE'): 111,
            (99, 'BINOP'): 86,
            (100, 'VNAME'): 38,
            (100, 'ATOMIC'): 84,
            (100, 'CONST'): 39,
            (104, 'VNAME'): 113,
            (107, 'VNAME'): 38,
            (107, 'ATOMIC'): 93,
            (107, 'CONST'): 39,
            (107, 'OP'): 94,
            (107, 'ARG'): 115,
            (107, 'UNOP'): 71,
            (107, 'BINOP'): 72,
            (108, 'VNAME'): 38,
            (108, 'ATOMIC'): 116,
            (108, 'CONST'): 39,
            (114, 'VNAME'): 120,
            (119, 'VTYP'): 123,
            (123, 'VNAME') : 125,
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