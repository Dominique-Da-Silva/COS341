import random
import os

# Define folders
input_folder = "inputs"
os.makedirs(input_folder, exist_ok=True)

# Maximum depth for recursion
MAX_DEPTH = 3
INDENT_SIZE = 2

# Terminal generators for tokens
def generate_vname():
    return f"V_{random.choice('abcdefghijklmnopqrstuvwxyz')}{random.choice('abcdefghijklmnopqrstuvwxyz0123456789')}"

def generate_fname():
    return f"F_{random.choice('abcdefghijklmnopqrstuvwxyz')}{random.choice('abcdefghijklmnopqrstuvwxyz0123456789')}"

def generate_const():
    if random.choice([True, False]):
        # Generate a number (N)
        return str(random.uniform(-100, 100))
    else:
        # Generate a text (T)
        length = random.randint(1, 8)
        return f'"{"".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length)).capitalize()}"'

def generate_vtyp():
    return random.choice(["num", "text"])

def generate_ftyp():
    return random.choice(["num", "void"])

def generate_binop():
    return random.choice(["or", "and", "eq", "grt", "add", "sub", "mul", "div"])

def generate_unop():
    return random.choice(["not", "sqrt"])

# Production rules based random expansion functions
def generate_prog(depth=0):
    return f"main\n{generate_globvars(depth)}\n{generate_algo(depth)}\n{generate_functions(depth)}"


def generate_globvars(depth=0, indent_level=0):
    if depth >= MAX_DEPTH or random.choice([True, False]):
        # Base case: return epsilon (empty string)
        return ""
    else:
        # Recursive case
        return f"{generate_vtyp()} {generate_vname()}, {generate_globvars(depth + 1, indent_level)}"
   

def generate_algo(depth=0, indent_level=0):
    indent = " " * (INDENT_SIZE * indent_level)
    return f"{indent}begin\n{generate_instruc(depth, indent_level + 1)}\n{indent}end"

def generate_instruc(depth=0, indent_level=0):
    indent = " " * (INDENT_SIZE * indent_level)
    if depth >= MAX_DEPTH or random.choice([True, False]):
        # Base case: return epsilon (empty string)
        return ""
    else:
        # Recursive case
        return f"{indent}{generate_command(depth, indent_level)} ;\n{generate_instruc(depth + 1, indent_level)}"


def generate_command(depth=0, indent_level=0):
    if depth >= MAX_DEPTH:
        return "skip"  # Terminal to avoid deep recursion
    options = [
        "skip",
        "halt",
        f"print {generate_atomic()}",
        generate_assign(),
        generate_call(),
        generate_branch(depth + 1, indent_level + 1),
        f"return {generate_atomic()}"
    ]
    return random.choice(options)

def generate_atomic():
    return random.choice([generate_vname(), generate_const()])

def generate_assign():
    return random.choice([f"{generate_vname()} < input", f"{generate_vname()} = {generate_term()}"])

def generate_call():
    return f"{generate_fname()}({generate_atomic()}, {generate_atomic()}, {generate_atomic()})"

def generate_branch(depth=0, indent_level=0):
    if depth >= MAX_DEPTH:
        return "skip"  # Terminal to avoid deep recursion
    indent = " " * (INDENT_SIZE * indent_level)
    return (
        f"if {generate_cond(depth + 1)} then\n"
        f"{generate_algo(depth + 1, indent_level + 1)}\n"
        f"{indent}else\n"
        f"{generate_algo(depth + 1, indent_level + 1)}"
    )

def generate_term(depth=0):
    if depth >= MAX_DEPTH:
        return generate_atomic()
    return random.choice([
        generate_atomic(),
        generate_call(),
        generate_op(depth + 1)  # Pass incremented depth
    ])


def generate_op(depth=0):
    if depth >= MAX_DEPTH:
        return f"{generate_unop()}({generate_atomic()})"
    else:
        if random.choice([True, False]):
            return f"{generate_unop()}({generate_arg(depth + 1)})"
        else:
            return f"{generate_binop()}({generate_arg(depth + 1)}, {generate_arg(depth + 1)})"

def generate_arg(depth=0):
    if depth >= MAX_DEPTH:
        return generate_atomic()
    else:
        return random.choice([
            generate_atomic(),
            generate_op(depth + 1)  # Allow nesting of OP within ARG
        ])


def generate_binop_arg(depth=0):
    # Separate function for generating a binary operation argument to avoid nested UNOPs
    return f"{generate_binop()}({generate_atomic()}, {generate_atomic()})"

def generate_cond(depth=0):
    if depth >= MAX_DEPTH:
        return generate_simple()
    else:
        return random.choice([
            generate_simple(),
            generate_composit(depth + 1)
        ])

def generate_simple():
    return f"{generate_binop()}({generate_atomic()}, {generate_atomic()})"

def generate_composit(depth=0):
    if depth >= MAX_DEPTH:
        return generate_simple()
    else:
        return random.choice([
            f"{generate_binop()}({generate_simple(depth + 1)}, {generate_simple(depth + 1)})",
            f"{generate_unop()}({generate_simple(depth + 1)})"
        ])

def generate_functions(depth=0, indent_level=0):
    if depth >= MAX_DEPTH or random.choice([True, False]):
        return ""
    return f"{generate_decl(depth + 1, indent_level)}\n{generate_functions(depth + 1, indent_level)}"

def generate_decl(depth=0, indent_level=0):
    indent = " " * (INDENT_SIZE * indent_level)
    return f"{indent}{generate_header()}\n{generate_body(depth + 1, indent_level)}"

def generate_header():
    return f"{generate_ftyp()} {generate_fname()}({generate_vname()}, {generate_vname()}, {generate_vname()})"

def generate_body(depth=0, indent_level=0):
    indent = " " * (INDENT_SIZE * indent_level)
    return (
        f"{indent}{{\n"
        f"{generate_locvars(indent_level + 1)}\n"
        f"{generate_algo(depth, indent_level + 1)}\n"
        f"{indent}}}\n"
        f"{generate_functions(depth, indent_level)}\n"
        f"{indent}end"
    )

def generate_locvars(indent_level=0):
    indent = " " * (INDENT_SIZE * indent_level)
    return (
        f"{indent}{generate_vtyp()} {generate_vname()}, "
        f"{generate_vtyp()} {generate_vname()}, "
        f"{generate_vtyp()} {generate_vname()},"
    )

# Create a random valid input file
def create_random_input_file():
    random_prog = generate_prog()
    file_path = os.path.join(input_folder, "random_input.txt")
    with open(file_path, "w") as file:
        file.write(random_prog)
    print(f"Random input file generated at {file_path}")

# Generate a random input file
create_random_input_file()
