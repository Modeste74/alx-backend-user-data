#!/usr/bin/env python3
"""defines a class Auth"""
import os
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
        for excluded_path in excluded_paths:
            if self._path_matches_wildcard(path, excluded_path):
                return False
        return True

    def _path_matches_wildcard(
            self, path: str, wildcard_path: str) -> bool:
        """checks if path matches wildcard path"""
        wildcard_path = wildcard_path.rstrip('/') + '/'
        if wildcard_path.endswith('*'):
            return path.startswith(wildcard_path[:-1])
        else:
            return path == wildcard_path

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        session_cookie_nme = os.environ.get(
                'SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_cookie_nme)
