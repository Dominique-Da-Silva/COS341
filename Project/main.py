import os
from lexer import Lexer
from parser import SLRParser  # Import your SLR parser

def main():
    # Specify the input and output directories
    input_dir = "inputs"
    output_dir = "outputs"

    # List all .txt files in the input directory
    input_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    # Process each input file
    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_file = os.path.splitext(input_file)[0] + ".xml"
        output_path = os.path.join(output_dir, output_file)

        # Read the content of the input file
        with open(input_path, 'r') as file:
            input_text = file.read()

        # Initialize the lexer with the input text
        lexer = Lexer(input_text)
        
        try:
            # Tokenize the input text
            tokens = lexer.tokenize()

            # Generate XML output
            generate_xml(tokens, output_path)
            print(f"Processed {input_file} successfully. Output saved to {output_path}.")

            # Parse the XML file with the SLR parser
            parse_result = parse_xml(output_path)
            if parse_result:
                print(f"Parsing successful for {input_file}.")

        except SyntaxError as e:
            print(f"Lexical error in {input_file}: {e}")
        except Exception as e:
            print(f"Error in {input_file}: {e}")

def generate_xml(tokens, output_path):
    """
    Generate an XML file from the list of tokens.
    """
    # XML header and root element
    xml_content = "<TOKENSTREAM>\n"
    
    for i, token in enumerate(tokens, start=1):
        xml_content += f"  <TOK>\n"
        xml_content += f"    <ID>{i}</ID>\n"
        xml_content += f"    <CLASS>{token.type}</CLASS>\n"
        xml_content += f"    <WORD>{token.value}</WORD>\n"
        xml_content += f"  </TOK>\n"

    # Closing root element
    xml_content += "</TOKENSTREAM>\n"

    # Write XML content to the output file
    with open(output_path, 'w') as xml_file:
        xml_file.write(xml_content)

def parse_xml(xml_path):
    """
    Use the SLRParser to parse the XML token stream.
    """
    try:
        parser = SLRParser(xml_path)  # Initialize the parser with the XML file
        return parser.parse()  # Call the parse method and return the result
    except SyntaxError as e:
        print(f"Parsing error: {e}")
        return False
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return False

if __name__ == "__main__":
    main()
