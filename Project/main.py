import os
import time
import subprocess  # To run external commands
from lexer import Lexer, LexicalError
from parser import SLRParser
from semantic import perform_semantic_analysis  # Importing the semantic analysis function
from typecheck import type_check_input_file  # Importing the type checking function
import xml.etree.ElementTree as ET
from translate import translate_to_basic  # Importing the translation function from the translator module
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
RESET = '\033[0m'

BASIC_INTERPRETER = "bwbasic"  # Placeholder for basic interpreter

def process_input(input_file):
    output_dir = "outputs"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dynamic naming for output files based on input file
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    lexer_output_path = os.path.join(output_dir, f"{base_filename}_lexer_output.xml")
    syntax_tree_output = os.path.join(output_dir, f"{base_filename}_syntaxtree.xml")
    basic_output_path = os.path.join(output_dir, f"{base_filename}.bas")

    try:
        with open(input_file, 'r') as file:
            input_text = file.read()

        # Lexing
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()

        # Generate XML from tokens
        generate_xml(tokens, lexer_output_path)

        # Parsing
        parser = SLRParser(lexer_output_path, input_text, base_filename)
        parser.parse()
        parser.generate_syntax_tree_xml(syntax_tree_output)

        # Semantic Analysis
        perform_semantic_analysis(syntax_tree_output, input_file)

        # Type Checking
        type_check_input_file(input_file)

        # Translation to BASIC
        basic_code = translate_to_basic(input_text.splitlines())

        # Save the BASIC code to a file
        with open(basic_output_path, 'w') as basic_file:
            basic_file.write(basic_code)

        return basic_code  # Returning the BASIC code for display in the GUI

    except LexicalError as e:
        raise Exception(f"Lexical Error: {e}")
    except SyntaxError as e:
        raise Exception(f"Syntax Error: {e}")
    except TypeError as e:
        raise Exception(f"Type Error: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")


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
        line_element = ET.SubElement(tok_element, 'LINE')
        line_element.text = str(token.line_num)
        col_element = ET.SubElement(tok_element, 'COL')
        col_element.text = str(token.col_num)

    indent_xml(root)

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)


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


# GUI Code
def on_compile():
    try:
        # Get the input text from the text area
        input_text = input_text_area.get("1.0", tk.END).strip()

        # Create a temporary input file from the text area content
        temp_input_file = "temp_input.txt"
        with open(temp_input_file, 'w') as temp_file:
            temp_file.write(input_text)

        # Run the full process on the temporary input file
        basic_code = process_input(temp_input_file)
        
        # Display the BASIC code output
        basic_output_area.delete("1.0", tk.END)
        basic_output_area.insert(tk.END, basic_code)

        # Display internal process output (for now, just placeholder text)
        internal_output_area.delete("1.0", tk.END)
        internal_output_area.insert(tk.END, "Parsing completed successfully.\nType checking completed successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_browse():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(tk.END, file_path)

        # Preview the content in the input text area
        with open(file_path, 'r') as file:
            input_text = file.read()
            input_text_area.delete("1.0", tk.END)
            input_text_area.insert(tk.END, input_text)


# GUI Setup
root = tk.Tk()
root.title("Compiler GUI")
root.geometry("800x600")

# File Path Entry and Browse Button
file_frame = tk.Frame(root)
file_frame.pack(pady=10)

file_label = tk.Label(file_frame, text="Select Input File (optional):")
file_label.pack(side=tk.LEFT)

file_path_entry = tk.Entry(file_frame, width=50)
file_path_entry.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(file_frame, text="Browse", command=on_browse)
browse_button.pack(side=tk.LEFT)

# Input Text Area
input_label = tk.Label(root, text="Input File Content (Editable):")
input_label.pack()
input_text_area = scrolledtext.ScrolledText(root, width=90, height=10)
input_text_area.pack()

# Compile Button
compile_button = tk.Button(root, text="Compile", command=on_compile)
compile_button.pack()

# Internal Process Output Area
internal_label = tk.Label(root, text="Internal Process Results:")
internal_label.pack()
internal_output_area = scrolledtext.ScrolledText(root, width=90, height=5)
internal_output_area.pack()

# BASIC Output Area
basic_label = tk.Label(root, text="Generated BASIC Code:")
basic_label.pack()
basic_output_area = scrolledtext.ScrolledText(root, width=90, height=10)
basic_output_area.pack()

root.mainloop()
