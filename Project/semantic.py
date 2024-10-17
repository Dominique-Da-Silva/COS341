import re

# ANSI color codes for colored output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
RESET = '\033[0m'

class SemanticError(Exception):
    """ Custom exception for semantic analysis errors. """
    pass

class Scope:
    def __init__(self, name, parent_scope=None, level=0):
        self.name = name
        self.symbols = {}  # Store variable/function names and their internal unique identifiers
        self.parent_scope = parent_scope
        self.level = level

    def declare(self, name, symbol_type, unid):
        """ Declares a new variable or function in the current scope. """
        if name in self.symbols:
            raise SemanticError(f"Error: '{name}' is already declared in this scope '{self.name}'.")
        self.symbols[name] = {"type": symbol_type, "unid": unid}

    def lookup(self, name):
        """ Looks up a symbol in the current scope or any parent scope. """
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent_scope:
            return self.parent_scope.lookup(name)
        else:
            raise SemanticError(f"Error: '{name}' is used but not declared in any scope.")

    def has(self, name):
        """ Checks if a symbol is declared in the current scope (only). """
        return name in self.symbols


class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("global", level=0)
        self.current_scope = self.global_scope
        self.unique_id_counter = 0
        self.scopes = [self.global_scope]  # Global scope is the first one

    def enter_scope(self, scope_name):
        new_scope = Scope(scope_name, parent_scope=self.current_scope, level=self.current_scope.level + 1)
        self.current_scope = new_scope
        self.scopes.append(new_scope)

    def exit_scope(self):
        if self.current_scope.parent_scope:
            self.current_scope = self.current_scope.parent_scope
        else:
            raise SemanticError("Attempted to exit global scope, which is not allowed.")

    def declare_symbol(self, name, symbol_type, unid):
        self.current_scope.declare(name, symbol_type, unid)

    def lookup_symbol(self, name):
        return self.current_scope.lookup(name)

    def print_table(self):
        print("\n=== Symbol Table ===")
        for scope in self.scopes:
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
        metadata.append((word, class_name, unid))
    
    return metadata


def analyze_scopes_from_input_file(input_file, symbol_table, metadata):
    """
    Analyze scopes based on the input file to determine scope nesting.
    """
    with open(input_file, 'r') as file:
        input_text = file.read()

    # Regular expressions to identify functions and scopes
    function_regex = re.compile(r"(num|void)\s+(\w+)\s*\(([^)]*)\)\s*\{", re.MULTILINE)
    variable_regex = re.compile(r"(num|text)\s+(\w+)")
    begin_regex = re.compile(r"begin")
    end_regex = re.compile(r"end")

    # Track scope nesting level
    current_scope_stack = [symbol_table.global_scope]  # Stack to track scope levels

    # Process functions and declare them in the global scope
    for match in function_regex.finditer(input_text):
        return_type, func_name, params = match.groups()

        # Declare the function in the global scope
        for name, class_name, unid in metadata:
            if name == func_name and class_name == "FNAME":
                symbol_table.declare_symbol(func_name, "func", unid)

        # Enter the function scope
        symbol_table.enter_scope(func_name)
        current_scope_stack.append(symbol_table.current_scope)

        # Declare function parameters in the function's scope
        for param in params.split(','):
            param = param.strip()
            if param:
                param_name = param.split()[-1]  # Get the parameter variable name
                for name, class_name, unid in metadata:
                    if name == param_name and class_name == "V":
                        symbol_table.declare_symbol(param_name, "var", unid)

        # Declare local variables within the function
        for var_match in variable_regex.finditer(input_text, match.end()):
            var_type, var_name = var_match.groups()
            for name, class_name, unid in metadata:
                if name == var_name and class_name == "V":
                    symbol_table.declare_symbol(var_name, "var", unid)

        # Process block scopes within the function
        analyze_block_scopes(input_text[match.end():], symbol_table, metadata, current_scope_stack)

        # Exit function scope after handling
        if len(current_scope_stack) > 1:  # Ensure we don't exit the global scope
            symbol_table.exit_scope()
            current_scope_stack.pop()


def analyze_block_scopes(block_text, symbol_table, metadata, current_scope_stack):
    """
    Analyze block scopes within a function.
    """
    begin_regex = re.compile(r"begin")
    end_regex = re.compile(r"end")

    # Process block scopes defined by 'begin' and 'end'
    for line in block_text.splitlines():
        if begin_regex.search(line):
            # Enter a new block scope
            block_scope_name = f"Block_Level_{len(current_scope_stack)}"
            symbol_table.enter_scope(block_scope_name)
            current_scope_stack.append(symbol_table.current_scope)

        elif end_regex.search(line):
            # Exit the current block scope
            if len(current_scope_stack) > 1:  # Prevent exiting global scope
                symbol_table.exit_scope()
                current_scope_stack.pop()


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
    analyze_scopes_from_input_file(input_file, symbol_table, metadata)

    # Step 3: Print the symbol table after analysis
    symbol_table.print_table()
