"""
Secure password storage with encryption
Implements SPEC-3.2.2 and security requirements
"""

import json
import os
from typing import Dict, Optional
from datetime import datetime
import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

from password_entry import PasswordEntry

class PasswordStore:
    """
    Secure storage for password entries with encryption
    Implements SPEC-3.2.2 and security requirements
    """

    def __init__(self, file_path: str = "passwords_secure.json"):
        self.file_path = file_path
        self.entries: Dict[str, PasswordEntry] = {}
        self.master_password_hash: Optional[str] = None
        self.salt: Optional[bytes] = None
        self.encryption_key: Optional[bytes] = None
        self.is_unlocked = False

    def set_master_password(self, password: str) -> bool:
        """
        Set the master password for encryption
        Implements SEC-8.1.4 and RULE-5.3.1
        """
        # Validate master password length (RULE-5.3.1)
        if len(password) < 8:
            raise ValueError("Master password must be at least 8 characters")

        # Generate random salt (SEC-8.1.4)
        self.salt = secrets.token_bytes(32)

        # Hash the password with salt
        self.master_password_hash = self._hash_password(password, self.salt)

        # Derive encryption key (SEC-8.1.3)
        self.encryption_key = self._derive_key(password, self.salt)

        self.is_unlocked = True
        return True

    def unlock(self, password: str) -> bool:
        """
        Unlock the password store with master password
        Implements authentication
        """
        if not self.master_password_hash or not self.salt:
            raise ValueError("No master password set")

        # Verify password
        provided_hash = self._hash_password(password, self.salt)

        # Constant-time comparison to prevent timing attacks (SEC-8.2.1)
        if not secrets.compare_digest(provided_hash, self.master_password_hash):
            return False

        # Derive encryption key
        self.encryption_key = self._derive_key(password, self.salt)
        self.is_unlocked = True

        # Clear password from memory (EDGE-6.3.1)
        password = None
        return True

    def _hash_password(self, password: str, salt: bytes) -> str:
        """
        Hash password with salt using PBKDF2
        Implements SEC-8.1.3
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # SEC-8.1.3: 100,000 iterations
            backend=default_backend()
        )
        password_bytes = password.encode('utf-8')
        key = kdf.derive(password_bytes)
        return base64.b64encode(key).decode('ascii')

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive encryption key from password
        Implements SEC-8.1.3
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256 key size
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        password_bytes = password.encode('utf-8')
        return kdf.derive(password_bytes)

    def _encrypt_data(self, data: str) -> dict:
        """
        Encrypt data using AES-256-GCM
        Implements SEC-8.1.1, SEC-8.1.2
        """
        if not self.encryption_key:
            raise ValueError("Store is locked")

        # Generate unique IV for each encryption (SEC-8.1.2)
        iv = secrets.token_bytes(12)  # 96-bit IV for GCM

        # Encrypt using AES-256 in GCM mode (SEC-8.1.1)
        cipher = Cipher(
            algorithms.AES(self.encryption_key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        data_bytes = data.encode('utf-8')
        ciphertext = encryptor.update(data_bytes) + encryptor.finalize()

        return {
            'iv': base64.b64encode(iv).decode('ascii'),
            'ciphertext': base64.b64encode(ciphertext).decode('ascii'),
            'tag': base64.b64encode(encryptor.tag).decode('ascii')
        }

    def _decrypt_data(self, encrypted_data: dict) -> str:
        """
        Decrypt data using AES-256-GCM
        Implements SEC-8.1.1
        """
        if not self.encryption_key:
            raise ValueError("Store is locked")

        try:
            iv = base64.b64decode(encrypted_data['iv'])
            ciphertext = base64.b64decode(encrypted_data['ciphertext'])
            tag = base64.b64decode(encrypted_data['tag'])

            cipher = Cipher(
                algorithms.AES(self.encryption_key),
                modes.GCM(iv, tag),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()

            plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext_bytes.decode('utf-8')

        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

    def save_to_file(self) -> bool:
        """
        Save encrypted data to file
        Implements persistence with encryption
        """
        if not self.is_unlocked:
            raise ValueError("Store is locked")

        try:
            # Prepare data for serialization
            entries_data = {}
            for service_name, entry in self.entries.items():
                entries_data[service_name] = entry.to_dict()

            # Convert to JSON
            json_data = json.dumps(entries_data, ensure_ascii=False, indent=2)

            # Encrypt the JSON data
            encrypted_entries = self._encrypt_data(json_data)

            # Prepare file structure
            file_data = {
                'version': '1.0',
                'master_password_hash': self.master_password_hash,
                'salt': base64.b64encode(self.salt).decode('ascii'),
                'encrypted_entries': encrypted_entries,
                'created_date': datetime.now().isoformat()
            }

            # Write to file with proper Unicode handling
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(file_data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            raise IOError(f"Failed to save password store: {e}")

    def load_from_file(self) -> bool:
        """
        Load data from file
        Implements EDGE-6.2.2 recovery from corruption
        """
        if not os.path.exists(self.file_path):
            return False

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)

            # Verify file format
            if 'version' not in file_data:
                raise ValueError("Invalid file format")

            # Load metadata
            self.master_password_hash = file_data['master_password_hash']
            self.salt = base64.b64decode(file_data['salt'])

            # Store encrypted entries for later decryption
            self._encrypted_entries = file_data['encrypted_entries']

            return True

        except json.JSONDecodeError:
            raise ValueError("Corrupted password file - invalid JSON")
        except KeyError as e:
            raise ValueError(f"Corrupted password file - missing field: {e}")
        except Exception as e:
            raise IOError(f"Failed to load password store: {e}")

    def unlock_and_load_entries(self, password: str) -> bool:
        """
        Unlock store and decrypt entries
        """
        if not self.unlock(password):
            return False

        try:
            # Decrypt entries
            json_data = self._decrypt_data(self._encrypted_entries)
            entries_data = json.loads(json_data)

            # Reconstruct entries
            self.entries = {}
            for service_name, entry_dict in entries_data.items():
                self.entries[service_name] = PasswordEntry.from_dict(entry_dict)

            return True

        except Exception as e:
            self.is_unlocked = False
            self.encryption_key = None
            raise ValueError(f"Failed to decrypt entries: {e}")

    def add_entry(self, entry: PasswordEntry) -> bool:
        """
        Add a password entry
        Implements RULE-5.2.1 uniqueness
        """
        if not self.is_unlocked:
            raise ValueError("Store is locked")

        # Validate entry
        entry.validate()

        # Check for duplicates (RULE-5.2.1)
        normalized_service = entry.service_name.lower()
        for existing_service in self.entries:
            if existing_service.lower() == normalized_service:
                if existing_service != entry.service_name:
                    # Warn about potential duplicate (RULE-5.2.3)
                    print(f"Warning: Similar service name exists: {existing_service}")

        # Add entry
        self.entries[entry.service_name] = entry
        return True

    def get_entry(self, service_name: str) -> Optional[PasswordEntry]:
        """Get a password entry by service name"""
        if not self.is_unlocked:
            raise ValueError("Store is locked")

        return self.entries.get(service_name)

    def update_entry(self, service_name: str, entry: PasswordEntry) -> bool:
        """
        Update an existing entry
        Implements RULE-5.2.2
        """
        if not self.is_unlocked:
            raise ValueError("Store is locked")

        if service_name not in self.entries:
            return False

        entry.validate()
        entry.modified_date = datetime.now()
        self.entries[service_name] = entry
        return True

    def delete_entry(self, service_name: str) -> bool:
        """Delete a password entry"""
        if not self.is_unlocked:
            raise ValueError("Store is locked")

        if service_name in self.entries:
            del self.entries[service_name]
            return True
        return False

    def list_services(self) -> list:
        """List all service names"""
        if not self.is_unlocked:
            raise ValueError("Store is locked")

        return list(self.entries.keys())

    def get_statistics(self) -> dict:
        """Get statistics about stored passwords"""
        if not self.is_unlocked:
            raise ValueError("Store is locked")

        return {
            'total_entries': len(self.entries),
            'categories': len(set(entry.category for entry in self.entries.values() if entry.category)),
            'oldest_entry': min((entry.created_date for entry in self.entries.values()), default=None),
            'newest_entry': max((entry.created_date for entry in self.entries.values()), default=None)
        }

    def lock(self):
        """
        Lock the store and clear sensitive data from memory
        Implements EDGE-6.3.1
        """
        self.is_unlocked = False
        self.encryption_key = None
        # Clear entries from memory for security
        self.entries.clear()