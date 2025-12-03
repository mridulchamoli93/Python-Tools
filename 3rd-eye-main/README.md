# 🔍 Third Eye – Facial Recognition Criminal Detection System

**Third Eye** is a secure, visually rich facial recognition web application that identifies known criminals using image matching. It combines Python-based facial recognition, EJS-powered frontend views, and an Express-Flask microservice architecture to simulate real-time surveillance and identification.

---

## 📁 Project Structure

third-eye/
│
├── views/ # EJS templates
│ ├── display.ejs
│ ├── home.ejs
│ ├── index.ejs
│ ├── login.ejs
│ └── register.ejs
│
├── facerec.py # Facial recognition script
├── server.js # Node.js Express server
├── server.py # System 1 (Flask API to receive face match)
├── server2.py # System 2 (Simulated database lookup)



---

## 🧠 Features

- 🔐 **Authentication System** – User login/register with validations.
- 🎭 **Face Matching** – Compares live image input with a local criminal image database.
- 📡 **Microservices Communication** – Python Flask APIs forward detected criminal ID between systems.
- 🕵️‍♂️ **Criminal Profile Viewer** – Displays a stylized profile if the face matches a criminal.
- 🎨 **Futuristic UI** – Built with glitch and matrix-style animations for immersive feel.

---

## 🚀 How It Works

1. User uploads or captures a face image (`facerec.py`).
2. If matched with the database, it sends the criminal ID to a Flask server (`server.py`).
3. Flask relays this ID to another server (`server2.py`) simulating metadata lookup.
4. Express (`server.js`) renders a visually dynamic criminal profile via `display.ejs`.

---

## 🖥️ Technologies Used

- **Frontend**: HTML, CSS, EJS Templates
- **Backend**:
  - Express.js (Node.js)
  - Flask (Python)
  - OpenCV + face_recognition (Python)
- **APIs**: REST-based ID forwarding and matching
- **Styling**: Techno, glitch, and matrix animation styles (CSS + JS)

---

## ⚙️ Setup Instructions

1. **Install Node and Python dependencies**:
    ```bash
    pip install opencv-python face_recognition flask requests
    npm install express ejs
    ```

2. **Run the Flask Servers**:
    - Start `server2.py` (System 2):
      ```bash
      python server2.py
      ```
    - Start `server.py` (System 1):
      ```bash
      python server.py
      ```

3. **Start the Node.js Server**:
    ```bash
    node server.js
    ```

4. **Run Facial Recognition Script**:
    ```bash
    python facerec.py
    ```

---

## 📷 Sample Data

- Store images of criminals in the `/criminal` folder.
- Ensure filenames match the ID used in the mock database in `server2.py`.

---

## ✨ Screens (EJS Views)

| View           | Description                            |
|----------------|----------------------------------------|
| `index.ejs`    | Home search page for criminal ID       |
| `home.ejs`     | Animated fingerprint scan intro        |
| `login.ejs`    | User login form                        |
| `register.ejs` | User registration form                 |
| `display.ejs`  | Profile UI for matched criminals       |

---

## 🔒 Security Considerations

- Input validation is done for login and registration.
- Password validation (length ≥ 8 characters).
- Simulated secure communication between services.

---

## 📌 Future Enhancements

- Integrate live CCTV footage.
- Use a real database (MongoDB/PostgreSQL).
- Deploy via Docker Compose.
- Add audio alerts and multi-factor authentication.

---

## 👨‍💻 Author

**Mridul Chamoli**  
📫 [GitHub](https://github.com/mridulchamoli93)

---

## 📜 License

This project is licensed under the MIT License.
