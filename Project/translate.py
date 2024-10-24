import re

# Translate the input to BASIC syntax
def translate_to_basic(input_lines):
    basic_code = []
    declared_variables = set()  # Track declared variables
    function_names = set()      # Track function names to avoid declaring them as variables
    context_stack = []          # Track current context (e.g., IF, FUNCTION, MAIN)
    indent_level = 0            # Track indentation
    current_function = None     # Track current function name

    # Function to add line with indentation
    def add_line(line):
        basic_code.append(f'{"    " * indent_level}{line}')

    # Process lines with lookahead for function declaration
    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Skip empty lines or comments
        if not line or line.startswith('#'):
            i += 1
            continue

        # Handle 'main' declaration
        if re.match(r'^main$', line, re.IGNORECASE):
            context_stack.append('MAIN')
            i += 1
            continue  # BASIC doesn't require a main declaration

        # Handle function declaration (num FunctionName(params) { ) or num FunctionName(params) followed by '{'
        func_decl_match = re.match(r'^num\s+(\w+)\s*\((.*?)\)\s*{?$', line, re.IGNORECASE)
        if func_decl_match:
            func_name = func_decl_match.group(1)
            params = func_decl_match.group(2).strip()
            function_names.add(func_name)  # Add to function names to prevent 'Dim' statements

            # Check if '{' is at the end of the line
            has_open_brace = line.endswith('{')
            if has_open_brace:
                add_line(f'Function {func_name} ({params})')
                context_stack.append('FUNCTION')
                indent_level += 1
            else:
                # Next line should have '{'
                if i + 1 < len(input_lines):
                    next_line = input_lines[i + 1].strip()
                    if next_line == '{':
                        add_line(f'Function {func_name} ({params})')
                        context_stack.append('FUNCTION')
                        indent_level += 1
                        i += 1  # Skip the '{' line
            current_function = func_name
            i += 1
            continue

        # Handle variable declarations (e.g., num V_x, num V_y, ...)
        # This regex finds all 'num Var' in the line
        var_decl_matches = re.findall(r'num\s+(\w+)', line, re.IGNORECASE)
        if var_decl_matches:
            for var in var_decl_matches:
                if var not in declared_variables and var not in function_names:
                    add_line(f'Dim {var} As Integer')
                    declared_variables.add(var)
            i += 1
            continue

        # Handle begin block
        if re.match(r'^begin$', line, re.IGNORECASE):
            # 'begin' is implicit in BASIC by indentation, no action needed
            i += 1
            continue

        # Handle end block or closing brace '}'
        if re.match(r'^end$', line, re.IGNORECASE) or re.match(r'^}$', line):
            if context_stack:
                context = context_stack.pop()
                indent_level -= 1
                if context == 'IF':
                    add_line('End If')
                elif context == 'FUNCTION':
                    add_line('End Function')
                    current_function = None
                elif context == 'MAIN':
                    # In BASIC, there's no explicit 'End Main', so nothing
                    pass
            i += 1
            continue

        # Handle assignment from input (V_x < input ;)
        input_assign_match = re.match(r'^(\w+)\s*<\s*input\s*;?$', line, re.IGNORECASE)
        if input_assign_match:
            var_name = input_assign_match.group(1)
            add_line(f'Input {var_name}')
            i += 1
            continue

        # Handle return statement (return V_result ;)
        return_match = re.match(r'^return\s+(.+?)\s*;?$', line, re.IGNORECASE)
        if return_match:
            return_val = return_match.group(1).strip()
            translated_return = translate_expression(return_val)
            if context_stack and context_stack[-1] == 'FUNCTION':
                # In function, assign to function name
                add_line(f'{current_function} = {translated_return}')
            else:
                # In main, translate to Print
                add_line(f'Print {translated_return}')
            i += 1
            continue

        # Handle print statement (print V_x ;)
        print_match = re.match(r'^print\s+(.+?)\s*;?$', line, re.IGNORECASE)
        if print_match:
            var_name = print_match.group(1).strip()
            translated_print = translate_expression(var_name)
            add_line(f'Print {translated_print}')
            i += 1
            continue

        # Handle if statements (if condition then)
        if_match = re.match(r'^if\s+(.+?)\s+then$', line, re.IGNORECASE)
        if if_match:
            condition = translate_condition(if_match.group(1))
            add_line(f'If {condition} Then')
            context_stack.append('IF')
            indent_level += 1
            i += 1
            continue

        # Handle else statement (else)
        if re.match(r'^else$', line, re.IGNORECASE):
            if context_stack and context_stack[-1] == 'IF':
                indent_level -= 1
                add_line('Else')
                indent_level += 1
            i += 1
            continue

        # Handle assignments (V_result = F_average(V_x, V_y, 0) ;)
        assign_match = re.match(r'^(\w+)\s*=\s*(.+?)\s*;?$', line)
        if assign_match:
            var_name = assign_match.group(1)
            expr = assign_match.group(2).strip()
            translated_expr = translate_expression(expr)
            add_line(f'{var_name} = {translated_expr}')
            i += 1
            continue

        # Handle comments after code (e.g., ' Print V_result ; ' with comments)
        comment_match = re.match(r'^print\s+(.+?)\s*;?\s*(\'.*)$', line, re.IGNORECASE)
        if comment_match:
            var_name = comment_match.group(1).strip()
            comment = comment_match.group(2).strip()
            translated_print = translate_expression(var_name)
            add_line(f'Print {translated_print} {comment}')
            i += 1
            continue

        # If line does not match any known patterns, ignore or report
        # Could add error handling here
        i += 1
        continue

    # After processing all lines, ensure all contexts are closed
    while context_stack:
        context = context_stack.pop()
        indent_level -= 1
        if context == 'IF':
            add_line('End If')
        elif context == 'FUNCTION':
            add_line('End Function')

    return "\n".join(basic_code)

# Translate condition (handles nested conditions)
def translate_condition(condition):
    condition = condition.strip()
    binop_mapping = {
        'grt': '>',
        'lt': '<',
        'eq': '=',
        'and': 'And',
        'or': 'Or',
        'add': '+',
        'sub': '-',
        'mul': '*',
        'div': '/'
    }

import re

import re

def translate_condition(condition_str):
    """
    Translates a condition from the custom language to BASIC syntax.
    
    Args:
        condition_str (str): The condition string in the custom language.
        
    Returns:
        str: The translated condition string in BASIC syntax.
    """
    
    # Define operator mappings
    operator_mapping = {
        'grt': '>',
        'lt': '<',
        'eq': '=',
        'and': 'And',
        'or': 'Or'
    }
    
    def recursive_translate(cond):
        """
        Recursively translates conditions.
        """
        cond = cond.strip()
        
        # Match logical operators with two operands: and(cond1, cond2) or or(cond1, cond2)
        logical_match = re.match(r'^(and|or)\s*\(\s*(.+)\s*,\s*(.+)\s*\)$', cond, re.IGNORECASE)
        if logical_match:
            logical_op = logical_match.group(1).lower()
            operand1 = logical_match.group(2).strip()
            operand2 = logical_match.group(3).strip()
            
            # Recursively translate operands
            translated_operand1 = recursive_translate(operand1)
            translated_operand2 = recursive_translate(operand2)
            
            # Map logical operator
            mapped_logical_op = operator_mapping.get(logical_op, logical_op)
            
            return f"{translated_operand1} {mapped_logical_op} {translated_operand2}"
        
        # Match binary comparison operators: grt(V_x, V_y), lt(V_a, V_b), eq(V_a, 0), etc.
        binary_match = re.match(r'^(grt|lt|eq)\s*\(\s*(\w+)\s*,\s*([\w"]+)\s*\)$', cond, re.IGNORECASE)
        if binary_match:
            comp_op = binary_match.group(1).lower()
            left_operand = binary_match.group(2)
            right_operand = binary_match.group(3)
            
            # Map comparison operator
            mapped_comp_op = operator_mapping.get(comp_op, comp_op)
            
            return f"{left_operand} {mapped_comp_op} {right_operand}"
        
        # If condition is a simple comparison like V_x > V_y
        simple_cmp_match = re.match(r'^(\w+)\s*([><=]+)\s*([\w"]+)$', cond)
        if simple_cmp_match:
            left = simple_cmp_match.group(1)
            operator = simple_cmp_match.group(2)
            right = simple_cmp_match.group(3)
            return f"{left} {operator} {right}"
        
        # Handle cases where condition might be enclosed in parentheses
        parenthesis_match = re.match(r'^\(\s*(.+)\s*\)$', cond)
        if parenthesis_match:
            inner_cond = parenthesis_match.group(1).strip()
            return f"({recursive_translate(inner_cond)})"
        
        # If none of the above, return the condition as is
        return cond
    
    # Start parsing from the full condition string
    translated_condition = recursive_translate(condition_str)
    return translated_condition


def translate_line(line):
    """
    Translates a single line from the custom language to BASIC.
    
    Args:
        line (str): The line in custom language.
        
    Returns:
        str: The translated line in BASIC syntax.
    """
    # Match if statements
    if_match = re.match(r'^if\s+(.+?)\s+then$', line, re.IGNORECASE)
    if if_match:
        condition = if_match.group(1).strip()
        translated_condition = translate_condition(condition)
        return f'If {translated_condition} Then'
    
    # Handle other translations...
    # (This part remains as in your main translator script)
    
    return line  # Return the line as is if no translation is needed

# Example usage within the translator
input_line = "if and ( grt ( V_x , V_y ) , grt ( V_y , 0 ) ) then"
translated_line = translate_line(input_line)
print(translated_line)  # Output: If V_x > V_y And V_y > 0 Then

# Translate expressions (handles arithmetic functions and function calls)
def translate_expression(expr):
    expr = expr.strip()
    binop_mapping = {
        'add': '+',
        'sub': '-',
        'mul': '*',
        'div': '/'
    }

    # Match arithmetic function calls like add(V_a, V_b)
    func_binop_match = re.match(r'^(\w+)\s*\(\s*([\w"]+)\s*,\s*([\w"]+)\s*\)$', expr)
    if func_binop_match:
        func = func_binop_match.group(1).lower()
        arg1 = func_binop_match.group(2)
        arg2 = func_binop_match.group(3)
        if func in binop_mapping:
            return f'{arg1} {binop_mapping[func]} {arg2}'

    # Match function calls like F_average(V_x, V_y, 0)
    func_call_match = re.match(r'^(\w+)\s*\((.*)\)$', expr)
    if func_call_match:
        func_name = func_call_match.group(1)
        params = func_call_match.group(2).strip()
        return f'{func_name}({params})'

    # If it's a string literal, ensure quotes
    str_match = re.match(r'^"(.+)"$', expr)
    if str_match:
        return f'"{str_match.group(1)}"'

    # Otherwise, return as is (handles variables and numeric literals)
    return expr

# Example Main Code for Testing
def main():
    input_file = "inputs/example_input.txt"

    with open(input_file, 'r') as file:
        input_lines = file.readlines()

    # Translate input to BASIC code
    basic_code = translate_to_basic(input_lines)

    # Print the generated BASIC code
    print("Generated BASIC Code:")
    print(basic_code)

if __name__ == "__main__":
    main()
