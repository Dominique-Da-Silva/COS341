# main.py

from lexer import Lexer  # Import the Lexer class from lexer.py

def main():
    # Sample input program 1 test
    input_program_1 = """
    main
    begin
        num V_x, text V_y,
        V_x < input
        print V_x;
        return V_x
    end
    """
    
    # Initialize the lexer with the input program
    lexer = Lexer(input_program_1)
    # Tokenize the input program
    tokens = lexer.tokenize()
    
    # Print the tokens to verify the output
    print("Tokens:")
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
