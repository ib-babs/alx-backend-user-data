#!/usr/bin/env python3
'''Session Expiration Authentication get sessionID
expired upon time elapsed'''
from datetime import datetime, timedelta
from os import getenv
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''Session Expire Authentication'''

    def __init__(self) -> None:
        '''Initialization'''
        duration = getenv('SESSION_DURATION')
        self.session_duration = int(duration) \
            if duration else 0

    def create_session(self, user_id=None):
        '''Create session'''
        sID = super().create_session(user_id)
        if not sID:
            return None
        self.user_id_by_session_id.update({sID: {
            'user_id': user_id,
            'created_at': datetime.now()
        }})
        return sID

    def user_id_for_session_id(self, session_id=None):
        '''User ID for session ID'''
        # uID_for_sID = super().user_id_for_session_id(session_id)
        if not session_id or \
                session_id not in self.user_id_by_session_id:
            return None
        session_Dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_Dict.get('user_id')
        if 'created_at' not in session_Dict:
            return None
        if session_Dict.get('created_at') + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return session_Dict.get('user_id')
