import sys
import io
import math
import random
import secrets
from pathlib import Path
from datetime import datetime

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, QRect, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QIcon, QColor, QPainter, QPen, QBrush
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout,
    QListWidget, QFileDialog, QMessageBox, QStackedWidget, QTextEdit, QCheckBox, QDialog
)

# ensure vault_logic available
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import vault_logic as logic

from PIL import Image, ImageDraw, ImageFont

APP_NAME = "NightVault"

# ---------------- THEMES ----------------
THEMES = {
    "blue": {
        "bg": "#06101a",
        "accent": "#6EE8FF",
        "accent2": "#2ec4ff",
        "panel": "rgba(6,12,18,0.86)",
        "muted": "#9fdcff",
        "glow": QColor(110, 232, 255, 180)
    },
    "matrix": {
        "bg": "#001402",
        "accent": "#7CFF5A",
        "accent2": "#3EFF2E",
        "panel": "rgba(1,10,3,0.86)",
        "muted": "#a8ff9a",
        "glow": QColor(124, 255, 90, 180)
    },
    "alert": {
        "bg": "#140606",
        "accent": "#FF6B6B",
        "accent2": "#FF3B3B",
        "panel": "rgba(20,6,6,0.88)",
        "muted": "#ffb3b3",
        "glow": QColor(255, 107, 107, 180)
    },
    "purple": {
        "bg": "#0b0414",
        "accent": "#c57fff",
        "accent2": "#9a6bff",
        "panel": "rgba(12,6,20,0.88)",
        "muted": "#d5b3ff",
        "glow": QColor(197,127,255,180)
    }
}
CURRENT_THEME = "blue"
# add near the top of vault_app.py, after THEMES and CURRENT_THEME definitions

def apply_theme_to_widget(widget):
    """Simple helper to apply the current theme background color to a widget."""
    t = THEMES[CURRENT_THEME]
    try:
        widget.setStyleSheet(f"background: {t['bg']}; color: #dfefff;")
    except Exception:
        # defensive: if widget doesn't accept stylesheet, ignore
        pass

def neon_button_css():
    t = THEMES[CURRENT_THEME]
    return f"""
    QPushButton {{
        color: #ecfeff;
        background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
            stop:0 rgba(6,12,18,220), stop:1 rgba(12,22,32,210));
        border: 1px solid {t['accent']};
        border-radius: 9px;
        padding: 9px 14px;
    }}
    QPushButton:hover {{
        border: 1px solid {t['accent2']};
    }}
    """

def neon_border_css():
    t = THEMES[CURRENT_THEME]
    return f"""
        background: {t['panel']};
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(255,255,255,0.03);
    """

# ---------------- Icon/Avatar ----------------
def generate_logo_bytes(size=256):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i in range(6):
        r = int(size * (0.45 - i * 0.06))
        alpha = max(0, int(40 - i * 6))
        draw.ellipse([(size//2 - r, size//2 - r), (size//2 + r, size//2 + r)], fill=(10, 12, 18, alpha))
    ring_color = (30, 200, 255, 200)
    draw.ellipse([(int(size*0.12), int(size*0.12)), (int(size*0.88), int(size*0.88))], outline=ring_color, width=max(2, int(size*0.04)))
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", int(size*0.46))
    except Exception:
        try:
            font = ImageFont.truetype("arial.ttf", int(size*0.46))
        except Exception:
            font = ImageFont.load_default()
    text = "N"
    try:
        tw, th = font.getsize(text)
    except Exception:
        try:
            bbox = draw.textbbox((0,0), text, font=font)
            tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        except Exception:
            try:
                tw, th = draw.textsize(text, font=font)
            except Exception:
                tw, th = int(size*0.5), int(size*0.5)
    x = (size - tw) / 2
    y = (size - th) / 2 - size*0.04
    draw.text((x+2, y+2), text, font=font, fill=(20,120,160,80))
    draw.text((x, y), text, font=font, fill=(110,232,255,220))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()

def set_app_icon(window):
    try:
        b = generate_logo_bytes(256)
        pix = QPixmap()
        pix.loadFromData(b)
        window.setWindowIcon(QIcon(pix))
    except Exception:
        pass

def generate_initials_avatar(name: str, size=128, bg="#071021", fg=(110,232,255,255)):
    initials = "".join([p[0].upper() for p in str(name).split()][:2]) or "N"
    img = Image.new("RGBA", (size, size), bg)
    draw = ImageDraw.Draw(img)
    font = None
    font_size = max(12, int(size * 0.48))
    for f in ("DejaVuSans-Bold.ttf", "arial.ttf"):
        try:
            font = ImageFont.truetype(f, font_size)
            break
        except Exception:
            font = None
    if font is None:
        font = ImageFont.load_default()
    try:
        w, h = font.getsize(initials)
    except Exception:
        try:
            bbox = draw.textbbox((0,0), initials, font=font)
            w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        except Exception:
            try:
                w, h = draw.textsize(initials, font=font)
            except Exception:
                w, h = int(size*0.5), int(size*0.5)
    x = (size - w) / 2
    y = (size - h) / 2 - int(size * 0.04)
    draw.text((x+2, y+2), initials, font=font, fill=(0,0,0,120))
    draw.text((x, y), initials, font=font, fill=fg)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()

# ---------------- Visuals ----------------
class BinaryRainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.cols = []
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(60)
        self.glitch_phase = 0

    def resizeEvent(self, ev):
        w = max(1, self.width())
        col_w = 12
        cols = max(8, w // col_w)
        self.cols = [{"y": random.uniform(-200, 0), "speed": random.uniform(1.0, 5.0)} for _ in range(cols)]
        self.particles = [{"x": random.uniform(0, w), "y": random.uniform(0, self.height()), "r": random.uniform(1.5,4.5), "vy": random.uniform(0.2,1.2), "alpha": random.uniform(30,140)} for _ in range(14)]

    def tick(self):
        for c in self.cols:
            c["y"] += c["speed"]
            if c["y"] > self.height() + 200:
                c["y"] = random.uniform(-200, -10)
                c["speed"] = random.uniform(1.0, 5.0)
        for p in self.particles:
            p["y"] += p["vy"]
            if p["y"] > self.height() + 20:
                p.update({"x": random.uniform(0, self.width()), "y": -10, "r": random.uniform(1.5,4.5), "vy": random.uniform(0.2,1.2), "alpha": random.uniform(30,140)})
        self.glitch_phase = (self.glitch_phase + 1) % 240
        self.update()

    def paintEvent(self, ev):
        p = QPainter(self)
        w, h = self.width(), self.height()
        grad = QtGui.QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, QColor(4,8,16,160))
        grad.setColorAt(1, QColor(6,12,24,120))
        p.fillRect(0, 0, w, h, grad)
        pen = QPen(QColor(8,20,32,30))
        p.setPen(pen)
        step = 40
        for x in range(0, w, step):
            p.drawLine(x, 0, x, h)
        for idx, c in enumerate(self.cols):
            col_w = max(8, w // max(10, len(self.cols)))
            col_x = idx * col_w
            y = c["y"]
            count = int(h / 12) + 2
            font = QtGui.QFont("Consolas", 10)
            p.setFont(font)
            for i in range(count):
                yy = y + i * 12
                if yy < -20 or yy > h + 20:
                    continue
                bit = random.choice(["0", "1"])
                alpha = int(60 + (i % 6) * 30)
                if i == 0:
                    color = QColor(180,255,200, min(220, alpha+80))
                else:
                    color = QColor(100,220,160, alpha)
                p.setPen(color)
                p.drawText(col_x + 2, int(yy), bit)
        for particle in self.particles:
            col = QColor(120,200,255, int(particle["alpha"]))
            p.setBrush(QBrush(col))
            p.setPen(Qt.PenStyle.NoPen)
            r = particle["r"]
            p.drawEllipse(QPoint(int(particle["x"]), int(particle["y"])), int(r), int(r))
        if (self.glitch_phase % 120) < 6:
            p.setPen(QPen(QColor(255,255,255,8)))
            for i in range(6):
                gy = random.randint(0, h)
                p.drawLine(0, gy, w, gy)
        p.end()

class RippleOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ripples = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(20)

    def add_ripple(self, x, y, color=QColor(90,220,255,160)):
        self.ripples.append({"x": x, "y": y, "r": 4.0, "a": 220, "col": color})

    def animate(self):
        new = []
        for r in self.ripples:
            r["r"] += 6
            r["a"] -= 8
            if r["a"] > 6:
                new.append(r)
        self.ripples = new
        if self.ripples:
            self.update()

    def paintEvent(self, ev):
        if not self.ripples:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        for r in self.ripples:
            col = QColor(r["col"])
            col.setAlpha(max(4, int(r["a"])))
            pen = QPen(col)
            pen.setWidth(3)
            p.setPen(pen)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(QPoint(int(r["x"]), int(r["y"])), int(r["r"]), int(r["r"]))
        p.end()

class NeonButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(neon_button_css())
        self.clicked.connect(self._on_click)
        self._ripple_cb = None

    def set_ripple_callback(self, cb):
        self._ripple_cb = cb

    def _on_click(self):
        if self._ripple_cb:
            pos = self.mapToGlobal(self.rect().center())
            parent_pos = self.parent().mapFromGlobal(pos)
            self._ripple_cb(parent_pos.x(), parent_pos.y())

# ---------------- ENHANCED DASHBOARD (MainWindow) ----------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME + " — Dashboard")
        self.resize(1240, 760)
        set_app_icon(self)
        self._animations = []
        self.ripple_overlay = RippleOverlay(self)
        self.bg_effect = BinaryRainWidget(self)
        self.bg_effect.setGeometry(0, 0, self.width(), self.height())
        self.ripple_overlay.setGeometry(0, 0, self.width(), self.height())
        self.sidebar = Sidebar(self, self.navigate)
        self.stack = QStackedWidget()
        self._build_pages()
        layout = QHBoxLayout()
        layout.setContentsMargins(12,12,12,12)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)
        self.setLayout(layout)
        apply_theme_to_widget(self)
        # state
        self.current_user = None
        self.vault_key = None

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.bg_effect.setGeometry(0,0,self.width(), self.height())
        self.ripple_overlay.setGeometry(0,0,self.width(), self.height())

    def _build_pages(self):
        # Dashboard
        dash = QWidget()
        dl = QVBoxLayout()
        self.user_panel = QWidget()
        self.user_panel.setStyleSheet(neon_border_css())
        upl = QHBoxLayout()
        self.avatar_lbl = QLabel()
        self.avatar_lbl.setFixedSize(92,92)
        self.avatar_lbl.setStyleSheet("border-radius:46px;")
        upl.addWidget(self.avatar_lbl)
        self.info_lbl = QLabel("Not logged in")
        self.info_lbl.setStyleSheet("font-weight:700; color: " + THEMES[CURRENT_THEME]['accent'] + ";")
        upl.addWidget(self.info_lbl)
        upl.addStretch()
        self.user_panel.setLayout(upl)
        dl.addWidget(self.user_panel)
        stats_and_term = QHBoxLayout()
        self.stats_panel = QWidget()
        self.stats_panel.setStyleSheet(neon_border_css())
        sp_layout = QVBoxLayout()
        self.files_count_lbl = QLabel("Files: 0")
        self.total_size_lbl = QLabel("Size: 0 bytes")
        self.last_login_lbl = QLabel("Last login: -")
        for w in (self.files_count_lbl, self.total_size_lbl, self.last_login_lbl):
            w.setStyleSheet("color: " + THEMES[CURRENT_THEME]['muted'])
            sp_layout.addWidget(w)
        self.stats_panel.setLayout(sp_layout)
        stats_and_term.addWidget(self.stats_panel, 0)
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background: rgba(0,0,0,0.18); color: " + THEMES[CURRENT_THEME]['muted'] + "; border-radius:8px;")
        self.terminal.setFixedHeight(220)
        stats_and_term.addWidget(self.terminal, 1)
        dl.addLayout(stats_and_term)
        dash.setLayout(dl)

        # Files
        files_page = QWidget()
        f_layout = QVBoxLayout()
        self.drop_zone = QLabel("Drag & drop files here")
        self.drop_zone.setFixedHeight(84)
        self.drop_zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_zone.setStyleSheet("border:1px dashed rgba(255,255,255,0.04); border-radius:8px; color:" + THEMES[CURRENT_THEME]['muted'])
        self.drop_zone.setAcceptDrops(True)
        self.drop_zone.installEventFilter(self)
        f_layout.addWidget(self.drop_zone)
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("background: rgba(0,0,0,0.16); color: #dfefff;")
        f_layout.addWidget(self.file_list)
        btns = QHBoxLayout()
        btn_upload = NeonButton("Upload")
        btn_upload.set_ripple_callback(self.ripple_overlay.add_ripple)
        btn_upload.clicked.connect(self.upload_file)
        btn_download = NeonButton("Download")
        btn_download.set_ripple_callback(self.ripple_overlay.add_ripple)
        btn_download.clicked.connect(self.download_selected)
        btn_delete = NeonButton("Delete")
        btn_delete.set_ripple_callback(self.ripple_overlay.add_ripple)
        btn_delete.clicked.connect(self.delete_selected)
        btns.addWidget(btn_upload); btns.addWidget(btn_download); btns.addWidget(btn_delete)
        f_layout.addLayout(btns)
        files_page.setLayout(f_layout)

        # Settings
        settings = QWidget()
        s_layout = QVBoxLayout()
        s_layout.addWidget(QLabel("Theme presets"))
        for key in THEMES.keys():
            b = NeonButton(key.title())
            b.set_ripple_callback(self.ripple_overlay.add_ripple)
            b.clicked.connect(lambda _, k=key: self.set_theme(k))
            s_layout.addWidget(b)
        s_layout.addSpacing(8)
        s_layout.addWidget(QLabel("About / Developer"))
        about_lbl = QLabel("NightVault — Developer: You\nMade with ❤️ — UI enhancements included.")
        about_lbl.setWordWrap(True)
        s_layout.addWidget(about_lbl)
        settings.setLayout(s_layout)

        about = QWidget()
        a_layout = QVBoxLayout()
        a_layout.addWidget(QLabel("NightVault — Glass + Neon UI\nContact: dev@nightvault.local"))
        about.setLayout(a_layout)

        self.stack.addWidget(dash)
        self.stack.addWidget(files_page)
        self.stack.addWidget(settings)
        self.stack.addWidget(about)

    def eventFilter(self, obj, ev):
        try:
            if ev.type() == QtCore.QEvent.Type.DragEnter and ev.mimeData().hasUrls():
                ev.acceptProposedAction()
                return True
            if ev.type() == QtCore.QEvent.Type.Drop:
                urls = ev.mimeData().urls()
                paths = [u.toLocalFile() for u in urls if u.isLocalFile()]
                self._handle_dropped_files(paths)
                ev.acceptProposedAction()
                return True
        except Exception:
            pass
        return super().eventFilter(obj, ev)

    def navigate(self, key):
        mapping = {"dashboard": 0, "files": 1, "settings": 2, "about": 3}
        idx = mapping.get(key, 0)
        if self.stack.currentIndex() == idx:
            return
        prev = self.stack.currentWidget()
        nxt = self.stack.widget(idx)
        self._animate_crossfade(prev, nxt)
        self.stack.setCurrentIndex(idx)

    def _animate_crossfade(self, prev_w, next_w):
        if prev_w:
            a1 = QPropertyAnimation(prev_w, b"windowOpacity")
            a1.setDuration(260)
            a1.setStartValue(1.0)
            a1.setEndValue(0.0)
            a1.start()
            self._animations.append(a1)
        if next_w:
            next_w.setWindowOpacity(0.0)
            a2 = QPropertyAnimation(next_w, b"windowOpacity")
            a2.setDuration(300)
            a2.setStartValue(0.0)
            a2.setEndValue(1.0)
            a2.start()
            self._animations.append(a2)

    # Public: initialize dashboard with logged-in user
    def start_with_user(self, username: str, key_bytes: bytes):
        self.current_user = username
        self.vault_key = key_bytes
        avatar = generate_initials_avatar(username, size=128, fg=(THEMES[CURRENT_THEME]['glow'].red(), THEMES[CURRENT_THEME]['glow'].green(), THEMES[CURRENT_THEME]['glow'].blue(), 255))
        pix = QPixmap()
        pix.loadFromData(avatar)
        self.avatar_lbl.setPixmap(pix.scaled(92,92, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.info_lbl.setText(f"@{username}")
        self.refresh_files()
        # fade/slide effect for showing dashboard
        self.setWindowOpacity(0.0)
        a = QPropertyAnimation(self, b"windowOpacity")
        a.setDuration(450)
        a.setStartValue(0.0)
        a.setEndValue(1.0)
        a.setEasingCurve(QEasingCurve.Type.InOutCubic)
        a.start()
        self._animations.append(a)

    def refresh_files(self):
        try:
            files = logic.list_vault_files(self.current_user) if self.current_user else []
            self.file_list.clear()
            for f in files:
                self.file_list.addItem(f)
            stats = logic.vault_analytics(self.current_user, self.vault_key if self.vault_key else b"") if hasattr(logic, "vault_analytics") else {"file_count": len(files), "total_size_bytes": 0, "last_upload": None}
            self.files_count_lbl.setText(f"Files: {stats.get('file_count', len(files))}")
            self.total_size_lbl.setText(f"Size: {stats.get('total_size_bytes', 0)} bytes")
            self.last_login_lbl.setText(f"Last: {stats.get('last_upload') or '-'}")
            self.terminal.append(f"[{datetime.utcnow().isoformat()}] Refreshed vault listing.")
        except Exception as e:
            self.terminal.append(f"[ERROR] {e}")

    def _handle_dropped_files(self, paths):
        cnt = 0
        for p in paths:
            try:
                if Path(p).is_file():
                    if hasattr(logic, "save_file_with_vaultkey"):
                        logic.save_file_with_vaultkey(self.current_user, self.vault_key, p)
                    else:
                        logic.save_encrypted_file(self.current_user, "", p)
                    cnt += 1
            except Exception as e:
                self.terminal.append(f"[WARN] Failed upload {Path(p).name}: {e}")
        self.terminal.append(f"[INFO] Uploaded {cnt} files.")
        self.refresh_files()

    def upload_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select file to upload", "", "All Files (*)")
        if not path:
            return
        try:
            if hasattr(logic, "save_file_with_vaultkey"):
                logic.save_file_with_vaultkey(self.current_user, self.vault_key, path)
            else:
                logic.save_encrypted_file(self.current_user, "", path)
            self.refresh_files()
        except Exception as e:
            QMessageBox.critical(self, "Upload failed", str(e))

    def download_selected(self):
        it = self.file_list.currentItem()
        if not it:
            QMessageBox.warning(self, "No selection", "Select a file.")
            return
        fname = it.text()
        try:
            orig, payload = logic.read_encrypted_file(self.current_user, fname)
            if hasattr(logic, "decrypt_payload"):
                dec = logic.decrypt_payload(self.vault_key, payload)
            else:
                dec = logic.xor_encrypt_bytes(payload, logic.derive_key(""))
            save_path, _ = QFileDialog.getSaveFileName(self, "Save as", orig, "All Files (*)")
            if not save_path:
                return
            Path(save_path).write_bytes(dec)
            QMessageBox.information(self, "Saved", f"Saved to {save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_selected(self):
        it = self.file_list.currentItem()
        if not it:
            QMessageBox.warning(self, "No selection", "Select a file.")
            return
        fname = it.text()
        if QMessageBox.question(self, "Delete", f"Delete {fname}?") == QMessageBox.StandardButton.Yes:
            logic.delete_vault_file(self.current_user, fname)
            self.refresh_files()

    def set_theme(self, key):
        global CURRENT_THEME
        if key not in THEMES:
            return
        CURRENT_THEME = key
        self.user_panel.setStyleSheet(neon_border_css())
        self.stats_panel.setStyleSheet(neon_border_css())
        self.drop_zone.setStyleSheet("border:1px dashed rgba(255,255,255,0.04); border-radius:8px; color:" + THEMES[CURRENT_THEME]['muted'])
        self.terminal.setStyleSheet("background: rgba(0,0,0,0.18); color: " + THEMES[CURRENT_THEME]['muted'] + "; border-radius:8px;")
        self.terminal.append(f"[INFO] Theme changed to {key}")

# ---------------- ORIGINAL LOGIN WINDOW (keeps your original design) ----------------
class ScanlineBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.offset = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(50)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def tick(self):
        self.offset = (self.offset + 1) % 2000
        self.update()

    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        w = self.width()
        h = self.height()
        grad = QtGui.QLinearGradient(0, 0, w, h)
        grad.setColorAt(0, QtGui.QColor("#03060a"))
        grad.setColorAt(1, QtGui.QColor("#071018"))
        p.fillRect(0, 0, w, h, grad)
        pen = QtGui.QPen(QtGui.QColor(10, 40, 60, 40))
        pen.setWidth(1)
        p.setPen(pen)
        step = 40
        for x in range(0, w, step):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, step):
            p.drawLine(0, y, w, y)
        scan_y = (self.offset % (h + 200)) - 100
        gradient = QtGui.QLinearGradient(0, scan_y, 0, scan_y+120)
        gradient.setColorAt(0.0, QtGui.QColor(0,0,0,0))
        gradient.setColorAt(0.45, QtGui.QColor(30,120,160,40))
        gradient.setColorAt(0.5, QtGui.QColor(40,160,220,80))
        gradient.setColorAt(0.55, QtGui.QColor(30,120,160,40))
        gradient.setColorAt(1.0, QtGui.QColor(0,0,0,0))
        p.fillRect(0, scan_y, w, 120, gradient)
        p.end()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NightVault — Login")
        self.setFixedSize(1280, 720)
        self.bg = ScanlineBackground(self)
        self.bg.setGeometry(0, 0, 1280, 720)
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 1280, 720)
        self.container.setStyleSheet("background: transparent; color: #dfefff;")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("NightVault")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:52px; color: #69e8ff; font-weight:900;")
        subtitle = QLabel("Hacker-vibe secure vault")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color:#9fdcff; font-size:13px;")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedWidth(460)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedWidth(460)
        btns = QHBoxLayout()
        self.login_btn = NeonButton("LOGIN")
        self.login_btn.clicked.connect(self.try_login)
        self.login_btn.set_ripple_callback(self._ripple_cb)
        self.register_btn = NeonButton("REGISTER")
        self.register_btn.clicked.connect(self.open_register)
        self.register_btn.set_ripple_callback(self._ripple_cb)
        btns.addWidget(self.login_btn)
        btns.addWidget(self.register_btn)
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.username, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(btns)
        layout.addStretch()
        footer = QLabel("XOR vault • Local only • Ask for AES upgrade")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color:#7fbfdc; font-size:12px;")
        layout.addWidget(footer)
        self.container.setLayout(layout)

    def _ripple_cb(self, x, y):
        # route to any overlay in parent if set
        pass

    def try_login(self):
        u = self.username.text().strip()
        p = self.password.text()
        if not u or not p:
            QMessageBox.warning(self, "Empty", "Please fill both fields.")
            return
        try:
            # preferred unwrap (vault_logic may provide wrapped vault key)
            if hasattr(logic, "unwrap_vault_key_with_password"):
                key = logic.unwrap_vault_key_with_password(u, p)
                if key:
                    self.open_dashboard(u, key)
                    return
            if logic.verify_user(u, p):
                # fallback derive a key to use in GUI (not used to decrypt vault if wrapped key exists)
                key = logic.derive_key(p) if hasattr(logic, "derive_key") else secrets.token_bytes(32)
                self.open_dashboard(u, key)
                return
        except Exception as e:
            print("login-check-error:", e)
        # failed: shake and alert
        self.shake()
        QMessageBox.critical(self, "Access Denied", "Wrong credentials.")

    def open_register(self):
        self.reg = RegisterWindow()
        self.reg.show()

    def open_dashboard(self, username, key_bytes):
        # create the enhanced dashboard, pass user and key, show; close login
        self.dashboard = MainWindow()
        # ensure overlay ripples work: set ripple callback for login buttons to dashboard overlay (if any)
        self.login_btn.set_ripple_callback(self.dashboard.ripple_overlay.add_ripple)
        self.register_btn.set_ripple_callback(self.dashboard.ripple_overlay.add_ripple)
        self.dashboard.start_with_user(username, key_bytes)
        self.dashboard.show()
        self.close()

    def shake(self):
        anim = QPropertyAnimation(self, b"geometry")
        orig = self.geometry()
        anim.setDuration(420)
        anim.setKeyValueAt(0, orig)
        anim.setKeyValueAt(0.2, QRect(orig.x()-14, orig.y(), orig.width(), orig.height()))
        anim.setKeyValueAt(0.4, QRect(orig.x()+14, orig.y(), orig.width(), orig.height()))
        anim.setKeyValueAt(0.6, QRect(orig.x()-8, orig.y(), orig.width(), orig.height()))
        anim.setKeyValueAt(0.8, QRect(orig.x()+6, orig.y(), orig.width(), orig.height()))
        anim.setKeyValueAt(1, orig)
        anim.start()

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NightVault — Register")
        self.setFixedSize(820,520)
        self.bg = ScanlineBackground(self)
        self.bg.setGeometry(0,0,820,520)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("Create your Vault")
        title.setStyleSheet("font-size:30px; color: #7ae6ff; font-weight:700;")
        self.un = QLineEdit(); self.un.setPlaceholderText("Choose username"); self.un.setFixedWidth(460)
        self.pw = QLineEdit(); self.pw.setPlaceholderText("Choose password"); self.pw.setEchoMode(QLineEdit.EchoMode.Password); self.pw.setFixedWidth(460)
        btn = NeonButton("Create Vault"); btn.clicked.connect(self.create_account)
        msg = QLabel("Password protects your XOR vault locally."); msg.setStyleSheet("color:#9fdcff;")
        layout.addStretch()
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.un, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.pw, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def create_account(self):
        username = self.un.text().strip()
        password = self.pw.text()
        if not username or not password:
            QMessageBox.warning(self, "Empty", "Please choose both username and password.")
            return
        ok, recovery = logic.create_user(username, password) if hasattr(logic, "create_user") else (False, None)
        if ok:
            QMessageBox.information(self, "Done", f"Vault created for {username}.\nSave recovery key: {recovery}")
            self.close()
        else:
            QMessageBox.warning(self, "Exists", "Username exists. Pick another.")

# ---------------- Sidebar used by dashboard ----------------
class Sidebar(QWidget):
    def __init__(self, parent, on_nav):
        super().__init__(parent)
        self.on_nav = on_nav
        self.setFixedWidth(220)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        title = QLabel("NightVault")
        title.setStyleSheet("font-weight:900; font-size:18px; color:" + THEMES[CURRENT_THEME]['accent'])
        layout.addWidget(title)
        layout.addSpacing(6)
        for label, key in [("Dashboard","dashboard"), ("Files","files"), ("Settings","settings"), ("About","about")]:
            b = NeonButton(label)
            b.clicked.connect(lambda _, k=key: self.on_nav(k))
            b.set_ripple_callback(lambda x,y: None)
            layout.addWidget(b)
        layout.addStretch()
        self.setLayout(layout)
        self.setStyleSheet("background: transparent;")

# ---------------- Entry point ----------------
def main():
    try:
        logic.init_db()
    except Exception:
        pass
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    # Start with original login window
    login = LoginWindow()
    set_app_icon(login)
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
