"""Fernet encryption helpers for patient data at rest."""

import os
import json
from cryptography.fernet import Fernet


def generate_key() -> str:
    """Generate a new Fernet encryption key (base64-encoded string)."""
    return Fernet.generate_key().decode()


def load_encrypted_json(path: str, key_env_var: str = "DATA_ENCRYPTION_KEY") -> dict:
    """
    Load and decrypt a JSON file encrypted with Fernet.

    Args:
        path: File path to the encrypted .enc file
        key_env_var: Name of the environment variable holding the encryption key

    Returns:
        Decrypted dict parsed from JSON

    Raises:
        RuntimeError: If the encryption key is not set
        Exception: If decryption or parsing fails
    """
    key = os.environ.get(key_env_var)
    if not key:
        raise RuntimeError(
            f"PHI encryption key '{key_env_var}' is not set.\n"
            f"Set it via: export {key_env_var}=<key>\n"
            f"Generate a new key with: python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
        )

    fernet = Fernet(key.encode())
    with open(path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data)


def encrypt_json_file(plain_path: str, out_path: str, key_env_var: str = "DATA_ENCRYPTION_KEY") -> None:
    """
    Encrypt a plaintext JSON file.

    Args:
        plain_path: Path to plaintext JSON file
        out_path: Path to write encrypted file
        key_env_var: Name of the environment variable holding the encryption key
    """
    key = os.environ.get(key_env_var)
    if not key:
        raise RuntimeError(f"Encryption key '{key_env_var}' is not set.")

    fernet = Fernet(key.encode())
    with open(plain_path, "r") as f:
        json_data = f.read()

    encrypted_data = fernet.encrypt(json_data.encode())
    with open(out_path, "wb") as f:
        f.write(encrypted_data)
