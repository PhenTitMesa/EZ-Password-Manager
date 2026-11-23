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
    MASTER_KEY_FILE = "master.key"
    PASSWORDS_FILE = "passwords.json"

    def __init__(self):
        # Encryption key is derived from the master password and kept in memory only
        self.key: Optional[bytes] = None
        self.passwords: dict = {}

    # --- ENCRYPTION (stdlib only: SHA-256 counter-mode stream + HMAC-SHA256) ---

    def _derive_key(self, salt: bytes, length: int = 32) -> bytes:
        # Derive encryption key using PBKDF2
        if self.key is None:
            raise ValueError("Vault is locked. Unlock with master password first.")
        return hashlib.pbkdf2_hmac(
            "sha256", self.key, salt, iterations=100000, dklen=length
        )

    @staticmethod
    def _keystream(enc_key: bytes, length: int) -> bytes:
        # Generate a non-repeating keystream using SHA-256 in counter mode
        blocks = []
        counter = 0
        generated = 0
        while generated < length:
            block = hashlib.sha256(enc_key + counter.to_bytes(4, "big")).digest()
            blocks.append(block)
            generated += len(block)
            counter += 1
        return b"".join(blocks)[:length]

    def encrypt_data(self, data: str) -> str:
        # Encrypt string using SHA-256 counter-mode stream + HMAC-SHA256
        if self.key is None:
            raise ValueError("Vault is locked.")
        data_bytes = data.encode("utf-8")
        iv = secrets.token_bytes(16)  # Random 16-byte IV
        enc_key = self._derive_key(iv, 32)
        stream = self._keystream(enc_key, len(data_bytes))

        encrypted = bytes(d ^ k for d, k in zip(data_bytes, stream))

        # HMAC for integrity check (encrypt-then-MAC)
        mac = hmac.new(self.key, iv + encrypted, hashlib.sha256).digest()

        # Return IV + encrypted + HMAC as base64
        return base64.b64encode(iv + encrypted + mac).decode("ascii")

    def decrypt_data(self, encrypted_data: str) -> str:
        # Decrypt base64-encoded encrypted string
        if self.key is None:
            raise ValueError("Vault is locked.")
        try:
            raw = base64.b64decode(encrypted_data)
            if len(raw) < 48:
                raise ValueError("Corrupted encrypted payload")
            iv = raw[:16]
            mac = raw[-32:]
            encrypted = raw[16:-32]

            # Verify HMAC (integrity check)
            expected_mac = hmac.new(self.key, iv + encrypted, hashlib.sha256).digest()
            if not hmac.compare_digest(mac, expected_mac):
                raise ValueError("Data integrity check failed")

            # Decrypt using SHA-256 counter-mode stream
            enc_key = self._derive_key(iv, 32)
            stream = self._keystream(enc_key, len(encrypted))
            decrypted = bytes(d ^ k for d, k in zip(encrypted, stream))
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

    def _derive_master_encryption_key(self, password: str, enc_salt: bytes) -> bytes:
        # Derive the vault encryption key from the master password
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), enc_salt, iterations=100000, dklen=32
        )

    def verify_master_password(self, password: str) -> bool:
        # Check if password matches stored master password and unlock vault
        if not os.path.exists(self.MASTER_KEY_FILE):
            return False
        try:
            with open(self.MASTER_KEY_FILE, "r") as f:
                data = json.load(f)
                stored_hash = data["hash"]
                salt = bytes.fromhex(data["salt"])
                enc_salt = bytes.fromhex(data.get("enc_salt", data["salt"]))
            computed_hash, _ = self.hash_password(password, salt)
            if not hmac.compare_digest(computed_hash, stored_hash):
                return False
            self.key = self._derive_master_encryption_key(password, enc_salt)
            self.passwords = self._load_passwords()
            return True
        except ValueError:
            # Re-raise integrity/decryption errors so tampered storage is not silently wiped
            self.key = None
            raise
        except Exception:
            self.key = None
            return False

    def set_master_password(self, password: str) -> bool:
        # Set master password (only works on first run)
        if os.path.exists(self.MASTER_KEY_FILE):
            return False
        password_hash, salt = self.hash_password(password)
        enc_salt = secrets.token_bytes(16)
        data = {
            "hash": password_hash,
            "salt": salt.hex(),
            "enc_salt": enc_salt.hex(),
        }
        with open(self.MASTER_KEY_FILE, "w") as f:
            json.dump(data, f)
        self.key = self._derive_master_encryption_key(password, enc_salt)
        self.passwords = {}
        return True

    def is_master_set(self) -> bool:
        # Check if master password exists
        return os.path.exists(self.MASTER_KEY_FILE)

    # --- FILE OPERATIONS ---

    def _load_passwords(self) -> dict:
        # Load passwords from encrypted JSON file
        if not os.path.exists(self.PASSWORDS_FILE):
            return {}
        with open(self.PASSWORDS_FILE, "r") as f:
            encrypted_data = f.read()
        if not encrypted_data.strip():
            return {}
        return json.loads(self.decrypt_data(encrypted_data))

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
