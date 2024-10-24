import re
import os

# ANSI color codes for colored output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
RESET = '\033[0m'

# Define the set of reserved keywords
reserved_keywords = {'num', 'text', 'begin', 'end', 'if', 'else', 'return', 'main', 'void',
                     'and', 'or', 'not', 'grt', 'eq', 'add', 'sub', 'mul', 'div', 'input'}

class SemanticError(Exception):
    """Custom exception for semantic analysis errors."""
    def __init__(self, message, input_file=None, line_number=None, line_content=None):
        if line_number is not None and line_content is not None:
            if input_file is not None:
                message = f"Error in {input_file}: Error at line {line_number}: {line_content}\n{message}"
            else:
                message = f"Error at line {line_number}: {line_content}\n{message}"
        super().__init__(message)

class TypeError(Exception):
    """Custom exception for type checking errors."""
    def __init__(self, message, input_file=None, line_number=None, line_content=None):
        if line_number is not None and line_content is not None:
            if input_file is not None:
                message = f"Type error in {input_file}: Error at line {line_number}: {line_content}\n{message}"
            else:
                message = f"Type error at line {line_number}: {line_content}\n{message}"
        super().__init__(message)


class Scope:
    def __init__(self, name, parent_scope=None, level=0, scope_type='block', func_name=None):
        self.name = name
        self.symbols = {}  # Store variable/function names and their data types
        self.parent_scope = parent_scope
        self.level = level
        self.scope_type = scope_type
        self.func_name = func_name  # For function scopes

    def declare(self, name, symbol_type, data_type=None, line_number=None, line_content=None):
        """Declares a new variable or function in the current scope."""
        if name in self.symbols:
            # Pass line_number and line_content as keyword arguments
            raise SemanticError(f"Variable '{name}' is already declared in this scope '{self.name}'.", 
                                line_number=line_number, line_content=line_content)
        self.symbols[name] = {
            "type": symbol_type,
            "data_type": data_type  # Retain data_type for type checking
        }

    def lookup(self, name, line_number=None, line_content=None):
        """Looks up a symbol in the current scope or any parent scope."""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent_scope:
            return self.parent_scope.lookup(name, line_number, line_content)
        else:
            # Pass line_number and line_content as keyword arguments
            raise SemanticError(f"'{name}' is used but not declared in any scope.", 
                                line_number=line_number, line_content=line_content)

    def has(self, name):
        """Checks if a symbol is declared in the current scope (only)."""
        return name in self.symbols


class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("Global", level=0)
        self.current_scope = self.global_scope
        self.scopes = [self.global_scope]  # Global scope is the first one

    def enter_scope(self, scope_name, scope_type='block', level=None, func_name=None):
        if level is None:
            new_level = self.current_scope.level + 1
        else:
            new_level = level
        new_scope = Scope(scope_name, parent_scope=self.current_scope, level=new_level, scope_type=scope_type, func_name=func_name)
        self.current_scope = new_scope
        self.scopes.append(new_scope)

    def exit_scope(self):
        if self.current_scope.parent_scope:
            self.current_scope = self.current_scope.parent_scope
        else:
            raise SemanticError("Attempted to exit global scope, which is not allowed.")

    def declare_symbol(self, name, symbol_type, data_type=None, scope=None, line_number=None, line_content=None):
        if scope is None:
            scope = self.current_scope
        scope.declare(name, symbol_type, data_type, line_number=line_number, line_content=line_content)

    def lookup_symbol(self, name, line_number=None, line_content=None):
        # Start lookup from the current scope
        scope = self.current_scope
        while scope is not None:
            if name in scope.symbols:
                return scope.symbols[name]
            scope = scope.parent_scope  # Move up to the parent scope
        # If not found in any scope
        # Pass line_number and line_content as keyword arguments
        raise SemanticError(f"'{name}' is used but not declared in any scope.", 
                            line_number=line_number, line_content=line_content)

    def print_table(self):
        print("\n=== Type Table ===")
        
        for scope in self.scopes:
            # Skip printing empty block levels
            if not scope.symbols:
                continue

            # Print the scope name
            print(f"Scope: {scope.name}")

            # Print all symbols in the current scope
            for name, info in scope.symbols.items():
                if info['type'] == 'func':
                    # For functions, display 'Return Type'
                    return_type = info.get('data_type', 'Unknown')
                    print(f"  {name} -> Return Type: {return_type}")
                else:
                    # For variables, display 'Data Type'
                    data_type = info.get('data_type', 'Unknown')
                    if data_type is None:
                        data_type = 'text'
                    print(f"  {name} -> Data Type: {data_type}")
        
        print("====================\n")


def type_check_input_file(input_file):
    """
    Perform semantic analysis and type checking on the input file.
    Save the symbol table to outputs/{input_file}_symboltable.txt.
    """
    symbol_table = SymbolTable()
    output_dir = "outputs"
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Correct file path for saving the symbol table
    symbol_table_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_symboltable.txt")

    # Read the entire input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # First Pass: Collect all function declarations and global variables
    in_global_scope = True  # Flag to indicate if we are in the global scope

    # First Pass: Collect all function declarations and global variables
    for line_number, line in enumerate(lines, start=1):
        original_line = line.rstrip('\n')
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Function declaration
        function_decl_match = re.match(r'(num|void)\s+(\w+)\s*\(([^)]*)\)', line)
        if function_decl_match:
            in_global_scope = False  # We've encountered a function declaration; we're no longer in global scope
            return_type, func_name, params = function_decl_match.groups()

            # Enforce that functions must have 'num' return type only
            if return_type != 'num':
                raise SemanticError(f"Function '{func_name}' has an invalid return type '{return_type}'. Only 'num' return types are allowed.",
                                    input_file, line_number, original_line)

            # Check if the function name is a reserved keyword
            if func_name in reserved_keywords:
                raise SemanticError(f"Function name '{func_name}' is a reserved keyword.",
                                    input_file, line_number, original_line)

            # Check if the function is already declared in the global scope
            if symbol_table.global_scope.has(func_name):
                raise SemanticError(f"Function '{func_name}' is already declared in the global scope.",
                                    input_file, line_number, original_line)

            # Declare function in the global scope with return type 'num'
            symbol_table.declare_symbol(func_name, "func", data_type=return_type, 
                                        scope=symbol_table.global_scope, 
                                        line_number=line_number, line_content=original_line)
            continue


        # Variable declarations in global scope
        if in_global_scope:
            variable_decl_matches = re.findall(r'(num|text)\s+(\w+)', line)
            if variable_decl_matches:
                for var_type, var_name in variable_decl_matches:
                    # Check if variable name is reserved
                    if var_name in reserved_keywords:
                        raise SemanticError(f"Variable name '{var_name}' is a reserved keyword.", 
                                            input_file, line_number, original_line)
                    # Check if variable is already declared in global scope
                    if symbol_table.global_scope.has(var_name):
                        raise SemanticError(f"Variable '{var_name}' is already declared in the global scope.", 
                                            input_file, line_number, original_line)
                    # Declare variable in global scope
                    try:
                        symbol_table.declare_symbol(var_name, "var", data_type=var_type, 
                                                   scope=symbol_table.global_scope, 
                                                   line_number=line_number, line_content=original_line)
                    except SemanticError as e:
                        raise SemanticError(str(e), line_number, original_line)
                continue

        # Skip other lines in the first pass
        continue

    # Second Pass: Perform type checking and variable declarations in correct scopes
    # Reset current_scope to global
    symbol_table.current_scope = symbol_table.global_scope
    current_scope_stack = [symbol_table.global_scope]
    inside_function = False
    current_function_name = None

    for line_number, line in enumerate(lines, start=1):
        original_line = line.rstrip('\n')
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Check for 'main' function
        if line == 'main':
            # Enter main function scope
            symbol_table.enter_scope('main', scope_type='main')
            current_scope_stack.append(symbol_table.current_scope)
            inside_function = True
            continue

        # Begin block
        if line == 'begin' or line == '{':
            # Enter new block scope
            if inside_function and symbol_table.current_scope.scope_type in ['function', 'main']:
                # Enter function body scope
                func_body_scope_name = f"{current_function_name}_body" if current_function_name else "main_body"
                symbol_table.enter_scope(func_body_scope_name, scope_type='function_body', func_name=current_function_name)
            else:
                block_scope_name = f"Block_Level_{len(current_scope_stack)}"
                symbol_table.enter_scope(block_scope_name, scope_type='block')
            current_scope_stack.append(symbol_table.current_scope)
            continue

        # End block or function
        if line == 'end' or line == '}':
            if len(current_scope_stack) > 1:
                current_scope = current_scope_stack[-1]
                if current_scope.scope_type in ['function', 'main']:
                    inside_function = False
                    current_function_name = None
                symbol_table.exit_scope()
                current_scope_stack.pop()
            continue

        # Function declaration (handled in first pass)
        function_decl_match = re.match(r'(num|void)\s+(\w+)\s*\(([^)]*)\)', line)
        if function_decl_match:
            func_name = function_decl_match.group(2)
            # Enter function scope
            symbol_table.enter_scope(func_name, scope_type='function')
            current_scope_stack.append(symbol_table.current_scope)
            current_function_name = func_name
            inside_function = True

            # Declare function parameters in the function's scope
            params = function_decl_match.group(3)
            params_list = params.split(',')
            for param in params_list:
                param = param.strip()
                if param:
                    param_name = param
                    # **Declare parameter in current scope and enforce `num` type**
                    symbol_table.declare_symbol(param_name, "var", data_type="num", 
                                                line_number=line_number, line_content=original_line)
            continue

        # Variable declaration
        variable_decl_matches = re.findall(r'(num|text)\s+(\w+)', line)
        if variable_decl_matches:
            for var_type, var_name in variable_decl_matches:
                # Check if variable name is reserved
                if var_name in reserved_keywords:
                    raise SemanticError(f"Variable name '{var_name}' is a reserved keyword.", 
                                        input_file, line_number, original_line)

                # Check if variable is already declared in current scope
                if symbol_table.current_scope.has(var_name):
                    raise SemanticError(f"Variable '{var_name}' is already declared in this scope '{symbol_table.current_scope.name}'.", 
                                        input_file, line_number, original_line)

                # Declare variable in current scope
                try:
                    symbol_table.declare_symbol(var_name, "var", data_type=var_type, 
                                               line_number=line_number, line_content=original_line)
                except SemanticError as e:
                    raise SemanticError(str(e), line_number, original_line)
            continue

        # Assignment statement
        assignment_match = re.match(r'(\w+)\s*(<|=)\s*(.+);', line)
        if assignment_match:
            var_name, operator, expression = assignment_match.groups()

            # Check that the variable being assigned to is declared
            try:
                var_info = symbol_table.lookup_symbol(var_name, line_number=line_number, line_content=original_line)
            except SemanticError as e:
                raise SemanticError(str(e), line_number, original_line)

            # Type checking for the assignment
            expr_type = type_check_expression(expression, symbol_table, line_number=line_number, 
                                             line_content=original_line)
            var_type = var_info.get('data_type', None)

            # Enforce that variable must have a type already; no type inference allowed
            if var_type is None:
                raise TypeError(f"Variable '{var_name}' must be declared with a type before use.", 
                                input_file, line_number, original_line)
            elif var_type != expr_type:
                raise TypeError(f"Type mismatch: Cannot assign {expr_type} to {var_type}.", 
                                input_file, line_number, original_line)
            continue

        # 'return' statement
        return_match = re.match(r'return\s+(.+);', line)
        if return_match:
            return_expression = return_match.group(1)
            return_type = type_check_expression(return_expression, symbol_table, 
                                                line_number=line_number, 
                                                line_content=original_line)
            # Check if the return type matches the function's declared return type
            if inside_function and current_function_name:
                func_info = symbol_table.global_scope.symbols.get(current_function_name)
                if func_info:
                    func_return_type = func_info['data_type']
                    if func_return_type != return_type:
                        raise TypeError(f"Return type mismatch in function '{current_function_name}': expected {func_return_type}, got {return_type}.", 
                                        input_file, line_number, original_line)
            continue

        # Handle 'if', 'else', and other statements
        if line.startswith('if') or line.startswith('else'):
            # Type checking for condition expressions can be added here if needed
            continue

        # Handle function calls
        # Handle function calls
        func_call_match = re.match(r'(\w+)\s*\((.*)\)\s*;', line)
        if func_call_match:
            func_name, args = func_call_match.groups()
            args = args.strip()
            args_list = [arg.strip() for arg in args.split(',')] if args else []

            # Verify that each argument is of type 'num'
            for arg in args_list:
                arg_type = type_check_expression(arg, symbol_table, 
                                                line_number=line_number, 
                                                line_content=original_line)

                if arg_type != 'num':
                    raise TypeError(f"Function '{func_name}' expects 'num' type arguments, but got '{arg_type}' for argument '{arg}'.", 
                                    input_file, line_number, original_line)
            continue


        # Handle other statements as needed
        # ...

    # Step 3: Save the symbol table to a file
    with open(symbol_table_file, 'w') as file:
        for scope in symbol_table.scopes:
            file.write(f"Scope: {scope.name}\n")
            for name, info in scope.symbols.items():
                if info['type'] == 'func':
                    file.write(f"  Function: {name} -> Return Type: {info['data_type']}\n")
                else:
                    file.write(f"  Variable: {name} -> Data Type: {info['data_type']}\n")
            file.write("\n")

    print(f"Semantic analysis symbol table written to: {symbol_table_file}")
    
    # Print the symbol table after analysis
    symbol_table.print_table()
    print(f"{GREEN}Type checking completed successfully for {input_file}.{RESET}")

def type_check_expression(expression, symbol_table, line_number=None, line_content=None, param_types=None):
    """
    Check the type of the given expression.
    """
    expression = expression.strip()

    # Handle 'input' keyword
    if expression == 'input':
        return 'num'

    # Handle numeric literals
    if re.match(r'^\d+(\.\d+)?$', expression):
        return 'num'

    # Handle string literals
    if re.match(r'^".*"$', expression):
        return 'text'

    # Handle variables
    try:
        var_info = symbol_table.lookup_symbol(expression, line_number=line_number, line_content=line_content)
        var_type = var_info.get('data_type', None)
        if var_type:
            return var_type
        else:
            return 'Unknown'
    except SemanticError:
        pass  # Not a variable, proceed to next check

    # Built-in binary operators
    built_in_binops = {'add', 'sub', 'mul', 'div', 'grt', 'eq', 'and', 'or'}

    # Handle binary operators
    binop_match = re.match(r'(\w+)\s*\((.*)\)', expression)
    if binop_match:
        func_name, args = binop_match.groups()
        args = args.strip()
        args_list = [arg.strip() for arg in args.split(',')] if args else []

        # If the function is a built-in binary operator, handle it
        if func_name in built_in_binops:
            if len(args_list) != 2:
                raise TypeError(f"Operator '{func_name}' requires two arguments, but got {len(args_list)}.", 
                                input_file=None, line_number=line_number, line_content=line_content)

            # Type check both arguments of the binary operator
            arg1_type = type_check_expression(args_list[0], symbol_table, line_number=line_number, line_content=line_content)
            arg2_type = type_check_expression(args_list[1], symbol_table, line_number=line_number, line_content=line_content)

            # Ensure both arguments are of type 'num'
            if arg1_type != 'num':
                raise TypeError(f"Operator '{func_name}' requires 'num' type arguments, but got '{arg1_type}' for the first argument.", 
                                input_file=None, line_number=line_number, line_content=line_content)
            if arg2_type != 'num':
                raise TypeError(f"Operator '{func_name}' requires 'num' type arguments, but got '{arg2_type}' for the second argument.", 
                                input_file=None, line_number=line_number, line_content=line_content)

            return 'num'

    # Handle function calls (after binary operators)
    func_call_match = re.match(r'(\w+)\s*\((.*)\)', expression)
    if func_call_match:
        func_name, args = func_call_match.groups()
        args = args.strip()
        args_list = [arg.strip() for arg in args.split(',')] if args else []

        # Type check each argument passed to the function
        for arg in args_list:
            arg_type = type_check_expression(arg, symbol_table, 
                                             line_number=line_number, 
                                             line_content=line_content)

            # Ensure that all arguments are of type 'num'
            if arg_type != 'num':
                raise TypeError(f"Function '{func_name}' expects 'num' type arguments, but got '{arg_type}' for argument '{arg}'.", 
                                input_file=None, line_number=line_number, line_content=line_content)

        # After checking arguments, assume the function itself returns 'num'
        return 'num'

    # If none of the above, raise an error
    raise TypeError(f"Unable to determine the type of expression '{expression}'.", 
                    input_file=None, line_number=line_number, line_content=line_content)
