import re

# ANSI color codes for colored output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
RESET = '\033[0m'

# Define the set of reserved keywords
reserved_keywords = {'num', 'text', 'begin', 'end', 'if', 'else', 'return', 'main', 'void',
                     'and', 'or', 'not', 'grt', 'eq', 'add', 'sub', 'mul', 'div', 'input'}

class SemanticError(Exception):
    """ Custom exception for semantic analysis errors. """
    def __init__(self, message, line_number=None, line_content=None):
        if line_number is not None and line_content is not None:
            message = f"Error at line {line_number}: {line_content}\n{message}"
        super().__init__(message)

class TypeError(Exception):
    """ Custom exception for type checking errors. """
    def __init__(self, message, line_number=None, line_content=None):
        if line_number is not None and line_content is not None:
            message = f"Type Error at line {line_number}: {line_content}\n{message}"
        super().__init__(message)

class Scope:
    def __init__(self, name, parent_scope=None, level=0, scope_type='block'):
        self.name = name
        self.symbols = {}  # Store variable/function names and their internal unique identifiers and types
        self.parent_scope = parent_scope
        self.level = level
        self.scope_type = scope_type

    def declare(self, name, symbol_type, unid, data_type=None, line_number=None, line_content=None):
        """ Declares a new variable or function in the current scope. """
        if name in self.symbols:
            raise SemanticError(f"'{name}' is already declared in this scope '{self.name}'.", line_number, line_content)
        self.symbols[name] = {"type": symbol_type, "unid": unid, "data_type": data_type}

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

    def declare_symbol(self, name, symbol_type, unid, data_type=None, scope=None, line_number=None, line_content=None):
        if scope is None:
            scope = self.current_scope
        scope.declare(name, symbol_type, unid, data_type, line_number, line_content)

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
                data_type = info.get('data_type', 'Unknown')
                print(f"  {name} -> Type: {info['type']}, UNID: {info['unid']}, Data Type: {data_type}")
        print("====================\n")

def type_check_input_file(input_file):
    """
    Perform type checking on the input file.
    """
    symbol_table = SymbolTable()

    # Read the entire input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # First Pass: Collect all function declarations
    for line_number, line in enumerate(lines, start=1):
        original_line = line.rstrip('\n')
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Function declaration
        function_decl_match = re.match(r'(num|void|text)\s+(\w+)\s*\(([^)]*)\)', line)
        if function_decl_match:
            return_type, func_name, params = function_decl_match.groups()
            # Check if the function name is a reserved keyword
            if func_name in reserved_keywords:
                raise SemanticError(f"Function name '{func_name}' is a reserved keyword.", line_number, original_line)
            # Check if function is already declared in global scope
            if symbol_table.global_scope.has(func_name):
                raise SemanticError(f"Function '{func_name}' is already declared in the global scope.", line_number, original_line)
            # Declare function in global scope with return type
            try:
                symbol_table.declare_symbol(func_name, "func", unid=f"unid_{func_name}", data_type=return_type, scope=symbol_table.global_scope, line_number=line_number, line_content=original_line)
            except SemanticError as e:
                raise SemanticError(str(e), line_number, original_line)
            continue

        # Skip other lines in the first pass
        continue

    # Second Pass: Perform type checking and variable declarations in correct scopes
    symbol_table.current_scope = symbol_table.global_scope
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
        function_decl_match = re.match(r'(num|void|text)\s+(\w+)\s*\(([^)]*)\)', line)
        if function_decl_match:
            func_name = function_decl_match.group(2)
            # Enter function scope
            symbol_table.enter_scope(func_name, scope_type='function')
            current_scope_stack.append(symbol_table.current_scope)
            # Declare function parameters in the function's scope
            params = function_decl_match.group(3)
            params_list = params.split(',')
            for param in params_list:
                param = param.strip()
                if param:
                    param_name = param
                    param_type = 'num'  # Assuming default type as 'num'
                    # Check if the parameter name is a reserved keyword
                    if param_name in reserved_keywords:
                        raise SemanticError(f"Parameter name '{param_name}' is a reserved keyword.", line_number, original_line)
                    # Declare parameter in current scope
                    try:
                        symbol_table.declare_symbol(param_name, "var", unid=f"unid_{param_name}", data_type=param_type, line_number=line_number, line_content=original_line)
                    except SemanticError as e:
                        raise SemanticError(str(e), line_number, original_line)
            inside_function = True
            continue

        # Variable declaration
        variable_decl_matches = re.findall(r'(num|text)\s+(\w+)', line)
        if variable_decl_matches:
            for var_type, var_name in variable_decl_matches:
                # Check if variable name is reserved
                if var_name in reserved_keywords:
                    raise SemanticError(f"Variable name '{var_name}' is a reserved keyword.", line_number, original_line)
                # Check if variable is already declared in current scope
                if symbol_table.current_scope.has(var_name):
                    raise SemanticError(f"Variable '{var_name}' is already declared in this scope '{symbol_table.current_scope.name}'.", line_number, original_line)
                # Declare variable in current scope
                try:
                    symbol_table.declare_symbol(var_name, "var", unid=f"unid_{var_name}", data_type=var_type, line_number=line_number, line_content=original_line)
                except SemanticError as e:
                    raise SemanticError(str(e), line_number, original_line)
            continue

        # Assignment statement
        assignment_match = re.match(r'(\w+)\s*(<|=)\s*(.+);', line)
        if assignment_match:
            var_name, operator, expression = assignment_match.groups()
            # Check that the variable being assigned to is declared
            try:
                var_info = symbol_table.lookup_symbol(var_name, line_number, original_line)
            except SemanticError as e:
                raise SemanticError(str(e), line_number, original_line)

            # Type checking for the assignment
            expr_type = type_check_expression(expression, symbol_table, line_number, original_line)
            var_type = var_info.get('data_type', 'Unknown')
            if var_type != expr_type:
                raise TypeError(f"Type mismatch: Cannot assign {expr_type} to {var_type}.", line_number, original_line)
            continue

        # 'return' statement
        return_match = re.match(r'return\s+(.+);', line)
        if return_match:
            return_expression = return_match.group(1)
            return_type = type_check_expression(return_expression, symbol_table, line_number, original_line)
            # Check if the return type matches the function's declared return type
            if inside_function:
                func_scope = symbol_table.current_scope.parent_scope  # Function scope
                func_name = func_scope.name
                func_info = symbol_table.global_scope.symbols.get(func_name)
                if func_info:
                    func_return_type = func_info['data_type']
                    if func_return_type != return_type:
                        raise TypeError(f"Return type mismatch in function '{func_name}': expected {func_return_type}, got {return_type}.", line_number, original_line)
            continue

        # Handle 'if' and 'else' blocks
        if line.startswith('if') or line.startswith('else'):
            # Type checking for condition expressions can be added here if needed
            continue

        # Handle other statements as needed
        # ...

    # Print the type table
    symbol_table.print_table()
    print(f"{GREEN}Type checking completed successfully.{RESET}")

def type_check_expression(expression, symbol_table, line_number=None, line_content=None):
    """
    Check the type of the given expression.
    """
    expression = expression.strip()
    
    # Handle 'input' keyword
    if expression == 'input':
        # Assuming 'input' returns 'num'
        return 'num'
    
    # Handle literals
    if re.match(r'^\d+(\.\d+)?$', expression):
        return 'num'
    if re.match(r'^".*"$', expression):
        return 'text'
    
    # Handle variables
    try:
        var_info = symbol_table.lookup_symbol(expression, line_number, line_content)
        return var_info.get('data_type', 'Unknown')
    except SemanticError:
        pass  # Not a variable, proceed to next check
    
    # Built-in unary operators
    built_in_unops = {'not', 'sqrt'}
    # Built-in binary operators
    built_in_binops = {'add', 'sub', 'mul', 'div', 'grt', 'eq', 'and', 'or'}
    
    # Handle function calls and built-in operators
    func_call_match = re.match(r'(\w+)\s*\((.*)\)', expression)
    if func_call_match:
        func_name, args = func_call_match.groups()
        args = args.strip()
        args_list = [arg.strip() for arg in args.split(',')] if args else []
        if func_name in built_in_unops:
            if len(args_list) != 1:
                raise TypeError(f"Operator '{func_name}' requires one argument.", line_number, line_content)
            arg_type = type_check_expression(args_list[0], symbol_table, line_number, line_content)
            if arg_type != 'num':
                raise TypeError(f"Operator '{func_name}' requires 'num' type argument, got '{arg_type}'.", line_number, line_content)
            return 'num'
        elif func_name in built_in_binops:
            if len(args_list) != 2:
                raise TypeError(f"Operator '{func_name}' requires two arguments.", line_number, line_content)
            arg1_type = type_check_expression(args_list[0], symbol_table, line_number, line_content)
            arg2_type = type_check_expression(args_list[1], symbol_table, line_number, line_content)
            if arg1_type != 'num' or arg2_type != 'num':
                raise TypeError(f"Operator '{func_name}' requires 'num' type arguments, got '{arg1_type}' and '{arg2_type}'.", line_number, line_content)
            return 'num'
        else:
            # Not a built-in operator, check if function is declared
            try:
                func_info = symbol_table.lookup_symbol(func_name, line_number, line_content)
                if func_info['type'] != 'func':
                    raise TypeError(f"'{func_name}' is not a function.", line_number, line_content)
                func_type = func_info.get('data_type', 'Unknown')
                # Optionally, type-check the function arguments here
                return func_type
            except SemanticError as e:
                raise TypeError(str(e), line_number, line_content)
    
    # If none of the above, raise an error
    raise TypeError(f"Unable to determine the type of expression '{expression}'.", line_number, line_content)


if __name__ == "__main__":
    # Assuming the input file is "example3.txt"
    input_file = "example3.txt"
    print(f"Starting Type Checking for {input_file}.")
    try:
        # Call the type_check_input_file function
        type_check_input_file(input_file)
    except (SemanticError, TypeError) as e:
        print(f"{RED}{e}{RESET}")
