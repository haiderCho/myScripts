#!/usr/bin/env python3
"""
Secure File Encryption / Decryption Tool
Uses Fernet symmetric encryption.
"""

import argparse
import os
from pathlib import Path
from cryptography.fernet import Fernet


# ----------------------------- KEY HANDLING ----------------------------- #

def generate_key() -> bytes:
    """Generate a secure Fernet key."""
    return Fernet.generate_key()


def save_key(key: bytes, file_path: Path) -> None:
    """Save encryption key to the given file."""
    file_path.write_bytes(key)


def load_key(file_path: Path) -> bytes:
    """Load a key from a file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Key file not found: {file_path}")
    return file_path.read_bytes()


# ----------------------------- ENCRYPTION ------------------------------- #

def encrypt_file(key: bytes, file_path: Path, keep_original: bool = False) -> Path:
    """Encrypt a file and return the encrypted file path."""
    fernet = Fernet(key)

    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    data = file_path.read_bytes()
    encrypted = fernet.encrypt(data)

    encrypted_path = file_path.with_suffix(file_path.suffix + ".encrypted")
    encrypted_path.write_bytes(encrypted)

    if not keep_original:
        file_path.unlink()

    return encrypted_path


# ----------------------------- DECRYPTION ------------------------------- #

def decrypt_file(key: bytes, file_path: Path, keep_original: bool = False) -> Path:
    """Decrypt a file and return the decrypted file path."""
    fernet = Fernet(key)

    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    data = file_path.read_bytes()
    decrypted = fernet.decrypt(data)

    # Smart output: remove last suffix (".encrypted")
    output_path = file_path.with_suffix("")
    output_path.write_bytes(decrypted)

    if not keep_original:
        file_path.unlink()

    return output_path


# ----------------------------- CLI INTERFACE ---------------------------- #

def main():
    parser = argparse.ArgumentParser(
        description="🔐 Secure file encryption & decryption tool"
    )

    parser.add_argument("file", help="File to encrypt or decrypt")
    parser.add_argument("mode", choices=["encrypt", "decrypt"],
                        help="Choose encrypt or decrypt")
    parser.add_argument("--key", default="secret.key",
                        help="Custom key file path (default: secret.key)")
    parser.add_argument("--keep", action="store_true",
                        help="Keep original file (do not auto-delete)")

    args = parser.parse_args()

    file_path = Path(args.file)
    key_path = Path(args.key)

    try:
        if args.mode == "encrypt":
            key = generate_key()
            save_key(key, key_path)

            encrypted_file = encrypt_file(key, file_path, args.keep)

            print(f"\n✅ File encrypted successfully:")
            print(f"   🔑 Key saved to: {key_path}")
            print(f"   📁 Output file: {encrypted_file}\n")

        elif args.mode == "decrypt":
            key = load_key(key_path)

            decrypted_file = decrypt_file(key, file_path, args.keep)

            print(f"\n🔓 File decrypted successfully:")
            print(f"   📁 Output file: {decrypted_file}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
