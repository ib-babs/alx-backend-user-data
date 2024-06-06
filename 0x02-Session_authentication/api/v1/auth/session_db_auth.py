#!/usr/bin/env python3
'''Prevents all Session IDs from lost if application stops.'''

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    '''SessionExpAuth subclass'''

    def create_session(self, user_id=None):
        '''creates and stores new instance of UserSession and\
            returns the Session ID'''
        if not user_id:
            return None
        usersession = UserSession(user_id=user_id)
        usersession.save()
        return super().create_session(user_id)

    def user_id_for_session_id(self, session_id=None):
        '''Returns the User ID by requesting UserSession in the\
            database based on session_id'''
        if not session_id:
            return None
        user_session = UserSession(session_id=session_id)
        if session_id in user_session.session_id:
            return user_session.user_id
        return None
