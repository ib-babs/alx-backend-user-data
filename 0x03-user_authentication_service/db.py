#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    id = 0

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, email: str, hashed_password: str) -> User:
        '''Add a new user to the database'''
        DB.id += 1
        new_user = User(**{"id": DB.id, 'email': email,
                        'hashed_password': hashed_password})
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''
        Returns the first row found in the users table as filtered by
        the method’s input arguments.
        '''
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
        user_retrieved = self.find_user_by(**{'id': user_id})
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise ValueError()
            else:
                setattr(user_retrieved, k, v)
        self._session.commit()
