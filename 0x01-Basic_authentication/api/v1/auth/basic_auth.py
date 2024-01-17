#!/usr/bin/env python3
""" Basic Auth class
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuthentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = base64.b64decode(encoded)
            return decoded64.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Returns the user email and password from the
        Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        user_credentials = decoded_base64_authorization_header.split(':', 1)

        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his
        email and password
        """
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

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request:
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        email, pwd = self.extract_user_credentials(decoded_auth)
        user = self.user_object_from_credentials(email, pwd)
        return user
