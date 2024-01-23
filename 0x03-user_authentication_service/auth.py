#!/usr/bin/env python3
"""defines a method _hash_password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes a password and return its encoded bytes"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
