# Compiler GUI Application

## Description:
This application allows you to compile source code into BASIC syntax, with live editing, internal process viewing, and phase summaries. It was built using Python and packaged into an executable for ease of use.

## How to Run:
1. **Download** the executable (`main.exe`) from the provided link or folder.
2. **Double-click** on the `main.exe` file to open the GUI.
3. **Use the Browse button** to select a text file, or edit the content directly in the input text area.
4. **Click Compile** to process the input file or text and view the output in the summary section.
5. Optionally, you can view detailed internal process logs by clicking the "See Internal Processing" button.

## System Requirements:
- **Operating System**: Windows 10 or later.
- **No additional software is required**, as the application is packaged as a standalone executable. You do not need Python or any other libraries installed.

## Common Issues:
- If your anti-virus flags the executable, you may need to temporarily allow it through the firewall.
- If the application doesn't open, try running it as an administrator by right-clicking the executable and selecting **Run as Administrator**.

## Known Limitations:
- Binary operations such as grt are not correctly translated into BASIC syntax. 
- Type Checking for Built-in Binary Operations is overly lenient (will allow num and text arguments when it should just allow num.)

