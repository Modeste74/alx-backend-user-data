#!/usr/bin/env python3
"""main to test update_password"""
from auth import Auth
auth = Auth()


user = auth.register_user(email="ken@ken.com", password="ken")
reset_token = auth.get_reset_password_token(email=user.email)
print(reset_token)
print(f"Old password: {user.hashed_password}")
session_id = auth.create_session(email=user.email)
print(session_id)
auth.update_password(reset_token=reset_token, password="ken123")
user_got = auth.get_user_from_session_id(session_id=session_id)
print(f"New password: {user_got.hashed_password}")
