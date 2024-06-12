#!/usr/bin/env python3
"""
Authentication class module
"""
from uuid import uuid4
from db import DB
from bcrypt import checkpw, hashpw, gensalt

from user import User


def _hash_password(password: str) -> bytes:
    '''Hashes password and returns bytes of unique characters
    @params `password`: Password to hashF
    Return: Bytes of the password hashed'''
    if not password:
        return
    return hashpw(str(password).encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    '''Generate id'''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''Initialization'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Register a user with email and his password hashed'''
        if not email or not password:
            return
        user_exists = self.get_user(self, 'email', email)
        if user_exists:
            raise ValueError("User {} already exists".format(email))
        new_user = self._db.add_user(email, _hash_password(password))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        '''Validate password
        :params `email`: user email
        :params `password`: User accout password
        Return: True if account_exists and password \
            matches with hashed_password. False if othrwise'''
        if not email or not password:
            return
        user_by_email = self.get_user(self, 'email', email)
        if user_by_email and checkpw(str(password).encode('utf-8'),
                                     user_by_email.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        '''Create new session ID'''
        if not email:
            return
        user = self.get_user(self, 'email', email)
        if not user:
            return None
        user.session_id = _generate_uuid()
        self._db._session.commit()
        return user.session_id

    @staticmethod
    def get_user(cls, key: str, value: str) -> User:
        '''Get user by email
        Returns user object or None if not found'''
        user_exists = cls._db._session.query(User).\
            filter(getattr(User, key) == value).first()
        return user_exists

    def get_user_from_session_id(self, session_id: str) -> User:
        '''Find a user by session id'''
        if not session_id:
            return None
        user_obj = self.get_user(self, 'session_id', session_id)
        return None if not user_obj else user_obj

    def destroy_session(self, user_id: int) -> None:
        '''Set session_id of the user object to None'''
        user_obj = self.get_user(self, 'id', user_id)
        if user_obj:
            user_obj.session_id = None
            self._db._session.commit()

    def get_reset_password_token(self, email: str) -> str:
        """Get token for resetting a user password
        :param `email`: User email"""

        if not email:
            return

        user_obj = self.get_user(self, 'email', email)
        if not user_obj:
            raise ValueError
        user_obj.reset_token = _generate_uuid()
        self._db._session.commit()
        return user_obj.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''Update the user's password'''
        if reset_token and password:
            user_obj = self.get_user(self, 'reset_token', reset_token)
            if not user_obj:
                raise ValueError
            user_obj.hashed_password = _hash_password(password)
            user_obj.reset_token = None
            self._db._session.commit()
