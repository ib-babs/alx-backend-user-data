#!/usr/bin/env python3
"""
Main file
"""

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User

my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)
user_3 = my_db.add_user("test2@test.com", "SuperHashedPwd2")
print(user_3.id)
