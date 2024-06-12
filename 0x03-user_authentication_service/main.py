#!/usr/bin/env python3
"""
Main: End-to-end integration test
"""

import requests
from requests.exceptions import InvalidJSONError

'''assert to validate the response’s
expected status code and payload(if any) for each task.'''


url = ' http://127.0.0.1:5000/{}'


def register_user(email: str, password: str) -> None:
    '''Register a new user'''
    payload = {
        'email': email,
        'password': password
    }
    req = requests.post(url.format('users'), data=payload)
    try:
        message = req.json().get('message')
        if message == "email already registered":
            assert req.status_code == 400
        if message == "user created":
            assert req.status_code == 200
    except InvalidJSONError as IJE:
        assert req.status_code == 500


def log_in_wrong_password(email: str, password: str) -> None:
    '''Login with wrong password'''
    payload = {
        'email': email,
        'password': password
    }
    req = requests.post(url.format('sessions'), payload)
    try:
        res_json = req.json().get('message')
        assert res_json == 'logged in'

    except InvalidJSONError as IJE:
        assert req.status_code == 401


def log_in(email: str, password: str) -> str:
    '''Log user in'''
    payload = {
        'email': email,
        'password': password
    }
    req = requests.post(url.format('sessions'), data=payload)
    try:
        res_json = req.json().get('message')
        assert res_json == 'logged in'
        assert req.status_code == 200
        return req.cookies.get('session_id')

    except InvalidJSONError as IJE:
        assert req.status_code == 401


def profile_unlogged() -> None:
    '''Profile not logged in'''
    req = requests.get(url.format('profile'))
    assert req.status_code == 403


def profile_logged(session_id: str) -> None:
    '''Assert profile availability'''

    req = requests.get(url.format('profile'), cookies={
                       'session_id': session_id})
    try:
        req.json().get('email')
        assert req.status_code == 200
    except InvalidJSONError as IJE:
        assert req.status_code == 403


def log_out(session_id: str) -> None:
    '''Log the current user out using sessionID'''
    req = requests.delete(url.format('sessions'),
                          cookies={'session_id': session_id})
    try:
        res = req.json().get('message')
        assert req.status_code == 200
        assert res == 'Bienvenue'
    except InvalidJSONError as IJE:
        assert req.status_code == 403


def reset_password_token(email: str) -> str:
    '''Reset the user's password'''
    payload = {'email': email}
    req = requests.post(url.format('reset_password'), payload)
    try:
        token = req.json().get('reset_token')
        assert req.status_code == 200
        assert req.json().get('email') == email
        return token
    except InvalidJSONError as IJE:
        assert req.status_code == 403


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    '''Update user's password'''
    payload = {'email': email, 'reset_token': reset_token,
               'new_password': new_password}
    req = requests.put(url.format('reset_password'), payload)
    try:
        res_json_message = req.json().get('message')
        assert res_json_message == 'Password updated'
        assert req.status_code == 200
    except InvalidJSONError as IJE:
        assert req.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
