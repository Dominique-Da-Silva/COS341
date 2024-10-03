import os
from lexer import Lexer, LexicalError  # Import LexicalError from lexer
from parser import SLRParser  # Import your SLR parser
import xml.etree.ElementTree as ET

def main():
    # Specify the input and output directories
    input_dir = "inputs"
    output_dir = "outputs"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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
            print(f"Lexing successful for {input_file}. Output saved to {output_path}.")

            # Parse the XML file with the SLR parser
            parse_result = parse_xml(output_path)
            if parse_result:
                print(f"Parsing successful for {input_file}.")

        except LexicalError as e:
            print(f"Lexing failed for {input_file}: {e}")
        except SyntaxError as e:
            print(f"Syntax error in {input_file}: {e}")

        except Exception as e:
            print(f"Error in {input_file}: {e}")

import xml.etree.ElementTree as ET

def indent_xml(elem, level=0):
    """
    Recursively adds indentation to the XML elements for pretty printing.
    """
    indent = "  "  # Two spaces for indentation; adjust as needed
    i = "\n" + level * indent
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        for child in elem:
            indent_xml(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def generate_xml(tokens, output_path):
    """
    Generate an XML file from the list of tokens.
    """
    root = ET.Element('TOKENSTREAM')
    
    for i, token in enumerate(tokens, start=1):
        tok_element = ET.SubElement(root, 'TOK')
        id_element = ET.SubElement(tok_element, 'ID')
        id_element.text = str(i)
        class_element = ET.SubElement(tok_element, 'CLASS')
        class_element.text = token.type
        word_element = ET.SubElement(tok_element, 'WORD')
        word_element.text = token.value  # Special characters will be escaped automatically

    # Indent the XML for pretty printing
    indent_xml(root)

    # Create the tree and write to the output file
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)





def parse_xml(xml_path):
    """
    Use the SLRParser to parse the XML token stream.
    """
    try:
        parser = SLRParser(xml_path)  # Initialize the parser with the XML file
        return parser.parse()  # Call the parse method and return the result
    except SyntaxError as e:
        print(f"Parsing failed: {e}")
        return False
    except Exception as e:
        print(f"An exception was caught during parsing: {e}")
        return False

if __name__ == "__main__":
    main()
