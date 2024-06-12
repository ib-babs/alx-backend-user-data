#!/usr/bin/env python3
"""DB module - contains database class
which is responsible for collecting and store data
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Union
from user import Base, User


class DB:
    """Database class
    IMPLEMENTATION
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) ->\
            Union[User, None]:
        '''Add a new user to the database'''
        if email and hashed_password:
            new_user = User(**{'email': email,
                            'hashed_password': hashed_password})
            self._session.add(new_user)
            self._session.commit()
            return new_user

    def find_user_by(self, **kwargs) -> User:
        '''Returns the first row found in the users table as filtered by
        the method input arguments.
        '''
        if kwargs:
            key = list(kwargs.keys())[0]
            if not hasattr(User, key):
                raise InvalidRequestError
            res = self._session.query(User).filter(
                getattr(User, key) == kwargs[key]).first()
            if not res:
                raise NoResultFound
            return res

    def update_user(self, user_id: int, **kwargs) -> None:
        '''Update user account'''
        if not user_id or not kwargs:
            return
        user_retrieved = self.find_user_by(**{'id': user_id})
        if user_retrieved:
            for k, v in kwargs.items():
                if not hasattr(User, k):
                    raise ValueError()
                else:
                    setattr(user_retrieved, k, v)
            self._session.commit()
