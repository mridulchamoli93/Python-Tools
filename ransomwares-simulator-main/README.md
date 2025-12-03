# 💀 Ransomware Simulator — Pandora  
A **safe and controlled ransomware simulation tool** created for educational, learning, and cybersecurity testing purposes.  
This simulator mimics real ransomware behavior *without causing any real harm*, allowing users to understand encryption and decryption workflows.

---

## 🧩 What Is a Ransomware Simulator?

A ransomware simulator is a controlled tool used to demonstrate how ransomware:
- Encrypts files  
- Demands a key for decryption  
- Interacts with the user  

This helps developers, students, and security researchers test their defenses and learn how ransomware works **without risking actual damage**.

---

# 🔐 Pandora Ransomware Simulator

Pandora simulates a ransomware attack by:
- Encrypting selected files using a custom algorithm  
- Requiring a correct key to decrypt them  
- Providing a GUI for easy decryption testing  

Perfect for cybersecurity training environments.

---

## ⭐ Features

### 🔸 File Encryption  
Encrypts files using a **custom algorithm** written purely in Python.

### 🔸 File Decryption  
Decrypts the encrypted files using the **correct decryption key**.

### 🔸 GUI Support  
A user-friendly interface for decryption, built using Tkinter/PIL.

### 🔸 Controlled & Safe  
Does **not** harm your system or spread like real ransomware.  
You decide:
- what to encrypt  
- when to decrypt  
- which environment to test  

---

## 📦 Installation

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/ransomwares-simulator.git
cd ransomwares-simulator
````

### 2️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

Add these to your `requirements.txt` if needed:

```
tkinter
Pillow
os
base64
```

---

## ▶️ Usage

### 🔐 Encrypt Files

Run the encryption script:

```bash
python encr.py
```

You will be prompted to select files or a folder to encrypt.

---

### 🔓 Decrypt Files (CLI)

```bash
python dec.py
```

This will ask for the **decryption key**.

---

### 🖥 GUI Decryption

Run either GUI:

```bash
python gui.py
```

or

```bash
python pandora_gui.py
```

The GUI will:

* Display the status
* Ask for the decryption key
* Decrypt files upon successful validation

---

## 📁 Project Files

| File               | Description                           |
| ------------------ | ------------------------------------- |
| `encr.py`          | Handles file encryption               |
| `dec.py`           | Handles file decryption               |
| `gui.py`           | Basic Tkinter decryption interface    |
| `pandora_gui.py`   | Extended GUI with additional features |
| `README.md`        | Project documentation                 |
| `requirements.txt` | Dependency list                       |

---

## ⚠️ Disclaimer

This tool is strictly for:

* Cybersecurity education
* Research
* Simulation
* Demonstration in controlled environments

**Do NOT use this tool for malicious purposes.
The author is not responsible for any misuse.**

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 📬 Contact

For questions, issues, or suggestions:

**Mridul Chamoli**
📧 **[mridulchamoli93@gmail.com](mailto:mridulchamoli93@gmail.com)**

---


