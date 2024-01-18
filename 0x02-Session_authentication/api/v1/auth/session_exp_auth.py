#!/usr/bin/env python3
"""defines a sub class SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv
from uuid import uuid4


class SessionExpAuth(SessionAuth):
    """defines method for session authentification
    with expiration"""
    def __init__(self):
        """intializes the class"""
        super().__init__()
        self.session_duration = int(getenv(
            'SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Creates a Session ID with expiration"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a
        Session ID with expiration"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict['user_id']

        if 'created_at' not in session_dict:
            return None
        created_at = session_dict['created_at']
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None
        return session_dict['user_id']
