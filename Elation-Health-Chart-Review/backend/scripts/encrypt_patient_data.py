#!/usr/bin/env python3
"""
One-time migration script: encrypt plaintext patient data.

Usage:
    python backend/scripts/encrypt_patient_data.py [--force]

This script:
1. Reads data/sample_patients.json (plaintext)
2. Encrypts it with a Fernet key
3. Writes encrypted data to data/sample_patients.json.enc
4. Prints the encryption key if not already set via DATA_ENCRYPTION_KEY env var
"""

import os
import sys
import json

# Add parent directory to path so we can import crypto_store
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from crypto_store import generate_key, encrypt_json_file


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Encrypt patient data at rest")
    parser.add_argument("--force", action="store_true", help="Overwrite existing .enc file")
    args = parser.parse_args()

    # data/ is at the project root, not in backend/
    base_dir = os.path.join(os.path.dirname(__file__), "..", "..")
    plain_file = os.path.join(base_dir, "data", "sample_patients.json")
    enc_file = os.path.join(base_dir, "data", "sample_patients.json.enc")

    # Check if plaintext file exists
    if not os.path.exists(plain_file):
        print(f"❌ Plaintext file not found: {plain_file}")
        sys.exit(1)

    # Check if encrypted file already exists
    if os.path.exists(enc_file) and not args.force:
        print(f"⚠️  Encrypted file already exists: {enc_file}")
        print("   Use --force to overwrite")
        sys.exit(1)

    # Get or generate encryption key
    key = os.environ.get("DATA_ENCRYPTION_KEY")
    if not key:
        print("📝 No DATA_ENCRYPTION_KEY set. Generating a new key...")
        key = generate_key()
        print(f"\n🔑 Generated encryption key:\n{key}\n")
        print("⚠️  Save this key in your .env file:")
        print(f"   export DATA_ENCRYPTION_KEY={key}")
        print("\n   Or add to .env:")
        print(f"   DATA_ENCRYPTION_KEY={key}\n")
        os.environ["DATA_ENCRYPTION_KEY"] = key
    else:
        print(f"✓ Using DATA_ENCRYPTION_KEY from environment")

    # Encrypt the file
    print(f"🔐 Encrypting {plain_file}...")
    try:
        encrypt_json_file(plain_file, enc_file, key_env_var="DATA_ENCRYPTION_KEY")
        print(f"✅ Success! Encrypted data written to: {enc_file}")

        # Verify by reading it back
        from crypto_store import load_encrypted_json
        data = load_encrypted_json(enc_file)
        patient_count = len(data.get("patients", []))
        print(f"✓ Verified: {patient_count} patients encrypted successfully")

        print("\n📋 Next steps:")
        print(f"1. Delete the plaintext file: rm {plain_file}")
        print(f"2. Remove from git tracking: git rm --cached {plain_file}")
        print(f"3. Commit the encrypted version: git add {enc_file}")
        print(f"4. Update .env with the encryption key")

    except Exception as e:
        print(f"❌ Encryption failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
