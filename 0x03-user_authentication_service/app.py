#!/usr/bin/env python3
"""
Main flask application
"""
from flask import Flask, abort, jsonify, redirect, request, url_for
from auth import Auth, _hash_password

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    '''Index'''
    return jsonify({'message': 'Bienvenue'})


@app.post('/users')
def users():
    '''Create new user'''
    email = request.form.get('email')
    password = request.form.get('password')
    user_exists = Auth.get_user(AUTH, 'email', email)
    if user_exists:
        return jsonify({"message": "email already registered"}), 400
    AUTH._db.add_user(email, _hash_password(password))
    return jsonify({"email": email, "message": "user created"})


@app.post('/sessions')
def login():
    '''Authenticate a user and then log in'''
    email = request.form.get('email')
    password = request.form.get('password')
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    sessionID = AUTH.create_session(email)
    res = jsonify({'email': email, 'message': 'logged in'})
    res.set_cookie('session_id', sessionID)
    return res


@app.delete('/sessions')
def logout():
    sessionID = request.cookies.get('session_id')
    if not sessionID:
        abort(403)
    user_obj = Auth.get_user(AUTH, 'session_id', sessionID)
    if not user_obj:
        abort(403)
    AUTH.destroy_session(user_obj.id)
    return redirect(url_for('index'))


@app.get('/profile')
def profile():
    sessionID = request.cookies.get('session_id')
    if not sessionID or type(sessionID) != str:
        abort(403)
    user_obj = Auth.get_user(AUTH, 'session_id', sessionID)
    if user_obj:
        return jsonify({'email': user_obj.email}), 200
    abort(403)


@app.post('/reset_password')
def get_reset_password_token():
    '''Get reset token'''
    email = request.form.get('email')
    user_obj = Auth.get_user(AUTH, 'email', email)
    if not user_obj:
        abort(403)
    return jsonify({'email': email, 'reset_token':
                    AUTH.get_reset_password_token(email)}), 200


@app.put('/reset_password')
def update_password():
    '''Update th user password'''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if email and reset_token and new_password:
        user_obj = Auth.get_user(AUTH, 'email', email)
        if not user_obj or user_obj.reset_token != reset_token:
            abort(403)
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email,
                        "message": "Password updated"}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
