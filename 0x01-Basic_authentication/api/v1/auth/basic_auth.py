#!/usr/bin/env python3
'''
BasicAuth class
'''

from typing import List, TypeVar
from flask import request
from .auth import Auth
from base64 import b64encode, b64decode


class BasicAuth(Auth):
    '''Auth subclass - Basic Authentication'''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''Extraction of base64 authorization header'''
        if (not authorization_header or
            type(authorization_header) != str or
                not authorization_header.startswith('Basic ')):
            return None
        return authorization_header.replace('Basic ', '', 1)

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        '''Decoding base64 enconding characters'''
        if (not base64_authorization_header or
                type(base64_authorization_header) != str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception as e:
            return None
