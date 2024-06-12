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
"""
Main file
"""


# my_db = DB()

# user = my_db.add_user("test@test.com", "PwdHashed")
# print(user.id)

# find_user = my_db.find_user_by(email="test@test.com")
# print(find_user.id)

# try:
#     find_user = my_db.find_user_by(email="test2@test.com")
#     print(find_user.id)
# except NoResultFound:
#     print("Not found")

# try:
#     find_user = my_db.find_user_by(no_email="test@test.com")
#     print(find_user.id)
# except InvalidRequestError:
#     print("Invalid")
