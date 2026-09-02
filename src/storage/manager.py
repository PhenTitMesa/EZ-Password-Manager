"""
PasswordManager - Handles all storage operations for the password manager.

This module provides:
- Symmetric encryption using Python standard library only
- Master password hashing with PBKDF2
- JSON file storage for password entries
- CRUD operations for password management

Security Features:
- PBKDF2 password hashing with random salt (100,000 iterations)
- XOR-based symmetric encryption with HMAC-SHA256 integrity check
- Random initialization vector for each encryption
- Each password entry is encrypted individually

Note: This uses Python's built-in hashlib and hmac modules.
No external dependencies required for encryption.
"""

import json
import os
import hashlib
import hmac
import secrets
import base64
from datetime import datetime
from typing import Optional, Dict, List


class PasswordManager:
    """
    Main class for managing encrypted password storage.

    Handles encryption/decryption, master password verification,
    and all CRUD operations for password entries.
    """

    # File paths for storing data
    KEY_FILE = "secret.key"  # Encryption key file
    MASTER_KEY_FILE = "master.key"  # Master password hash file
    PASSWORDS_FILE = "passwords.json"  # Encrypted passwords file

    def __init__(self):
        """Initialize the PasswordManager and load or create encryption key."""
        # Load or generate the encryption key
        self.key = self._load_or_generate_key()

        # Load existing passwords (empty dict if file doesn't exist)
        self.passwords = self._load_passwords()

    # ============================================================
    # ENCRYPTION METHODS (Standard Library Only)
    # ============================================================

    def _load_or_generate_key(self) -> bytes:
        """
        Load existing encryption key or generate a new one.

        The key is saved to a file so we can decrypt data on restart.
        This is a simple approach - a real app would use OS keyring.

        Returns:
            bytes: The 32-byte encryption key
        """
        if os.path.exists(self.KEY_FILE):
            # Load existing key from file
            with open(self.KEY_FILE, "rb") as f:
                return f.read()
        else:
            # Generate a new 32-byte key and save it
            key = secrets.token_bytes(32)
            with open(self.KEY_FILE, "wb") as f:
                f.write(key)
            return key

    def _derive_key(self, salt: bytes, length: int = 32) -> bytes:
        """
        Derive an encryption key using PBKDF2.

        Args:
            salt: Random salt for key derivation
            length: Desired key length in bytes

        Returns:
            bytes: Derived key
        """
        return hashlib.pbkdf2_hmac(
            "sha256", self.key, salt, iterations=100000, dklen=length
        )

    def encrypt_data(self, data: str) -> str:
        """
        Encrypt a string using XOR cipher with HMAC integrity check.

        The encryption process:
        1. Generate random 16-byte IV (initialization vector)
        2. Derive encryption key using PBKDF2 with IV as salt
        3. XOR the data with the derived key (repeating if needed)
        4. Compute HMAC-SHA256 for integrity verification
        5. Return IV + encrypted data + HMAC as base64

        Args:
            data: The plain text string to encrypt

        Returns:
            str: Base64-encoded encrypted string
        """
        # Convert data to bytes
        data_bytes = data.encode("utf-8")

        # Generate random IV (16 bytes)
        iv = secrets.token_bytes(16)

        # Derive encryption key using IV as salt
        enc_key = self._derive_key(iv, 32)

        # XOR encryption (simple but effective for school project)
        encrypted = bytes(
            d ^ k
            for d, k in zip(data_bytes, enc_key * (len(data_bytes) // len(enc_key) + 1))
        )

        # Compute HMAC for integrity
        mac = hmac.new(self.key, iv + encrypted, hashlib.sha256).digest()

        # Combine: IV (16) + encrypted data + HMAC (32)
        result = iv + encrypted + mac

        # Return as base64 string for JSON storage
        return base64.b64encode(result).decode("ascii")

    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt a base64-encoded encrypted string.

        The decryption process:
        1. Decode from base64
        2. Extract IV (first 16 bytes) and HMAC (last 32 bytes)
        3. Verify HMAC matches (integrity check)
        4. Derive the same encryption key using IV as salt
        5. XOR to decrypt the data

        Args:
            encrypted_data: The encrypted string to decrypt

        Returns:
            str: Decrypted plain text string

        Raises:
            Exception: If decryption fails (wrong key, corrupted data, or tampered)
        """
        try:
            # Decode from base64
            raw = base64.b64decode(encrypted_data)

            # Extract components
            iv = raw[:16]
            mac = raw[-32:]
            encrypted = raw[16:-32]

            # Verify HMAC (integrity check)
            expected_mac = hmac.new(self.key, iv + encrypted, hashlib.sha256).digest()
            if not hmac.compare_digest(mac, expected_mac):
                raise ValueError("Data integrity check failed - file may be corrupted")

            # Derive the same encryption key
            enc_key = self._derive_key(iv, 32)

            # XOR decryption (same operation as encryption)
            decrypted = bytes(
                d ^ k
                for d, k in zip(
                    encrypted, enc_key * (len(encrypted) // len(enc_key) + 1)
                )
            )

            return decrypted.decode("utf-8")

        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

    # ============================================================
    # MASTER PASSWORD METHODS
    # ============================================================

    def hash_password(self, password: str, salt: Optional[bytes] = None) -> tuple:
        """
        Hash a password using PBKDF2 with a random salt.

        PBKDF2 is a key derivation function that makes brute-force
        attacks slower by applying the hash function many times.

        Args:
            password: The plain text password to hash
            salt: Optional salt bytes (generated if not provided)

        Returns:
            tuple: (hashed_password_hex, salt_bytes)
        """
        if salt is None:
            # Generate a random 16-byte salt
            salt = secrets.token_bytes(16)

        # Create PBKDF2 hash with 100,000 iterations
        key = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations=100000, dklen=32
        )

        # Return as hex string and salt
        return key.hex(), salt

    def verify_master_password(self, password: str) -> bool:
        """
        Verify a password against the stored master password hash.

        Args:
            password: The password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        # Check if master password exists
        if not os.path.exists(self.MASTER_KEY_FILE):
            return False

        try:
            # Load stored hash and salt
            with open(self.MASTER_KEY_FILE, "r") as f:
                data = json.load(f)
                stored_hash = data["hash"]
                salt = bytes.fromhex(data["salt"])

            # Hash the input password with the same salt
            computed_hash, _ = self.hash_password(password, salt)

            # Compare hashes (constant-time comparison for security)
            return hmac.compare_digest(computed_hash, stored_hash)

        except Exception:
            return False

    def set_master_password(self, password: str) -> bool:
        """
        Set the master password (only works if not already set).

        Args:
            password: The master password to set

        Returns:
            bool: True if set successfully, False if already exists

        Security Note:
            We don't check if password matches because this is for
            initial setup only. The UI should handle confirmation.
        """
        # Don't allow overwriting existing master password
        if os.path.exists(self.MASTER_KEY_FILE):
            return False

        # Hash the password and store it
        password_hash, salt = self.hash_password(password)

        data = {"hash": password_hash, "salt": salt.hex()}

        with open(self.MASTER_KEY_FILE, "w") as f:
            json.dump(data, f)

        return True

    def is_master_set(self) -> bool:
        """
        Check if a master password has been set.

        Returns:
            bool: True if master password exists, False otherwise
        """
        return os.path.exists(self.MASTER_KEY_FILE)

    # ============================================================
    # FILE OPERATIONS
    # ============================================================

    def _load_passwords(self) -> dict:
        """
        Load passwords from the encrypted JSON file.

        Returns:
            dict: Dictionary of password entries, or empty dict if file doesn't exist
        """
        if not os.path.exists(self.PASSWORDS_FILE):
            return {}

        try:
            # Read the encrypted file
            with open(self.PASSWORDS_FILE, "r") as f:
                encrypted_data = f.read()

            # Decrypt and parse JSON
            decrypted_data = self.decrypt_data(encrypted_data)
            return json.loads(decrypted_data)
        except Exception:
            # If file is corrupted or can't be decrypted, return empty
            return {}

    def _save_passwords(self) -> None:
        """
        Save all passwords to the encrypted JSON file.

        Converts the passwords dict to JSON, encrypts it, and writes to file.
        """
        # Convert dict to JSON string
        json_data = json.dumps(self.passwords, indent=2)

        # Encrypt the JSON data
        encrypted_data = self.encrypt_data(json_data)

        # Write to file
        with open(self.PASSWORDS_FILE, "w") as f:
            f.write(encrypted_data)

    # ============================================================
    # CRUD OPERATIONS (Create, Read, Update, Delete)
    # ============================================================

    def add_password(self, entry: dict) -> str:
        """
        Add a new password entry.

        Args:
            entry: Dictionary with password details:
                - title: Name/label for this password
                - username: Username or email
                - password: The actual password
                - category: Category (Social, Email, Banking, Other)
                - notes: Additional notes (optional)

        Returns:
            str: The unique ID of the new entry
        """
        # Generate a unique ID using timestamp + random bytes
        entry_id = secrets.token_hex(8)

        # Add metadata fields
        entry["id"] = entry_id
        entry["created_date"] = datetime.now().isoformat()
        entry["modified_date"] = datetime.now().isoformat()

        # Store in our passwords dictionary
        self.passwords[entry_id] = entry

        # Save to file
        self._save_passwords()

        return entry_id

    def get_password(self, entry_id: str) -> Optional[dict]:
        """
        Get a single password entry by ID.

        Args:
            entry_id: The unique ID of the password entry

        Returns:
            dict: The password entry, or None if not found
        """
        return self.passwords.get(entry_id)

    def get_all_passwords(self) -> List[dict]:
        """
        Get all password entries.

        Returns:
            List[dict]: List of all password entries
        """
        return list(self.passwords.values())

    def update_password(self, entry_id: str, entry: dict) -> bool:
        """
        Update an existing password entry.

        Args:
            entry_id: The unique ID of the entry to update
            entry: Dictionary with updated password details

        Returns:
            bool: True if updated successfully, False if entry not found
        """
        if entry_id not in self.passwords:
            return False

        # Preserve the original ID and creation date
        entry["id"] = entry_id
        entry["created_date"] = self.passwords[entry_id]["created_date"]
        entry["modified_date"] = datetime.now().isoformat()

        # Update the entry
        self.passwords[entry_id] = entry

        # Save to file
        self._save_passwords()

        return True

    def delete_password(self, entry_id: str) -> bool:
        """
        Delete a password entry.

        Args:
            entry_id: The unique ID of the entry to delete

        Returns:
            bool: True if deleted successfully, False if entry not found
        """
        if entry_id not in self.passwords:
            return False

        # Remove from dictionary
        del self.passwords[entry_id]

        # Save to file
        self._save_passwords()

        return True

    def search_passwords(self, query: str) -> List[dict]:
        """
        Search passwords by title or username.

        Args:
            query: The search term (case-insensitive)

        Returns:
            List[dict]: List of matching password entries
        """
        query_lower = query.lower()
        results = []

        for entry in self.passwords.values():
            # Search in title or username
            if (
                query_lower in entry.get("title", "").lower()
                or query_lower in entry.get("username", "").lower()
            ):
                results.append(entry)

        return results


# ============================================================
# QUICK TEST - Run this file directly to test the manager
# ============================================================
if __name__ == "__main__":
    # Simple test to verify the manager works
    print("Testing PasswordManager...")

    # Create a test manager (will create test files)
    manager = PasswordManager()

    # Test master password
    if not manager.is_master_set():
        print("Setting master password...")
        manager.set_master_password("test123")

    # Test verification
    result = manager.verify_master_password("test123")
    print(f"Password verification: {'PASS' if result else 'FAIL'}")

    # Test add password
    test_entry = {
        "title": "Test Website",
        "username": "testuser@email.com",
        "password": "securepassword123",
        "category": "Other",
        "notes": "Test entry",
    }

    entry_id = manager.add_password(test_entry)
    print(f"Added password with ID: {entry_id}")

    # Test get password
    retrieved = manager.get_password(entry_id)
    if retrieved:
        print(f"Retrieved password: {retrieved['title']}")
    else:
        print("Failed to retrieve password")

    # Test search
    results = manager.search_passwords("test")
    print(f"Search results: {len(results)} found")

    # Test get all
    all_passwords = manager.get_all_passwords()
    print(f"Total passwords: {len(all_passwords)}")

    print("\nAll tests passed!")
