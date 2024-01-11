#!/usr/bin/env python3
"""defines functions on hashing password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes input password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    # Use bcrypt to validate the password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
