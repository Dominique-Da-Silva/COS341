# IDEA & TIPS OF THE PROJECT
* SPL stands for "Students' Programming Language", and Rec stands for "Recursive": You see that in this year's version (2024) the SPL does not offer any WHILE commands for Loops, because all repetitions must be programmed purely recursively in RecSPL.

* As you see, I have kept the "design" of RecSPL so simple that the "Lexing" of its tokens will not be difficult; and also its "Parsing" will be quite straightforward, too :)

* At the end of the semester, you should be able to write a small RecSPL program, compile it with your own compiler, and let the generated output code actually run and "do stuff"; that will be a HAPPY DAY when you'll see that it really works :)

* The RecSPL input file, which your Lexer software must analyse, will be given as a plain *.txt file; for the purpose of experimenting and testing you can easily create such *.txt files (containing some RecSPL program code) by yourself.

* IF the input *.txt file contains any lexical errors (which corresponds, in theory, to the underlying DFA getting 'stuck' in a non-accepting state), then your Lexer software must "throw" a reasonably understandable Error-Message back to the User.

* IF the input *.txt file does not contain any lexical errors, then your Lexer software must create, write, and store (as its output) an XLM file which the Parser can later use as its input.

# COMPILER CONSTRUCTION INSTALLATION GUIDE

> [!Important]
> Clone the repository into WSL. Running the following commands in Windows might lead to problems.
> 
> Don't have WSL installed? Check out [How to install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

### 1. Working directory setup
Open a terminal in your IDE and set backend folder as the current working directory (if you have not already done so):
```
cd Project
```

### 2. Be sure to install Python
Check whether it has been installed:
```
python3 --version
```
Installing in case it has not previously been installed:
```
sudo apt update
```
```
sudo apt install python3
```
```
python3 --version
```

### 3. Create the python virtual environment named venv
```
python3 -m venv venv
```

### 4. Activate the virtual environment
```
source venv/bin/activate
```
After activation, you should see (venv) at the start of your terminal prompt, indicating the environment is active.

### 5. To run the python script
```
python main.py
```

### 6. Deactivating the virtual environment
```
deactivate
```

### 7. Formatting the file
```
sudo pip install black
```
```
black <filename>
```