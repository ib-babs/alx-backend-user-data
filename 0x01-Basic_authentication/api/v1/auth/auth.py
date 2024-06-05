#!/usr/bin/env python3
'''
Auth class
'''

from typing import List, TypeVar
from flask import request


class Auth:
    '''Authentication: handle all the errors, unauthorized user,
    incorrect authentication data and the current user'''

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        '''Checks if the requested `path` is in the `excluded paths`
        if true, then return False to that the same path wont require any
        authentication. Otherwise authentication is required'''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Checking excluded_paths string that ends with `*` to
        # match all paths that start with such string until `*`.
        # Simply, wildcard
        for xc_path in excluded_paths:
            if xc_path.endswith('*'):
                if path.startswith(xc_path.replace('*', '')):
                    return False

        slash_resistant = path + '/'
        # Confirming  path  existence
        if path in excluded_paths or slash_resistant in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        '''Checking authorization header existence.
        if `request` is None, then no request to the route link has been made.
        Or if the header is not exist in the request made to access
        the resource from the route link requested then
        401 (Unauthorized) http status code is raised'''
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        '''Return current user or None'''
        return None
