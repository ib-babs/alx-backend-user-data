#!/usr/bin/env python3
'''Prevents all Session IDs from lost if application stops.'''

from uuid import uuid4
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    '''SessionExpAuth subclass'''

    def create_session(self, user_id=None):
        '''creates and stores new instance of UserSession and\
            returns the Session ID'''
        if not user_id or type(user_id) != str:
            return None
        usersession = UserSession(user_id=user_id,
                                  session_id=str(uuid4()))
        usersession.save()
        return usersession.session_id

    def user_id_for_session_id(self, session_id=None):
        '''Returns the User ID by requesting UserSession in the\
            database based on session_id'''
        if not session_id or type(session_id) != str:
            return None
        user_session_obj = UserSession.search()
        new_session_obj = None
        if not user_session_obj:
            return None
        for user in user_session_obj:
            if session_id == user.session_id:
                new_session_obj = user
                break
        return new_session_obj.user_id if new_session_obj else None
