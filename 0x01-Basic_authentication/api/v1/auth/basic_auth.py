#!/usr/bin/env python3
"""defines a sub class BasicAuth"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Inherits from super Auth class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string
        base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_value = base64.b64decode(
                    base64_authorization_header).decode('utf-8')
            return decode_value
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, user_password = decoded_base64_authorization_header.split(
                ':', 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password"""
        user = User()
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            dictionary = {"email": user_email, }
            user = user.search(dictionary)[0]
        except Exception:
            return None
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_ser(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the
        User instance for a request"""
        authorization_header = super().authorization_header(request)
        base64_authorization_header = self.extract_base64_authorization_header(
                base64_authorization_header)
        base64_initialize = self.decode_base64_authorization_header
        decoded_base64_authorization_header = base64_initialize(
                base64_authorization_header)
        credential_ext = self.extract_user_credentials
        user_email, user_pwd = credential_ext(
                decoded_base64_authorization_header)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
