Here is a **professional, clean, GitHub-ready `README.md`** for your login-registration Python GUI project, including folder instructions and requirements.

You can **copy–paste this directly** into your repository.

---

```md
# 🔐 Python Login & Registration System (Tkinter + MySQL)

A modern Python-based **Login & Registration System** built using **Tkinter**, **MySQL**, and **Base64 image handling**.  
This project includes a clean graphical UI, user authentication, secure password handling, and image-based UI elements.

---

## 🚀 Features

- 🖥 **Modern Tkinter GUI**
- 🔑 User Registration & Login
- 🔒 Password show / hide toggle (eye icon)
- 🗄 MySQL database connectivity
- 🖼 Image-based buttons, icons & UI elements
- 📂 Organized asset structure (image folders)
- ⚙ Easy to configure and extend

---

## 📁 Project Structure

```

📦 project
┣ 📂 image
┃ ┣ backbutton.png
┃ ┣ icon.png
┃ ┣ Layer 4.png
┃ ┣ LOGIN.png
┃ ┣ logo.png
┃ ┣ register.png
┃ ┣ search.png
┃ ┗ upload photo.png
┣ 📂 images
┃ ┣ backbutton.png
┃ ┣ closeeye.png
┃ ┣ icon.png
┃ ┣ LOGIN.png (blue one)
┃ ┣ openeye.png
┃ ┣ search.png
┃ ┗ upload.png
┣ main.py
┣ login.py
┣ registration.py
┣ requirements.txt
┗ README.md

```

---

## 📦 Requirements

Install the following modules before running the project:

```

tkinter
os
mysql.connector
base64

````

You can install MySQL connector via:

```bash
pip install mysql-connector-python
````

Tkinter comes pre-installed with Python on most systems.

---

## 📂 Mandatory Folder Setup

You must create **two folders** in the project root:

### ✔ Folder: `image`

Move these files into `image/`:

* backbutton.png
* icon.png
* Layer 4.png
* LOGIN.png
* logo.png
* register.png
* search.png
* upload photo.png

### ✔ Folder: `images`

Move these files into `images/`:

* backbutton.png
* closeeye.png
* icon.png
* LOGIN.png *(blue version)*
* openeye.png
* search.png
* upload.png

This structure ensures all GUI images load correctly.

---

## ▶️ How to Run

1. Configure your MySQL database:

```sql
CREATE DATABASE login_system;
USE login_system;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);
```

2. Update database credentials inside:

```
login.py  
registration.py  
```

3. Run the main application:

```bash
python main.py
```

---

## 🧩 Files Overview

| File              | Description             |
| ----------------- | ----------------------- |
| `main.py`         | Launches the full app   |
| `login.py`        | Login window logic      |
| `registration.py` | User registration logic |
| PNG files         | GUI assets & icons      |

---

## 🎯 Purpose

This project is ideal for:

* Students learning Tkinter GUI development
* Beginners practicing MySQL + Python integration
* Anyone building authentication systems
* Portfolio projects

---

## 🤝 Contributing

Pull requests and improvements are always welcome.

---

## ⭐ Support

If this project helped you, please consider giving the repo a **star** ⭐ — it motivates future improvements!

```

---

If you want, I can also make:  
✅ A **dark hacker-style README**  
✅ A **student-friendly README**  
✅ Add badges (Python, Tkinter, MySQL, License, etc.)  
Just tell me!
```
