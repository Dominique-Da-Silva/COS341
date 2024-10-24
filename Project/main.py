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
import sys

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
RESET = '\033[0m'

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)  # Auto-scroll to the end of the text area

    def flush(self):
        pass

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

# Function to toggle between views
def toggle_view():
    if internal_output_area.winfo_ismapped():  # If internal processing is currently shown
        internal_output_area.pack_forget()
        summary_output_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Show summary
        toggle_button.config(text="See Internal Processing")
    else:
        summary_output_area.pack_forget()
        internal_output_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Show internal processing
        toggle_button.config(text="Hide Internal Processing")

# Compilation function
def run_compilation(input_text):
    try:
        # Redirect stdout and stderr to the internal output area
        sys.stdout = TextRedirector(internal_output_area)
        sys.stderr = TextRedirector(internal_output_area)

        # Create a temporary input file from the text area content
        temp_input_file = "temp_input.txt"
        with open(temp_input_file, 'w') as temp_file:
            temp_file.write(input_text)

        # Run the full process on the temporary input file
        basic_code = process_input(temp_input_file)
        
        # Display the BASIC code output
        basic_output_area.delete("1.0", tk.END)
        basic_output_area.insert(tk.END, basic_code)

        # Update the summary area with phase completion info
        summary_output_area.delete("1.0", tk.END)
        summary_output_area.insert(tk.END, "Lexing completed successfully.\n")
        summary_output_area.insert(tk.END, "Parsing completed successfully.\n")
        summary_output_area.insert(tk.END, "Semantic Analysis completed successfully.\n")
        summary_output_area.insert(tk.END, "Type Checking completed successfully.\n")
        summary_output_area.insert(tk.END, "Translation to BASIC completed successfully.\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        # Restore stdout and stderr back to the default behavior
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

# GUI Code
def on_compile():
    try:
        # Clear the summary, internal, and basic output areas before compiling
        summary_output_area.delete("1.0", tk.END)
        internal_output_area.delete("1.0", tk.END)
        basic_output_area.delete("1.0", tk.END)

        # Get the input text from the text area
        input_text = input_text_area.get("1.0", tk.END).strip()

        # Run the compilation process
        run_compilation(input_text)

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
compile_frame = tk.Frame(root)
compile_frame.pack()

compile_button = tk.Button(compile_frame, text="Compile", command=on_compile)
compile_button.pack(side=tk.LEFT, padx=10)

# Warning Label (blue text as requested)
compile_warning_label = tk.Label(compile_frame, text="Compiling may take a few seconds, and the UI may momentarily freeze.", fg="blue")
compile_warning_label.pack(side=tk.LEFT)

# Summary Output Area and Internal Process Output Area share the same position
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True)

# Summary Output Area (default visible, showing phase completion)
summary_output_area = scrolledtext.ScrolledText(output_frame, width=90, height=10)
summary_output_area.pack(fill=tk.BOTH, expand=True)

# Internal Process Output Area (hidden by default)
internal_output_area = scrolledtext.ScrolledText(output_frame, width=90, height=15)
internal_output_area.pack_forget()

# Toggle Button
toggle_button = tk.Button(root, text="See Internal Processing", command=toggle_view)
toggle_button.pack(pady=5)

# BASIC Output Area
basic_label = tk.Label(root, text="Generated BASIC Code:")
basic_label.pack()
basic_output_area = scrolledtext.ScrolledText(root, width=90, height=10)
basic_output_area.pack()

root.mainloop()
