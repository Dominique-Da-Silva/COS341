import os
from lexer import Lexer, LexicalError
from parser import SLRParser
import xml.etree.ElementTree as ET

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
RESET = '\033[0m'

def main():
    input_dir = "inputs"
    output_dir = "outputs"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_file = os.path.splitext(input_file)[0] + ".xml"
        output_path = os.path.join(output_dir, output_file)

        print(f"\n{PURPLE}{'='*40}{RESET}")
        print(f"{BLUE}Processing file: {input_file}{RESET}")
        print(f"{PURPLE}{'='*40}{RESET}\n")

        with open(input_path, 'r') as file:
            input_text = file.read()

        lexer = Lexer(input_text)
        
        try:
            # Tokenize the input text
            tokens = lexer.tokenize()

            # Divider for lexing success
            print(f"{PURPLE}{'-'*40}{RESET}")
            print(f"{GREEN}Lexing successful for {input_file}. Output saved to {output_path}.{RESET}")
            print(f"{PURPLE}{'-'*40}{RESET}")

            # Generate XML output
            generate_xml(tokens, output_path)

            # Parse the XML file with the SLR parser
            parse_result = parse_xml(output_path)
            if parse_result:
                print(f"{GREEN}Parsing successful for {input_file}.{RESET}")
            else:
                print(f"{RED}Parsing failed for {input_file}.{RESET}")

        except LexicalError as e:
            print(f"{RED}Lexing failed for {input_file}: {e}{RESET}")
        except SyntaxError as e:
            print(f"{RED}Syntax error in {input_file}: {e}{RESET}")
        except Exception as e:
            print(f"{RED}Error in {input_file}: {e}{RESET}")



def indent_xml(elem, level=0):
    """
    Recursively adds indentation to the XML elements for pretty printing.
    """
    indent = "  " 
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
        word_element.text = token.value

    indent_xml(root)

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

def parse_xml(xml_path):
    """
    Use the SLRParser to parse the XML token stream.
    """
    try:
        parser = SLRParser(xml_path)
        return parser.parse()
    except SyntaxError as e:
        print(f"{RED}Parsing failed: {e}{RESET}")
        return False
    except Exception as e:
        print(f"{RED}An exception was caught during parsing: {e}{RESET}")
        return False

if __name__ == "__main__":
    main()
