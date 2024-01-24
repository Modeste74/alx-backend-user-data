#!/usr/bin/env python3
"""defines a method _hash_password"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """takes a password and return its encoded bytes"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """returns string rep of a new uuid"""
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password: str = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """returns true of false based on the validation of
        the provided email and password"""
        try:
            user = self._db.find_user_by(email=email)
            user_pass = user.hashed_password
            passwd_check = bcrypt.checkpw(password.encode('utf-8'), user_pass)
            return passwd_check
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Args:
        - email: users email.
        Find user and creates session_id
        Returns:
        - id string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
