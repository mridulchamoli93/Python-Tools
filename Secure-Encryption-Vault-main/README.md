# 📦 **NightVault — Encrypted Cyberpunk File Vault**

NightVault is a modern, cyberpunk-themed secure file vault built with **PyQt6** and a hybrid encryption backend.
It features smooth UI animations, glowing neon visuals, hacker-style themes, and strong local encryption designed to keep your files safe, private, and stylish.

---

## 🚀 **Features**

### 🔐 **Security**

* Password-protected vaults
* PBKDF2-derived keys
* Encrypted vault storage using **Fernet (AES-128 CBC + HMAC)**
* Legacy XOR mode for backward compatibility
* Per-user vault directories
* Automatic salt & wrapped key handling
* Recovery key support
* Optional trusted-device login token

---

## 🎨 **Cyberpunk UI / UX**

* Full neon hacker theme
* Dark glass panels with glow edges
* Particle scanline animation
* Optional glitch & binary-rain overlays
* User avatar with neon circular mask
* Animated transitions:

  * Fade-in
  * Slide-in for dashboard
  * Wrong password shake
  * Neon ripple button clicks

---

## 🖥️ **Pages & Navigation**

### 1️⃣ **Login Page**

Clean and simple, no distractions — the gateway to the vault.


<img width="1589" height="939" alt="Screenshot 2025-12-04 121052" src="https://github.com/user-attachments/assets/bbe15921-5223-400b-bbd3-8cbbe023c331" />


### 2️⃣ **Dashboard**

* Hacker terminal
* Vault analytics
* Stats:

  * File count
  * Total size
  * Last upload
  * File type distribution
* Custom avatar
* Animated glow UI

<img width="1535" height="985" alt="Screenshot 2025-12-04 121126" src="https://github.com/user-attachments/assets/61757014-1784-4859-a80a-68d80e6a8b36" />



### 3️⃣ **File Manager**

* Drag & drop upload
* Encrypted save
* Decrypt & export
* Permanent delete
* Bulk selection
* File filters
<img width="1550" height="984" alt="Screenshot 2025-12-04 121351" src="https://github.com/user-attachments/assets/8da55b76-138d-4602-9936-d2b126105f10" />


---

### 4️⃣ **Settings**

* Theme selector (Blue, Matrix-Green, Red Alert, Purple Cyber)
* Trust device toggle
* Recovery key reset
* Vault export (encrypted archive)
* App personalization

<img width="1557" height="991" alt="Screenshot 2025-12-04 121747" src="https://github.com/user-attachments/assets/a6d14887-d1a5-4206-a632-c93365110bf9" />


### 5️⃣ **Themes Page**

<img width="1546" height="988" alt="Screenshot 2025-12-04 121417" src="https://github.com/user-attachments/assets/27b29775-6f2c-4e98-978e-4e63bcb5cb81" />


## 📁 **Project Structure**

```
📦 NightVault
 ┣ 📂 vaults/
 ┣ 📜 vault_app.py         → PyQt6 UI / UX
 ┣ 📜 vault_logic.py       → Backend encryption & DB logic
 ┣ 📜 trusted_tokens.json  → Trusted device tokens
 ┣ 📜 vault_users.db       → SQLite user database
 ┣ 🖼️ avatar.jpg           → User profile avatar (optional)
 ┣ 📜 requirements.txt
 ┗ 📜 README.md
```

---

## 🔧 **Installation**

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Run the app

```
python vault_app.py
```

---

## 🛠️ **Build EXE / MSI / Portable**

### EXE (Windows)

```
pyinstaller --noconsole --icon=icon.ico --onefile vault_app.py
```

### Portable Folder

```
pyinstaller --noconsole --icon=icon.ico --add-data "vaults;vaults" vault_app.py
```

### MSI (via Inno Setup or Wix Toolset)

Will generate:

* Installer
* Desktop shortcut
* Auto-create AppData storage

*(Ask me and I will generate the full `.iss` script or Wix config.)*

---

## 🔥 Planned Enhancements

* Animated splash screen
* Avatar selector in settings
* Cloud-sync optional module
* MFA code lock
* File preview (image, PDF, text)

---

## 🧑‍💻 Developer

Created by ** Mridul**
Cyberpunk-inspired secure storage system built with love.

---

## 📜 License

MIT License

