#!/usr/bin/env python3
'''Prevents all Session IDs from lost if application stops.'''

from .base import Base


class UserSession(Base):
    '''Authentication system, based on Session ID\
        stored in database'''

    def __init__(self, *args: list, **kwargs: dict):
        '''Initialization'''
        super().__init__(*args, *kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
