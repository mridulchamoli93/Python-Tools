# vault_logic.py
# NightVault backend logic — safe migration + compatibility
# (Updated: defensive ensure_columns_exist and retry on insert)

import hashlib
import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from datetime import datetime
import secrets
import json
import zipfile
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

DB_PATH = Path("vault_users.db")
VAULT_ROOT = Path("vaults")
VAULT_ROOT.mkdir(parents=True, exist_ok=True)
TOKENS_PATH = Path("trusted_tokens.json")
if not TOKENS_PATH.exists():
    TOKENS_PATH.write_text(json.dumps({}))


# ---------------- Utilities / KDF ----------------
def _kdf(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    if not isinstance(salt, (bytes, bytearray)):
        salt = bytes(salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def xor_encrypt_bytes(data: bytes, key: bytes) -> bytes:
    out = bytearray(len(data))
    keylen = len(key)
    for i, b in enumerate(data):
        out[i] = b ^ key[i % keylen]
    return bytes(out)


# ---------------- DB initialization + migration helpers ----------------
def _get_columns() -> List[str]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(users)")
    cols = [r[1] for r in cur.fetchall()]
    con.close()
    return cols


def ensure_users_table_exists():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cur.fetchone():
        cur.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                pass_hash TEXT,
                salt BLOB,
                vault_key_wrapped BLOB,
                recovery_key_wrapped BLOB,
                last_login TEXT
            )
        """)
        con.commit()
    con.close()


def ensure_columns_exist():
    """
    Add missing modern columns to the users table if the DB was created with an older schema.
    Safe to call multiple times.
    """
    ensure_users_table_exists()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(users)")
    existing = {r[1] for r in cur.fetchall()}  # set of column names
    required = {
        "salt": "BLOB",
        "vault_key_wrapped": "BLOB",
        "recovery_key_wrapped": "BLOB",
        "last_login": "TEXT"
    }
    for name, typ in required.items():
        if name not in existing:
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {name} {typ}")
            except Exception:
                # If something goes wrong, ignore and continue (best effort)
                pass
    con.commit()
    con.close()


def init_db() -> None:
    """
    Public init_db: create table if missing and ensure columns exist.
    """
    ensure_users_table_exists()
    ensure_columns_exist()


# ---------------- user helpers ----------------
def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(username: str, password: str) -> Tuple[bool, Optional[str]]:
    """
    Create a new user in the modern schema. Returns (True, recovery_token) if created,
    (False, None) if username already exists.
    This function defensively ensures the required columns exist and retries the insert
    if the schema was older.
    """
    ensure_columns_exist()
    salt = secrets.token_bytes(16)
    pass_hash = _hash_password(password)
    vault_key = Fernet.generate_key()
    pwd_k = _kdf(password, salt)
    f_pwd = Fernet(pwd_k)
    wrapped_for_pwd = f_pwd.encrypt(vault_key)
    recovery_token = secrets.token_urlsafe(24)
    rec_k = _kdf(recovery_token, salt)
    f_rec = Fernet(rec_k)
    wrapped_for_rec = f_rec.encrypt(vault_key)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, pass_hash, salt, vault_key_wrapped, recovery_key_wrapped, last_login) VALUES (?, ?, ?, ?, ?, ?)",
            (username, pass_hash, sqlite3.Binary(salt), sqlite3.Binary(wrapped_for_pwd), sqlite3.Binary(wrapped_for_rec), None)
        )
        con.commit()
        con.close()
        (VAULT_ROOT / username).mkdir(parents=True, exist_ok=True)
        return True, recovery_token
    except sqlite3.OperationalError as e:
        # Possibly missing columns — try to ensure then retry once
        con.close()
        try:
            ensure_columns_exist()
            con2 = sqlite3.connect(DB_PATH)
            cur2 = con2.cursor()
            cur2.execute(
                "INSERT INTO users (username, pass_hash, salt, vault_key_wrapped, recovery_key_wrapped, last_login) VALUES (?, ?, ?, ?, ?, ?)",
                (username, pass_hash, sqlite3.Binary(salt), sqlite3.Binary(wrapped_for_pwd), sqlite3.Binary(wrapped_for_rec), None)
            )
            con2.commit()
            con2.close()
            (VAULT_ROOT / username).mkdir(parents=True, exist_ok=True)
            return True, recovery_token
        except sqlite3.IntegrityError:
            return False, None
        except Exception:
            # Give up and return False (but don't crash)
            return False, None
    except sqlite3.IntegrityError:
        con.close()
        return False, None
    except Exception:
        con.close()
        return False, None


def verify_user(username: str, password: str) -> bool:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("SELECT pass_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        con.close()
        if not row:
            return False
        stored = row[0]
        return stored == _hash_password(password)
    except Exception:
        con.close()
        return False


def load_user_wraps(username: str) -> Optional[Dict]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("PRAGMA table_info(users)")
        cols = [r[1] for r in cur.fetchall()]
        select_cols = ["pass_hash"]
        for c in ("salt", "vault_key_wrapped", "recovery_key_wrapped", "last_login"):
            if c in cols:
                select_cols.append(c)
        cols_sql = ", ".join(select_cols)
        cur.execute(f"SELECT {cols_sql} FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        con.close()
        if not row:
            return None
        res = {}
        for idx, col in enumerate(select_cols):
            res[col] = row[idx]
        return res
    except Exception:
        con.close()
        return None


def update_last_login(username: str) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("PRAGMA table_info(users)")
        cols = [r[1] for r in cur.fetchall()]
        if "last_login" not in cols:
            try:
                cur.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
            except Exception:
                pass
        cur.execute("UPDATE users SET last_login = ? WHERE username = ?", (datetime.utcnow().isoformat(), username))
        con.commit()
    except Exception:
        pass
    finally:
        con.close()


# ---------------- Key unwrap ----------------
def unwrap_vault_key_with_password(username: str, password: str) -> Optional[bytes]:
    info = load_user_wraps(username)
    if not info:
        return None
    salt = info.get("salt")
    wrapped = info.get("vault_key_wrapped")
    if not salt or not wrapped:
        return None
    try:
        k = _kdf(password, salt)
        f = Fernet(k)
        key = f.decrypt(wrapped)
        update_last_login(username)
        return key
    except Exception:
        return None


def unwrap_vault_key_with_recovery(username: str, recovery_token: str) -> Optional[bytes]:
    info = load_user_wraps(username)
    if not info:
        return None
    salt = info.get("salt")
    wrapped = info.get("recovery_key_wrapped")
    if not salt or not wrapped:
        return None
    try:
        k = _kdf(recovery_token, salt)
        f = Fernet(k)
        key = f.decrypt(wrapped)
        return key
    except Exception:
        return None


def reset_password_with_recovery(username: str, new_password: str, recovery_token: str) -> bool:
    key = unwrap_vault_key_with_recovery(username, recovery_token)
    if not key:
        return False
    info = load_user_wraps(username)
    salt = info.get("salt") or secrets.token_bytes(16)
    new_k = _kdf(new_password, salt)
    f_new = Fernet(new_k)
    wrapped_new = f_new.encrypt(key)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("UPDATE users SET pass_hash = ?, vault_key_wrapped = ? WHERE username = ?",
                    (_hash_password(new_password), sqlite3.Binary(wrapped_new), username))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()


# ---------------- Trusted tokens ----------------
def _load_tokens() -> dict:
    try:
        return json.loads(TOKENS_PATH.read_text())
    except Exception:
        return {}


def _save_tokens(d: dict):
    TOKENS_PATH.write_text(json.dumps(d))


def create_trust_token(username: str) -> str:
    token = secrets.token_urlsafe(32)
    d = _load_tokens()
    d[username] = token
    _save_tokens(d)
    return token


def check_trust_token(username: str, token: str) -> bool:
    d = _load_tokens()
    return d.get(username) == token


def get_trusted_token_for_user(username: str) -> Optional[str]:
    d = _load_tokens()
    return d.get(username)


# ---------------- Vault file operations ----------------
def user_vault_dir(username: str) -> Path:
    d = VAULT_ROOT / username
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_file_with_vaultkey(username: str, vault_key: bytes, src_path: str) -> str:
    fernet = Fernet(vault_key)
    src = Path(src_path)
    data = src.read_bytes()
    token = fernet.encrypt(data)
    name_bytes = src.name.encode("utf-8")
    header = len(name_bytes).to_bytes(2, "big") + name_bytes
    out = header + token
    out_name = f"{src.name}.nv"
    dst = user_vault_dir(username) / out_name
    dst.write_bytes(out)
    return out_name


def save_encrypted_file(username: str, password: str, src_path: str) -> str:
    key = derive_key(password)
    src = Path(src_path)
    data = src.read_bytes()
    enc = xor_encrypt_bytes(data, key)
    name_bytes = src.name.encode("utf-8")
    header = len(name_bytes).to_bytes(2, "big") + name_bytes
    out = header + enc
    out_name = f"{src.name}.nv"
    dst = user_vault_dir(username) / out_name
    dst.write_bytes(out)
    return out_name


def list_vault_files(username: str) -> List[str]:
    d = user_vault_dir(username)
    files = []
    for p in sorted(d.iterdir()):
        if p.is_file():
            files.append(p.name)
    return files


def read_encrypted_file(username: str, filename: str) -> Tuple[str, bytes]:
    src = user_vault_dir(username) / filename
    raw = src.read_bytes()
    name_len = int.from_bytes(raw[:2], "big")
    orig_name = raw[2:2 + name_len].decode("utf-8")
    payload = raw[2 + name_len:]
    return orig_name, payload


def decrypt_payload(vault_key: bytes, payload: bytes) -> bytes:
    f = Fernet(vault_key)
    return f.decrypt(payload)


def delete_vault_file(username: str, filename: str) -> bool:
    src = user_vault_dir(username) / filename
    if src.exists():
        src.unlink()
        return True
    return False


# ---------------- Analytics & export ----------------
def vault_analytics(username: str, vault_key: bytes) -> dict:
    files = list_vault_files(username)
    total_bytes = 0
    last_upload = None
    types = {}
    for fn in files:
        p = user_vault_dir(username) / fn
        try:
            total_bytes += p.stat().st_size
            ext = Path(fn).suffix.lower()
            types[ext] = types.get(ext, 0) + 1
            m = datetime.fromtimestamp(p.stat().st_mtime)
            if not last_upload or m > last_upload:
                last_upload = m
        except Exception:
            continue
    return {
        "file_count": len(files),
        "total_size_bytes": total_bytes,
        "last_upload": (last_upload.isoformat() if last_upload else None),
        "type_distribution": types
    }


def export_vault_as_encrypted_zip(username: str, vault_key: bytes, out_path: str) -> str:
    tmp_zip = user_vault_dir(username) / "__export_tmp__.zip"
    with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for fn in list_vault_files(username):
            zf.write(user_vault_dir(username) / fn, arcname=fn)
    data = tmp_zip.read_bytes()
    f = Fernet(vault_key)
    enc = f.encrypt(data)
    dst = Path(out_path)
    dst.write_bytes(enc)
    try:
        tmp_zip.unlink()
    except Exception:
        pass
    return str(dst)
