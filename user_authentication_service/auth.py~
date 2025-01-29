#!/usr/bin/env python3
"""Auth Module"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User
import uuid


def _hash_password(password: str) -> str:
    """Hash password

    Args:
        password (str): String password

    Returns:
        str: Password hashed as a string
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')



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

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for a user

        Args:
            email (str): User email

        Returns:
            str: Reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("User does not exist")

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user's password using reset token

        Args:
            reset_token (str): Reset token
            password (str): New password

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")

    def generate_reset_token(self, email: str) -> str:
        """Generate a reset token for a registered email

        Args:
            email (str): User email

        Returns:
            str: Reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("User does not exist")

    def is_registered_email(self, email: str) -> bool:
        """Check if the email is registered

        Args:
            email (str): User email

        Returns:
            bool: True if email is registered, else False
        """
        try:
            self._db.find_user_by(email=email)
            return True
        except NoResultFound:
            return False
