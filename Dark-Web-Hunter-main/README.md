# Dark-Web-Hunter
Dark Web Hunter is a Python-based desktop application that enables users to perform dark web searches through DuckDuckGo’s onion service using the Tor network. Featuring a sleek tkinter-based GUI, the app allows for keyword-based search, image hash generation for uploaded files, and simulated dark web image analysis.
# 🕶️ Dark Web Hunter

> An interactive GUI application to search dark web content using keywords or image hashes, with simulated image search and a sleek dark-themed interface.

## 📌 Features

- Keyword-based search on DuckDuckGo's onion service via Tor
- Upload an image to generate its SHA-256 hash
- Display image hash and simulate dark web lookup
- Show related surface web images
- Save search results to a file
- Minimal dark-themed GUI built with `tkinter`

## 🖼️ Preview
<img width="1399" height="940" alt="Screenshot 2025-12-04 123111" src="https://github.com/user-attachments/assets/73dab29b-88b4-4ab3-84a9-2cddb7025cd2" />

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/mridulchamoli93/Python-Tools/tree/main/Dark-Web-Hunter-main
cd DarkWebHunter
2. Install dependencies
Use pip to install required libraries:

bash
Copy
Edit
pip install -r requirements.txt
3. Set up Tor
Ensure Tor is running and the SOCKS5 proxy is available at 127.0.0.1:9050.

Install Tor:

Linux: sudo apt install tor

Windows: Download Tor Expert Bundle

Start Tor before launching the app.

🚀 Run the App
bash
Copy
Edit
python main2.py
📂 Output
Search results will be saved to:

Copy
Edit
search_results.txt
⚠️ Disclaimer
This tool uses publicly available .onion search interfaces and is intended strictly for ethical, educational, and legal use only. Always respect privacy and security laws.

🛠️ Tech Stack
Python

tkinter

PIL (Pillow)

requests

BeautifulSoup

Tor Network (SOCKS5 proxy)

📃 License
MIT - free to use and modify.

yaml
Copy
Edit

---

### (Optional) 📁 `.gitignore`

```gitignore
__pycache__/
*.pyc
search_results.txt
*.log
