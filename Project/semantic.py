import re

# ANSI color codes for colored output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
RESET = '\033[0m'

# Define the set of reserved keywords
reserved_keywords = {'num', 'text', 'begin', 'end', 'if', 'else', 'return', 'main', 'void', 'and', 'or', 'not', 'grt', 'eq', 'add', 'sub', 'mul', 'div', 'input'}

class SemanticError(Exception):
    """ Custom exception for semantic analysis errors. """
    def __init__(self, message, line_number=None, line_content=None):
        if line_number is not None and line_content is not None:
            message = f"Error at line {line_number}: {line_content}\n{message}"
        super().__init__(message)

class Scope:
    def __init__(self, name, parent_scope=None, level=0, scope_type='block'):
        self.name = name
        self.symbols = {}  # Store variable/function names and their internal unique identifiers
        self.parent_scope = parent_scope
        self.level = level
        self.scope_type = scope_type

    def declare(self, name, symbol_type, unid, line_number=None, line_content=None):
        """ Declares a new variable or function in the current scope. """
        if name in self.symbols:
            raise SemanticError(f"'{name}' is already declared in this scope '{self.name}'.", line_number, line_content)
        self.symbols[name] = {"type": symbol_type, "unid": unid}

    def lookup(self, name, line_number=None, line_content=None):
        """ Looks up a symbol in the current scope or any parent scope. """
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent_scope:
            return self.parent_scope.lookup(name, line_number, line_content)
        else:
            raise SemanticError(f"'{name}' is used but not declared in any scope.", line_number, line_content)

    def has(self, name):
        """ Checks if a symbol is declared in the current scope (only). """
        return name in self.symbols

class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("global", level=0)
        self.current_scope = self.global_scope
        self.unique_id_counter = 0
        self.scopes = [self.global_scope]  # Global scope is the first one

    def enter_scope(self, scope_name, scope_type='block', level=None):
        if level is None:
            new_level = self.current_scope.level + 1
        else:
            new_level = level
        new_scope = Scope(scope_name, parent_scope=self.current_scope, level=new_level, scope_type=scope_type)
        self.current_scope = new_scope
        self.scopes.append(new_scope)

    def exit_scope(self):
        if self.current_scope.parent_scope:
            self.current_scope = self.current_scope.parent_scope
        else:
            raise SemanticError("Attempted to exit global scope, which is not allowed.")

    def declare_symbol(self, name, symbol_type, unid, scope=None, line_number=None, line_content=None):
        if scope is None:
            scope = self.current_scope
        scope.declare(name, symbol_type, unid, line_number, line_content)

    def lookup_symbol(self, name, line_number=None, line_content=None):
        # Start lookup from the current scope
        scope = self.current_scope
        while scope is not None:
            if name in scope.symbols:
                return scope.symbols[name]
            scope = scope.parent_scope  # Move up to the parent scope
        # If not found in any scope
        raise SemanticError(f"'{name}' is used but not declared in any scope.", line_number, line_content)

    def print_table(self):
        print("\n=== Symbol Table ===")
        for scope in self.scopes:
            # Skip printing empty block levels
            if not scope.symbols and "Block_Level" in scope.name:
                continue
            print(f"Scope: {scope.name} (Level: {scope.level})")
            for name, info in scope.symbols.items():
                print(f"  {name} -> Type: {info['type']}, UNID: {info['unid']}")
        print("====================\n")

def extract_metadata_from_syntax_tree(xml_file):
    """
    Extract all function and variable names and their unique IDs from the syntax tree.
    """
    import xml.etree.ElementTree as ET

    # Load the XML syntax tree
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        print(f"{GREEN}Loaded XML file successfully: {xml_file}{RESET}")
    except ET.ParseError as e:
        print(f"{RED}XML Parse Error: {e}{RESET}")
        return None

    metadata = []
    for leaf in root.findall(".//LEAF"):
        terminal = leaf.find("TERMINAL")
        word = terminal.find("WORD").text
        class_name = terminal.find("CLASS").text
        unid = leaf.find("UNID").text
        metadata.append({'word': word, 'class_name': class_name, 'unid': unid})
    return metadata

def perform_semantic_analysis(xml_file, input_file):
    """
    Perform semantic analysis by combining syntax tree metadata and input file scope analysis.
    """
    symbol_table = SymbolTable()

    # Step 1: Extract metadata (names, IDs) from the syntax tree
    metadata = extract_metadata_from_syntax_tree(xml_file)
    if not metadata:
        return

    # Step 2: Analyze scopes based on the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    current_scope_stack = [symbol_table.global_scope]
    inside_function = False

    for line_number, line in enumerate(lines, start=1):
        original_line = line.rstrip('\n')
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Begin block
        if line == 'begin':
            # Enter new block scope
            block_scope_name = f"Block_Level_{len(current_scope_stack)}"
            symbol_table.enter_scope(block_scope_name, scope_type='block')
            current_scope_stack.append(symbol_table.current_scope)
            continue

        # End block or function
        if line == 'end':
            if len(current_scope_stack) > 1:
                current_scope = current_scope_stack[-1]
                if current_scope.scope_type == 'function':
                    inside_function = False
                symbol_table.exit_scope()
                current_scope_stack.pop()
            continue

        # Function declaration
        function_decl_match = re.match(r'(num|void)\s+(\w+)\s*\(([^)]*)\)', line)
        if function_decl_match:
            return_type, func_name, params = function_decl_match.groups()
            # Check if the function name is a reserved keyword
            if func_name in reserved_keywords:
                raise SemanticError(f"Function name '{func_name}' is a reserved keyword.", line_number, original_line)
            # Find the unid from metadata
            unid = None
            for i, entry in enumerate(metadata):
                if entry['word'] == func_name and entry['class_name'] == 'FNAME':
                    unid = entry['unid']
                    del metadata[i]
                    break
            if unid is None:
                raise SemanticError(f"Function '{func_name}' not found in syntax tree metadata.", line_number, original_line)
            # Declare function in global scope
            try:
                symbol_table.declare_symbol(func_name, "func", unid, scope=symbol_table.global_scope, line_number=line_number, line_content=original_line)
            except SemanticError as e:
                raise SemanticError(str(e), line_number, original_line)
            # Enter function scope
            symbol_table.enter_scope(func_name, scope_type='function')
            current_scope_stack.append(symbol_table.current_scope)
            # Declare function parameters in the function's scope
            params_list = params.split(',')
            for param in params_list:
                param = param.strip()
                if param:
                    param_name = param.split()[-1]  # Get parameter name
                    # Check if the parameter name is a reserved keyword
                    if param_name in reserved_keywords:
                        raise SemanticError(f"Parameter name '{param_name}' is a reserved keyword.", line_number, original_line)
                    # Find the unid from metadata
                    unid = None
                    for i, entry in enumerate(metadata):
                        if entry['word'] == param_name and entry['class_name'] == 'V':
                            unid = entry['unid']
                            del metadata[i]
                            break
                    if unid is None:
                        raise SemanticError(f"Parameter '{param_name}' not found in syntax tree metadata.", line_number, original_line)
                    try:
                        symbol_table.declare_symbol(param_name, "var", unid, line_number=line_number, line_content=original_line)
                    except SemanticError as e:
                        raise SemanticError(str(e), line_number, original_line)
            inside_function = True
            continue

        # Variable declaration
        variable_decl_matches = re.findall(r'(num|text)\s+(\w+)', line)
        if variable_decl_matches:
            for var_type, var_name in variable_decl_matches:
                # Check if the variable name is a reserved keyword
                if var_name in reserved_keywords:
                    raise SemanticError(f"Variable name '{var_name}' is a reserved keyword.", line_number, original_line)
                # Find the unid from metadata
                unid = None
                for i, entry in enumerate(metadata):
                    if entry['word'] == var_name and entry['class_name'] == 'V':
                        unid = entry['unid']
                        del metadata[i]
                        break
                if unid is None:
                    raise SemanticError(f"Variable '{var_name}' not found in syntax tree metadata.", line_number, original_line)
                try:
                    symbol_table.declare_symbol(var_name, "var", unid, line_number=line_number, line_content=original_line)
                except SemanticError as e:
                    raise SemanticError(str(e), line_number, original_line)
            continue

        # Variable usage in assignments and expressions
        variable_use_matches = re.findall(r'\b(V_\w+)\b', line)
        # Exclude string literals
        if '"' in line or "'" in line:
            line_no_strings = re.sub(r'".*?"|\'.*?\'', '', line)
            variable_use_matches = re.findall(r'\b(V_\w+)\b', line_no_strings)

        for var_name in variable_use_matches:
            # Skip if already handled (e.g., in declarations)
            if re.match(r'(num|text)\s+' + var_name, line):
                continue
            # Skip if part of a function declaration or call
            if re.match(r'\w+\s*\(.*\)', line):
                continue
            try:
                symbol_table.lookup_symbol(var_name, line_number, original_line)
            except SemanticError as e:
                raise SemanticError(str(e), line_number, original_line)

        # Assignment statements
        assignment_match = re.match(r'(\w+)\s*(<|=)\s*(.+);', line)
        if assignment_match:
            var_name, operator, expression = assignment_match.groups()
            # Check that the variable being assigned to is declared
            try:
                symbol_table.lookup_symbol(var_name, line_number, original_line)
            except SemanticError as e:
                raise SemanticError(str(e), line_number, original_line)

            # Optionally, check variables used in the expression
            expression_vars = re.findall(r'\b(V_\w+)\b', expression)
            for expr_var in expression_vars:
                try:
                    symbol_table.lookup_symbol(expr_var, line_number, original_line)
                except SemanticError as e:
                    raise SemanticError(str(e), line_number, original_line)
            continue

        # Function call
        function_call_match = re.match(r'(\w+)\s*\(([^)]*)\)\s*;', line)
        if function_call_match:
            func_name, args = function_call_match.groups()
            # Ensure function is declared
            try:
                symbol_table.lookup_symbol(func_name, line_number, original_line)
            except SemanticError as e:
                raise SemanticError(str(e), line_number, original_line)

            # Enter call scope at the same level as current scope
            symbol_table.enter_scope(f"Call_{func_name}", scope_type='call', level=symbol_table.current_scope.level)
            current_scope_stack.append(symbol_table.current_scope)
            # Check arguments are declared
            args_list = args.split(',')
            for arg in args_list:
                arg = arg.strip()
                if arg:
                    # Handle string literals (e.g., "Zero")
                    if arg.startswith('"') and arg.endswith('"'):
                        continue  # Skip string literals
                    try:
                        symbol_table.lookup_symbol(arg, line_number, original_line)
                    except SemanticError as e:
                        raise SemanticError(str(e), line_number, original_line)
            # Exit call scope
            symbol_table.exit_scope()
            current_scope_stack.pop()
            continue

        # Handle 'main' and global variables after 'main'
        if line == 'main':
            continue  # 'main' keyword, proceed to next line

    # Step 3: Print the symbol table after analysis
    symbol_table.print_table()
