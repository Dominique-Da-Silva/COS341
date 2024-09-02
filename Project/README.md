# COMPILER CONSTRUCTION INSTALLATION GUIDE
### 1. Working directory setup
Open a terminal in your IDE and set backend folder as the current working directory (if you have not already done so):
```cd Project```

### 2. Be sure to install Python
Check whether it has been installed:
```python3 --version```
Installing in case it has not previously been installed:
```sudo apt update```
```sudo apt install python3```
```python3 --version```

### 3. Create the python virtual environment named venv
```python3 -m venv venv```

### 4. Activate the virtual environment
```source venv/bin/activate```
After activation, you should see (venv) at the start of your terminal prompt, indicating the environment is active.

### 5. To run the python script
```python main.py```

### 6. Deactivating the virtual environment
```deactivate```