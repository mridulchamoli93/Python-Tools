
---

```md
# 🐚 Thanatos Python Shell  
A simple yet powerful shell built in Python, designed to execute standard shell commands with enhanced features such as **colored output**, **error handling**, **ASCII art**, and **custom command processing**.

---

## 🖼️ Images / Assets

Place all shell-related images inside a folder named:

```

images/

````

This will keep the project organized and compatible with the UI/theme you may add later.

---

## 📑 Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Contact](#contact)

---

## ⚙️ Installation

Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
````

---

## ▶️ Usage

Run the shell using:

```bash
python shell.py
```

Once launched, you will see a prompt like:

```
/current/directory $
```

You can now enter commands as you would in a standard shell.

---

## ⭐ Features

### 🔹 Basic Shell Prompt

* Displays the **current working directory** followed by a `$` symbol.

### 🔹 Built-in Command Execution

The shell supports several core commands:

| Command | Description                           |
| ------- | ------------------------------------- |
| `cd`    | Change directory                      |
| `ls`    | List files/directories (green output) |
| `pwd`   | Print current directory               |
| `cat`   | Display file content                  |
| `mkdir` | Create a directory                    |
| `grep`  | Search text pattern inside files      |
| `rm`    | Delete files or folders               |
| `cp`    | Copy files/directories                |
| `mv`    | Move or rename files                  |
| `head`  | Show first N lines of file            |
| `tail`  | Show last N lines of file             |

---

### 🔹 Error Handling

* Detects missing files
* Invalid arguments
* Permission issues
* Provides **clear, colored error messages**

---

### 🎨 Colored Output

ANSI colors are used for better readability:

* **Green** → `ls` output
* **Red** → error messages
* **Blue** → current working directory
* **Cyan** → ASCII art (pyfiglet)
* **Yellow** → exit messages

---

### 🔹 ASCII Art Banner

Displays a **Thanatos ASCII Art** using `pyfiglet` when the shell starts, giving it a professional/hacker-style look.

---

### 🔹 External Command Execution

If a command is not recognized as built-in, the shell attempts to run it as a **system command** using:

```
subprocess.run()
```

This allows:

* Running scripts
* Launching programs
* Executing system utilities

---

### 🔹 Smart Command Handling

* Splits user input into **command + arguments**
* Automatically matches built-in or external commands
* Handles invalid syntax gracefully

---

### 🔹 Graceful Exit

Typing:

```
exit
```

Shows a styled exit message and shuts down with a smooth delay.

---

### 🔹 Input Validation

Ensures the user provides correct arguments:

* Missing file names
* Unsupported flags
* Invalid directories

Shell responds with meaningful feedback instead of failing silently.

---

## 🤝 Contributing

Contributions are welcome!
To contribute:

1. Fork the repository
2. Make changes
3. Submit a pull request

---

## 📬 Contact

For questions, issues, or suggestions:

**Mridul Chamoli**
📧 **[mridulchamoli93@gmail.com](mailto:mridulchamoli93@gmail.com)**


