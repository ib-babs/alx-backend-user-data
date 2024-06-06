#!/usr/bin/env python3
'''Session Auth'''
from os import getenv
from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'])
@app_views.route('/auth_session/login/', methods=['POST'])
def auth_session_login():
    '''Handle authentication session login'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400
    user_obj = User.search()
    new_obj = None
    if not user_obj:
        return None
    for user in user_obj:
        if email == user.email:
            new_obj = user
            break
    if not new_obj:
        return jsonify({"error": "no user found for this email"}), 404
    if not new_obj.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(new_obj.id)
    response = jsonify(new_obj.to_json())
    # print(session_id)
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'])
@app_views.route('/auth_session/logout/', methods=['DELETE'])
def logout():
    '''Logout with session_ID'''
    from api.v1.app import auth
    destroy_ses = auth.destroy_session(request)
    if not destroy_ses:
        abort(404)
    return jsonify({}), 200
