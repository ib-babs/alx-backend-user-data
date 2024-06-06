#!/usr/bin/env python3
""" Session Authentication
"""
from uuid import uuid4

from models.user import User
from .auth import Auth


class SessionAuth(Auth):
    '''SessionAuth: Session Authentication authenticates session
    `Auth` subclass'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Create new session id.
        @param:
            `user_id`: ID of the user
        `Returns`: new session ID otherwise None if `user_id` is None or\
            `user_id` type is not string.'''
        if not user_id or type(user_id) != str:
            return None
        id = str(uuid4())
        self.user_id_by_session_id.update({id: user_id})
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Get ID of user for the session ID
        @param:
            `session_id`: ID of the session
        Returns: UserID'''
        if not session_id or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''Return current user'''
        if not request:
            return None
        cookies = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookies)
        return User.get(user_id)
