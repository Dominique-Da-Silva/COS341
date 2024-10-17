# ANSI color codes for colored output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
RESET = '\033[0m'

class SemanticError(Exception):
    """
    Custom exception for semantic analysis errors.
    """
    pass

class Scope:
    def __init__(self, name, parent_scope=None):
        self.name = name
        self.symbols = {}  # Store variable/function names and their internal unique identifiers
        self.parent_scope = parent_scope

    def declare(self, name, symbol_type, unid):
        """
        Declares a new variable or function in the current scope.
        Throws an error if the name is already declared in this scope.
        """
        if name in self.symbols:
            raise SemanticError(f"Error: '{name}' is already declared in this scope '{self.name}'.")
        self.symbols[name] = {"type": symbol_type, "unid": unid}

    def lookup(self, name):
        """
        Looks up a symbol in the current scope or any parent scope.
        Returns the symbol information if found, or raises an error if not declared.
        """
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent_scope:
            return self.parent_scope.lookup(name)
        else:
            raise SemanticError(f"Error: '{name}' is used but not declared in any scope.")

    def has(self, name):
        """
        Checks if a symbol is declared in the current scope (only).
        """
        return name in self.symbols


class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.unique_id_counter = 0
        self.scopes = []

    def enter_scope(self, scope_name):
        new_scope = Scope(scope_name, parent_scope=self.current_scope)
        self.current_scope = new_scope
        self.scopes.append(new_scope)

    def exit_scope(self):
        if self.current_scope.parent_scope:
            self.current_scope = self.current_scope.parent_scope

    def declare_symbol(self, name, symbol_type):
        unique_id = f"{symbol_type}_{self.unique_id_counter}"
        self.current_scope.declare(name, symbol_type, unique_id)
        self.unique_id_counter += 1

    def lookup_symbol(self, name):
        return self.current_scope.lookup(name)

    def print_table(self):
        print("\n=== Symbol Table ===")
        for scope in self.scopes:
            print(f"Scope: {scope.name}")
            for name, info in scope.symbols.items():
                print(f"  {name} -> {info}")
        print("====================\n")


def perform_semantic_analysis(xml_file):
    """
    Perform semantic analysis on the syntax tree provided in xml_file.
    """
    import xml.etree.ElementTree as ET

    # Debug: Print the first 5 lines of the XML file
    try:
        with open(xml_file, 'r') as file:
            lines = file.readlines()[:5]  # Read the first 5 lines
            print(f"{GREEN}First 5 lines of the syntax tree:{RESET}")
            for line in lines:
                print(line.strip())
    except Exception as e:
        print(f"{RED}Error reading XML file: {e}{RESET}")
        return

    # Load the XML syntax tree
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"{RED}XML Parse Error: {e}{RESET}")
        return

    symbol_table = SymbolTable()

    def process_node(node, scope_name):
        # Ensure node is not None before proceeding
        if node is None:
            raise SemanticError(f"{RED}Error: Received NoneType node during processing.{RESET}")
        
        tag = node.tag

        if tag == 'ROOT' or tag == 'IN':
            symb_node = node.find('SYMB')
            if symb_node is not None:
                symb_text = symb_node.text
                # Check if we need to enter a new scope for 'ALGO' or 'FUNCTIONS'
                if symb_text in ['ALGO', 'FUNCTIONS']:
                    symbol_table.enter_scope(symb_text)

            # Check if the node has any children before processing
            children_node = node.find('CHILDREN')
            if children_node is not None and len(children_node.findall('ID')) > 0:
                for child in children_node.findall('ID'):
                    child_node = find_node_by_id(child.text, root)
                    if child_node is not None:
                        process_node(child_node, scope_name)

            # Exit scope if necessary
            if symb_text in ['ALGO', 'FUNCTIONS']:
                symbol_table.exit_scope()

        elif tag == 'LEAF':
            terminal = node.find('TERMINAL')
            if terminal is not None:
                word = terminal.find('WORD').text
                class_name = terminal.find('CLASS').text

                # Handle variable and function declarations
                if class_name == 'V':
                    symbol_table.declare_symbol(word, 'var')
                elif class_name == 'FNAME':
                    symbol_table.declare_symbol(word, 'func')
                elif class_name in ('CONST_N', 'CONST_S', 'CALL'):
                    # Ensure symbol has been declared
                    symbol_table.lookup_symbol(word)
            else:
                raise SemanticError(f"{RED}Error: LEAF node missing TERMINAL section.{RESET}")

    def find_node_by_id(unid, root):
        """
        Helper function to find a node by its unique ID in the XML tree.
        """
        for node in root.iter():
            unid_node = node.find('UNID')
            if unid_node is not None and unid_node.text == unid:
                return node
        return None


    # Start processing the syntax tree from 'ROOT'
    try:
        root_node = root.find('./ROOT')
        if root_node is None:
            raise SemanticError(f"{RED}Error: 'ROOT' node not found in the syntax tree.{RESET}")
        
        process_node(root_node, "global")

        # Print the symbol table after analysis
        symbol_table.print_table()

    except SemanticError as e:
        print(f"{RED}{e}{RESET}")
