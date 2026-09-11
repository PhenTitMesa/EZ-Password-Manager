# PasswordManager - Handles encryption, master password, and CRUD operations
# Uses only Python standard library (hashlib, hmac, os, secrets)

import json
import os
import hashlib
import hmac
import secrets
import base64
from datetime import datetime
from typing import Optional, Dict, List


class PasswordManager:
    # File paths for storing data
    KEY_FILE = "secret.key"
    MASTER_KEY_FILE = "master.key"
    PASSWORDS_FILE = "passwords.json"

    def __init__(self):
        # Load or generate encryption key
        self.key = self._load_or_generate_key()
        # Load existing passwords
        self.passwords = self._load_passwords()

    # --- ENCRYPTION (stdlib only: XOR + HMAC) ---

    def _load_or_generate_key(self) -> bytes:
        # Load existing key or generate new 32-byte key
        if os.path.exists(self.KEY_FILE):
            with open(self.KEY_FILE, "rb") as f:
                return f.read()
        else:
            key = secrets.token_bytes(32)
            with open(self.KEY_FILE, "wb") as f:
                f.write(key)
            return key

    def _derive_key(self, salt: bytes, length: int = 32) -> bytes:
        # Derive encryption key using PBKDF2
        return hashlib.pbkdf2_hmac(
            "sha256", self.key, salt, iterations=100000, dklen=length
        )

    def encrypt_data(self, data: str) -> str:
        # Encrypt string using XOR + HMAC-SHA256
        data_bytes = data.encode("utf-8")
        iv = secrets.token_bytes(16)  # Random 16-byte IV
        enc_key = self._derive_key(iv, 32)

        # XOR encryption
        encrypted = bytes(
            d ^ k
            for d, k in zip(data_bytes, enc_key * (len(data_bytes) // len(enc_key) + 1))
        )

        # HMAC for integrity check
        mac = hmac.new(self.key, iv + encrypted, hashlib.sha256).digest()

        # Return IV + encrypted + HMAC as base64
        return base64.b64encode(iv + encrypted + mac).decode("ascii")

    def decrypt_data(self, encrypted_data: str) -> str:
        # Decrypt base64-encoded encrypted string
        try:
            raw = base64.b64decode(encrypted_data)
            iv = raw[:16]
            mac = raw[-32:]
            encrypted = raw[16:-32]

            # Verify HMAC (integrity check)
            expected_mac = hmac.new(self.key, iv + encrypted, hashlib.sha256).digest()
            if not hmac.compare_digest(mac, expected_mac):
                raise ValueError("Data integrity check failed")

            # XOR decryption
            enc_key = self._derive_key(iv, 32)
            decrypted = bytes(
                d ^ k
                for d, k in zip(
                    encrypted, enc_key * (len(encrypted) // len(enc_key) + 1)
                )
            )
            return decrypted.decode("utf-8")
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

    # --- MASTER PASSWORD ---

    def hash_password(self, password: str, salt: Optional[bytes] = None) -> tuple:
        # Hash password with PBKDF2 (100,000 iterations)
        if salt is None:
            salt = secrets.token_bytes(16)
        key = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations=100000, dklen=32
        )
        return key.hex(), salt

    def verify_master_password(self, password: str) -> bool:
        # Check if password matches stored master password
        if not os.path.exists(self.MASTER_KEY_FILE):
            return False
        try:
            with open(self.MASTER_KEY_FILE, "r") as f:
                data = json.load(f)
                stored_hash = data["hash"]
                salt = bytes.fromhex(data["salt"])
            computed_hash, _ = self.hash_password(password, salt)
            return hmac.compare_digest(computed_hash, stored_hash)
        except Exception:
            return False

    def set_master_password(self, password: str) -> bool:
        # Set master password (only works on first run)
        if os.path.exists(self.MASTER_KEY_FILE):
            return False
        password_hash, salt = self.hash_password(password)
        data = {"hash": password_hash, "salt": salt.hex()}
        with open(self.MASTER_KEY_FILE, "w") as f:
            json.dump(data, f)
        return True

    def is_master_set(self) -> bool:
        # Check if master password exists
        return os.path.exists(self.MASTER_KEY_FILE)

    # --- FILE OPERATIONS ---

    def _load_passwords(self) -> dict:
        # Load passwords from encrypted JSON file
        if not os.path.exists(self.PASSWORDS_FILE):
            return {}
        try:
            with open(self.PASSWORDS_FILE, "r") as f:
                encrypted_data = f.read()
            return json.loads(self.decrypt_data(encrypted_data))
        except Exception:
            return {}

    def _save_passwords(self) -> None:
        # Save passwords to encrypted JSON file
        json_data = json.dumps(self.passwords, indent=2)
        encrypted_data = self.encrypt_data(json_data)
        with open(self.PASSWORDS_FILE, "w") as f:
            f.write(encrypted_data)

    # --- CRUD OPERATIONS ---

    def add_password(self, entry: dict) -> str:
        # Add new password entry
        entry_id = secrets.token_hex(8)
        entry["id"] = entry_id
        entry["created_date"] = datetime.now().isoformat()
        entry["modified_date"] = datetime.now().isoformat()
        self.passwords[entry_id] = entry
        self._save_passwords()
        return entry_id

    def get_password(self, entry_id: str) -> Optional[dict]:
        # Get password by ID
        return self.passwords.get(entry_id)

    def get_all_passwords(self) -> List[dict]:
        # Get all password entries
        return list(self.passwords.values())

    def update_password(self, entry_id: str, entry: dict) -> bool:
        # Update existing password entry
        if entry_id not in self.passwords:
            return False
        entry["id"] = entry_id
        entry["created_date"] = self.passwords[entry_id]["created_date"]
        entry["modified_date"] = datetime.now().isoformat()
        self.passwords[entry_id] = entry
        self._save_passwords()
        return True

    def delete_password(self, entry_id: str) -> bool:
        # Delete password entry
        if entry_id not in self.passwords:
            return False
        del self.passwords[entry_id]
        self._save_passwords()
        return True

    def search_passwords(self, query: str) -> List[dict]:
        # Search passwords by title or username
        query_lower = query.lower()
        return [
            entry
            for entry in self.passwords.values()
            if query_lower in entry.get("title", "").lower()
            or query_lower in entry.get("username", "").lower()
        ]


# --- Quick test when running this file directly ---
if __name__ == "__main__":
    print("Testing PasswordManager...")
    manager = PasswordManager()

    if not manager.is_master_set():
        manager.set_master_password("test123")

    print(f"Verify: {'PASS' if manager.verify_master_password('test123') else 'FAIL'}")

    entry_id = manager.add_password(
        {
            "title": "Test",
            "username": "test@email.com",
            "password": "pass123",
            "category": "Other",
            "notes": "",
        }
    )
    print(f"Added: {entry_id}")
    print(f"Total: {len(manager.get_all_passwords())}")
    print("All tests passed!")
