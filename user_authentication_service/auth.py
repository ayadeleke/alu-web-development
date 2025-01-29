#!/usr/bin/env python3
"""Auth Module"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Hash password

    Args:
        password (str): String password

    Returns:
        bytes: Password hashed
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a uuid4

    Returns:
        str: string repr of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user to the db

        Args:
            email (str): Email
            password (str): Password

        Returns:
            User: User object created
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Valid login method

        Args:
            email (str): email credential
            password (str): password credential

        Returns:
            bool: True or False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Session

        Args:
            email (str): email credential

        Returns:
            str: session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=session_uuid)
            return session_uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve a user by session ID

        Args:
            session_id (str): Session ID

        Returns:
            User or None: User object if found, else None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user's session

        Args:
            user_id (int): User ID

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass