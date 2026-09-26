#!/usr/bin/env python3
"""
Seed demo users into backend/data/users.json

Usage:
    python backend/scripts/seed_users.py [--init]  (creates default demo users)
    python backend/scripts/seed_users.py --add-user <username> <role> <display_name> (prompts for password)
"""

import os
import sys
import json
import getpass

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from auth import hash_password


def load_users():
    """Load existing users.json or return empty structure."""
    users_file = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return {"users": []}


def save_users(data):
    """Save users to users.json."""
    users_file = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
    os.makedirs(os.path.dirname(users_file), exist_ok=True)
    with open(users_file, "w") as f:
        json.dump(data, f, indent=2)


def find_user(users, username):
    """Find a user by username."""
    for user in users["users"]:
        if user["username"] == username:
            return user
    return None


def init_demo_users():
    """Initialize with demo users."""
    demo_passwords = {
        "admin": "demo-admin-2026",
        "schen": "demo-schen-2026",
        "mpark": "demo-mpark-2026",
    }

    data = {"users": []}

    # Admin user
    data["users"].append({
        "username": "admin",
        "password_hash": hash_password(demo_passwords["admin"]),
        "role": "admin",
        "display_name": "System Administrator"
    })

    # Clinician: Dr. Sarah Chen (owns P001234)
    data["users"].append({
        "username": "schen",
        "password_hash": hash_password(demo_passwords["schen"]),
        "role": "clinician",
        "display_name": "Dr. Sarah Chen"
    })

    # Clinician: Dr. Michael Park (owns P005678)
    data["users"].append({
        "username": "mpark",
        "password_hash": hash_password(demo_passwords["mpark"]),
        "role": "clinician",
        "display_name": "Dr. Michael Park"
    })

    save_users(data)

    print("✅ Demo users created:")
    print("   admin        / demo-admin-2026   (sees all patients)")
    print("   schen        / demo-schen-2026   (Dr. Sarah Chen — owns P001234)")
    print("   mpark        / demo-mpark-2026   (Dr. Michael Park — owns P005678)")
    print("\n⚠️  These are demo passwords only — never use in production.")


def add_user(username, role, display_name):
    """Interactively add a new user."""
    if role not in ["admin", "clinician"]:
        print(f"❌ Invalid role: {role}. Must be 'admin' or 'clinician'.")
        sys.exit(1)

    data = load_users()

    if find_user(data, username):
        print(f"❌ User '{username}' already exists.")
        sys.exit(1)

    password = getpass.getpass(f"Enter password for {username}: ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("❌ Passwords do not match.")
        sys.exit(1)

    data["users"].append({
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "display_name": display_name
    })

    save_users(data)
    print(f"✅ User '{username}' created successfully.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Seed demo users")
    parser.add_argument("--init", action="store_true", help="Initialize with demo users")
    parser.add_argument("--add-user", nargs=3, metavar=("USERNAME", "ROLE", "DISPLAY_NAME"),
                        help="Add a new user (will prompt for password)")

    args = parser.parse_args()

    if args.init:
        init_demo_users()
    elif args.add_user:
        username, role, display_name = args.add_user
        add_user(username, role, display_name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
