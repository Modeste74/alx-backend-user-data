#!/usr/bin/env python3
"""defines a class Auth"""
from flask import request
from typing import List, TypeVar


class Auth:
    """defines methods for authentication purposes"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths"""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        path = path.rstrip('/') + '/'
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object"""
        return None
