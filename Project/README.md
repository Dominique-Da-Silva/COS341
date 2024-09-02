# Compiler-Construction-Project

## Installation guide
1. Working directory setup
Open terminal in IDE and set the 'Project' folder as the current working directory.
cd Project

2. Install Python 3
Check whether python has been installed by running the following command
python3 --version

Steps to install Python 3
* update the package repository: sudo apt update
* install python: sudo apt install python3
* verify installation: python3 --version

3. Create the python virtual environment
python3 -m venv cos341-venv

4. Activate the virtual environment
source cos341-venv/bin/activate

5. Install dependencies
pip install pytest
python3 -m pip install -r requirements.txt

6. Formatting of python files
pip install black
For all files in the environment: black .
For specific file: black <filename>

## Addition to the project that should be noted
The bug is that the non-void functions were not given their necessary return statement. (Void-functions obviously do not need any such return statement.)

The bugfix is as follows: Into the project grammar you simply insert this one additional production rule:

COMMAND ::= return ATOMIC

Thereby, return is now a new terminal token (in fact a reserved keyword) for which your Lexer must also be prepared and adjusted.

This simple bugfix allows us now to write a return-statement into the final line of the ALGO of a non-void function :)

Comment: Obviously this simple bugfix now also allows us to write the most silly return statements everywhere into an ALGO - even in the middle of the main program where does not make any sense at all - but we can still deal with this semantic problem in the semantic analysis phase of the compiler after the parser has produces a syntax tree.
"Normally" a function without return - or a return in the middle of main - would (should) be regarded as a syntax problem to be picked up already by the parser; but to follow that route I would be forced to completely rewrite the project grammar on which students have already started working; that would not be good. Therefore we will deal with wrongly placed return-commands as "semantic" problems in the semantic analysis phases after the parsing.