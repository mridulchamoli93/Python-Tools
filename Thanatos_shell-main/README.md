# Python Shell

A simple yet powerful shell built in Python, designed to execute common shell commands with added features like colored output, error handling, and ASCII art.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

To install the necessary dependencies, ensure you have Python installed and run:

bash
pip install -r requirements.txt

Usage
To start the shell, simply run the Python script:


python shell.py
You'll see a prompt displaying your current working directory followed by a $, ready to accept commands.

Features
Basic Shell Prompt
Displays the current working directory followed by a $ prompt for user input.
Command Execution
cd: Change the current working directory.
ls: List the contents of the current directory, with output in green.
pwd: Print the current working directory.
cat: Concatenate and display the contents of specified files.
mkdir: Create a new directory.
grep: Search for a pattern within specified files and display matching lines.
rm: Remove specified files or directories.
cp: Copy files or directories from a source to a destination.
mv: Move or rename files or directories.
head: Display the first few lines of a specified file.
tail: Display the last few lines of a specified file.
Error Handling
Provides informative error messages for issues such as missing files, incorrect arguments, or permission problems.
Colored Output
Uses ANSI escape codes to color the text output:
Green: Directory contents (ls output).
Red: Error messages.
Blue: Current working directory.
Cyan: ASCII art display.
Yellow: Exit messages.
ASCII Art Display
Uses pyfiglet to print ASCII art text ("Thanatos") when the shell starts, enhancing the visual appeal.
External Command Execution
Executes external commands using subprocess.run(), allowing the shell to run system commands and scripts.
Command Handling
Splits user input into commands and arguments, then executes built-in or external commands accordingly.
Graceful Exit
Exits the shell with a delay when the user types exit, allowing a smooth shutdown process.
Input Validation
Checks if the required arguments are provided for each command and gives feedback if they are missing or incorrect.
Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.


Contact
For questions, issues, or suggestions, please contact [Mridul chamoli] at [mridulchamoli93@gmail.com].

Feel free to replace `[Mridul Chamoli]` and `[mridulchamoli93@gmail.com]` with your actual contact information. This template should give a clear overview of your project and guide users through installation and usage.


![image](https://github.com/user-attachments/assets/d60185c8-ed35-4dba-bc07-a0c14d8d6d09)









