#!/usr/bin/env python3
'''
BasicAuth class
'''

from typing import List, TypeVar
from flask import request

from models.user import User
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):  # type: ignore
        '''Extracting user credential through decoded_base64
        auth string header'''
        if (not decoded_base64_authorization_header or
                type(decoded_base64_authorization_header) != str or
                ":" not in decoded_base64_authorization_header):
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):  # type: ignore
        '''Get user_object credential through email and password validation'''
        if ((not user_email or type(user_email) != str) or
                (not user_pwd or type(user_pwd) != str)):
            return None
        user_obj = User.search()
        new_obj = None
        if not user_obj:
            return None
        for user in user_obj:
            if user_email == user.email:
                new_obj = user
                break
        return new_obj if new_obj and\
            new_obj.is_valid_password(user_pwd) else None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        '''Get current user
        Arg:
            `request`: request object
        Returns: `current user object` or `None` if any of the validations fails.'''
        header = self.authorization_header(request)
        extract_b64_header = self.extract_base64_authorization_header(header)
        decode_b64_header = self.decode_base64_authorization_header(
            extract_b64_header)
        extract_credential = self.extract_user_credentials(decode_b64_header)
        extract_user_obj = self.user_object_from_credentials(
            *extract_credential)
        return extract_user_obj
