import re

# Translate the input to BASIC syntax
def translate_to_basic(input_lines):
    basic_code = []
    
    for line in input_lines:
        line = line.strip()

        # Variable declarations (num V_x -> DIM V_x AS INTEGER)
        var_decl_match = re.match(r'num\s+(\w+)', line)
        if var_decl_match:
            var_name = var_decl_match.group(1)
            basic_code.append(f'DIM {var_name} AS INTEGER')
            continue
        
        # Assignment from input (e.g., V_x < input -> INPUT V_x)
        input_assign_match = re.match(r'(\w+)\s*<\s*input', line)
        if input_assign_match:
            var_name = input_assign_match.group(1)
            basic_code.append(f'INPUT {var_name}')
            continue

        # Assignment statement (e.g., V_x = 5 -> V_x = 5)
        assign_match = re.match(r'(\w+)\s*=\s*(.+)', line)
        if assign_match:
            var_name = assign_match.group(1)
            value = assign_match.group(2)
            basic_code.append(f'{var_name} = {value}')
            continue

        # Print statement (print V_x -> PRINT V_x)
        print_match = re.match(r'print\s+(.+)', line, re.IGNORECASE)
        if print_match:
            var_name = print_match.group(1)
            basic_code.append(f'PRINT {var_name}')
            continue

        # Function declaration (num F_name(V_a, V_b, V_c) -> FUNCTION F_name(V_a, V_b, V_c))
        func_decl_match = re.match(r'num\s+(\w+)\s*\((.*)\)', line)
        if func_decl_match:
            func_name = func_decl_match.group(1)
            params = func_decl_match.group(2)
            basic_code.append(f'FUNCTION {func_name}({params})')
            continue

        # Function return statement (return V_sum -> RETURN V_sum)
        return_match = re.match(r'return\s+(.+)', line, re.IGNORECASE)
        if return_match:
            return_val = return_match.group(1)
            basic_code.append(f'RETURN {return_val}')
            continue

        # If/else statements (if grt(V_x, V_y) then -> IF V_x > V_y THEN)
        if_match = re.match(r'if\s+(.+)\s+then', line, re.IGNORECASE)
        if if_match:
            condition = translate_condition(if_match.group(1))
            basic_code.append(f'IF {condition} THEN')
            continue

        # Else statements (else -> ELSE)
        if re.match(r'else', line, re.IGNORECASE):
            basic_code.append('ELSE')
            continue

        # End if (end if -> END IF)
        if re.match(r'end if', line, re.IGNORECASE):
            basic_code.append('END IF')
            continue

        # End function (end -> END FUNCTION)
        if re.match(r'end', line, re.IGNORECASE):
            basic_code.append('END FUNCTION')
            continue

    return "\n".join(basic_code)

# Translate condition (grt(V_x, V_y) -> V_x > V_y)
def translate_condition(condition):
    condition = condition.strip()
    binop_mapping = {
        'grt': '>',
        'eq': '=',
        'and': 'AND',
        'or': 'OR',
        'add': '+',
        'sub': '-',
        'mul': '*',
        'div': '/'
    }
    
    # Example: grt(V_x, V_y) -> V_x > V_y
    condition_match = re.match(r'(\w+)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)', condition)
    if condition_match:
        binop = condition_match.group(1)
        left_operand = condition_match.group(2)
        right_operand = condition_match.group(3)
        if binop in binop_mapping:
            return f'{left_operand} {binop_mapping[binop]} {right_operand}'
    
    return condition

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
