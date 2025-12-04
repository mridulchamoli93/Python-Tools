import sys
import os
import io
import threading
import hashlib
import webbrowser
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageOps

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFileDialog, QProgressBar, QMessageBox,
    QSizePolicy, QFrame, QSpacerItem
)
from PyQt6.QtGui import QPixmap, QIcon, QAction, QCursor, QTextCursor
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer

# ---------- Config ----------
DEFAULT_AVATAR = "67344c876c473c001d68c123.jpg"  # file you said is in repo
PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}
HTTP_TIMEOUT = 18

# ---------- Utility: circular avatar + neon ring ----------
def make_circular_avatar_bytes(image_path: str, size: int = 140, ring_color=(30,200,255,220), ring_width: int = 6):
    """
    Returns PNG bytes of a circular-masked avatar with a neon ring.
    """
    # load image
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception:
        img = Image.new("RGBA", (size, size), (12, 18, 28, 255))

    # crop to square and resize
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left+side, top+side)).resize((size, size), Image.LANCZOS)

    # circular mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size-1, size-1), fill=255)
    img.putalpha(mask)

    # neon ring overlay
    ring = Image.new("RGBA", (size, size), (0,0,0,0))
    rdraw = ImageDraw.Draw(ring)

    # outer glow - multiple faint ellipses
    for i, a in enumerate((80, 48, 28)):
        alpha = int(a)
        col = (ring_color[0], ring_color[1], ring_color[2], alpha)
        extra = i * 2
        rdraw.ellipse((extra, extra, size-1-extra, size-1-extra), outline=col, width=1)

    inset = ring_width//2 + 2
    rdraw.ellipse((inset, inset, size - inset - 1, size - inset - 1), outline=ring_color, width=ring_width)

    out = Image.alpha_composite(img, ring)

    bio = io.BytesIO()
    out.save(bio, format="PNG")
    bio.seek(0)
    return bio.read()

def qpixmap_from_bytes(png_bytes):
    pix = QPixmap()
    pix.loadFromData(png_bytes)
    return pix

# ---------- Worker thread for searching ----------
class SearchWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, keyword: str, use_tor=True):
        super().__init__()
        self.keyword = keyword
        self.use_tor = use_tor

    def run(self):
        try:
            onion_url = f"https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/html?q={self.keyword}"
            headers = {"User-Agent": "PyQt-DarkHunter/1.0"}
            if self.use_tor:
                try:
                    resp = requests.get(onion_url, proxies=PROXIES, headers=headers, timeout=HTTP_TIMEOUT)
                except Exception:
                    fallback = f"https://html.duckduckgo.com/html/?q={self.keyword}"
                    resp = requests.get(fallback, headers=headers, timeout=HTTP_TIMEOUT)
            else:
                fallback = f"https://html.duckduckgo.com/html/?q={self.keyword}"
                resp = requests.get(fallback, headers=headers, timeout=HTTP_TIMEOUT)

            soup = BeautifulSoup(resp.text, "html.parser")
            results = []
            anchors = soup.find_all("a")
            for a in anchors:
                txt = a.get_text(strip=True)
                href = a.get("href", "")
                if not txt:
                    continue
                if len(txt) < 8:
                    continue
                results.append(f"• {txt}\n  ➜ {href}")
                if len(results) >= 12:
                    break
            if not results:
                out = "[×] No readable results found (page structure may differ)."
            else:
                out = "\n\n".join(results)
            self.finished.emit(out)
        except Exception as e:
            self.error.emit(str(e))

# ---------- Main Window ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NightVault — PyQt6 Hunter")
        self.resize(1120, 720)
        self._central = QWidget()
        self.setCentralWidget(self._central)
        self._build_ui()
        self._apply_dark_theme()

        # try to load default avatar
        self.current_avatar_path = DEFAULT_AVATAR if Path(DEFAULT_AVATAR).exists() else None
        self._load_avatar(self.current_avatar_path)
        self.search_thread = None

    def _build_ui(self):
        root = QHBoxLayout()
        self._central.setLayout(root)

        # Sidebar (left)
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #06101a, stop:1 #071018);")
        v = QVBoxLayout(sidebar)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(10)

        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(120, 120)
        self.avatar_label.setStyleSheet("border-radius:60px;")
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(self.avatar_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        title = QLabel("NightVault Hunter")
        title.setStyleSheet("color: #9fdcff; font-weight:700; font-size:16px;")
        v.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)

        v.addSpacing(8)

        # Theme toggle
        self.theme_btn = QPushButton("Toggle Light/Dark")
        self.theme_btn.clicked.connect(self._toggle_theme)
        v.addWidget(self.theme_btn)

        # Quick buttons
        self.btn_search_tab = QPushButton("New Search")
        self.btn_search_tab.clicked.connect(lambda: self._focus_search())
        self.btn_upload = QPushButton("Upload Image")
        self.btn_upload.clicked.connect(self._on_upload)
        self.btn_save = QPushButton("Save Results")
        self.btn_save.clicked.connect(self._save_results)
        self.btn_open_images = QPushButton("Image Search")
        self.btn_open_images.clicked.connect(lambda: self._open_image_search(self.search_input.text().strip()))

        for btn in (self.btn_search_tab, self.btn_upload, self.btn_save, self.btn_open_images):
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setMinimumHeight(36)
            v.addWidget(btn)

        v.addStretch()
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #8fbfdc;")
        v.addWidget(self.status_label)

        root.addWidget(sidebar)

        # Main area (right)
        main_frame = QFrame()
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(12,12,12,12)
        main_layout.setSpacing(8)

        # Top: search bar
        top = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter keyword or phrase...")
        self.search_input.returnPressed.connect(self._start_search)
        top.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self._start_search)
        top.addWidget(self.search_button)

        self.spinner_label = QLabel("")  # animated text spinner
        top.addWidget(self.spinner_label)
        main_layout.addLayout(top)

        # Middle: split - left output, right preview
        mid = QHBoxLayout()

        # Output text
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self._log(f"[{datetime.utcnow().isoformat()}] App started. Ready.\n")
        mid.addWidget(self.output, 3)

        # Right column - preview and details
        right_col = QVBoxLayout()
        self.preview_title = QLabel("Preview")
        right_col.addWidget(self.preview_title, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(260, 260)
        self.preview_label.setStyleSheet("border-radius:8px; background: rgba(8,12,20,0.6);")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_col.addWidget(self.preview_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.hash_label = QLabel("SHA-256: —")
        self.hash_label.setWordWrap(True)
        right_col.addWidget(self.hash_label)

        btns = QHBoxLayout()
        self.preview_upload_btn = QPushButton("Upload")
        self.preview_upload_btn.clicked.connect(self._on_upload)
        self.preview_open_btn = QPushButton("Open Images")
        self.preview_open_btn.clicked.connect(lambda: self._open_image_search(self.search_input.text().strip()))
        btns.addWidget(self.preview_upload_btn)
        btns.addWidget(self.preview_open_btn)
        right_col.addLayout(btns)
        right_col.addStretch()

        self.copy_btn = QPushButton("Copy Output")
        self.copy_btn.clicked.connect(self._copy_output)
        right_col.addWidget(self.copy_btn)

        mid.addLayout(right_col, 1)

        main_layout.addLayout(mid)

        # Bottom: progress bar and footer
        bottom = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        bottom.addWidget(self.progress)
        self.save_btn = QPushButton("Save Log")
        self.save_btn.clicked.connect(self._save_results)
        bottom.addWidget(self.save_btn)
        main_layout.addLayout(bottom)

        root.addWidget(main_frame, 1)

        # Drag & drop onto preview_label
        self.preview_label.setAcceptDrops(True)
        self.preview_label.installEventFilter(self)

    # ---------- Drag & Drop ----------
    def eventFilter(self, obj, event):
        if obj is self.preview_label:
            if event.type() == event.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.accept()
                    return True
            if event.type() == event.Type.Drop:
                urls = event.mimeData().urls()
                if urls:
                    path = urls[0].toLocalFile()
                    self._set_preview_image(path)
                event.accept()
                return True
        return super().eventFilter(obj, event)

    # ---------- Theming ----------
    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background: #051018; }
            QTextEdit { background: #071018; color: #dfefff; border: 1px solid rgba(255,255,255,0.05); }
            QLineEdit { background: #08121a; color: #dfefff; padding: 6px; border-radius: 6px; }
            QPushButton { background: #0b1720; color: #e8fbff; padding: 6px; border-radius:6px; border: 1px solid rgba(110,232,255,0.12); }
            QLabel { color: #cfeefe; }
            QProgressBar { height: 12px; border-radius:6px; background: #031016; color: #dff6ff; }
        """)

    def _apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow { background: #f6fbff; }
            QTextEdit { background: #ffffff; color: #042029; border: 1px solid rgba(0,0,0,0.06); }
            QLineEdit { background: #fff; color: #042029; padding: 6px; border-radius: 6px; }
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #e8faff, stop:1 #dff6ff); color: #022; padding: 6px; border-radius:6px; }
            QLabel { color: #042029; }
            QProgressBar { height: 12px; border-radius:6px; background: #e8f8ff; color: #022; }
        """)

    def _toggle_theme(self):
        current = getattr(self, "_light", False)
        if current:
            self._apply_dark_theme()
            self._light = False
            self._log("[INFO] Switched to Dark theme")
        else:
            self._apply_light_theme()
            self._light = True
            self._log("[INFO] Switched to Light theme")

    # ---------- Avatar / preview ----------
    def _load_avatar(self, path):
        if not path:
            b = make_circular_avatar_bytes("", size=140)
        else:
            b = make_circular_avatar_bytes(path, size=140)
        pix = qpixmap_from_bytes(b).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.avatar_label.setPixmap(pix)
        p2 = qpixmap_from_bytes(b).scaled(260, 260, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.preview_label.setPixmap(p2)

    def _set_preview_image(self, path):
        self.current_avatar_path = path
        try:
            b = make_circular_avatar_bytes(path, size=260, ring_color=(30,200,255,200), ring_width=8)
            pix = qpixmap_from_bytes(b).scaled(260, 260, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.preview_label.setPixmap(pix)
            b2 = make_circular_avatar_bytes(path, size=120, ring_color=(30,200,255,200), ring_width=6)
            pix2 = qpixmap_from_bytes(b2).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.avatar_label.setPixmap(pix2)
            h = self._compute_hash(path)
            self.hash_label.setText(f"SHA-256: {h}")
            self._log(f"[{datetime.utcnow().isoformat()}] Uploaded {os.path.basename(path)}\nHash: {h}\n")
        except Exception as e:
            self._log(f"[WARN] Could not set preview: {e}")

    def _compute_hash(self, path):
        try:
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as e:
            return f"err:{e}"

    # ---------- Search flow ----------
    def _focus_search(self):
        self.search_input.setFocus()

    def _start_search(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, "Empty", "Please enter a search keyword.")
            return
        self._set_busy(True)
        self.progress.setValue(0)
        self._start_spinner()
        self.search_thread = SearchWorker(keyword, use_tor=True)
        self.search_thread.finished.connect(self._on_search_finished)
        self.search_thread.error.connect(self._on_search_error)
        self.search_thread.start()
        self._log(f"[{datetime.utcnow().isoformat()}] Searching for: {keyword}")

    def _on_search_finished(self, text):
        self._stop_spinner()
        self._set_busy(False)
        self.progress.setValue(100)
        snippet = f"\n[RESULTS @ {datetime.utcnow().isoformat()}]\n{text}\n\n"
        self._log(snippet)
        self.status_label.setText("Search complete")

    def _on_search_error(self, message):
        self._stop_spinner()
        self._set_busy(False)
        self.progress.setValue(0)
        self._log(f"[ERROR] {message}\n")
        QMessageBox.critical(self, "Search error", message)
        self.status_label.setText("Error")

    # ---------- Spinner animation (text) ----------
    def _start_spinner(self):
        self._spinner_tick = 0
        self._spinner_timer = QTimer()
        self._spinner_timer.timeout.connect(self._spinner_frame)
        self._spinner_timer.start(200)

    def _spinner_frame(self):
        self._spinner_tick = (self._spinner_tick + 1) % 6
        dots = "." * (self._spinner_tick % 4)
        self.spinner_label.setText(f"Searching{dots}")

    def _stop_spinner(self):
        if hasattr(self, "_spinner_timer"):
            self._spinner_timer.stop()
            self.spinner_label.setText("")

    def _set_busy(self, busy: bool):
        for w in (self.search_button, self.btn_upload, self.btn_search_tab, self.btn_save, self.btn_open_images, self.preview_upload_btn, self.preview_open_btn):
            w.setDisabled(busy)

    # ---------- File / preview actions ----------
    def _on_upload(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Choose an image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not fname:
            return
        self._set_preview_image(fname)

    def _open_image_search(self, keyword):
        if not keyword:
            QMessageBox.information(self, "No keyword", "Enter a keyword to open image search.")
            return
        url = f"https://duckduckgo.com/?q={keyword}+images&t=h_&iar=images&iax=images&ia=images"
        webbrowser.open(url)

    def _save_results(self):
        txt = self.output.toPlainText().strip()
        if not txt:
            QMessageBox.information(self, "No results", "There's no output to save.")
            return
        fname, _ = QFileDialog.getSaveFileName(self, "Save results", "search_results.txt", "Text files (*.txt)")
        if not fname:
            return
        with open(fname, "w", encoding="utf-8") as f:
            f.write(txt)
        QMessageBox.information(self, "Saved", f"Saved to {fname}")

    def _copy_output(self):
        txt = self.output.toPlainText()
        if txt:
            QApplication.clipboard().setText(txt)
            self._log("[INFO] Output copied to clipboard.\n")

    # ---------- Logging helper (fixed for PyQt6) ----------
    def _log(self, text):
        """
        Append text to the output QTextEdit safely in PyQt6.
        """
        cursor = self.output.textCursor()
        # move to end using QTextCursor MoveOperation (PyQt6)
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.output.setTextCursor(cursor)
        # insert text
        self.output.insertPlainText(text + ("\n" if not text.endswith("\n") else ""))
        self.output.ensureCursorVisible()

# ---------- Entrypoint ----------
def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    if Path(DEFAULT_AVATAR).exists():
        mw._load_avatar(DEFAULT_AVATAR)
    mw.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
