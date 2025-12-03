import os
import subprocess
import time
import re
import shutil
import pyfiglet

def print_ascii_art(text):
    """Print ASCII art text."""
    ascii_art = pyfiglet.figlet_format(text)
    print(colored_text(ascii_art, "cyan"))

def grep(pattern, files):
    """Search for a pattern in the specified files and print matching lines."""
    compiled_pattern = re.compile(pattern)  # Compile the pattern for efficiency
    
    for file in files:
        try:
            with open(file, 'r') as f:
                line_number = 0
                for line in f:
                    line_number += 1
                    if compiled_pattern.search(line):
                        print(f"{file}:{line_number}: {line.strip()}")
        except FileNotFoundError:
            print(f"grep: {file}: No such file or directory")
        except IsADirectoryError:
            print(f"grep: {file}: Is a directory")
        except Exception as e:
            print(f"grep: {file}: Error: {e}")



def colored_text(text, color):
    """Print text in the specified color."""
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }
    color_code = colors.get(color.lower(), colors["reset"])
    return f"{color_code}{text}{colors['reset']}"

def cat(files):
    """Concatenate and display the content of files."""
    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read()
                print(content)
        except FileNotFoundError:
            print(colored_text(f"cat: {file}: No such file or directory", "red"))
        except IsADirectoryError:
            print(colored_text(f"cat: {file}: Is a directory", "red"))
        except Exception as e:
            print(colored_text(f"cat: {file}: Error: {e}", "red"))


def mkdir(directory):
    """Create a new directory."""
    try:
        # Create the directory
        os.makedirs(directory, exist_ok=False)  # exist_ok=False ensures an error if the directory already exists
        print(f"Directory '{directory}' created successfully")
    except FileExistsError:
        print(f"mkdir: cannot create directory '{directory}': File exists")
    except PermissionError:
        print(f"mkdir: cannot create directory '{directory}': Permission denied")
    except Exception as e:
        print(f"mkdir: cannot create directory '{directory}': {e}")
def rm(files):
    """Remove files or directories."""
    for file in files:
        try:
            if os.path.isdir(file):
                os.rmdir(file)  # Use os.rmdir for empty directories
            else:
                os.remove(file)
            print(f"Removed: {file}")
        except FileNotFoundError:
            print(f"rm: {file}: No such file or directory")
        except IsADirectoryError:
            print(f"rm: {file}: Is a directory")
        except PermissionError:
            print(f"rm: {file}: Permission denied")
        except Exception as e:
            print(f"rm: {file}: Error: {e}")


def cd(directory):
    try:
        os.chdir(directory)
    except FileNotFoundError:
        print(colored_text(f"No such directory: {directory}", "red"))
    except Exception as e:
        print(colored_text(f"Error: {e}", "red"))

def ls():
    try:
        for item in os.listdir(os.getcwd()):
            print(colored_text(item,"green"))
    except Exception as e:
        print(colored_text(f"Error: {e}", "red"))

def pwd():
    print(colored_text(os.getcwd(), "blue"))

def execute_external_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(colored_text(result.stdout, "green"))
        if result.stderr:
            print(colored_text(result.stderr, "red"))
    except Exception as e:
        print(colored_text(f"Error executing command: {e}", "red"))


def cp(source, destination):
    """Copy files or directories."""
    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)  # Copy entire directory
        else:
            shutil.copy(source, destination)  # Copy file
        print(f"Copied: {source} to {destination}")
    except FileNotFoundError:
        print(f"cp: {source}: No such file or directory")
    except FileExistsError:
        print(f"cp: {destination}: File exists")
    except PermissionError:
        print(f"cp: Permission denied")
    except Exception as e:
        print(f"cp: Error: {e}")

def mv(source, destination):
    """Move or rename files or directories."""
    try:
        shutil.move(source, destination)
        print(f"Moved: {source} to {destination}")
    except FileNotFoundError:
        print(f"mv: {source}: No such file or directory")
    except FileExistsError:
        print(f"mv: {destination}: File exists")
    except PermissionError:
        print(f"mv: Permission denied")
    except Exception as e:
        print(f"mv: Error: {e}")

def main():
    print_ascii_art("Thanatos")
    while True:
        try:
            # Prompt user for input
            current_dir = os.getcwd()
            user_input = input(f"{colored_text(current_dir, 'cyan')}$ ").strip()
            
            # Handle exit
            if user_input.lower() == 'exit':
                print(colored_text("Exiting in 3 seconds...", "yellow"))
                time.sleep(3)
                break

            # Split the input into command and arguments
            parts = user_input.split()
            if len(parts) == 0:
                continue
            command = parts[0]
            args = parts[1:]

            # Handle built-in commands
            if command == 'cd':
                if len(args) > 0:
                    cd(args[0])
                else:
                    print(colored_text("cd requires a directory argument", "red"))
            elif command == 'ls':
                ls()
            elif command == 'pwd':
                pwd()
            elif command == 'cat':
                if len(args) > 0:
                    cat(args)
                else:
                    print(colored_text("cat requires at least one file argument", "red"))
            elif command == 'mkdir':
                if len(args) > 0:
                    mkdir(args[0])
                else:
                    print(colored_text("mkdir requires a directory argument", "red"))
            
            elif command == 'grep':
                if len(args) > 1:
                    pattern = args[0]
                    files = args[1:]
                    grep(pattern, files)
                else:
                    print(colored_text("grep requires a pattern and at least one file argument", "red"))

            elif command == 'rm':
                if len(args) > 0:
                    rm(args)
                else:
                    print(colored_text("rm requires at least one file or directory argument", "red"))
            elif command == 'cp':
                if len(args) == 2:
                    cp(args[0], args[1])
                else:
                    print(colored_text("cp requires source and destination arguments", "red"))
            elif command == 'mv':
                if len(args) == 2:
                    mv(args[0], args[1])




            else:
                # Execute external commands
                execute_external_command(user_input)

        except KeyboardInterrupt:
            print(colored_text("\nExiting in 3 seconds...", "yellow"))
            time.sleep(3)
            break

if __name__ == "__main__":
    
    main()
